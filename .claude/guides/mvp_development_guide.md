# Fullstack FastAPI App Development Guidelines

This document outlines our approach to developing FastAPI applications. These guidelines ensure consistency, simplicity, and ease of sharing across MVP projects.

## Project Structure
- Keep all backend FastAPI code in a single Python file
- Use plain HTML, CSS, and JavaScript (with CDN's) for the frontend
- No build steps

### Standard Structure

```
├── app.py            # All FastAPI backend code
├── static/           # Static assets
│   ├── css/          # CSS files
│   ├── js/           # JavaScript files
│   └── images/       # Image assets
├── templates/        # HTML templates (for Jinja2 templating if needed)
├── requirements.txt  # Dependencies with pinned versions
├── .env.example      # Example environment variables
└── README.md         # Setup and usage instructions
```

### Alternative Structure with Static HTML

For simpler applications or when decoupling frontend from backend, you can serve static HTML directly:

```
├── app.py            # All FastAPI backend code
├── static/           # Static assets
│   ├── index.html    # Main HTML file (served directly)
│   ├── css/          # CSS files
│   ├── js/           # JavaScript files
│   └── images/       # Image assets
├── requirements.txt  # Dependencies with pinned versions
├── .env.example      # Example environment variables
└── README.md         # Setup and usage instructions
```

In this approach, the HTML file is served directly from the static directory:

```python
@app.get("/", response_class=HTMLResponse)
async def get_root():
    """Serve the chat interface."""
    with open("static/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
```

## Backend Guidelines

- Use FastAPI for the backend API
- Keep all routes and logic in a single Python file when possible
- Use Pydantic models for request/response validation
- Implement proper error handling and status codes
- Use async/await for database operations and external API calls

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
```

## Frontend Guidelines

- Use plain HTML, CSS, and JavaScript (no frameworks required)
- Utilize CDNs for dependencies:
  - Tailwind CSS for styling
  - Other libraries as needed (React, etc.)
- Keep the frontend code simple, clean and functional
- The UI should look professional with a great user experience

### Basic HTML/JS Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My FastAPI App</title>
    <!-- Tailwind CSS from CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-4">
        <h1 class="text-2xl font-bold mb-4">My App</h1>
        <div id="content"></div>
    </div>
    
    <script>
        // Fetch data from API
        fetch('/api/data')
            .then(response => response.json())
            .then(data => {
                document.getElementById('content').textContent = data.message;
            });
    </script>
</body>
</html>
```

### React with CDN Example

For more complex UIs, you can use React via CDN without a build step:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>React FastAPI App</title>
    <!-- Tailwind CSS from CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    <!-- Root element for React -->
    <div id="root"></div>
    
    <!-- React CDN -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone@7.8.3/babel.js"></script>
    
    <!-- React Application -->
    <script type="text/babel">
        function App() {
            const [data, setData] = React.useState(null);
            
            React.useEffect(() => {
                fetch('/api/data')
                    .then(response => response.json())
                    .then(result => setData(result));
            }, []);
            
            return (
                <div className="container mx-auto p-4">
                    <h1 className="text-2xl font-bold mb-4">React App</h1>
                    {data ? <div>{data.message}</div> : <div>Loading...</div>}
                </div>
            );
        }
        
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
```

### Component-Based React Structure

For more complex applications, you can organize your React code into components within the same file. This approach is used in the `langgraph-tools-agent` project:

```javascript
// Message types
const MESSAGE_TYPES = {
  USER: 'user',
  ASSISTANT: 'assistant',
  TOOL_CALL: 'tool_call',
  TOOL_RESULT: 'tool_result'
};

// User Message Component
function UserMessage({ message }) {
  return (
    <div className="message-wrapper user">
      <div className="user-message">{message.content}</div>
      <div className="avatar user">U</div>
    </div>
  );
}

// Assistant Message Component
function AssistantMessage({ message }) {
  return (
    <div className="message-wrapper assistant">
      <div className="avatar assistant">AI</div>
      <div className="assistant-message">{message.content}</div>
    </div>
  );
}

// Message Item Component (router for different message types)
function MessageItem({ message }) {
  switch (message.type) {
    case MESSAGE_TYPES.USER:
      return <UserMessage message={message} />;
    case MESSAGE_TYPES.ASSISTANT:
      return <AssistantMessage message={message} />;
    case MESSAGE_TYPES.TOOL_CALL:
      return <ToolCallMessage message={message} />;
    case MESSAGE_TYPES.TOOL_RESULT:
      return <ToolResultMessage message={message} />;
    default:
      return null;
  }
}

// Main App Component
function App() {
  // State management
  const [messages, setMessages] = React.useState([initialMessage]);
  const [input, setInput] = React.useState('');
  
  // API interaction
  const handleSubmit = async (e) => {
    e.preventDefault();
    // Add user message to state
    // Make API call
    // Process response
  };
  
  return (
    <div className="container mx-auto p-4">
      {/* Message display area */}
      <div className="message-container">
        {messages.map(message => (
          <MessageItem key={message.id} message={message} />
        ))}
      </div>
      
      {/* Input form */}
      <form onSubmit={handleSubmit}>
        <input 
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
```

This component-based approach offers several advantages:
- Better organization of UI elements
- Reusable components for similar UI patterns
- Easier maintenance and updates
- Clear separation of concerns

## Dependency Management


- **For sharing**: Each project must be independently sharable
- Create a `requirements.txt` file with pinned versions of all dependencies
- Include a `.env.example` file with required environment variables
- Provide instructions for using environment variables from the root project
- Document all setup steps in README.md, including both options for environment setup:
  1. Creating a new `.env` file from `.env.example`
  2. Using the existing environment variables from the root project


## Deployment and Sharing

- Each project must be independently sharable with others
- Recipients should be able to install dependencies using simple pip commands
- All commands must be documented in the project's README.md file
- Include clear setup instructions in README.md with both UV and pip options:
- Hardcode all package versions to ensure consistency
- Provide a simple way to run the app:



## Database
- Use any simple file base system. It's just MVP. Should not requre any fancy installation. A collection of simple YAML, or JSON, or CSV, TSV - anything simple should be good enough. A simple libary like TinyDB should be good enough.


## Development Guidelines
- for fullstack app prefer a fully working Backend before starting on Frontned
- Every interaction with the BE should be available though API
- document the API contracts withing the file where it's written as comments
- test every api as the extrernal world or frontend would interact with it (maybe using curl commands)
- Do not over complicate. Do not over engineer. 
- Keep things short & simple. 
- Once the Backend is fully tested then start on frontend
- For frontend ask the user for inspiration related to look and feel (give them options)
- In the env file, there should be an email_webhook. That webhook will be used to send emails to any one. (most probably the developer will use make.com to create an email webhook capable of sending an email)
- create all api commands in a rest.rest file. I should be compatible with VSCode REST Client                                         https://marketplace.visualstudio.com/items?itemName=humao.rest-client
- Frontend or end-to-end can be tested with your (claude code) Playwright MCP server.

## Deisgn, Look and Feel
use <project_root>/.claude/guides/designsystem-development-guide.md to create a designguide for this app. designsystem-development-guide.md file sits right next to this file.

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