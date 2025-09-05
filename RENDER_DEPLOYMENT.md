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
- Static files not found: Use absolute paths with `Path(__file__).parent / "static"`

## Static Files Fix
Always use absolute paths for static files in production:
```python
from pathlib import Path

# For mounting static files
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir), html=True), name="static")

# For serving HTML files
file_path = Path(__file__).parent / "static" / "index.html"
if file_path.exists():
    async with aiofiles.open(str(file_path), 'r') as f:
        content = await f.read()
```