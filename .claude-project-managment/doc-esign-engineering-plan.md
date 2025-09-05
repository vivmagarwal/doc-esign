# Document E-Signature with Knowledge Verification - Engineering Plan

## Usage
1. Read at session start
2. Update status after EACH task
3. Document discoveries inline
4. Keep sections current

## Workflow
1. Verify previous story = `completed`
2. Check ALL pre_implementation flags = `true` (never skip)
3. Execute task by task systematically
4. Update `task_notes` with context (critical - only source of truth)
5. Ensure working app after EVERY step

## Recommended MCP Servers
- **Playwright**: Verify UI changes and test signing flow
- **Context7**: Get FastAPI and TinyDB documentation
- **Firecrawl**: Research webhook patterns if needed

## Rules
- NO legacy fallback (unless explicit)
- NO backwards compatibility (unless explicit)
- Simple, robust, reliable, maintainable code
- After EACH feature: compile → test → verify
- Test external behavior (API calls, tools executed, results returned)
- Remove ALL mocks/simulations before completion
- Ask clarifying questions upfront
- Identify files to change per task

## Project Overview
Build a free document e-signature platform with AI-powered knowledge verification. Users send pre-stored documents via API, recipients acknowledge and sign, then must pass a 3-question AI-generated quiz for valid signature. Features include public dashboard, email notifications via webhook, and uses FastAPI backend with vanilla JS frontend following MVP principles.

## Story Breakdown and Status

