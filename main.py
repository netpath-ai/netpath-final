import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import httpx
import uvicorn
from typing import Optional

# NetPath Network AI Configuration
COMPANY_NAME = "NetPath Network AI"

app = FastAPI(
    title=COMPANY_NAME,
    description="Advanced Network Engineering AI for Students",
    version="2.0.0"
)

# DeepSeek API Configuration - APNA ACTUAL API KEY
DEEPSEEK_API_KEY = "sk-ebf9122c1e304ff68184d1acab6ae194"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    success: bool

async def get_deepseek_answer(question: str) -> str:
    """DeepSeek API se answer get karein"""
    try:
        print(f"🔧 DEBUG: Calling DeepSeek API...")  # Debug line
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }
        
        # Network Engineering focused prompt
        system_prompt = """You are an expert Network Engineering AI assistant. 
        Provide detailed, technical answers about networking topics.
        Answer in Hindi or English based on the user's language."""
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "max_tokens": 800,
            "temperature": 0.7
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            print(f"🔧 DEBUG: Sending request...")  # Debug
            response = await client.post(DEEPSEEK_API_URL, headers=headers, json=payload)
            print(f"🔧 DEBUG: Response status: {response.status_code}")  # Debug
            
            if response.status_code == 200:
                data = response.json()
                print(f"🔧 DEBUG: Success! Got response")  # Debug
                return data["choices"][0]["message"]["content"]
            else:
                error_msg = f"API Error {response.status_code}"
                print(f"🔧 DEBUG: {error_msg}")  # Debug
                return error_msg
            
    except Exception as e:
        error_msg = f"Exception: {str(e)}"
        print(f"🔧 DEBUG: {error_msg}")  # Debug
        return error_msg    """DeepSeek API se answer get karein"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }
        
        # Network Engineering focused prompt
        system_prompt = """You are an expert Network Engineering AI assistant. 
        Provide detailed, technical answers about networking topics like OSPF, BGP, TCP/IP, 
        subnetting, VLANs, network security, and troubleshooting.
        Answer in Hindi or English based on the user's language.
        Be helpful and educational for students."""
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(DEEPSEEK_API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                return f"API Error {response.status_code}: Please try again later."
            
    except httpx.TimeoutException:
        return "Request timeout. Please try again."
    except Exception as e:
        return f"Technical issue. Please try again."

# Local knowledge base for fallback
NETWORK_KNOWLEDGE = {
    "namaste": "Namaste! Main NetPath Network AI hoon. Aap OSPF, BGP, subnetting, VLANs, network security - koi bhi networking question puchh sakte hain!",
    "hello": "Hello! I'm NetPath Network AI. How can I help you with networking topics today?",
    "help": "Main aapki networking, routing protocols, switching, security, aur troubleshooting mein madad kar sakta hoon!",
    "ospf": "OSPF (Open Shortest Path First) ek link-state routing protocol hai jo areas use karta hai scalability ke liye.",
    "bgp": "BGP (Border Gateway Protocol) internet ka routing protocol hai, path vector use karta hai.",
    "subnetting": "Subnetting large networks ko smaller parts mein divide karta hai. Example: 192.168.1.0/24 = 256 IPs.",
}

def get_local_answer(question: str) -> str:
    """Local knowledge base se answer dein"""
    question_lower = question.lower()
    
    # Direct matches
    if question_lower in NETWORK_KNOWLEDGE:
        return NETWORK_KNOWLEDGE[question_lower]
    
    # Keyword matches
    if "ospf" in question_lower:
        return NETWORK_KNOWLEDGE["ospf"]
    elif "bgp" in question_lower:
        return NETWORK_KNOWLEDGE["bgp"] 
    elif "subnet" in question_lower:
        return NETWORK_KNOWLEDGE["subnetting"]
    elif any(word in question_lower for word in ["hello", "hi", "namaste"]):
        return NETWORK_KNOWLEDGE["namaste"]
    
    return "I'm here to help with networking topics. Please ask about OSPF, BGP, subnetting, VLANs, or network security."

# Simple HTML Interface
HTML_CONTENT = """
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
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        .chat-container {
            padding: 25px;
            height: 500px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        .message {
            margin: 15px 0;
            padding: 18px;
            border-radius: 15px;
            max-width: 80%;
            animation: fadeIn 0.3s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .user-message {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            margin-left: auto;
            text-align: right;
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
        }
        .ai-message {
            background: white;
            border-left: 5px solid #2ecc71;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        .input-container {
            padding: 25px;
            background: white;
            border-top: 1px solid #eee;
            display: flex;
            gap: 15px;
            align-items: center;
        }
        .input-container input {
            flex: 1;
            padding: 18px;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            font-size: 16px;
            outline: none;
        }
        .input-container input:focus {
            border-color: #3498db;
        }
        .input-container button {
            padding: 18px 30px;
            background: linear-gradient(135deg, #2ecc71, #27ae60);
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
        }
        .input-container button:hover {
            background: linear-gradient(135deg, #27ae60, #219653);
        }
        .typing {
            font-style: italic;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌐 NetPath Network AI</h1>
            <p>Your Network Engineering Learning Assistant</p>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message ai-message">
                <strong>AI:</strong> Namaste! Main NetPath Network AI hoon. Aap OSPF, BGP, subnetting, VLANs, network security - koi bhi networking question puchh sakte hain! 🎓
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="userInput" 
                   placeholder="Ask about OSPF, BGP, subnetting, VLANs... (Hindi or English)" 
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
            
            // User message display
            const userMessage = document.createElement('div');
            userMessage.className = 'message user-message';
            userMessage.innerHTML = `<strong>You:</strong> ${question}`;
            chatContainer.appendChild(userMessage);
            
            // Clear input
            userInput.value = '';
            
            // Show typing indicator
            const typingMessage = document.createElement('div');
            typingMessage.className = 'message ai-message';
            typingMessage.innerHTML = '<strong>AI:</strong> <span class="typing">Thinking...</span>';
            chatContainer.appendChild(typingMessage);
            
            try {
                // API call
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
                
                // Remove typing message
                chatContainer.removeChild(typingMessage);
                
                // AI response
                const aiMessage = document.createElement('div');
                aiMessage.className = 'message ai-message';
                aiMessage.innerHTML = `<strong>AI:</strong> ${data.answer}`;
                chatContainer.appendChild(aiMessage);
                
            } catch (error) {
                // Remove typing message
                chatContainer.removeChild(typingMessage);
                
                // Error message
                const errorMessage = document.createElement('div');
                errorMessage.className = 'message ai-message';
                errorMessage.innerHTML = '<strong>AI:</strong> Sorry, technical issue. Please try again.';
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
    return HTMLResponse(HTML_CONTENT)

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """AI questions ka answer dein"""
    try:
        print(f"🔧 DEBUG: User asked: {request.question}")  # Debug
        
        # Pehle DeepSeek API try karein
        deepseek_answer = await get_deepseek_answer(request.question)
        print(f"🔧 DEBUG: DeepSeek response: {deepseek_answer}")  # Debug
        
        # Agar API se accha answer mila, toh woh return karein
        if deepseek_answer and "Error" not in deepseek_answer and "API Error" not in deepseek_answer:
            print(f"🔧 DEBUG: Returning DeepSeek answer")  # Debug
            return AnswerResponse(answer=deepseek_answer, success=True)
        else:
            # Fallback to local knowledge
            print(f"🔧 DEBUG: Using local fallback")  # Debug
            local_answer = get_local_answer(request.question)
            return AnswerResponse(answer=local_answer, success=True)
            
    except Exception as e:
        print(f"🔧 DEBUG: Exception in ask_question: {str(e)}")  # Debug
        local_answer = get_local_answer(request.question)
        return AnswerResponse(answer=local_answer, success=True)
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "NetPath AI",
        "api_configured": True,
        "version": "2.0.0"
    }

# Render deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
