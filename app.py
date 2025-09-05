"""
Document E-Signature Platform with Knowledge Verification
A FastAPI application for document signing with AI-powered quiz validation
"""

import os
import json
import uuid
import asyncio
import random
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager
from enum import Enum
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# FastAPI and dependencies
from fastapi import FastAPI, HTTPException, Query, Path as PathParam, Depends, Header
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, EmailStr

# Additional dependencies
from tinydb import TinyDB, Query as TinyQuery
from dotenv import load_dotenv
import httpx
import openai
import markdown
import aiofiles

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
EMAIL_WEBHOOK_URL = os.getenv("EMAIL_WEBHOOK_URL")
APP_URL = os.getenv("APP_URL", "http://localhost:8000")
DB_PATH = os.getenv("DB_PATH", "db/esign.json")
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "your-secure-admin-key-here")  # For admin endpoints

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Initialize database
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
db = TinyDB(DB_PATH)
signatures_table = db.table('signatures')
quizzes_table = db.table('quizzes')

# Initialize scheduler for automatic data cleanup
scheduler = AsyncIOScheduler(timezone=pytz.timezone('Asia/Kolkata'))

# Forward declaration for scheduled_data_cleanup (defined later in admin section)
async def scheduled_data_cleanup():
    """Forward declaration - actual implementation in admin section"""
    pass

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    scheduler.add_job(
        scheduled_data_cleanup,
        CronTrigger(hour=0, minute=0, timezone=pytz.timezone('Asia/Kolkata')),
        id='daily_cleanup',
        name='Daily data cleanup at midnight IST',
        replace_existing=True
    )
    scheduler.start()
    logger.info("Scheduler started - Daily cleanup scheduled at midnight IST")
    yield
    # Shutdown
    scheduler.shutdown()
    logger.info("Scheduler stopped")

# FastAPI app initialization
app = FastAPI(
    title="Document E-Signature Platform",
    description="Document signing with AI-powered knowledge verification",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir), html=True), name="static")

# ===============================
# Pydantic Models
# ===============================

class DocumentStatus(str, Enum):
    SENT = "sent"
    ACKNOWLEDGED = "acknowledged"
    QUIZ_PENDING = "quiz_pending"
    QUIZ_FAILED = "quiz_failed"
    COMPLETED = "completed"

class SendDocumentRequest(BaseModel):
    sender_email: EmailStr
    sender_name: str = Field(..., min_length=1, max_length=100)
    purpose: str = Field(..., min_length=1, max_length=500)
    receiver_email: EmailStr
    document_id: str = Field(..., pattern="^[a-z_]+$")

class SignatureSubmission(BaseModel):
    acknowledged: bool = Field(..., description="User acknowledged the document")
    date: str = Field(..., description="Date of signature")
    location: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=100)

class QuizAnswer(BaseModel):
    question_id: str
    answer: str

class QuizSubmission(BaseModel):
    answers: Dict[str, str] = Field(..., description="Question ID to answer mapping")

class QuizQuestion(BaseModel):
    id: str
    question: str
    options: List[str]
    correct_answer: str

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

# ===============================
# Document Management
# ===============================

DOCUMENT_MAPPING = {
    "company_policy": "documents/company_policy.md",
    "nda_policy": "documents/nda_policy.md",
    "dev_guidelines": "documents/dev_guidelines.md"
}

def list_available_documents() -> List[Dict[str, str]]:
    """List all available documents"""
    documents = []
    for doc_id, file_path in DOCUMENT_MAPPING.items():
        if os.path.exists(file_path):
            documents.append({
                "id": doc_id,
                "name": doc_id.replace("_", " ").title(),
                "path": file_path
            })
    return documents

async def load_document(document_id: str) -> Dict[str, str]:
    """Load a document by ID"""
    if document_id not in DOCUMENT_MAPPING:
        raise HTTPException(status_code=404, detail="Document not found")
    
    file_path = DOCUMENT_MAPPING[document_id]
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Document file not found")
    
    async with aiofiles.open(file_path, 'r') as f:
        content = await f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(content, extensions=['extra', 'codehilite'])
    
    # Extract title (first line)
    lines = content.split('\n')
    title = lines[0].strip('# ') if lines else document_id.replace("_", " ").title()
    
    return {
        "id": document_id,
        "title": title,
        "content": content,
        "html": html_content
    }