```yaml
stories:
  - story_id: "STORY-001"
    story_title: "Environment Setup and Project Structure"
    story_description: "Set up development environment with all required files and configurations"
    story_pre_implementation:
      requirements_understood: false
      context_gathered: false
      plan_read: false
      architecture_documented: false
      environment_ready: false
      tests_defined: false
    story_post_implementation:
      all_tasks_completed: false
      feature_working: false
      plan_updated: false
    story_implementation_status: "not_started"  # not_started | in_progress | completed
    tasks:
      - task_id: "TASK-001.1"
        task_title: "Create project structure and dependency files"
        task_description: "Set up all directories, create requirements.txt with FastAPI dependencies, and .env files"
        task_acceptance_criteria:
          - "requirements.txt created with FastAPI, TinyDB, OpenAI, httpx"
          - ".env.example created with all required variables"
          - "All directories created (static, db)"
          - ".env created with actual OpenAI key"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "requirements.txt (create)"
          - ".env.example (create)"
          - ".env (create)"
          - "README.md (create)"

  - story_id: "STORY-002"
    story_title: "Core FastAPI Backend Setup"
    story_description: "Implement FastAPI application with basic structure and CORS configuration"
    story_pre_implementation:
      requirements_understood: false
      context_gathered: false
      plan_read: false
      architecture_documented: false
      environment_ready: false
      tests_defined: false
    story_post_implementation:
      all_tasks_completed: false
      feature_working: false
      plan_updated: false
    story_implementation_status: "not_started"
    tasks:
      - task_id: "TASK-002.1"
        task_title: "Create FastAPI app with basic setup"
        task_description: "Initialize FastAPI app with CORS, static file serving, and database setup"
        task_acceptance_criteria:
          - "app.py created with FastAPI initialization"
          - "CORS middleware configured for all origins"
          - "Static file mounting configured"
          - "TinyDB initialized with tables for signatures and quizzes"
          - "Server runs on localhost:8000"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "app.py (create)"

      - task_id: "TASK-002.2"
        task_title: "Create Pydantic models for data validation"
        task_description: "Define all request/response models for API endpoints"
        task_acceptance_criteria:
          - "Models for SendDocumentRequest, SignatureSubmission, QuizSubmission"
          - "Response models for all endpoints"
          - "Proper validation rules applied"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "app.py (update)"

  - story_id: "STORY-003"
    story_title: "Document Management System"
    story_description: "Implement document loading and serving from pre-stored markdown files"
    story_pre_implementation:
      requirements_understood: false
      context_gathered: false
      plan_read: false
      architecture_documented: false
      environment_ready: false
      tests_defined: false
    story_post_implementation:
      all_tasks_completed: false
      feature_working: false
      plan_updated: false
    story_implementation_status: "not_started"
    tasks:
      - task_id: "TASK-003.1"
        task_title: "Create document loading and parsing system"
        task_description: "Load markdown documents from documents/ folder and convert to HTML for display"
        task_acceptance_criteria:
          - "Function to list available documents"
          - "Function to load document by ID"
          - "Markdown to HTML conversion working"
          - "Document metadata extracted (title, sections)"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "app.py (update)"

      - task_id: "TASK-003.2"
        task_title: "Create GET endpoint for document retrieval"
        task_description: "API endpoint to fetch document content and metadata"
        task_acceptance_criteria:
          - "GET /api/documents/{document_id} returns document content"
          - "404 error for non-existent documents"
          - "Document content properly formatted"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "app.py (update)"

  - story_id: "STORY-004"
    story_title: "Send Document API Implementation"
    story_description: "Create API endpoint to initiate document signature requests"
    story_pre_implementation:
      requirements_understood: false
      context_gathered: false
      plan_read: false
      architecture_documented: false
      environment_ready: false
      tests_defined: false
    story_post_implementation:
      all_tasks_completed: false
      feature_working: false
      plan_updated: false
    story_implementation_status: "not_started"
    tasks:
      - task_id: "TASK-004.1"
        task_title: "Implement POST /api/send-document endpoint"
        task_description: "Create endpoint to initiate signature request with all required parameters"
        task_acceptance_criteria:
          - "Accepts sender_email, sender_name, purpose, receiver_email, document_id"
          - "Generates unique tracking_id"
          - "Stores request in database"
          - "Returns tracking_id and status"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "app.py (update)"

      - task_id: "TASK-004.2"
        task_title: "Implement email notification for signature request"
        task_description: "Send initial email to recipient with signing link using webhook"
        task_acceptance_criteria:
          - "Email payload created with signing link"
          - "Webhook called to Make.com endpoint"
          - "Error handling for webhook failures"
          - "Retry mechanism implemented"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "app.py (update)"

  - story_id: "STORY-005"
    story_title: "OpenAI Integration for Quiz Generation"
    story_description: "Integrate OpenAI API to generate quiz questions from documents"
    story_pre_implementation:
      requirements_understood: false
      context_gathered: false
      plan_read: false
      architecture_documented: false
      environment_ready: false
      tests_defined: false
    story_post_implementation:
      all_tasks_completed: false
      feature_working: false
      plan_updated: false
    story_implementation_status: "not_started"
    tasks:
      - task_id: "TASK-005.1"
        task_title: "Create OpenAI client and quiz generation function"
        task_description: "Set up OpenAI client with GPT-4o mini and create function to generate 3 multiple choice questions"
        task_acceptance_criteria:
          - "OpenAI client initialized with API key from .env"
          - "Function generates exactly 3 questions with 4 options each"
          - "Structured output format for quiz questions"
          - "Error handling for API failures"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "app.py (update)"

      - task_id: "TASK-005.2"
        task_title: "Create email subject and body generation"
        task_description: "Use OpenAI to generate contextual email content based on document type"
        task_acceptance_criteria:
          - "Function generates email subject line"
          - "Function generates email body content"
          - "Content is contextual to document type"
          - "Fallback to template if generation fails"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "app.py (update)"

  - story_id: "STORY-006"
    story_title: "Signature Submission Flow"
    story_description: "Implement signature collection and quiz delivery system"
    story_pre_implementation:
      requirements_understood: false
      context_gathered: false
      plan_read: false
      architecture_documented: false
      environment_ready: false
      tests_defined: false
    story_post_implementation:
      all_tasks_completed: false
      feature_working: false
      plan_updated: false
    story_implementation_status: "not_started"
    tasks:
      - task_id: "TASK-006.1"
        task_title: "Create POST /api/submit-signature endpoint"
        task_description: "Endpoint to receive signature acknowledgment and trigger quiz generation"
        task_acceptance_criteria:
          - "Accepts acknowledged, date, location, name fields"
          - "Updates signature record in database"
          - "Generates quiz questions for the document"
          - "Returns quiz_url for recipient"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "app.py (update)"

      - task_id: "TASK-006.2"
        task_title: "Send quiz link email"
        task_description: "Send email with quiz link after signature submission"
        task_acceptance_criteria:
          - "Email sent with unique quiz link"
          - "Quiz questions stored in database"
          - "Quiz linked to signature record"
          - "Email uses AI-generated content"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "app.py (update)"

  - story_id: "STORY-007"
    story_title: "Quiz Validation System"
    story_description: "Implement quiz submission and validation logic"
    story_pre_implementation:
      requirements_understood: false
      context_gathered: false
      plan_read: false
      architecture_documented: false
      environment_ready: false
      tests_defined: false
    story_post_implementation:
      all_tasks_completed: false
      feature_working: false
      plan_updated: false
    story_implementation_status: "not_started"
    tasks:
      - task_id: "TASK-007.1"
        task_title: "Create POST /api/submit-quiz endpoint"
        task_description: "Endpoint to receive and validate quiz answers"
        task_acceptance_criteria:
          - "Accepts quiz_id and answers"
          - "Validates all 3 answers are correct"
          - "Updates signature status based on result"
          - "Returns pass/fail status"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "app.py (update)"

      - task_id: "TASK-007.2"
        task_title: "Send completion notifications"
        task_description: "Send success/failure emails to recipient and completion email to sender"
        task_acceptance_criteria:
          - "Success email sent to recipient if quiz passed"
          - "Failure message if quiz failed"
          - "Notification sent to original sender on success"
          - "Status updated in database"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "app.py (update)"

  - story_id: "STORY-008"
    story_title: "Public Dashboard API"
    story_description: "Create dashboard endpoint to display all document statuses"
    story_pre_implementation:
      requirements_understood: false
      context_gathered: false
      plan_read: false
      architecture_documented: false
      environment_ready: false
      tests_defined: false
    story_post_implementation:
      all_tasks_completed: false
      feature_working: false
      plan_updated: false
    story_implementation_status: "not_started"
    tasks:
      - task_id: "TASK-008.1"
        task_title: "Create GET /api/dashboard endpoint"
        task_description: "Endpoint to retrieve all signature records for public dashboard"
        task_acceptance_criteria:
          - "Returns list of all signature records"
          - "Includes sender info, recipient, status, timestamps"
          - "Sorted by creation date (newest first)"
          - "Pagination support for large datasets"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "app.py (update)"

  - story_id: "STORY-009"
    story_title: "Frontend - Dashboard Interface"
    story_description: "Create public dashboard HTML interface with real-time updates"
    story_pre_implementation:
      requirements_understood: false
      context_gathered: false
      plan_read: false
      architecture_documented: false
      environment_ready: false
      tests_defined: false
    story_post_implementation:
      all_tasks_completed: false
      feature_working: false
      plan_updated: false
    story_implementation_status: "not_started"
    tasks:
      - task_id: "TASK-009.1"
        task_title: "Create dashboard HTML with Tailwind styling"
        task_description: "Build responsive dashboard interface showing all document statuses"
        task_acceptance_criteria:
          - "index.html created with Tailwind CDN"
          - "Table layout for signature records"
          - "Status badges with colors"
          - "Mobile responsive design"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "static/index.html (create)"
          - "static/css/styles.css (create)"

      - task_id: "TASK-009.2"
        task_title: "Add JavaScript for data fetching and updates"
        task_description: "Implement JavaScript to fetch dashboard data and update UI"
        task_acceptance_criteria:
          - "Fetch data from /api/dashboard"
          - "Populate table with signature records"
          - "Auto-refresh every 30 seconds"
          - "Search and filter functionality"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "static/js/dashboard.js (create)"
          - "static/index.html (update)"

  - story_id: "STORY-010"
    story_title: "Frontend - Document Signing Interface"
    story_description: "Create document viewing and signature collection interface"
    story_pre_implementation:
      requirements_understood: false
      context_gathered: false
      plan_read: false
      architecture_documented: false
      environment_ready: false
      tests_defined: false
    story_post_implementation:
      all_tasks_completed: false
      feature_working: false
      plan_updated: false
    story_implementation_status: "not_started"
    tasks:
      - task_id: "TASK-010.1"
        task_title: "Create document signing HTML interface"
        task_description: "Build interface for viewing documents and collecting signature"
        task_acceptance_criteria:
          - "sign.html created with document display area"
          - "Signature form with all required fields"
          - "Acknowledge checkbox/button"
          - "Professional styling with Tailwind"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "static/sign.html (create)"

      - task_id: "TASK-010.2"
        task_title: "Add JavaScript for signature submission"
        task_description: "Implement form validation and submission logic"
        task_acceptance_criteria:
          - "Form validation for all required fields"
          - "Submit signature to API endpoint"
          - "Handle success/error responses"
          - "Redirect to quiz on success"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "static/js/sign.js (create)"
          - "static/sign.html (update)"

  - story_id: "STORY-011"
    story_title: "Frontend - Quiz Interface"
    story_description: "Create quiz interface for knowledge verification"
    story_pre_implementation:
      requirements_understood: false
      context_gathered: false
      plan_read: false
      architecture_documented: false
      environment_ready: false
      tests_defined: false
    story_post_implementation:
      all_tasks_completed: false
      feature_working: false
      plan_updated: false
    story_implementation_status: "not_started"
    tasks:
      - task_id: "TASK-011.1"
        task_title: "Create quiz HTML interface"
        task_description: "Build interface for displaying and answering quiz questions"
        task_acceptance_criteria:
          - "quiz.html created with question display"
          - "Multiple choice radio buttons for answers"
          - "Progress indicator for 3 questions"
          - "Submit button with confirmation"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "static/quiz.html (create)"

      - task_id: "TASK-011.2"
        task_title: "Add JavaScript for quiz functionality"
        task_description: "Implement quiz loading, answer selection, and submission"
        task_acceptance_criteria:
          - "Load quiz questions from API"
          - "Track selected answers"
          - "Submit answers to API"
          - "Display pass/fail result"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "static/js/quiz.js (create)"
          - "static/quiz.html (update)"

  - story_id: "STORY-012"
    story_title: "End-to-End Testing and Documentation"
    story_description: "Test complete flow and create documentation"
    story_pre_implementation:
      requirements_understood: false
      context_gathered: false
      plan_read: false
      architecture_documented: false
      environment_ready: false
      tests_defined: false
    story_post_implementation:
      all_tasks_completed: false
      feature_working: false
      plan_updated: false
    story_implementation_status: "not_started"
    tasks:
      - task_id: "TASK-012.1"
        task_title: "Test complete signature flow"
        task_description: "Test sending, signing, quiz, and completion flow end-to-end"
        task_acceptance_criteria:
          - "Send document via API works"
          - "Sign document interface works"
          - "Quiz generation and validation works"
          - "Email notifications sent correctly"
          - "Dashboard updates properly"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "test_api.py (create)"

      - task_id: "TASK-012.2"
        task_title: "Update README with setup instructions"
        task_description: "Create comprehensive README with installation and usage guide"
        task_acceptance_criteria:
          - "Installation steps documented"
          - "Environment variable setup explained"
          - "API usage examples provided"
          - "Troubleshooting section included"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
        files_to_change:
          - "README.md (update)"
```

