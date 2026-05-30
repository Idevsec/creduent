import os
import sys
import time
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Request, APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Add parent directory to path to allow importing from registry and creduent packages
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

from registry.store import save_attestation, get_attestation, revoke_agent, list_agents, is_redis_configured, get_redis_client
from registry.signer import sign_attestation
from registry.verifier import verify_agent_registration
from creduent.utils import load_dotenv

# Load local environment variables if present
load_dotenv()

app = FastAPI(title="Creduent Attestation Registry", version="1.0")
router = APIRouter()

class RegisterRequest(BaseModel):
    agent_id: str
    domain: str
    agent_json_url: str

def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # X-Forwarded-For can contain multiple IPs separated by comma. The first is the client.
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

RATE_LIMIT_WINDOW = 60 # seconds
RATE_LIMIT_MAX_REQUESTS = 5 # requests per IP per window

def check_rate_limit(request: Request):
    client_ip = get_client_ip(request)
    if client_ip == "unknown":
        return
        
    now = int(time.time())
    key = f"rate_limit:{client_ip}"
    
    if is_redis_configured():
        try:
            client = get_redis_client()
            current = client.get(key)
            if current is not None:
                count = int(current)
                if count >= RATE_LIMIT_MAX_REQUESTS:
                    raise HTTPException(status_code=429, detail="Too many registration requests. Please try again later.")
                client.incr(key)
            else:
                client.set(key, "1", ex=RATE_LIMIT_WINDOW)
        except HTTPException:
            raise
        except Exception as e:
            # Fallback if Redis fails
            print(f"[-] Rate limit Redis error: {e}", file=sys.stderr)
            pass
    else:
        # In-memory fallback (best effort for local server)
        if not hasattr(app, "rate_limit_db"):
            app.rate_limit_db = {}
        
        # Clean up old entries
        app.rate_limit_db = {k: v for k, v in app.rate_limit_db.items() if v["expiry"] > now}
        
        if key in app.rate_limit_db:
            entry = app.rate_limit_db[key]
            if entry["count"] >= RATE_LIMIT_MAX_REQUESTS:
                raise HTTPException(status_code=429, detail="Too many registration requests. Please try again later.")
            entry["count"] += 1
        else:
            app.rate_limit_db[key] = {
                "count": 1,
                "expiry": now + RATE_LIMIT_WINDOW
            }

@router.post("/register")
def register(req: RegisterRequest, request: Request):
    # Check rate limit
    check_rate_limit(request)

    # Run the verification pipeline
    success, reason, doc = verify_agent_registration(
        agent_id=req.agent_id,
        domain=req.domain,
        agent_json_url=req.agent_json_url
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=f"Verification failed: {reason}")
        
    # Sign the attestation
    agent_data = {
        "agent_id": doc["agent_id"],
        "public_key": doc["public_key"],
        "domain": req.domain
    }
    
    try:
        attestation = sign_attestation(agent_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signing failed: {str(e)}")
        
    # Save the attestation
    try:
        save_attestation(doc["agent_id"], attestation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database write failed: {str(e)}")
        
    return attestation

@router.get("/attest/{agent_id:path}")
def get_attest(agent_id: str):
    # Normalize paths where double slashes were merged by the router
    if agent_id.startswith("agent:/") and not agent_id.startswith("agent://"):
        agent_id = "agent://" + agent_id[7:]
    attestation = get_attestation(agent_id)
    if not attestation:
        raise HTTPException(status_code=404, detail="Attestation not found for agent.")
        
    # Check expiry
    expires_at_str = attestation.get("expires_at")
    if expires_at_str:
        try:
            expires_at = datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))
            if datetime.now(timezone.utc) > expires_at:
                raise HTTPException(status_code=404, detail="Attestation expired.")
        except HTTPException:
            raise
        except Exception as e:
            print(f"[-] Error parsing expires_at: {e}", file=sys.stderr)
            
    return attestation

@router.get("/agents")
def get_agents():
    return list_agents()

