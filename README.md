# Document E-Signature Platform with Knowledge Verification

A free document e-signature platform that ensures recipients understand what they're signing through AI-powered knowledge verification.

## Features

- 📝 Send pre-stored documents for e-signature via API
- ✍️ Recipients acknowledge and sign documents
- 🧠 AI-generated quiz to verify document comprehension
- 📊 Public dashboard showing all document statuses
- 📧 Automated email notifications via webhook
- 🎯 100% quiz pass requirement for valid signature

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip or uv package manager

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd doc_esign
```

2. Install dependencies
```bash
pip install -r requirements.txt
# OR using uv
uv pip install -r requirements.txt
```

3. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. Run the application
```bash
python app.py
# OR
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

5. Access the dashboard
```bash
open http://localhost:8000
```

## API Usage

### Send Document for Signature
```bash
curl -X POST http://localhost:8000/api/send-document \
  -H "Content-Type: application/json" \
  -d '{
    "sender_email": "sender@example.com",
    "sender_name": "John Doe",
    "purpose": "Annual policy acknowledgment",
    "receiver_email": "recipient@example.com",
    "document_id": "company_policy"
  }'
```

### Available Documents
- `company_policy` - Company Policy and Employee Handbook
- `nda_policy` - Non-Disclosure Agreement
- `dev_guidelines` - Development Guidelines and Standards

## Workflow

1. **Send Document**: Use API to send document to recipient
2. **Receive Email**: Recipient gets email with signing link
3. **Sign Document**: Recipient reads and acknowledges document
4. **Take Quiz**: Complete 3-question quiz about document content
5. **Validation**: All questions must be correct for valid signature
6. **Completion**: Both parties notified of successful signing

## Project Structure

```
doc_esign/
├── app.py                    # FastAPI backend
├── static/                   # Frontend files
│   ├── index.html           # Dashboard
│   ├── sign.html            # Signing interface
│   ├── quiz.html            # Quiz interface
│   └── js/                  # JavaScript files
├── documents/               # Pre-stored documents
├── db/                      # Database files
├── requirements.txt         # Python dependencies
└── .env                     # Configuration
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| OPENAI_API_KEY | OpenAI API key for quiz generation | sk-... |
| OPENAI_MODEL | Model to use (gpt-4o-mini recommended) | gpt-4o-mini |
| EMAIL_WEBHOOK_URL | Make.com webhook for email sending | https://hook.eu2.make.com/... |
| APP_URL | Application base URL | http://localhost:8000 |
| PORT | Server port | 8000 |
| DB_PATH | Database file path | db/esign.json |

## Technologies Used

- **Backend**: FastAPI, Python
- **Database**: TinyDB (file-based)
- **Frontend**: Vanilla JavaScript, Tailwind CSS
- **AI**: OpenAI GPT-4o mini
- **Email**: Make.com webhooks

## Cost Estimation

- Quiz generation: ~$15-30 per 1,000 quizzes using GPT-4o mini
- Email sending: Free tier available on Make.com

## Troubleshooting

### OpenAI API Errors
- Verify API key is correct in `.env`
- Check API quota and billing status
- Model fallback implemented for failures

### Email Not Sending
- Verify webhook URL is correct
- Check Make.com scenario is active
- Review webhook payload in logs

### Database Issues
- Ensure `db/` directory exists
- Check file permissions
- Database auto-creates on first run

## Support

For issues or questions, please check the documentation or create an issue in the repository.

## License

This is a free, open-source project for educational purposes.