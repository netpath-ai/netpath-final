import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="NetPath AI")

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    success: bool

# Simple HTML Page
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>NetPath AI</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f0f0f0; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
        .chat { border: 1px solid #ddd; padding: 20px; height: 300px; overflow-y: scroll; margin: 20px 0; }
        input { width: 70%; padding: 10px; margin-right: 10px; }
        button { padding: 10px 20px; background: blue; color: white; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 NetPath Network AI</h1>
        <div class="chat" id="chat">
            <div><b>AI:</b> Hello! Ask me networking questions.</div>
        </div>
        <div>
            <input type="text" id="question" placeholder="Ask about OSPF, BGP, subnetting...">
            <button onclick="askAI()">Send</button>
        </div>
    </div>
    <script>
        async function askAI() {
            const question = document.getElementById('question').value;
            const chat = document.getElementById('chat');
            
            chat.innerHTML += `<div><b>You:</b> ${question}</div>`;
            document.getElementById('question').value = '';
            
            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question })
            });
            
            const data = await response.json();
            chat.innerHTML += `<div><b>AI:</b> ${data.answer}</div>`;
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.get("/")
async def home():
    return HTMLResponse(HTML)

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    # Simple response - Baad mein AI add karenge
    answer = f"I received your question: '{request.question}'. AI service will be added soon!"
    return AnswerResponse(answer=answer, success=True)

@app.get("/health")
async def health():
    return {"status": "running", "service": "NetPath AI"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
