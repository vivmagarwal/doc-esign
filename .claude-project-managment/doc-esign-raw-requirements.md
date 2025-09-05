# Document E-Signature Platform with Knowledge Verification - Requirements

## Introduction

### Problem Statement
Organizations struggle with remote document signing and acknowledgment, particularly for critical policies and guidelines where comprehension verification is essential. Current solutions lack integrated knowledge testing to ensure signers have actually read and understood the documents they're signing.

### Solution Overview
A free, web-based e-signature platform that combines document signing with mandatory knowledge verification through AI-generated quizzes. The system ensures document comprehension by requiring signers to pass a 3-question quiz before their signature is considered valid.

### Target Users
- **Document Senders**: HR departments, legal teams, training coordinators, compliance officers
- **Document Recipients**: Employees, contractors, partners who need to sign and acknowledge important documents

## User Stories

### Sender Stories
1. **As a document sender**, I want to send documents for e-signature via a simple API call so that I can integrate the service into my existing workflows
2. **As a document sender**, I want to track signature status on a public dashboard so that I can monitor completion rates
3. **As a document sender**, I want to receive email notifications when documents are successfully signed so that I can take follow-up actions
4. **As a document sender**, I want recipients to prove they read the document so that I can ensure compliance and understanding

### Recipient Stories
5. **As a document recipient**, I want to easily read and acknowledge documents so that I can complete required signatures quickly
6. **As a document recipient**, I want to receive clear email communications so that I understand what actions I need to take
7. **As a document recipient**, I want immediate feedback on quiz completion so that I know my signature status

## Core Requirements

### Functional Requirements

#### 1. Document Management
- **Pre-stored Documents**: System shall maintain a library of pre-stored markdown documents
  - Company Policy document
  - NDA Policy document
  - Development Guidelines document
  - Additional documents as needed
- **Document Format**: All documents stored as simple markdown (.md) files
- **No Dynamic Upload**: Documents are pre-configured, not uploaded by users

#### 2. API Endpoint for Sending Documents
- **Single API Call**: POST endpoint to initiate document signature request
- **Required Parameters**:
  - `sender_email`: Email address of sender
  - `sender_name`: Name of the person sending the document
  - `purpose`: Reason for sending the document
  - `receiver_email`: Email address of recipient
  - `document_id`: Identifier for the pre-stored document
