import os
import sys
import json
import base64
import socket
import ssl
import urllib3
import requests
from datetime import datetime, timezone
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from urllib.parse import urlparse, urljoin

# Add parent directory to path to allow importing from creduent package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from creduent.crypto import canonicalize
from creduent.utils import is_private_ip, safe_requests_get, load_dotenv

# Load local environment variables if present
load_dotenv()


app = FastAPI(title="Creduent Agent Service", version="1.0")

# Enable CORS for all domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core agent metadata fallback (corresponds to our signed agent.json)
# NOTE: Keep this in sync with .well-known/agent.json whenever keys are rotated.
AGENT_METADATA_FALLBACK = {
  "version": "1.0",
  "agent_id": "agent://creduent/reconbot",
  "owner": "Creduent",
  "public_key": "ed25519:uMMQ6RfZB5RJuYcZPwzLoiv8b6EQfU7CUJ2oLragCHg=",
  "endpoint": "https://axi-beta.vercel.app",
  "capabilities": [
    "osint",
    "dns_lookup",
    "vulnerability_scan"
  ],
  "issued_at": "2026-05-28T22:29:03Z",
  "signature": "pWxvJRnW9bhtqSsehW7I//8/kBgV/GZsnZo7IccxUDv5ethFZJWZZdDv5qxuIZ3sI4iaw49bxHtDy6b3BrSRAA=="
}

AGENT_METADATA = AGENT_METADATA_FALLBACK

# Resolve path relative to this file to be robust on Vercel
AGENT_JSON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".well-known", "agent.json"))

try:
    if os.path.exists(AGENT_JSON_PATH):
        with open(AGENT_JSON_PATH, "r", encoding="utf-8") as f:
            AGENT_METADATA = json.load(f)
            print(f"[+] Successfully loaded AGENT_METADATA dynamically from {AGENT_JSON_PATH}")
    else:
        print(f"[!] Warning: agent.json not found at {AGENT_JSON_PATH}. Serving hardcoded fallback metadata.")
except Exception as e:
    print(f"[!] Warning: Failed to load agent.json from {AGENT_JSON_PATH} ({e}). Serving hardcoded fallback metadata.")


# is_private_ip and safe_requests_get imported from creduent.utils


def get_private_key():
    """
    Loads Ed25519 private key from environment variable or local file.
    """
    pkey_env = os.environ.get("CREDUENT_PRIVATE_KEY")
    if pkey_env:
        try:
            # Handle possible single-line base64 encoding or raw PEM format
            if "-----BEGIN PRIVATE KEY-----" not in pkey_env:
                # Decoded if it's base64 encoded
                pkey_bytes = base64.b64decode(pkey_env)
            else:
                pkey_bytes = pkey_env.encode('utf-8')
            return serialization.load_pem_private_key(pkey_bytes, password=None)
        except Exception as e:
            print(f"[-] Error loading private key from env: {e}")
            
    # Fallback to local file
    key_file = "private_key.pem"
    if os.path.exists(key_file):
        try:
            with open(key_file, "rb") as f:
                return serialization.load_pem_private_key(f.read(), password=None)
        except Exception as e:
            print(f"[-] Error loading private key from file: {e}")
            
    return None

@app.get("/.well-known/agent.json")
def serve_agent_json():
    """
    Serve the verified agent.json profile.
    """
    return JSONResponse(content=AGENT_METADATA)