# ===============================
# OpenAI Integration
# ===============================

async def generate_quiz_questions(document_content: str, num_questions: int = 3) -> List[QuizQuestion]:
    """Generate quiz questions from document content using OpenAI"""
    try:
        # Prepare the prompt
        prompt = f"""Generate exactly {num_questions} multiple choice questions based on the following document content.
        Each question should test understanding of key concepts.
        
        Format your response as a JSON array with this structure:
        [
            {{
                "question": "The question text",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "The correct option text (must be one of the options)"
            }}
        ]
        
        Document content:
        {document_content[:6000]}  # Limit content to avoid token limits
        """
        
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert educator creating quiz questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        
        # Parse the response
        response_text = response.choices[0].message.content
        quiz_data = json.loads(response_text)
        
        # Ensure we have the 'questions' key
        if isinstance(quiz_data, dict) and 'questions' in quiz_data:
            questions_list = quiz_data['questions']
        elif isinstance(quiz_data, list):
            questions_list = quiz_data
        else:
            # Fallback if structure is unexpected
            questions_list = []
        
        # Convert to QuizQuestion objects
        questions = []
        for idx, q in enumerate(questions_list[:num_questions]):
            questions.append(QuizQuestion(
                id=f"q{idx+1}",
                question=q['question'],
                options=q['options'],
                correct_answer=q['correct_answer']
            ))
        
        # Fallback questions if generation fails
        if len(questions) < num_questions:
            logger.warning("Using fallback questions due to generation failure")
            questions = get_fallback_questions(document_content)[:num_questions]
        
        return questions
        
    except Exception as e:
        logger.error(f"Error generating quiz questions: {str(e)}")
        return get_fallback_questions(document_content)[:num_questions]

def get_fallback_questions(document_content: str) -> List[QuizQuestion]:
    """Provide fallback questions if AI generation fails"""
    return [
        QuizQuestion(
            id="q1",
            question="What is the main purpose of this document?",
            options=[
                "To provide guidelines",
                "To establish rules",
                "To inform about policies",
                "All of the above"
            ],
            correct_answer="All of the above"
        ),
        QuizQuestion(
            id="q2",
            question="Who is required to follow these guidelines?",
            options=[
                "Only new employees",
                "Only management",
                "All employees",
                "External contractors only"
            ],
            correct_answer="All employees"
        ),
        QuizQuestion(
            id="q3",
            question="When do these policies take effect?",
            options=[
                "Immediately upon acknowledgment",
                "After 30 days",
                "At the next review cycle",
                "Only for new projects"
            ],
            correct_answer="Immediately upon acknowledgment"
        )
    ]

async def generate_email_content(document_title: str, purpose: str, context: str, 
                                sender_name: str = None, receiver_name: str = None) -> Dict[str, str]:
    """Generate email subject and body using OpenAI with better formatting"""
    try:
        prompt = f"""Generate a professional email for document signature request.
        
        Document: {document_title}
        Purpose: {purpose}
        Context: {context}
        Sender: {sender_name or 'Sender'}
        Recipient: {receiver_name or 'Recipient'}
        
        Return a JSON object with:
        {{
            "subject": "Clear, action-oriented subject line",
            "body_html": "HTML formatted email body with proper greeting using actual names, brief explanation, and clear call-to-action. Use <p> tags for paragraphs.",
            "body_text": "Plain text version of the email"
        }}
        
        Keep it concise and professional. Use the actual names provided.
        """
        
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a professional email writer. Format emails clearly with HTML."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Ensure we have the right keys
        if 'body_html' not in result:
            result['body_html'] = result.get('body', '')
        if 'body_text' not in result:
            result['body_text'] = result.get('body', result['body_html'])
            
        return result
        
    except Exception as e:
        logger.error(f"Error generating email content: {str(e)}")
        # Better fallback template with HTML
        return {
            "subject": f"Action Required: {document_title}",
            "body_html": f"""<p>Dear {receiver_name or 'Recipient'},</p>
            <p>{sender_name or 'Your colleague'} has requested that you review and sign the <strong>{document_title}</strong>.</p>
            <p><strong>Purpose:</strong> {purpose}</p>
            <p>Please review the document and provide your signature at your earliest convenience.</p>
            <p>Best regards,<br>{sender_name or 'Document Management System'}</p>""",
            "body_text": f"Dear {receiver_name or 'Recipient'},\n\n{sender_name or 'Your colleague'} has requested that you review and sign {document_title}.\n\nPurpose: {purpose}\n\nPlease review and sign at your earliest convenience.\n\nBest regards,\n{sender_name or 'Document Management System'}"
        }

