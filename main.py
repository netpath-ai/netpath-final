import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
from typing import Dict, List
import random

# NetPath Network AI Configuration
COMPANY_NAME = "NetPath Network AI"

app = FastAPI(
    title=COMPANY_NAME,
    description="Advanced Network Engineering AI for Students",
    version="2.0.0"
)

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    success: bool

# COMPREHENSIVE NETWORKING KNOWLEDGE BASE
NETWORK_KNOWLEDGE = {
    # Basic Networking Concepts
    "what is network": "A network is a collection of computers and devices connected together to share resources and communicate. Types include LAN (Local Area Network), WAN (Wide Area Network), MAN (Metropolitan Area Network), and WLAN (Wireless LAN).",
    
    "network": "Computer network devices ko connect karta hai resource sharing ke liye. Main components: Routers, Switches, Firewalls, Cables, Wireless Access Points. Network topology: Star, Bus, Ring, Mesh.",
    
    "types of network": """
🌐 Network Types:
• LAN (Local Area Network) - Small geographical area
• WAN (Wide Area Network) - Large geographical area  
• MAN (Metropolitan Area Network) - City-wide
• WLAN (Wireless LAN) - Wireless connectivity
• PAN (Personal Area Network) - Personal devices
• VPN (Virtual Private Network) - Secure remote access
""",

    # Network Models
    "osi model": """
📚 OSI Model - 7 Layers:
1. Physical - Cables, signals, hardware
2. Data Link - MAC addresses, switches
3. Network - IP addresses, routers
4. Transport - TCP/UDP, reliability
5. Session - Connections, sessions
6. Presentation - Encryption, compression
7. Application - HTTP, FTP, SMTP
""",

    "tcp/ip model": """
📡 TCP/IP Model - 4 Layers:
1. Network Interface - Ethernet, WiFi
2. Internet - IP, ICMP, routing
3. Transport - TCP (reliable), UDP (fast)
4. Application - HTTP, DNS, SSH, FTP
""",

    "difference between osi and tcp/ip": """
🔄 OSI vs TCP/IP:
• OSI - 7 layers, theoretical model
• TCP/IP - 4 layers, practical implementation
• OSI - Session & Presentation layers separate
• TCP/IP - Session & Presentation included in Application layer
""",

    # Network Devices
    "router": "🔄 Router - Layer 3 device, different networks ko connect karta hai. Routing tables use karta hai. Protocols: OSPF, BGP, EIGRP. Functions: Packet forwarding, path selection.",

    "switch": "🔀 Switch - Layer 2 device, same network ke devices ko connect karta hai. MAC address table maintain karta hai. VLANs create kar sakta hai.",

    "firewall": "🛡️ Firewall - Network security device, incoming/outgoing traffic control karta hai. Types: Packet-filtering, Stateful, Next-gen. ACL rules enforce karta hai.",

    # Protocols
    "tcp": "📨 TCP (Transmission Control Protocol) - Connection-oriented, reliable, sequencing, flow control. Used for: HTTP, FTP, SSH. Three-way handshake use karta hai.",

    "udp": "⚡ UDP (User Datagram Protocol) - Connectionless, faster, no guarantees. Used for: DNS, VoIP, streaming. No sequencing or flow control.",

    "tcp vs udp": """
🆚 TCP vs UDP:
TCP:
• Connection-oriented
• Reliable delivery
• Sequencing & flow control
• Slower but secure
• Example: HTTP, FTP

UDP:
• Connectionless  
• Faster but unreliable
• No sequencing
• Lower overhead
• Example: DNS, VoIP
""",

    "http": "🌐 HTTP (Hypertext Transfer Protocol) - Web browsing ke liye, port 80 use karta hai, unencrypted.",

    "https": "🔒 HTTPS (HTTP Secure) - Encrypted version of HTTP, port 443 use karta hai, SSL/TLS encryption.",

    "dns": "📡 DNS (Domain Name System) - Domain names ko IP addresses mein convert karta hai. Hierarchy: Root → TLD → Authoritative servers.",

    "dhcp": "🔌 DHCP (Dynamic Host Configuration Protocol) - Automatic IP address assignment, lease time manage karta hai.",

    # Routing Protocols
    "ospf": """
🔄 OSPF (Open Shortest Path First):
• Link-state routing protocol
• Areas use karta hai scalability ke liye
• Fast convergence
• Dijkstra algorithm use karta hai
• Metric: Cost (bandwidth based)
""",

    "bgp": """
🌍 BGP (Border Gateway Protocol):
• Internet routing protocol
• Path vector protocol
• AS (Autonomous System) numbers use karta hai
• Policies based routing
• TCP port 179 use karta hai
""",

    "eigrp": "🔷 EIGRP (Enhanced Interior Gateway Routing Protocol) - Cisco proprietary, hybrid protocol, DUAL algorithm use karta hai.",

    "rip": "🔄 RIP (Routing Information Protocol) - Distance vector, hop count metric, maximum 15 hops.",

    # IP Addressing & Subnetting
    "ip address": "📍 IP Address - Device ka network identity. IPv4: 32-bit (192.168.1.1), IPv6: 128-bit. Public aur Private IP addresses.",

    "subnetting": """
🧮 Subnetting - Large network ko smaller parts mein divide karna:
• 192.168.1.0/24 = 256 total, 254 usable
• 192.168.1.0/25 = 128 total, 126 usable
• 192.168.1.0/26 = 64 total, 62 usable
• Subnet mask: 255.255.255.0 = /24
""",

    "ipv4 vs ipv6": """
🆚 IPv4 vs IPv6:
IPv4:
• 32-bit address
• 4.3 billion addresses
• Dotted decimal notation
• NAT required

IPv6:
• 128-bit address
• 340 undecillion addresses  
• Hexadecimal notation
• Built-in security
""",

    # VLAN & Switching
    "vlan": """
🔷 VLAN (Virtual LAN):
• Logical network segmentation
• Broadcast domains control karta hai
• Security improve karta hai
• Trunk ports required between switches
• Types: Data VLAN, Voice VLAN, Native VLAN
""",

    "stp": "🔄 STP (Spanning Tree Protocol) - Switching loops prevent karta hai. Root bridge election. Port states: Blocking, Listening, Learning, Forwarding.",

    # Network Security
    "vpn": "🔐 VPN (Virtual Private Network) - Secure encrypted connection public internet par. Types: Site-to-Site, Remote Access. Protocols: IPsec, SSL VPN.",

    "acl": "📋 ACL (Access Control List) - Traffic ko allow/deny karne ke rules. Types: Standard ACL (source based), Extended ACL (source/destination both).",

    "network security": """
🛡️ Network Security Best Practices:
• Strong passwords use karein
• Regular updates karein
• Firewall configure karein
• VPN use karein remote access ke liye
• Network monitoring karein
• Access controls implement karein
""",

    # Troubleshooting
    "ping": "🔄 Ping - Network connectivity check karne ke liye. ICMP protocol use karta hai. Command: ping google.com",

    "tracert": "🛣️ Tracert - Packet ka path trace karta hai source se destination tak. Command: tracert 8.8.8.8",

    "ipconfig": "💻 IPConfig - Network configuration dikhata hai. Command: ipconfig /all (Windows), ifconfig (Linux)",

    "network troubleshooting": """
🔧 Network Troubleshooting Steps:
1. Physical connections check karein
2. IP configuration verify karein
3. Ping se connectivity test karein
4. DNS resolution check karein
5. Router/switch configuration verify karein
6. Firewall rules check karein
""",

    # Basic Greetings
    "namaste": "Namaste! 🙏 Main NetPath Network AI hoon. Aap OSPF, BGP, subnetting, VLANs, network security - koi bhi networking question puchh sakte hain!",
    
    "hello": "Hello! 👋 I'm NetPath Network AI. How can I help you with networking topics today?",
    
    "hi": "Hi there! 😊 I'm your Network Engineering assistant. Ask me anything about networking!",
    
    "help": """
🆘 How I can help you:

📚 Networking Concepts:
• OSI Model, TCP/IP Model
• Network devices, protocols
• IP addressing, subnetting

🔄 Routing & Switching:
• OSPF, BGP, EIGRP protocols
• VLANs, STP, switching concepts

🛡️ Security:
• Firewalls, VPNs, ACLs
• Network security best practices

🔧 Troubleshooting:
• Ping, tracert, ipconfig
• Network issue resolution

Koi bhi topic puchiye! 🎓
""",

    "thank you": "You're welcome! 😊 Agar koi aur sawal ho toh zaroor puchiye!",
    
    "bye": "Alvida! 👋 Aapse baat karke accha laga. Phir milenge!",
}