- **Response**: Returns tracking ID and status
- **No Authentication Required**: Public API (as it's a free service)

#### 3. Signature Collection Interface
- **Document Display**: Render markdown document in readable format
- **Signature Fields**:
  - Acknowledge button (checkbox or button click)
  - Date field (auto-populated or manual entry)
  - Location field (city/country)
  - Name field (full name entry)
  - Submit button
- **No Account Creation**: Recipients sign as guests without registration

#### 4. Knowledge Verification System
- **Quiz Generation**:
  - Use OpenAI API (GPT-4o mini model) to generate 3 multiple-choice questions
  - Questions dynamically generated from document content
  - Each question has 4 options (A, B, C, D)
- **Quiz Delivery**:
  - Link sent via email after initial document submission
  - Opens in browser with quiz interface
- **Validation Rules**:
  - All 3 questions must be answered correctly
  - No partial credit
  - Signature invalid until quiz passed
- **Quiz Retake**: Allow unlimited attempts (requirement to clarify)

#### 5. Email Integration
- **Webhook Configuration**:
  - Email webhook URL in .env file
  - Fixed webhook: `https://hook.eu2.make.com/57dd2q56dzq8yis4qbkrlt5p473i7q5e`
  - Send structured JSON payload to webhook
- **Email Types**:
  1. Initial signature request to recipient
  2. Quiz link after document acknowledgment
  3. Success notification to recipient (quiz passed)
  4. Completion notification to sender
- **AI-Generated Content**:
  - Use OpenAI to generate email subject lines
  - Use OpenAI to generate email body content
  - Based on document type and context

#### 6. Public Dashboard
- **Display Information**:
  - Document type
  - Sender name and email
  - Recipient email
  - Timestamp of sending
  - Current status (Sent, Acknowledged, Quiz Pending, Quiz Failed, Completed)
  - Completion timestamp (if applicable)
- **No Authentication**: Publicly accessible dashboard
- **Real-time Updates**: Status updates as actions occur
- **Simple Table View**: Clean, sortable table interface

### User Interface Requirements

#### 1. Document Signing Page
- Clean, professional layout
- Document displayed with good typography
- Clear action buttons
- Mobile-responsive design
- Progress indicator showing steps

#### 2. Quiz Interface
- Question displayed one at a time or all on one page
- Clear multiple-choice layout
- Submit button
- Immediate feedback on completion
- Show correct/incorrect status

#### 3. Public Dashboard
- Sortable table columns
- Status badges with colors
- Search/filter functionality
- Pagination for large datasets
- Export capability (CSV)

### Technical Architecture

#### Technology Stack (Based on MVP Guidelines)
- **Backend**: FastAPI (single Python file - app.py)
- **Frontend**: Plain HTML, CSS, JavaScript with CDN libraries
  - Tailwind CSS for styling
  - Vanilla JavaScript for interactivity
- **Database**: TinyDB or JSON files (simple file-based storage)
- **Email Service**: Webhook to Make.com
- **AI Service**: OpenAI API (GPT-4o mini)

#### Project Structure
```
doc_esign/
├── app.py                 # All FastAPI backend code
├── static/               
│   ├── index.html        # Dashboard interface
│   ├── sign.html         # Document signing interface
│   ├── quiz.html         # Quiz interface
│   ├── css/              
│   │   └── styles.css    # Custom styles
│   └── js/               
│       └── main.js       # Frontend JavaScript
├── documents/            # Pre-stored MD documents
│   ├── company_policy.md
│   ├── nda_policy.md
│   └── dev_guidelines.md
├── db/                   # Database files
│   ├── signatures.json   # Signature records
│   └── quizzes.json      # Quiz attempts
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Actual environment variables
└── README.md            # Setup instructions
```

### Edge Cases & Error Handling

1. **Invalid Email Addresses**: Validate email format before sending
2. **Document Not Found**: Return 404 if document_id doesn't exist
3. **Quiz Generation Failure**: Fallback to pre-generated questions
4. **Email Sending Failure**: Retry mechanism with exponential backoff
5. **Incomplete Submission**: Save progress and allow resumption
6. **Multiple Quiz Attempts**: Track all attempts in database
7. **Concurrent Submissions**: Handle race conditions in status updates
8. **OpenAI API Errors**: Graceful degradation with cached questions
9. **Webhook Timeout**: Queue system for retry
10. **Browser Compatibility**: Support modern browsers (Chrome, Firefox, Safari, Edge)

## Success Metrics

- **Signature Completion Rate**: % of sent documents that get signed
- **Quiz Pass Rate**: % of quiz attempts that pass on first try
- **Time to Complete**: Average time from send to successful completion
- **System Uptime**: 99% availability
- **API Response Time**: < 500ms for signature requests
- **Quiz Generation Time**: < 3 seconds

## Acceptance Criteria

### Minimum Viable Product (MVP)
1. ✓ Can send 3 types of pre-stored documents via API
2. ✓ Recipients can view and acknowledge documents
3. ✓ Quiz with 3 questions generated from document content
4. ✓ All 3 questions must be answered correctly for valid signature
5. ✓ Email notifications sent at key stages
6. ✓ Public dashboard shows all document statuses
7. ✓ System uses GPT-4o mini for cost-effective quiz generation
8. ✓ No user authentication required (free service)

### Definition of Done
- All API endpoints tested and documented
- Frontend interfaces responsive on mobile and desktop
- Email integration verified with Make.com webhook
- OpenAI integration generates relevant questions
- Dashboard updates in real-time
- Error handling for all edge cases
- README with complete setup instructions
- Environment variables properly configured

## Out of Scope

### Current Implementation
- User authentication and accounts
- Document upload functionality
- PDF generation or certificates
- Document templates or customization
- Signature drawing or image upload
- Multi-language support
- Document expiration dates
- Bulk sending capabilities
- Analytics beyond basic dashboard
- Integration with other e-signature platforms

### Future Enhancements (Not in MVP)
- User accounts with login
- Custom document uploads
- PDF certificate generation
- Advanced analytics and reporting
- API rate limiting and authentication
- Document versioning
- Conditional logic in documents
- Multiple signature workflows
- Mobile applications
- Blockchain verification
- Advanced quiz features (hints, explanations)
- Partial credit for quiz answers
- Time limits on quiz completion

## Environment Configuration

### Required Environment Variables
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-w5KbLu8HTYBTr_nLQLW2jS0rpzuIovVEcMPkpuU_FTCENadrgRjdQ1
  TP8i6yQGTLq-uxN_SuzCT3BlbkFJPHXWvTMHshWqXHI7f8kxx6gdb4oTXuieD6iuxZaG_OUwQo0QIHZV
  WuRT5TirN8hCTaPyDPLMIA  # Your OpenAI API key
OPENAI_MODEL=gpt-4o-mini      # Model for quiz generation

# Email Webhook
EMAIL_WEBHOOK_URL=https://hook.eu2.make.com/57dd2q56dzq8yis4qbkrlt5p473i7q5e

# Application Settings
APP_URL=http://localhost:8000  # Base URL for links in emails
PORT=8000                       # Server port
```

## API Contract

### Send Document for Signature
```http
POST /api/send-document
Content-Type: application/json

{
  "sender_email": "sender@example.com",
  "sender_name": "John Doe",
  "purpose": "Annual policy acknowledgment",
  "receiver_email": "recipient@example.com",
  "document_id": "company_policy"
}

Response:
{
  "success": true,
  "tracking_id": "uuid-here",
  "message": "Document sent successfully"
}
```

### Submit Signature
```http
POST /api/submit-signature/{tracking_id}
Content-Type: application/json

{
  "acknowledged": true,
  "date": "2024-01-15",
  "location": "New York, USA",
  "name": "Jane Smith"
}

Response:
{
  "success": true,
  "quiz_url": "http://localhost:8000/quiz/uuid-here",
  "message": "Acknowledgment received. Please complete the quiz."
}
```

### Submit Quiz
```http
POST /api/submit-quiz/{quiz_id}
Content-Type: application/json

{
  "answers": {
    "q1": "A",
    "q2": "C",
    "q3": "B"
  }
}

Response:
{
  "success": true,
  "passed": true,
  "score": 3,
  "message": "Congratulations! Document successfully signed."
}
```

### Get Dashboard Data
```http
GET /api/dashboard

Response:
{
  "signatures": [
    {
      "id": "uuid",
      "document": "Company Policy",
      "sender_name": "John Doe",
      "sender_email": "sender@example.com",
      "receiver_email": "recipient@example.com",
      "status": "Completed",
      "sent_at": "2024-01-15T10:00:00Z",
      "completed_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## Implementation Priority

### Phase 1: Core Backend (Week 1)
1. FastAPI setup with basic structure
2. Document storage and retrieval
3. Send document API endpoint
4. Database setup (TinyDB)

### Phase 2: Signature Flow (Week 1)
1. Signature submission endpoint
2. Email webhook integration
3. Basic email sending

### Phase 3: Quiz System (Week 2)
1. OpenAI integration
2. Quiz generation from documents
3. Quiz submission and validation
4. Status management

### Phase 4: Frontend (Week 2)
1. Document viewing interface
2. Signature form
3. Quiz interface
4. Public dashboard

### Phase 5: Polish & Testing (Week 3)
1. Error handling
2. Email templates with AI
3. Testing all flows
4. Documentation

## Risk Mitigation

1. **OpenAI API Costs**: Use GPT-4o mini and implement caching
2. **Email Deliverability**: Use established webhook service (Make.com)
3. **Data Privacy**: No sensitive data stored, public dashboard shows minimal info
4. **Scalability**: File-based DB suitable for MVP, can migrate later
5. **Security**: No authentication reduces attack surface for MVP