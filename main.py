from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx
import uvicorn
import os
from typing import Optional

# NetPath Network AI Configuration
COMPANY_NAME = "NetPath Network AI"
COMPANY_DOMAIN = "netpath.edu"

app = FastAPI(
    title=f"{COMPANY_NAME}",
    description="Advanced Network Engineering AI for Students",
    version="2.0.0"
)

# Static files serve karein
app.mount("/static", StaticFiles(directory="static"), name="static")

# DeepSeek API Configuration - YOUR API KEY HERE
DEEPSEEK_API_KEY = "sk-2cd9e8b7ecf043ca8cfcdf133aefb5b8"
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
    "company": "NetPath Network AI - Empowering students with advanced networking knowledge.",
}

@app.get("/")
async def serve_student_portal():
    return FileResponse("static/index.html")

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """AI questions ka answer dein"""
    try:
        # Pehle local knowledge check karein
        question_lower = request.question.lower().strip()
        if question_lower in NETWORK_KNOWLEDGE:
            return AnswerResponse(
                answer=NETWORK_KNOWLEDGE[question_lower],
                source="netpath_knowledge",
                success=True
            )
        
        # DeepSeek API call karein
        deepseek_answer = await get_deepseek_answer(request.question)
        
        return AnswerResponse(
            answer=deepseek_answer,
            source="netpath_ai",
            success=True
        )
        
    except Exception as e:
        return AnswerResponse(
            answer="🔧 System temporarily unavailable. Please try again in a moment.",
            source="error",
            success=False
        )

# AI ko naya knowledge add karne ka endpoint
class TeachRequest(BaseModel):
    question: str
    answer: str

@app.post("/teach")
async def teach_ai(request: TeachRequest):
    """Local knowledge base mein naya knowledge add karein"""
    NETWORK_KNOWLEDGE[request.question.lower()] = request.answer
    return {
        "success": True, 
        "message": f"NetPath knowledge updated: '{request.question}'",
        "total_knowledge": len(NETWORK_KNOWLEDGE)
    }

@app.get("/knowledge")
async def get_knowledge():
    """Local knowledge base dekhein"""
    return {
        "company": COMPANY_NAME,
        "total_responses": len(NETWORK_KNOWLEDGE),
        "knowledge_base": NETWORK_KNOWLEDGE
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": COMPANY_NAME,
        "version": "2.0.0",
        "environment": "production",
        "api_configured": True
    }

@app.get("/api/info")
async def api_info():
    return {
        "name": COMPANY_NAME,
        "version": "2.0.0",
        "description": "Network Engineering AI for Students",
        "features": [
            "Networking Q&A",
            "Student Learning", 
            "24/7 Available",
            "Multi-language Support",
            "DeepSeek AI Powered"
        ],
        "supported_topics": [
            "OSPF", "BGP", "TCP/IP", "Subnetting", "VLANs",
            "Network Security", "Routing Protocols", "Switching",
            "Firewall", "VPN", "DNS", "DHCP", "Troubleshooting"
        ]
    }

# Keep-alive endpoint for Render free tier
@app.get("/ping")
async def ping():
    return {"status": "alive", "service": "NetPath AI", "timestamp": "active"}

# Production mein ye use hoga
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 {COMPANY_NAME} Starting...")
    print(f"🔑 API Key: Configured")
    print(f"🌐 Server: http://0.0.0.0:{port}")
    print(f"📚 Student Portal: http://0.0.0.0:{port}")
    print(f"🔧 API Docs: http://0.0.0.0:{port}/docs")
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)