# ===============================
# Email Integration
# ===============================

async def send_webhook(payload: Dict[str, Any], max_retries: int = 3) -> bool:
    """Send webhook with retry mechanism"""
    async with httpx.AsyncClient() as client:
        for attempt in range(max_retries):
            try:
                response = await client.post(
                    EMAIL_WEBHOOK_URL,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code in [200, 201, 202]:
                    logger.info(f"Webhook sent successfully: {payload.get('event_type')}")
                    return True
                elif response.status_code >= 500:
                    # Server error, retry with exponential backoff
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"Webhook failed with status {response.status_code}")
                    return False
                    
            except httpx.TimeoutException:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    await asyncio.sleep(wait_time)
                else:
                    logger.error("Webhook timeout after all retries")
                    return False
            except Exception as e:
                logger.error(f"Webhook error: {str(e)}")
                return False
    
    return False

async def send_signature_request_email(tracking_id: str, sender_name: str, sender_email: str, 
                                       receiver_email: str, document_title: str, purpose: str):
    """Send initial signature request email with HTML formatting"""
    # Extract receiver name from email if possible
    receiver_name = receiver_email.split('@')[0].replace('.', ' ').replace('_', ' ').title()
    
    signing_link = f"{APP_URL}/sign/{tracking_id}"
    
    # Create well-formatted HTML body without relying on OpenAI
    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <p>Dear {receiver_name},</p>
        
        <p>I hope this message finds you well. As part of our annual review process, we need your acknowledgment of the updated <strong>{document_title}</strong> for 2024.</p>
        
        <p>Could you please review the document to ensure you understand our policies? Your acknowledgment is essential to ensure compliance and understanding of the updated policies.</p>
        
        <p><strong>Purpose:</strong><br>
        {purpose}</p>
        
        <p>Thank you for your attention to this matter.</p>
        
        <div style="margin: 30px 0; text-align: center;">
            <a href="{signing_link}" style="display: inline-block; padding: 14px 28px; background-color: #2563eb; color: white; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 16px;">
                Sign Document
            </a>
        </div>
        
        <p style="color: #666; font-size: 14px;">
            If the button above doesn't work, please copy and paste this link into your browser:<br>
            <a href="{signing_link}" style="color: #2563eb;">{signing_link}</a>
        </p>
        
        <p>Best regards,<br>
        <strong>{sender_name}</strong><br>
        {sender_email}</p>
    </div>
    """
    
    # Plain text version
    text_body = f"""Dear {receiver_name},

I hope this message finds you well. As part of our annual review process, we need your acknowledgment of the updated {document_title} for 2024.

Could you please review the document to ensure you understand our policies? Your acknowledgment is essential to ensure compliance and understanding of the updated policies.

Purpose: {purpose}

Thank you for your attention to this matter.

Sign Document: {signing_link}

Best regards,
{sender_name}
{sender_email}"""
    
    payload = {
        "event_type": "signature_request",
        "to": receiver_email,
        "from_name": sender_name,
        "from_email": sender_email,
        "subject": f"Action Required: {document_title}",
        "body": text_body,
        "body_html": html_body,
        "signing_link": signing_link,
        "tracking_id": tracking_id
    }
    
    return await send_webhook(payload)

async def send_quiz_link_email(quiz_id: str, receiver_email: str, document_title: str):
    """Send quiz link after signature with HTML formatting"""
    receiver_name = receiver_email.split('@')[0].replace('.', ' ').replace('_', ' ').title()
    
    quiz_link = f"{APP_URL}/quiz/{quiz_id}"
    
    html_body = f"""
    <p>Dear {receiver_name},</p>
    <p>Thank you for acknowledging the <strong>{document_title}</strong>.</p>
    <p>To complete the signature process, please take a short quiz to verify your understanding of the document.</p>
    <p style="margin-top: 20px;">
        <a href="{quiz_link}" style="display: inline-block; padding: 12px 24px; background-color: #8b5cf6; color: white; text-decoration: none; border-radius: 6px; font-weight: 600;">
            Take Quiz
        </a>
    </p>
    <p style="color: #666; font-size: 12px;">
        This quiz contains 3 questions and all must be answered correctly.
    </p>
    <p style="color: #666; font-size: 12px; margin-top: 20px;">
        Quiz link: {quiz_link}
    </p>
    """
    
    text_body = f"""Dear {receiver_name},

