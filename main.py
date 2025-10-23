import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import httpx
import uvicorn
from typing import Optional

# NetPath Network AI Configuration
COMPANY_NAME = "NetPath Network AI"
COMPANY_DOMAIN = "netpath.edu"

app = FastAPI(
    title=f"{COMPANY_NAME}",
    description="Advanced Network Engineering AI for Students",
    version="2.0.0"
)

# Safe API Key Configuration - Environment variable se lega
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-2cd9e8b7ecf043ca8cfcdf133aefb5b8")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

class QuestionRequest(BaseModel):
    question: str
    user_id: Optional[str] = None

class AnswerResponse(BaseModel):
    answer: str
    source: str
    success: bool

async def get_deepseek_answer(question: str) -> str:
    """DeepSeek API se answer get karein"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }
        
        system_prompt = f"""You are {COMPANY_NAME}'s expert Network Engineer AI Assistant for students. 
        Provide detailed, educational answers about networking concepts.
        Explain like a teacher to students.
        Use examples and practical scenarios.
        Answer in Hindi or English based on the user's language.
        Topics: OSPF, BGP, TCP/IP, subnetting, VLANs, network security, routing protocols, switching, firewall, VPN, DNS, DHCP, HTTP/HTTPS, network troubleshooting."""

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "max_tokens": 1500,
            "temperature": 0.3
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(DEEPSEEK_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
            
    except httpx.TimeoutException:
        return "⏰ Request timeout. Please try again."
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return "🔐 API Authentication Error. Please check API configuration."
        elif e.response.status_code == 429:
            return "📊 API Rate Limit Exceeded. Please try again after some time."
        else:
            return f"🔧 API Error: {e.response.status_code}"
    except Exception as e:
        return f"⚠️ Temporary technical issue. Please try again in a moment."

# Local knowledge for fallback
NETWORK_KNOWLEDGE = {
    "namaste": "Namaste! Main NetPath Network AI hoon. Aap koi bhi networking question puchh sakte hain - OSPF, BGP, subnetting, VLANs, network security, etc.!",
    "hello": "Hello! I'm NetPath Network AI. How can I help you with networking topics today?",
    "help": "Main aapki networking, routing protocols, switching, security, aur troubleshooting mein madad kar sakta hoon!",
    "netpath": "NetPath Network AI - Advanced Network Engineering Education Platform for Students.",
}

# Simple HTML Frontend
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NetPath Network AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif; }
        body { background: linear-gradient(135deg, #667eea, #764ba2); min-height: 100vh; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 15px; overflow: hidden; }
        .header { background: #2c3e50; color: white; padding: 30px; text-align: center; }
        .chat-container { padding: 20px; height: 400px; overflow-y: auto; background: #f8f9fa; }
        .message { margin: 10px 0; padding: 15px; border-radius: 10px; max-width: 80%; }
        .user-message { background: #3498db; color: white; margin-left: auto; text-align: right; }
        .ai-message { background: white; border-left: 4px solid #2ecc71; }
        .input-container { padding: 20px; background: white; display: flex; gap: 10px; }
        .input-container input { flex: 1; padding: 15px; border: 1px solid #ddd; border-radius: 8px; }
        .input-container button { padding: 15px 25px; background: #2ecc71; color: white; border: none; border-radius: 8px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌐 NetPath Network AI</h1>
            <p>Network Engineering Learning Platform</p>
        </div>
        <div class="chat-container" id="chatContainer">
            <div class="message ai-message">
                <strong>AI:</strong> Namaste! Ask me about networking topics.
            </div>
        </div>
        <div class="input-container">
            <input type="text" id="userInput" placeholder="Ask about OSPF, BGP, subnetting..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const container = document.getElementById('chatContainer');
            const question = input.value.trim();
            if (!question) return;
            
            // User message
            const userMsg = document.createElement('div');
            userMsg.className = 'message user-message';
            userMsg.innerHTML = '<strong>You:</strong> ' + question;
            container.appendChild(userMsg);
            
            input.value = '';
            
            // AI response
            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: question })
                });
                const data = await response.json();
                
                const aiMsg = document.createElement('div');
                aiMsg.className = 'message ai-message';
                aiMsg.innerHTML = '<strong>AI:</strong> ' + data.answer;
                container.appendChild(aiMsg);
            } catch (error) {
                const errorMsg = document.createElement('div');
                errorMsg.className = 'message ai-message';
                errorMsg.innerHTML = '<strong>AI:</strong> Sorry, error occurred.';
                container.appendChild(errorMsg);
            }
            
            container.scrollTop = container.scrollHeight;
        }
        function handleKeyPress(e) { if (e.key === 'Enter') sendMessage(); }
    </script>
</body>
</html>
"""

@app.get("/")
async def serve_frontend():
    return HTMLResponse(HTML_CONTENT)

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """AI questions ka answer dein"""
    try:
        # Local knowledge check
        question_lower = request.question.lower().strip()
        if question_lower in NETWORK_KNOWLEDGE:
            return AnswerResponse(
                answer=NETWORK_KNOWLEDGE[question_lower],
                source="netpath_knowledge",
                success=True
            )
        
        # DeepSeek API call
        deepseek_answer = await get_deepseek_answer(request.question)
        return AnswerResponse(
            answer=deepseek_answer,
            source="netpath_ai",
            success=True
        )
    except Exception as e:
        return AnswerResponse(
            answer="System temporarily unavailable. Please try again.",
            source="error",
            success=False
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "NetPath AI"}

if __name__ == "__main__":
    print("🚀 NetPath AI Server Starting...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