@app.get("/api/scan")
@app.post("/api/scan")
def run_agent_scan(
    domain: str = Query(..., description="Target domain to scan"),
    capability: str = Query("dns_lookup", description="Capability to run: dns_lookup, osint, vulnerability_scan")
):
    """
    Executes a real agent task based on capability, canonicalizes results, signs
    the payload using the agent's private key, and returns the authenticated response.
    """
    # Clean domain input
    domain = domain.strip().lower()
    if domain.startswith("http://"):
        domain = domain[7:]
    if domain.startswith("https://"):
        domain = domain[8:]
    domain = domain.split("/")[0]

    if capability not in ["dns_lookup", "osint", "vulnerability_scan"]:
        raise HTTPException(status_code=400, detail=f"Unsupported capability: {capability}")

    results = {
        "domain": domain,
        "capability": capability,
        "scanned_at": datetime.now(timezone.utc).isoformat(timespec='seconds').replace("+00:00", "Z"),
        "status": "pending"
    }

    # 1. Execute capability logic
    if capability == "dns_lookup":
        try:
            ip_address = socket.gethostbyname(domain)
            results.update({
                "status": "success",
                "ip": ip_address
            })
        except Exception as e:
            results.update({
                "status": "failed",
                "ip": None,
                "error": str(e)
            })

    elif capability == "osint":
        # Get IP first
        try:
            ip_address = socket.gethostbyname(domain)
        except Exception:
            ip_address = None

        # Fetch HTTP details
        try:
            url = f"https://{domain}"
            response = safe_requests_get(url, timeout=5)
            headers = response.headers
            server = headers.get("Server", "Unknown")
            powered_by = headers.get("X-Powered-By", "None")
            redirects_count = len(response.history)
            final_url = response.url

            results.update({
                "status": "success",
                "ip": ip_address,
                "server": server,
                "powered_by": powered_by,
                "status_code": response.status_code,
                "redirects_count": redirects_count,
                "final_url": final_url
            })
        except Exception as e:
            # Fallback to plain HTTP if HTTPS fails
            try:
                url = f"http://{domain}"
                response = safe_requests_get(url, timeout=5)
                headers = response.headers
                results.update({
                    "status": "success",
                    "ip": ip_address,
                    "server": headers.get("Server", "Unknown"),
                    "powered_by": headers.get("X-Powered-By", "None"),
                    "status_code": response.status_code,
                    "redirects_count": len(response.history),
                    "final_url": response.url
                })
            except Exception as inner_e:
                results.update({
                    "status": "failed",
                    "ip": ip_address,
                    "error": f"HTTP request failed: {str(inner_e)}"
                })

    elif capability == "vulnerability_scan":
        # Check security headers via HTTP/HTTPS request
        headers = {}
        status_code = None
        try:
            url = f"https://{domain}"
            response = safe_requests_get(url, timeout=5)
            headers = response.headers
            status_code = response.status_code
        except Exception:
            try:
                url = f"http://{domain}"
                response = safe_requests_get(url, timeout=5)
                headers = response.headers
                status_code = response.status_code
            except Exception:
                pass

        if not headers and not status_code:
            results.update({
                "status": "failed",
                "error": "Could not connect to domain to run header-based vulnerability scan."
            })
        else:
            findings = []
            
            # HSTS Check
            if "Strict-Transport-Security" not in headers:
                findings.append({
                    "id": "missing_hsts",
                    "severity": "medium",
                    "description": "Strict-Transport-Security (HSTS) header is missing. Man-in-the-middle attacks possible."
                })
                
            # Clickjacking Check
            if "X-Frame-Options" not in headers and "frame-ancestors" not in headers.get("Content-Security-Policy", ""):
                findings.append({
                    "id": "missing_x_frame_options",
                    "severity": "medium",
                    "description": "X-Frame-Options header is missing. Vulnerable to Clickjacking attacks."
                })
                
            # CSP Check
            if "Content-Security-Policy" not in headers:
                findings.append({
                    "id": "missing_csp",
                    "severity": "high",
                    "description": "Content-Security-Policy (CSP) is not configured. High risk of XSS attacks."
                })
                
            # MIME sniffing Check
            if "X-Content-Type-Options" not in headers:
                findings.append({
                    "id": "missing_x_content_type",
                    "severity": "low",
                    "description": "X-Content-Type-Options header is missing. Vulnerable to MIME-sniffing attacks."
                })

            # Calculate grade
            missing_count = len(findings)
            has_high = any(f["severity"] == "high" for f in findings)
            
            if missing_count == 0:
                grade = "A"
            elif missing_count == 1 and not has_high:
                grade = "B"
            elif missing_count <= 2 and not has_high:
                grade = "C"
            elif has_high and missing_count <= 2:
                grade = "D"
            else:
                grade = "F"

            results.update({
                "status": "success",
                "security_grade": grade,
                "vulnerabilities_found": missing_count,
                "findings": findings
            })

    # 2. Sign the results payload
    response_payload = {
        "version": "1.0",
        "agent_id": AGENT_METADATA["agent_id"],
        "results": results
    }

    private_key = get_private_key()
    if private_key:
        try:
            # JCS canonicalization
            canonical_str = canonicalize(response_payload)
            canonical_bytes = canonical_str.encode('utf-8')
            # Cryptographic signature
            signature_bytes = private_key.sign(canonical_bytes)
            signature_b64 = base64.b64encode(signature_bytes).decode('utf-8')
            response_payload["signature"] = signature_b64
            response_payload["verification_state"] = "signed"
        except Exception as e:
            response_payload["verification_state"] = f"signing_error: {e}"
    else:
        response_payload["verification_state"] = "unsigned (private key missing on server)"

    return JSONResponse(content=response_payload)


