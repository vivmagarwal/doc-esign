# FastAPI Render Deployment Checklist

## Required Files
- `requirements.txt` with all dependencies including `email-validator` if using Pydantic EmailStr
- `run.py` or proper startup script for uvicorn

### Example run.py
```python
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
```

## Environment Variables
Set all required env vars in Render dashboard:
- API keys
- Database paths
- Service URLs

## Start Command
Use one of these:
- `python run.py` (if you have a run.py with uvicorn)
- `uvicorn app:app --host 0.0.0.0 --port $PORT`
- `gunicorn app:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

## Common Issues
- FastAPI needs ASGI server (uvicorn), not WSGI (plain gunicorn)
- Missing `email-validator` when using Pydantic EmailStr
- Environment variables not set before first deployment