@router.delete("/revoke/{agent_id:path}")
def revoke(agent_id: str, request: Request):
    # Normalize paths where double slashes were merged by the router
    if agent_id.startswith("agent:/") and not agent_id.startswith("agent://"):
        agent_id = "agent://" + agent_id[7:]
    admin_key_env = os.environ.get("CREDUENT_ADMIN_KEY")
    if not admin_key_env:
        raise HTTPException(status_code=500, detail="Admin revocation is not configured on server (CREDUENT_ADMIN_KEY env var missing).")
        
    creduent_admin_key = request.headers.get("CREDUENT_ADMIN_KEY") or request.headers.get("CREDUENT-ADMIN-KEY")
    if not creduent_admin_key or creduent_admin_key != admin_key_env:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid or missing CREDUENT_ADMIN_KEY header.")
        
    revoke_agent(agent_id)
    return {"status": "revoked", "agent_id": agent_id}

@router.get("/health")
def health():
    return {"status": "healthy"}

app.include_router(router)
app.include_router(router, prefix="/registry")

LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Creduent Registry - The Trust Layer for the Agentic Web</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0b0d10;
            --card-bg: rgba(20, 24, 33, 0.65);
            --primary: #4f46e5;
            --primary-glow: rgba(79, 70, 229, 0.35);
            --success: #10b981;
            --success-glow: rgba(16, 185, 129, 0.2);
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --border-color: rgba(255, 255, 255, 0.08);
            --accent: #06b6d4;
            --accent-glow: rgba(6, 182, 212, 0.2);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            line-height: 1.6;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(79, 70, 229, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(6, 182, 212, 0.1) 0%, transparent 40%);
        }

        .container {
            max-width: 1000px;
            width: 90%;
            margin: 0 auto;
            padding: 40px 20px;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 60px;
        }

        .logo {
            font-size: 1.8rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(90deg, #ffffff, var(--text-muted));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-decoration: none;
        }

        /* Hero */
        .hero {
            text-align: center;
            padding: 60px 0 80px 0;
            position: relative;
        }

        .hero h1 {
            font-size: 4rem;
            font-weight: 800;
            letter-spacing: -1.5px;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #ffffff 30%, var(--text-muted) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero p {
            font-size: 1.4rem;
            color: var(--text-muted);
            max-width: 600px;
            margin: 0 auto 40px auto;
            font-weight: 300;
        }

        .btn-group {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }

        .btn {
            padding: 14px 28px;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
        }

        .btn-primary {
            background: var(--primary);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 20px var(--primary-glow);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 24px rgba(79, 70, 229, 0.5);
            background: #5a52ff;
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.03);
            color: var(--text-main);
            border: 1px solid var(--border-color);
        }

        .btn-secondary:hover {
            transform: translateY(-2px);
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
        }

        /* Philosophy */
        .section-title {
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 24px;
            text-align: center;
        }

        .philosophy-card {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            padding: 40px;
            margin-bottom: 60px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            position: relative;
        }

        .philosophy-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
        }

        .philosophy-text {
            font-size: 1.1rem;
            color: var(--text-main);
            margin-bottom: 20px;
            font-weight: 400;
        }

        .philosophy-text p {
            margin-bottom: 20px;
        }

        /* Cards Grid */
        .grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 25px;
            margin-bottom: 60px;
        }

        .info-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 30px;
            transition: all 0.3s ease;
        }

        .info-card:hover {
            transform: translateY(-4px);
            border-color: rgba(255, 255, 255, 0.15);
            background: rgba(255, 255, 255, 0.04);
        }

        .info-card h3 {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 12px;
            color: #ffffff;
        }

        .info-card p {
            color: var(--text-muted);
            font-size: 0.95rem;
        }

        /* Use Cases */
        .use-cases-section {
            margin-bottom: 80px;
        }

        .grid-4 {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
        }

        .use-case-card {
            background: rgba(255, 255, 255, 0.01);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            transition: all 0.3s ease;
        }

        .use-case-card:hover {
            border-color: var(--accent);
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.1);
        }

        .use-case-card h4 {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 10px;
            color: #ffffff;
        }

        .use-case-card p {
            color: var(--text-muted);
            font-size: 0.9rem;
        }

        /* Flow / Code blocks */
        .flow-section {
            margin-bottom: 80px;
        }

        pre {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid var(--border-color);
            padding: 25px;
            border-radius: 16px;
            overflow-x: auto;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: #e5e7eb;
            margin-bottom: 30px;
        }

        /* Stats Banner */
        .stats-banner {
            background: linear-gradient(90deg, rgba(79, 70, 229, 0.1), rgba(6, 182, 212, 0.1));
            border: 1px solid var(--border-color);
            padding: 25px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 80px;
            box-shadow: 0 0 30px rgba(79, 70, 229, 0.05);
        }

        .stats-banner .count {
            font-size: 2rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 6px;
            font-family: 'Outfit', sans-serif;
        }

        .stats-banner .count span {
            background: linear-gradient(90deg, var(--accent), var(--success));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .stats-banner p {
            color: var(--text-muted);
            font-size: 1rem;
        }

        /* Roadmap */
        .roadmap-section {
            margin-bottom: 80px;
        }

        .timeline {
            display: flex;
            flex-direction: column;
            gap: 30px;
            position: relative;
            padding-left: 20px;
        }

        .timeline::before {
            content: '';
            position: absolute;
            left: 5px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: var(--border-color);
        }

        .timeline-item {
            position: relative;
            padding-left: 20px;
        }

        .timeline-item::before {
            content: '';
            position: absolute;
            left: -20px;
            top: 6px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--bg-color);
            border: 2px solid var(--border-color);
        }

        .timeline-item.complete::before {
            background: var(--success);
            border-color: var(--success);
            box-shadow: 0 0 10px var(--success-glow);
        }

        .timeline-item.in-progress::before {
            background: var(--accent);
            border-color: var(--accent);
            box-shadow: 0 0 10px var(--accent-glow);
        }

        .timeline-content h4 {
            font-size: 1.15rem;
            font-weight: 600;
            margin-bottom: 8px;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .status-badge {
            font-size: 0.75rem;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 500;
        }

        .status-complete {
            background: rgba(16, 185, 129, 0.1);
            color: var(--success);
            border: 1px solid rgba(16, 185, 129, 0.2);
        }

        .status-progress {
            background: rgba(6, 182, 212, 0.1);
            color: var(--accent);
            border: 1px solid rgba(6, 182, 212, 0.2);
        }

        .status-future {
            background: rgba(255, 255, 255, 0.03);
            color: var(--text-muted);
            border: 1px solid var(--border-color);
        }

        .timeline-content ul {
            list-style: none;
            padding-left: 0;
            color: var(--text-muted);
            font-size: 0.95rem;
        }

        .timeline-content ul li {
            position: relative;
            padding-left: 15px;
            margin-bottom: 4px;
        }

        .timeline-content ul li::before {
            content: '–';
            position: absolute;
            left: 0;
        }

        /* Register Steps */
        .register-section {
            margin-bottom: 80px;
            scroll-margin-top: 40px;
        }

        .register-step {
            margin-bottom: 30px;
        }

        .register-step h4 {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 12px;
            color: #ffffff;
        }

        .register-step p {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-bottom: 12px;
        }

        /* Footer */
        footer {
            border-top: 1px solid var(--border-color);
            padding: 40px 0;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.9rem;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        footer a {
            color: var(--accent);
            text-decoration: none;
        }

        footer a:hover {
            text-decoration: underline;
        }

        /* Responsive */
        @media (max-width: 850px) {
            .grid-3 {
                grid-template-columns: 1fr;
            }
            .grid-4 {
                grid-template-columns: repeat(2, 1fr);
            }
            .hero h1 {
                font-size: 2.8rem;
            }
        }

        @media (max-width: 550px) {
            .grid-4 {
                grid-template-columns: 1fr;
            }
            .hero h1 {
                font-size: 2.2rem;
            }
            header {
                flex-direction: column;
                gap: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <a href="#" class="logo">Creduent Registry</a>
            <a href="https://github.com/cyberfascinate/creduent" class="btn btn-secondary" target="_blank">View GitHub</a>
        </header>

        <section class="hero">
            <h1>Creduent Registry</h1>
            <p>The trust layer for the agentic web.</p>
            <div class="btn-group">
                <a href="#register" class="btn btn-primary">Register Your Agent</a>
                <a href="https://github.com/cyberfascinate/creduent" class="btn btn-secondary" target="_blank">Read the Spec</a>
            </div>
        </section>

        <section class="philosophy-card">
            <h2 class="section-title" style="text-align: left; margin-bottom: 20px;">Why Creduent exists</h2>
            <div class="philosophy-text">
                <p>The internet was built for humans. Every website has a domain. Every connection has TLS. Every email has DKIM. Identity infrastructure exists everywhere, except for AI agents.</p>
                <p>As agents begin to talk to each other, call APIs, make decisions, and act autonomously, the question becomes unavoidable: how do you know the agent on the other end is who it claims to be?</p>
                <p>Creduent is our answer. Not a platform. Not a product. A protocol: open, minimal, and built to last. Modeled after the boring infrastructure that actually works: OAuth, robots.txt, DNS TXT records, JWT. Eight fields. One signature. Anyone can verify.</p>
            </div>
        </section>

        <section class="grid-3">
            <div class="info-card">
                <h3>Agents have no identity</h3>
                <p>Any agent can claim any name. There is no standard way to verify who is calling or acting.</p>
            </div>
            <div class="info-card">
                <h3>Self-signed is not enough</h3>
                <p>Cryptographic signatures prove integrity, not legitimacy. Anyone can generate a key and sign anything.</p>
            </div>
            <div class="info-card">
                <h3>Trust needs a foundation</h3>
                <p>Creduent provides DNS-verified, Ed25519-signed attestations. One API call confirms any agent is who they claim to be.</p>
            </div>
        </section>

        <section class="use-cases-section">
            <h2 class="section-title">Who needs this</h2>
            <div class="grid-4">
                <div class="use-case-card">
                    <h4>MCP Servers</h4>
                    <p>Verify calling agents before allowing tool execution.</p>
                </div>
                <div class="use-case-card">
                    <h4>AI Pipelines</h4>
                    <p>Confirm downstream agents are trusted before passing sensitive context.</p>
                </div>
                <div class="use-case-card">
                    <h4>Enterprise</h4>
                    <p>Maintain a verified registry of internal agents.</p>
                </div>
                <div class="use-case-card">
                    <h4>Open Ecosystems</h4>
                    <p>Let any agent prove its identity without a central gatekeeper.</p>
                </div>
            </div>
        </section>

        <section class="flow-section">
            <h2 class="section-title">How It Works</h2>
            <pre><code>[Agent Owner]
  → publishes agent.json at /.well-known/agent.json
  → adds DNS TXT record: _creduent.{domain} = agent_id
  → calls POST /registry/register

[Creduent Registry]
  → fetches + validates agent.json schema
  → verifies Ed25519 self-signature
  → confirms DNS TXT ownership
  → issues signed attestation (1 year validity)

[Any Client / MCP Server]
  → calls GET /registry/attest/{agent_id}
  → verifies Creduent signature on attestation
  → trusted or not: one call, cryptographic proof</code></pre>
        </section>

        <div class="stats-banner">
            <div class="count"><span id="agentsCount">0</span></div>
            <p id="agentsCountText">agents verified in the Creduent Registry</p>
        </div>

        <section class="roadmap-section">
            <h2 class="section-title">Where we are going</h2>
            <div class="timeline">
                <div class="timeline-item complete">
                    <div class="timeline-content">
                        <h4>Phase 1 - Foundation <span class="status-badge status-complete">Complete</span></h4>
                        <ul>
                            <li>agent.json schema + Ed25519 + JCS standard</li>
                            <li>DNS TXT domain ownership verification</li>
                            <li>Attestation registry with signed attestations</li>
                            <li>MCP server integration (verify_agent tool)</li>
                            <li>Vercel + Upstash Redis production deployment</li>
                            <li>v1.0 security hardening + full regression tests</li>
                        </ul>
                    </div>
                </div>
                <div class="timeline-item in-progress">
                    <div class="timeline-content">
                        <h4>Phase 2 - Ecosystem <span class="status-badge status-progress">In Progress</span></h4>
                        <ul>
                            <li>Python SDK: pip install creduent</li>
                            <li>agent:// URI public resolver</li>
                            <li>JavaScript/TypeScript SDK: npm install creduent-protocol</li>
                            <li>Auto-renewal daemon + Webhook notifications</li>
                            <li>Developer dashboard (key rotation, attestation status)</li>
                            <li>GitHub Action (creduent-attest action)</li>
                        </ul>
                    </div>
                </div>
                <div class="timeline-item">
                    <div class="timeline-content">
                        <h4>Phase 3 - Scale <span class="status-badge status-future">Future</span></h4>
                        <ul>
                            <li>CrewAI, LangGraph, AutoGen integrations</li>
                            <li>Multi-key support & Capability-level attestations</li>
                            <li>Agent discovery API (GET /agents?capability=osint)</li>
                            <li>Organization namespaces (agent://org/*)</li>
                            <li>Creduent CLI v2 packaged native tool</li>
                        </ul>
                    </div>
                </div>
                <div class="timeline-item">
                    <div class="timeline-content">
                        <h4>Phase 4 - Standard <span class="status-badge status-future">Future</span></h4>
                        <ul>
                            <li>Federated attestation & Cross-registry trust</li>
                            <li>Submit CREDUENT-001 as open RFC to standard body</li>
                            <li>Creduent Verification Badges for dashboards</li>
                            <li>Enterprise registry (SOC2 compliant hosted fleets)</li>
                            <li>agent:// IANA URI scheme registration</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <section class="register-section" id="register">
            <h2 class="section-title">Register your agent</h2>
            <p style="text-align: center; color: var(--text-muted); margin-bottom: 40px;">Three steps: Five minutes.</p>

            <div class="register-step">
                <h4>Step 1: Create and sign your agent.json</h4>
                <p>Generate keys and sign your metadata document using the CLI tools.</p>
                <pre><code>git clone https://github.com/cyberfascinate/creduent
python cli/creduent-sign.py generate-keys
python cli/creduent-sign.py sign --key private_key.pem --input examples/draft_agent.json --output .well-known/agent.json</code></pre>
            </div>

            <div class="register-step">
                <h4>Step 2: Add DNS TXT record</h4>
                <p>Create a DNS TXT record under the _creduent subdomain of your domain to bind it to the agent ID.</p>
                <pre><code>_creduent.yourdomain.com  TXT  "agent://yournamespace/agentname"</code></pre>
            </div>

            <div class="register-step">
                <h4>Step 3: Register</h4>
                <p>Send a POST request to register your agent on the Creduent registry.</p>
                <pre><code>curl -X POST https://api.idevsec.com/registry/register \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent://&lt;namespace&gt;/&lt;name&gt;",
    "domain": "&lt;your-domain&gt;",
    "agent_json_url": "https://&lt;your-domain&gt;/.well-known/agent.json"
  }'</code></pre>
            </div>
        </section>

        <footer>
            <p>Creduent Protocol v1.0 - MIT License - <a href="https://github.com/cyberfascinate/creduent" target="_blank">github.com/cyberfascinate/creduent</a></p>
            <p style="font-size: 0.8rem; margin-top: 5px;">Built by IDevSec</p>
        </footer>
    </div>

    <script>
        async function fetchStats() {
            let count = 0;
            try {
                const response = await fetch('/registry/agents');
                if (response.ok) {
                    const data = await response.json();
                    count = data.length || 0;
                }
            } catch (e) {
                console.error("Error fetching stats:", e);
                try {
                    const response = await fetch('/agents');
                    if (response.ok) {
                        const data = await response.json();
                        count = data.length || 0;
                    }
                } catch (err) {}
            }
            document.getElementById('agentsCount').textContent = count;
            document.getElementById('agentsCountText').textContent = count === 1 ? 'agent verified in the Creduent Registry' : 'agents verified in the Creduent Registry';
        }
        window.addEventListener('DOMContentLoaded', fetchStats);
    </script>
</body>
</html>"""

@app.get("/registry", response_class=HTMLResponse)
@app.get("/registry/", response_class=HTMLResponse)
def serve_registry_landing():
    return HTMLResponse(content=LANDING_HTML, status_code=200)