## Architecture Decisions

**Decision 1**: Single-file FastAPI architecture
- Reasoning: MVP simplicity, easier to share and deploy
- Impact: All backend code in app.py, may need refactoring for scale

**Decision 2:** TinyDB for storage
- Reasoning: No installation required, JSON-based, perfect for MVP
- Impact: Limited concurrent access, plan PostgreSQL migration path

**Decision 3:** GPT-4o mini for quiz generation
- Reasoning: 60% cheaper than GPT-3.5-turbo with better quality
- Impact: ~$15-30 per 1,000 quizzes with optimization

**Decision 4:** Vanilla JS with CDN libraries
- Reasoning: No build process, immediate development, easy sharing
- Impact: Modern browser required, may need bundling for production

**Decision 5:** Webhook-based email via Make.com
- Reasoning: No email server setup, reliable delivery, free tier available
- Impact: Dependency on external service, need error handling

## Commands

```bash
# Setup
pip install -r requirements.txt
# or with uv
uv pip install -r requirements.txt

# Development
python app.py
# or
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Test API
curl -X POST http://localhost:8000/api/send-document \
  -H "Content-Type: application/json" \
  -d '{
    "sender_email": "sender@example.com",
    "sender_name": "John Doe",
    "purpose": "Policy acknowledgment",
    "receiver_email": "recipient@example.com",
    "document_id": "company_policy"
  }'

# View Dashboard
open http://localhost:8000
```