Thank you for acknowledging the {document_title}.

To complete the signature process, please take a short quiz to verify your understanding:

Take Quiz: {quiz_link}

This quiz contains 3 questions and all must be answered correctly."""
    
    payload = {
        "event_type": "quiz_link",
        "to": receiver_email,
        "subject": f"Quiz Required: {document_title}",
        "body": text_body,
        "body_html": html_body,
        "quiz_link": quiz_link,
        "quiz_id": quiz_id
    }
    
    return await send_webhook(payload)

async def send_completion_email(receiver_email: str, sender_email: str, document_title: str, passed: bool, quiz_id: str):
    """Send completion notification with HTML formatting"""
    receiver_name = receiver_email.split('@')[0].replace('.', ' ').replace('_', ' ').title()
    sender_name = sender_email.split('@')[0].replace('.', ' ').replace('_', ' ').title()
    quiz_url = f"{APP_URL}/quiz/{quiz_id}"
    
    if passed:
        # Success email to recipient
        html_body = f"""
        <div style="text-align: center; padding: 20px;">
            <h2 style="color: #10b981;">✅ Success!</h2>
            <p>Congratulations {receiver_name},</p>
            <p>You have successfully signed and verified your understanding of:</p>
            <p><strong>{document_title}</strong></p>
            <p style="margin-top: 20px; color: #666;">Your signature has been recorded and confirmed.</p>
        </div>
        """
        
        text_body = f"""✅ Success!

Congratulations {receiver_name},

You have successfully signed and verified your understanding of:
{document_title}

Your signature has been recorded and confirmed."""
        
        await send_webhook({
            "event_type": "signature_completed",
            "to": receiver_email,
            "subject": f"✅ Successfully Signed: {document_title}",
            "body": text_body,
            "body_html": html_body
        })
        
        # Notification to sender
        sender_html = f"""
        <p>Hello {sender_name},</p>
        <p>Good news! <strong>{receiver_name}</strong> ({receiver_email}) has successfully:</p>
        <ul>
            <li>Signed the document: <strong>{document_title}</strong></li>
            <li>Passed the knowledge verification quiz</li>
        </ul>
        <p>The signature process is now complete.</p>
        <p style="color: #666; font-size: 12px; margin-top: 20px;">
            View all signatures at: <a href="{APP_URL}">{APP_URL}</a>
        </p>
        """
        
        sender_text = f"""Hello {sender_name},

Good news! {receiver_name} ({receiver_email}) has successfully:
- Signed the document: {document_title}
- Passed the knowledge verification quiz

The signature process is now complete.

View all signatures at: {APP_URL}"""
        
        await send_webhook({
            "event_type": "signature_completed_notification",
            "to": sender_email,
            "subject": f"✅ Document Signed: {document_title}",
            "body": sender_text,
            "body_html": sender_html
        })
        
    else:
        # Failure email to recipient
        html_body = f"""
        <div style="text-align: center; padding: 20px;">
            <h2 style="color: #ef4444;">❌ Quiz Not Passed</h2>
            <p>Hello {receiver_name},</p>
            <p>Unfortunately, you did not pass the verification quiz for:</p>
            <p><strong>{document_title}</strong></p>
            <p style="margin-top: 20px;">Please review the document again and retake the quiz.</p>
            <p style="margin-top: 20px;">
                <a href="{quiz_url}" style="display: inline-block; padding: 12px 24px; background-color: #ef4444; color: white; text-decoration: none; border-radius: 6px; font-weight: 600;">
                    Retake Quiz
                </a>
            </p>
        </div>
        """
        
        text_body = f"""❌ Quiz Not Passed

Hello {receiver_name},

Unfortunately, you did not pass the verification quiz for:
{document_title}

Please review the document again and retake the quiz.

