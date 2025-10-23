import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import httpx
import uvicorn
from typing import Optional

# NetPath Network AI
COMPANY_NAME = "NetPath Network AI"

app = FastAPI(title=COMPANY_NAME)

# API Configuration
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-2cd9e8b7ecf043ca8cfcdf133aefb5b8")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    success: bool

async def get_ai_response(question: str) -> str:
    """Get response from DeepSeek API"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a Network Engineering expert. Provide helpful answers about networking topics."
                },
                {
                    "role": "user", 
                    "content": question
                }
            ],
            "max_tokens": 500
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(DEEPSEEK_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
            
    except Exception:
        return "I'm currently learning about networking. Please try again later."

# Simple HTML Interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>NetPath Network AI</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: #2c3e50;
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 2.2em;
            margin-bottom: 10px;
        }
        .chat-container {
            padding: 20px;
            height: 400px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        .message {
            margin: 10px 0;
            padding: 15px;
            border-radius: 10px;
            max-width: 80%;
        }
        .user-message {
            background: #3498db;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        .ai-message {
            background: white;
            border-left: 4px solid #2ecc71;
        }
        .input-container {
            padding: 20px;
            background: white;
            display: flex;
            gap: 10px;
            border-top: 1px solid #eee;
        }
        .input-container input {
            flex: 1;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        .input-container button {
            padding: 15px 25px;
            background: #2ecc71;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }
        .input-container button:hover {
            background: #27ae60;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌐 NetPath Network AI</h1>
            <p>Your Network Engineering Assistant</p>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message ai-message">
                <strong>AI:</strong> Namaste! I'm your Network Engineering AI. Ask me about OSPF, BGP, subnetting, VLANs, or any networking topic!
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="userInput" 
                   placeholder="Ask about networking... (Hindi or English)" 
                   onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Send 🚀</button>
        </div>
    </div>

    <script>
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        async function sendMessage() {
            const userInput = document.getElementById('userInput');
            const chatContainer = document.getElementById('chatContainer');
            const question = userInput.value.trim();
            
            if (!question) return;
            
            // Add user message
            const userMessage = document.createElement('div');
            userMessage.className = 'message user-message';
            userMessage.innerHTML = `<strong>You:</strong> ${question}`;
            chatContainer.appendChild(userMessage);
            
            // Clear input
            userInput.value = '';
            
            // Show loading
            const loadingMessage = document.createElement('div');
            loadingMessage.className = 'message ai-message';
            loadingMessage.innerHTML = '<strong>AI:</strong> Thinking...';
            chatContainer.appendChild(loadingMessage);
            
            try {
                // Call API
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        question: question
                    })
                });
                
                const data = await response.json();
                
                // Remove loading message
                chatContainer.removeChild(loadingMessage);
                
                // Add AI response
                const aiMessage = document.createElement('div');
                aiMessage.className = 'message ai-message';
                aiMessage.innerHTML = `<strong>AI:</strong> ${data.answer}`;
                chatContainer.appendChild(aiMessage);
                
            } catch (error) {
                // Remove loading message
                chatContainer.removeChild(loadingMessage);
                
                // Error message
                const errorMessage = document.createElement('div');
                errorMessage.className = 'message ai-message';
                errorMessage.innerHTML = '<strong>AI:</strong> Sorry, temporary issue. Please try again.';
                chatContainer.appendChild(errorMessage);
            }
            
            // Scroll to bottom
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.get("/")
async def home():
    return HTMLResponse(HTML_TEMPLATE)

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        answer = await get_ai_response(request.question)
        return AnswerResponse(answer=answer, success=True)
    except Exception as e:
        return AnswerResponse(answer="Service temporarily unavailable. Please try again.", success=False)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "NetPath AI"}

# Render deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