def find_best_answer(question: str) -> str:
    """Question ka best answer dhoondhta hai"""
    question_lower = question.lower().strip()
    
    # Direct match
    if question_lower in NETWORK_KNOWLEDGE:
        return NETWORK_KNOWLEDGE[question_lower]
    
    # Smart keyword matching
    keyword_mapping = {
        "network": "what is network",
        "types of network": "types of network",
        "osi": "osi model",
        "tcp": "tcp/ip model", 
        "ip model": "tcp/ip model",
        "router": "router",
        "switch": "switch",
        "firewall": "firewall",
        "tcp vs udp": "tcp vs udp",
        "udp": "tcp vs udp",
        "http": "http",
        "https": "https",
        "dns": "dns",
        "dhcp": "dhcp",
        "ospf": "ospf",
        "bgp": "bgp",
        "eigrp": "eigrp",
        "rip": "rip",
        "ip address": "ip address",
        "subnet": "subnetting",
        "ipv4": "ipv4 vs ipv6",
        "ipv6": "ipv4 vs ipv6",
        "vlan": "vlan",
        "stp": "stp",
        "vpn": "vpn",
        "acl": "acl",
        "security": "network security",
        "ping": "ping",
        "tracert": "tracert",
        "ipconfig": "ipconfig",
        "troubleshoot": "network troubleshooting",
        "problem": "network troubleshooting",
        "issue": "network troubleshooting",
        "thanks": "thank you",
        "thank": "thank you",
        "bye": "bye",
        "goodbye": "bye",
    }
    
    for keyword, answer_key in keyword_mapping.items():
        if keyword in question_lower:
            return NETWORK_KNOWLEDGE[answer_key]
    
    # If no match found
    suggestions = [
        "I can help you with networking topics! Try asking about:",
        "OSI Model, TCP/IP protocols, routers, switches",
        "Subnetting, VLANs, network security, troubleshooting",
        "Routing protocols like OSPF, BGP, EIGRP"
    ]
    return f"{NETWORK_KNOWLEDGE['help']}"

# HTML Interface (same as before)
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
    answer = find_best_answer(request.question)
    return AnswerResponse(answer=answer, success=True)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "NetPath AI",
        "version": "2.0.0",
        "knowledge_topics": len(NETWORK_KNOWLEDGE)
    }

# Render deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