Try again at: {quiz_url}"""
        
        await send_webhook({
            "event_type": "quiz_failed",
            "to": receiver_email,
            "subject": f"❌ Quiz Failed: {document_title}",
            "body": text_body,
            "body_html": html_body
        })

# ===============================
# API Endpoints
# ===============================

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the dashboard"""
    file_path = Path(__file__).parent / "static" / "index.html"
    if file_path.exists():
        async with aiofiles.open(str(file_path), 'r') as f:
            content = await f.read()
        return HTMLResponse(content=content)
    else:
        return HTMLResponse(content="<h1>Dashboard coming soon...</h1>")

@app.get("/api/documents", response_model=ApiResponse)
async def get_documents():
    """List all available documents"""
    documents = list_available_documents()
    return ApiResponse(
        success=True,
        message="Documents retrieved successfully",
        data=documents
    )

@app.get("/api/documents/{document_id}", response_model=ApiResponse)
async def get_document(document_id: str = PathParam(..., pattern="^[a-z_]+$")):
    """Get a specific document by ID"""
    document = await load_document(document_id)
    return ApiResponse(
        success=True,
        message="Document retrieved successfully",
        data=document
    )

@app.post("/api/send-document", response_model=ApiResponse)
async def send_document(request: SendDocumentRequest):
    """Initiate a document signature request"""
    # Validate document exists
    document = await load_document(request.document_id)
    
    # Generate tracking ID
    tracking_id = str(uuid.uuid4())
    
    # Store in database
    signature_record = {
        "tracking_id": tracking_id,
        "document_id": request.document_id,
        "document_title": document["title"],
        "sender_email": request.sender_email,
        "sender_name": request.sender_name,
        "receiver_email": request.receiver_email,
        "purpose": request.purpose,
        "status": DocumentStatus.SENT,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "acknowledged": False,
        "quiz_id": None,
        "quiz_passed": False,
        "completed_at": None
    }
    
    signatures_table.insert(signature_record)
    
    # Send email notification
    email_sent = await send_signature_request_email(
        tracking_id,
        request.sender_name,
        request.sender_email,
        request.receiver_email,
        document["title"],
        request.purpose
    )
    
    if not email_sent:
        logger.warning(f"Failed to send email for tracking_id: {tracking_id}")
    
    return ApiResponse(
        success=True,
        message="Document sent successfully",
        data={
            "tracking_id": tracking_id,
            "status": DocumentStatus.SENT,
            "signing_url": f"{APP_URL}/sign/{tracking_id}"
        }
    )

@app.get("/api/signature/{tracking_id}", response_model=ApiResponse)
async def get_signature_status(tracking_id: str):
    """Get signature status and document content"""
    SignatureQuery = TinyQuery()
    signature = signatures_table.get(SignatureQuery.tracking_id == tracking_id)
    
    if not signature:
        raise HTTPException(status_code=404, detail="Signature request not found")
    
    # Load document content
    document = await load_document(signature["document_id"])
    
    return ApiResponse(
        success=True,
        message="Signature status retrieved",
        data={
            "signature": signature,
            "document": document
        }
    )

@app.post("/api/submit-signature/{tracking_id}", response_model=ApiResponse)
async def submit_signature(tracking_id: str, submission: SignatureSubmission):
    """Submit signature acknowledgment"""
    SignatureQuery = TinyQuery()
    signature = signatures_table.get(SignatureQuery.tracking_id == tracking_id)
    
    if not signature:
        raise HTTPException(status_code=404, detail="Signature request not found")
    
    # Generate quiz questions
    document = await load_document(signature["document_id"])
    questions = await generate_quiz_questions(document["content"])
    
    # Create quiz record
    quiz_id = str(uuid.uuid4())
    quiz_record = {
        "quiz_id": quiz_id,
        "tracking_id": tracking_id,
        "questions": [q.model_dump() for q in questions],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "attempts": 0,
        "passed": False
    }
    
    quizzes_table.insert(quiz_record)
    
    # Update signature record
    signatures_table.update(
        {
            "acknowledged": submission.acknowledged,
            "acknowledgment_date": submission.date,
            "acknowledgment_location": submission.location,
            "signer_name": submission.name,
            "status": DocumentStatus.QUIZ_PENDING,
            "quiz_id": quiz_id,
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        SignatureQuery.tracking_id == tracking_id
    )
    
    # Send quiz link email
    await send_quiz_link_email(quiz_id, signature["receiver_email"], signature["document_title"])
    
    return ApiResponse(
        success=True,
        message="Signature acknowledged. Please complete the quiz.",
        data={
            "quiz_id": quiz_id,
            "quiz_url": f"{APP_URL}/quiz/{quiz_id}"
        }
    )

@app.get("/api/quiz/{quiz_id}", response_model=ApiResponse)
async def get_quiz(quiz_id: str):
    """Get quiz questions"""
    QuizQuery = TinyQuery()
    quiz = quizzes_table.get(QuizQuery.quiz_id == quiz_id)
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Remove correct answers before sending to client
    questions = []
    for q in quiz["questions"]:
        questions.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        })
    
    return ApiResponse(
        success=True,
        message="Quiz retrieved successfully",
        data={
            "quiz_id": quiz_id,
            "questions": questions,
            "attempts": quiz["attempts"]
        }
    )