@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    """
    Serves a premium glassmorphic web interface.
    """
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Creduent Agent Control Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0b0d10;
            --card-bg: rgba(20, 24, 33, 0.65);
            --primary: #4f46e5;
            --primary-glow: rgba(79, 70, 229, 0.4);
            --success: #10b981;
            --success-glow: rgba(16, 185, 129, 0.2);
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --border-color: rgba(255, 255, 255, 0.08);
            --accent: #06b6d4;
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
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(79, 70, 229, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(6, 182, 212, 0.12) 0%, transparent 40%);
        }

        .container {
            max-width: 900px;
            width: 95%;
            padding: 20px;
        }

        /* Glassmorphic Card */
        .card {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
        }

        /* Header section */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 25px;
            margin-bottom: 30px;
        }

        .brand h1 {
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(90deg, #ffffff, #9ca3af);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .brand p {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-top: 4px;
        }

        .badge {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid var(--success);
            color: var(--success);
            padding: 8px 16px;
            border-radius: 30px;
            font-size: 0.85rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 0 15px var(--success-glow);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 5px var(--success-glow); }
            50% { box-shadow: 0 0 15px var(--success-glow); }
            100% { box-shadow: 0 0 5px var(--success-glow); }
        }

        /* Info Grid */
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 35px;
        }

        .info-item {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            padding: 16px 20px;
            border-radius: 16px;
        }

        .info-item label {
            display: block;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-bottom: 6px;
        }

        .info-item span {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.95rem;
            word-break: break-all;
        }

        /* Interactive Console Section */
        .console-section h3 {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 15px;
        }

        .input-group {
            display: flex;
            gap: 12px;
            margin-bottom: 20px;
        }

        input, select {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-color);
            padding: 16px 20px;
            border-radius: 14px;
            color: var(--text-main);
            font-family: 'Outfit', sans-serif;
            font-size: 1rem;
            transition: all 0.3s;
        }

        input {
            flex: 1;
        }

        select {
            cursor: pointer;
        }

        input:focus, select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 10px var(--primary-glow);
        }

        option {
            background-color: var(--bg-color);
            color: var(--text-main);
        }

        button {
            background: linear-gradient(135deg, var(--primary), #3b82f6);
            color: white;
            border: none;
            padding: 0 30px;
            border-radius: 14px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px var(--primary-glow);
        }

        /* Terminal Output */
        .terminal {
            background: #050608;
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 20px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            height: 250px;
            overflow-y: auto;
            color: #38bdf8;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.8);
        }

        .terminal-line {
            margin-bottom: 6px;
            line-height: 1.4;
        }

        .terminal-line.system { color: #94a3b8; }
        .terminal-line.success { color: #34d399; }
        .terminal-line.warning { color: #fbbf24; }
        .terminal-line.json { color: #a78bfa; }

        .footer {
            text-align: center;
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-top: 10px;
        }

        .footer a {
            color: var(--text-main);
            text-decoration: none;
            border-bottom: 1px dotted var(--text-main);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="header">
                <div class="brand">
                    <h1>Creduent Recon Agent</h1>
                    <p>Open Application-Layer Trust Protocol</p>
                </div>
                <div class="badge">
                    <span style="display:inline-block; width:8px; height:8px; background:var(--success); border-radius:50%;"></span>
                    IDENTITY VERIFIED
                </div>
            </div>

            <div class="info-grid">
                <div class="info-item">
                    <label>Agent URI</label>
                    <span id="agentIdDisplay">agent://creduent/reconbot</span>
                </div>
                <div class="info-item">
                    <label>Owner</label>
                    <span id="ownerDisplay">Creduent Protocol Group</span>
                </div>
                <div class="info-item" style="grid-column: span 2;">
                    <label>Public Key (Ed25519)</label>
                    <span id="publicKeyDisplay">ed25519:uMMQ6RfZB5RJuYcZPwzLoiv8b6EQfU7CUJ2oLragCHg=</span>
                </div>
                <div class="info-item" style="grid-column: span 2;">
                    <label>Discovery Endpoint</label>
                    <span><a href="/.well-known/agent.json" style="color:var(--accent); text-decoration:none;" target="_blank">/.well-known/agent.json</a></span>
                </div>
            </div>

            <div class="console-section">
                <h3>Delegated Task Console</h3>
                <div class="input-group">
                    <select id="capabilitySelect">
                        <option value="dns_lookup">dns_lookup (DNS Resolution)</option>
                        <option value="osint">osint (Server footprint scan)</option>
                        <option value="vulnerability_scan">vulnerability_scan (Header audit)</option>
                    </select>
                    <input type="text" id="targetInput" placeholder="Enter target domain (e.g., google.com)" value="google.com">
                    <button onclick="executeScan()">Execute Scan</button>
                </div>
                <div class="terminal" id="terminal">
                    <div class="terminal-line system">[SYSTEM] Console loaded. Ready for task delegation.</div>
                </div>
            </div>
        </div>
        <div class="footer">
            Powered by <a href="https://github.com/cyberfascinate/creduent" target="_blank">Creduent Protocol Specification</a> (v1.0)
        </div>
    </div>

    <script>
        const term = document.getElementById('terminal');

        function log(msg, type='system') {
            const line = document.createElement('div');
            line.className = `terminal-line ${type}`;
            if (type === 'json') {
                line.style.whiteSpace = 'pre-wrap';
            }
            line.textContent = msg;
            term.appendChild(line);
            term.scrollTop = term.scrollHeight;
        }

        async function loadAgentMetadata() {
            try {
                const response = await fetch('/.well-known/agent.json');
                if (response.ok) {
                    const data = await response.json();
                    document.getElementById('agentIdDisplay').textContent = data.agent_id || 'agent://creduent/reconbot';
                    document.getElementById('ownerDisplay').textContent = data.owner || 'Creduent Protocol Group';
                    document.getElementById('publicKeyDisplay').textContent = data.public_key || '';
                }
            } catch (e) {
                console.error("Error loading agent metadata:", e);
            }
        }
        window.addEventListener('DOMContentLoaded', loadAgentMetadata);

        async function executeScan() {
            const target = document.getElementById('targetInput').value.trim();
            const capability = document.getElementById('capabilitySelect').value;
            if (!target) return;

            // Clear terminal
            term.innerHTML = '';
            log(`[+] Delegating task: '${capability}' over domain: ${target}...`);
            
            try {
                log(`[+] Fetching verification status from local discovery /.well-known/agent.json...`);
                const discResponse = await fetch('/.well-known/agent.json');
                if (!discResponse.ok) {
                    throw new Error(`Failed to fetch agent.json: ${discResponse.statusText}`);
                }
                const discData = await discResponse.ok ? await discResponse.json() : {};
                
                if (discData.public_key) {
                    document.getElementById('publicKeyDisplay').textContent = discData.public_key;
                }
                log(`[OK] Discovery successful. Public key: ${discData.public_key}`, 'success');
                
                log(`[+] Sending request to API endpoint: /api/scan?domain=${target}&capability=${capability}...`);
                const response = await fetch(`/api/scan?domain=${encodeURIComponent(target)}&capability=${capability}`);
                const data = await response.json();
                
                log(`[SUCCESS] API responded. Processing signed response payload:`, 'success');
                log(JSON.stringify(data, null, 2), 'json');
                
                if (data.signature) {
                    log(`[OK] Cryptographic signature detected: ${data.signature.substring(0, 20)}...`, 'success');
                    log(`[OK] Verification state: ${data.verification_state.toUpperCase()}`, 'success');
                } else {
                    log(`[WARNING] Response returned unsigned. State: ${data.verification_state}`, 'warning');
                }
            } catch(e) {
                log(`[-] Error running delegation task: ${e.message}`, 'warning');
            }
        }
    </script>
</body>
</html>"""
    return HTMLResponse(content=html_content)