## Standards
- FastAPI async/await patterns for all endpoints
- Pydantic models for request/response validation
- TinyDB Query objects for database operations
- Structured logging with correlation IDs
- Error responses follow consistent format
- All timestamps in ISO 8601 format

## Git Flow
- Branch: feature/doc-esign-mvp
- Commit: "TASK-{id}: {description}"
- PR after story complete
- Main branch for production-ready code

## Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [TinyDB Docs](https://tinydb.readthedocs.io/)
- [OpenAI API](https://platform.openai.com/docs/)
- [Tailwind Play CDN](https://tailwindcss.com/docs/installation/play-cdn)

## Config Files
- requirements.txt: Python dependencies with pinned versions
- .env: Environment variables (OpenAI key, webhook URL, app settings)
- .env.example: Template for environment setup
- db/esign.json: TinyDB database file (auto-created)

## Directory Structure
```
doc_esign/
├── app.py                    # All FastAPI backend code
├── static/                   
│   ├── index.html           # Dashboard interface
│   ├── sign.html            # Document signing interface
│   ├── quiz.html            # Quiz interface
│   ├── css/                 
│   │   └── styles.css       # Custom CSS if needed
│   └── js/                  
│       ├── dashboard.js     # Dashboard functionality
│       ├── sign.js          # Signing functionality
│       └── quiz.js          # Quiz functionality
├── documents/               # Pre-stored MD documents [EXISTS]
│   ├── company_policy.md    # [EXISTS]
│   ├── nda_policy.md        # [EXISTS]
│   └── dev_guidelines.md    # [EXISTS]
├── db/                      # Database directory
│   └── esign.json          # TinyDB file (auto-created)
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── .env                    # Actual environment variables
├── README.md               # Setup and usage guide
└── test_api.py            # API testing script
```

## API Endpoints Summary

1. **POST /api/send-document** - Initiate signature request
2. **GET /api/documents/{document_id}** - Retrieve document content
3. **POST /api/submit-signature/{tracking_id}** - Submit signature acknowledgment
4. **GET /api/quiz/{quiz_id}** - Get quiz questions
5. **POST /api/submit-quiz/{quiz_id}** - Submit quiz answers
6. **GET /api/dashboard** - Get all signature records
7. **GET /** - Serve dashboard HTML
8. **GET /sign/{tracking_id}** - Serve signing interface
9. **GET /quiz/{quiz_id}** - Serve quiz interface

## Error Handling Strategy

- 400: Bad Request - Invalid input data
- 404: Not Found - Document or record doesn't exist
- 500: Internal Server Error - Server issues
- 503: Service Unavailable - External service failures (OpenAI, webhook)

All errors return consistent JSON:
```json
{
  "success": false,
  "error": "Error description",
  "message": "User-friendly message",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Security Considerations

- No authentication required (free service)
- Input validation on all endpoints
- SQL injection prevention via TinyDB
- XSS prevention in frontend
- CORS configured for production domain
- Environment variables for secrets
- No PII stored beyond email addresses

## Performance Targets

- API response time: < 200ms (except quiz generation)
- Quiz generation: < 3 seconds
- Dashboard load: < 1 second
- Webhook timeout: 30 seconds with retry
- Database queries: < 50ms
- Frontend page load: < 2 seconds