@app.post("/api/submit-quiz/{quiz_id}", response_model=ApiResponse)
async def submit_quiz(quiz_id: str, submission: QuizSubmission):
    """Submit quiz answers"""
    QuizQuery = TinyQuery()
    quiz = quizzes_table.get(QuizQuery.quiz_id == quiz_id)
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Check answers
    correct_count = 0
    total_questions = len(quiz["questions"])
    
    for question in quiz["questions"]:
        submitted_answer = submission.answers.get(question["id"])
        if submitted_answer == question["correct_answer"]:
            correct_count += 1
    
    # All must be correct
    passed = correct_count == total_questions
    
    # Update quiz record
    quizzes_table.update(
        {
            "attempts": quiz["attempts"] + 1,
            "passed": passed,
            "last_attempt": datetime.now(timezone.utc).isoformat(),
            "last_score": correct_count
        },
        QuizQuery.quiz_id == quiz_id
    )
    
    # Update signature status if passed
    if passed:
        SignatureQuery = TinyQuery()
        signature = signatures_table.get(SignatureQuery.quiz_id == quiz_id)
        
        signatures_table.update(
            {
                "status": DocumentStatus.COMPLETED,
                "quiz_passed": True,
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            },
            SignatureQuery.quiz_id == quiz_id
        )
        
        # Send completion emails
        await send_completion_email(
            signature["receiver_email"],
            signature["sender_email"],
            signature["document_title"],
            True,
            quiz_id
        )
    else:
        SignatureQuery = TinyQuery()
        signatures_table.update(
            {"status": DocumentStatus.QUIZ_FAILED},
            SignatureQuery.quiz_id == quiz_id
        )
        
        signature = signatures_table.get(SignatureQuery.quiz_id == quiz_id)
        await send_completion_email(
            signature["receiver_email"],
            signature["sender_email"],
            signature["document_title"],
            False,
            quiz_id
        )
    
    return ApiResponse(
        success=True,
        message="Quiz submitted successfully" if passed else "Quiz failed. Please try again.",
        data={
            "passed": passed,
            "score": f"{correct_count}/{total_questions}",
            "attempts": quiz["attempts"] + 1
        }
    )

@app.get("/api/dashboard", response_model=ApiResponse)
async def get_dashboard(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get all signature records for dashboard"""
    all_signatures = signatures_table.all()
    
    # Sort by created_at (newest first)
    all_signatures.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    # Apply pagination
    paginated = all_signatures[offset:offset + limit]
    
    return ApiResponse(
        success=True,
        message="Dashboard data retrieved",
        data={
            "signatures": paginated,
            "total": len(all_signatures),
            "limit": limit,
            "offset": offset
        }
    )

@app.get("/sign/{tracking_id}", response_class=HTMLResponse)
async def sign_document_page(tracking_id: str):
    """Serve the signing interface"""
    file_path = Path(__file__).parent / "static" / "sign.html"
    if file_path.exists():
        async with aiofiles.open(str(file_path), 'r') as f:
            content = await f.read()
        return HTMLResponse(content=content)
    else:
        return HTMLResponse(content="<h1>Signing interface coming soon...</h1>")

@app.get("/quiz/{quiz_id}", response_class=HTMLResponse)
async def quiz_page(quiz_id: str):
    """Serve the quiz interface"""
    file_path = Path(__file__).parent / "static" / "quiz.html"
    if file_path.exists():
        async with aiofiles.open(str(file_path), 'r') as f:
            content = await f.read()
        return HTMLResponse(content=content)
    else:
        return HTMLResponse(content="<h1>Quiz interface coming soon...</h1>")

# ===============================
# Admin Functions & Endpoints
# ===============================

async def verify_admin_key(x_admin_key: str = Header(None)):
    """Verify admin API key"""
    if not x_admin_key or x_admin_key != ADMIN_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing admin API key. Provide X-Admin-Key header."
        )
    return True

async def clear_all_signature_data():
    """Clear all signature and quiz data from the database"""
    try:
        # Clear all records from both tables
        signatures_cleared = len(signatures_table.all())
        quizzes_cleared = len(quizzes_table.all())
        
        signatures_table.truncate()
        quizzes_table.truncate()
        
        logger.info(f"Data cleared - Signatures: {signatures_cleared}, Quizzes: {quizzes_cleared}")
        
        return {
            "signatures_cleared": signatures_cleared,
            "quizzes_cleared": quizzes_cleared,
            "timestamp": datetime.now(pytz.timezone('Asia/Kolkata')).isoformat()
        }
    except Exception as e:
        logger.error(f"Error clearing data: {str(e)}")
        raise

@app.delete("/api/admin/clear-all-data", response_model=ApiResponse)
async def clear_all_data_endpoint(admin_verified: bool = Depends(verify_admin_key)):
    """
    Clear all signature and quiz data from the database.
    Requires admin authentication via X-Admin-Key header.
    """
    result = await clear_all_signature_data()
    
    return ApiResponse(
        success=True,
        message="All signature data cleared successfully",
        data=result
    )

@app.delete("/api/admin/clear-old-data", response_model=ApiResponse)
async def clear_old_data_endpoint(
    days: int = Query(30, ge=1, le=365, description="Delete data older than this many days"),
    admin_verified: bool = Depends(verify_admin_key)
):
    """
    Clear signature and quiz data older than specified days.
    Requires admin authentication via X-Admin-Key header.
    """
    try:
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        cutoff_str = cutoff_date.isoformat()
        
        # Count records to be deleted
        SignatureQuery = TinyQuery()
        QuizQuery = TinyQuery()
        
        old_signatures = signatures_table.search(SignatureQuery.created_at < cutoff_str)
        old_quizzes = quizzes_table.search(QuizQuery.created_at < cutoff_str)
        
        signatures_count = len(old_signatures)
        quizzes_count = len(old_quizzes)
        
        # Delete old records
        signatures_table.remove(SignatureQuery.created_at < cutoff_str)
        quizzes_table.remove(QuizQuery.created_at < cutoff_str)
        
        return ApiResponse(
            success=True,
            message=f"Cleared data older than {days} days",
            data={
                "signatures_cleared": signatures_count,
                "quizzes_cleared": quizzes_count,
                "cutoff_date": cutoff_str,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
    except Exception as e:
        logger.error(f"Error clearing old data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clear old data")

# Scheduled task for automatic data cleanup (replaces forward declaration)
scheduled_data_cleanup = None  # Clear the forward declaration
async def scheduled_data_cleanup():
    """Automatically clear all data at midnight IST"""
    try:
        result = await clear_all_signature_data()
        logger.info(f"Scheduled data cleanup completed: {result}")
        
        # Optional: Send notification about cleanup
        if EMAIL_WEBHOOK_URL:
            ist_time = datetime.now(pytz.timezone('Asia/Kolkata'))
            await send_webhook({
                "event_type": "scheduled_cleanup",
                "message": "Nightly data cleanup completed",
                "data": result,
                "timestamp": ist_time.isoformat()
            })
    except Exception as e:
        logger.error(f"Scheduled cleanup failed: {str(e)}")

# ===============================
# Health Check
# ===============================

@app.get("/health", response_model=ApiResponse)
async def health_check():
    """Health check endpoint"""
    return ApiResponse(
        success=True,
        message="Service is healthy",
        data={
            "service": "Document E-Signature Platform",
            "version": "1.0.0",
            "openai_configured": bool(OPENAI_API_KEY),
            "webhook_configured": bool(EMAIL_WEBHOOK_URL),
            "database_connected": True,
            "scheduler_running": scheduler.running
        }
    )

# ===============================
# Run the application
# ===============================

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)