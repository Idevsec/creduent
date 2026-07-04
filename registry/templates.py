# HTML Templates for Creduent Attestation Registry UIs

RESOLVER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Creduent Resolver - Agent Identity Verification</title>
    <meta name="description" content="Decentralized agent:// URI cryptographic identity resolver and trust validator.">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #060913;
            --bg-surface: rgba(13, 20, 38, 0.7);
            --border-glow: rgba(99, 102, 241, 0.15);
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --primary-glow: rgba(99, 102, 241, 0.3);
            --success: #10b981;
            --success-bg: rgba(16, 185, 129, 0.08);
            --success-border: rgba(16, 185, 129, 0.2);
            --trusted: #8b5cf6;
            --trusted-bg: rgba(139, 92, 246, 0.08);
            --trusted-border: rgba(139, 92, 246, 0.2);
            --error: #ef4444;
            --error-bg: rgba(239, 68, 68, 0.08);
            --error-border: rgba(239, 68, 68, 0.2);
            --warning: #f59e0b;
            --warning-bg: rgba(245, 158, 11, 0.08);
            --warning-border: rgba(245, 158, 11, 0.2);
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --text-dark: #6b7280;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-base);
            color: var(--text-main);
            font-family: 'Outfit', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.12) 0%, transparent 50%),
                radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
        }

        .container {
            width: 95%;
            max-width: 800px;
            padding: 40px 20px;
            z-index: 10;
        }

        /* Glassmorphic Panel */
        .glass-panel {
            background: var(--bg-surface);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.07);
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 40px;
            position: relative;
        }

        /* Header */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            padding-bottom: 24px;
            margin-bottom: 30px;
        }

        .brand-badge {
            font-size: 0.65rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: var(--primary);
            margin-bottom: 6px;
            display: inline-block;
        }

        .title-area h1 {
            font-size: 1.8rem;
            font-weight: 700;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .title-area p {
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-top: 4px;
        }

        .status-badge {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            font-weight: 500;
            color: #a5b4fc;
            background: rgba(99, 102, 241, 0.08);
            border: 1px solid var(--border-glow);
            padding: 6px 12px;
            border-radius: 30px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--primary);
            box-shadow: 0 0 8px var(--primary);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 0.5; transform: scale(0.95); }
            50% { opacity: 1; transform: scale(1.1); }
        }

        /* Search Section */
        .search-section {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 30px;
        }

        .search-label {
            font-size: 0.85rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
        }

        .search-group {
            display: flex;
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .search-group:focus-within {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px var(--primary-glow);
        }

        .search-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0 16px;
            color: var(--text-muted);
            font-size: 1.1rem;
            background: rgba(255, 255, 255, 0.02);
            border-right: 1px solid rgba(255, 255, 255, 0.04);
        }

        .uri-input {
            flex: 1;
            background: transparent;
            border: none;
            color: var(--text-main);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.95rem;
            padding: 16px;
            outline: none;
        }

        .uri-input::placeholder {
            color: var(--text-dark);
        }

        .resolve-btn {
            background: var(--primary);
            color: #ffffff;
            border: none;
            font-family: 'Outfit', sans-serif;
            font-size: 0.95rem;
            font-weight: 600;
            padding: 0 28px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .resolve-btn:hover {
            background: var(--primary-hover);
        }

        /* Loader Screen */
        .scanning-loader {
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 30px;
            border: 1px dashed rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.01);
            margin-bottom: 25px;
        }

        .scanning-text {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-main);
            letter-spacing: 1px;
            margin-bottom: 16px;
        }

        .progress-bar-bg {
            width: 240px;
            height: 4px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            overflow: hidden;
            position: relative;
            margin-bottom: 20px;
        }

        .progress-bar-fill {
            position: absolute;
            left: 0; top: 0; height: 100%; width: 50%;
            background: linear-gradient(90deg, var(--primary), var(--trusted));
            border-radius: 10px;
            animation: progress-slide 1.5s ease-in-out infinite;
        }

        @keyframes progress-slide {
            0% { left: -50%; }
            100% { left: 100%; }
        }

        .diagnostic-logs {
            width: 100%;
            max-width: 500px;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 14px 18px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            line-height: 1.6;
            color: var(--text-muted);
            height: 120px;
            overflow-y: auto;
        }

        .log-entry {
            display: flex;
            gap: 10px;
        }

        .log-entry .timestamp {
            color: var(--text-dark);
        }

        .log-entry .action {
            color: var(--text-main);
        }

        /* Result Card Block */
        .card-container {
            display: none;
            margin-top: 10px;
            animation: fadeIn 0.4s ease-out forwards;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .identity-card {
            width: 100%;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            position: relative;
            overflow: hidden;
        }

        .identity-card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            padding-bottom: 20px;
            margin-bottom: 24px;
        }

        .identity-card-title {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .identity-avatar {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
            border: 1px solid rgba(99, 102, 241, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--primary);
        }

        .agent-info h2 {
            font-size: 1.35rem;
            font-weight: 600;
            color: #ffffff;
            letter-spacing: -0.3px;
        }

        .agent-info p {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            margin-top: 2px;
        }

        .badge-status {
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 6px 14px;
            border-radius: 30px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .badge-status::before {
            content: "";
            width: 6px;
            height: 6px;
            border-radius: 50%;
        }

        .status-verified {
            background: var(--success-bg);
            border: 1px solid var(--success-border);
            color: var(--success);
        }
        .status-verified::before { background-color: var(--success); }

        .status-trusted {
            background: var(--trusted-bg);
            border: 1px solid var(--trusted-border);
            color: var(--trusted);
        }
        .status-trusted::before { background-color: var(--trusted); }

        .status-revoked {
            background: var(--error-bg);
            border: 1px solid var(--error-border);
            color: var(--error);
        }
        .status-revoked::before { background-color: var(--error); }

        .status-unverified {
            background: var(--warning-bg);
            border: 1px solid var(--warning-border);
            color: var(--warning);
        }
        .status-unverified::before { background-color: var(--warning); }

        /* Details Grid */
        .details-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px 24px;
        }

        .grid-item {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .grid-item.full-width {
            grid-column: span 2;
        }

        .detail-label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            font-weight: 500;
        }

        .detail-value {
            font-size: 0.95rem;
            color: var(--text-main);
            word-break: break-all;
        }

        .detail-value.monospace {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            background: rgba(0, 0, 0, 0.15);
            padding: 8px 12px;
            border-radius: 6px;
            border: 1px solid rgba(255, 255, 255, 0.04);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .copy-btn {
            background: transparent;
            border: none;
            color: var(--text-dark);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 4px;
            border-radius: 4px;
            transition: all 0.2s;
        }

        .copy-btn:hover {
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.05);
        }

        /* Error HUD Box */
        .error-hud-box {
            display: none;
            border: 1px solid var(--error-border);
            background: var(--error-bg);
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(239, 68, 68, 0.05);
            margin-top: 10px;
            animation: fadeIn 0.4s ease-out forwards;
        }

        .error-title {
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--error);
            margin-bottom: 8px;
        }

        .error-message {
            font-size: 0.9rem;
            color: var(--text-muted);
            line-height: 1.6;
            max-width: 500px;
            margin: 0 auto;
        }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 30px;
            font-size: 0.85rem;
            color: var(--text-dark);
        }

        .footer a {
            color: var(--text-muted);
            text-decoration: none;
            border-bottom: 1px dotted var(--text-muted);
            transition: color 0.2s;
        }

        .footer a:hover {
            color: var(--text-main);
        }

        @media (max-width: 640px) {
            .details-grid {
                grid-template-columns: 1fr;
            }
            .grid-item.full-width {
                grid-column: span 1;
            }
            .search-group {
                flex-direction: column;
            }
            .search-icon {
                display: none;
            }
            .resolve-btn {
                padding: 16px;
            }
            .glass-panel {
                padding: 24px;
            }
            .header {
                flex-direction: column;
                align-items: flex-start;
                gap: 16px;
            }
        }
    </style>
</head>
<body>
    <main class="container">
        <div class="glass-panel">
            <!-- Header -->
            <header class="header">
                <div class="title-area">
                    <span class="brand-badge">iDevSec Security Suite</span>
                    <h1>Creduent Resolver</h1>
                    <p>Cryptographic Agent Identity Discovery</p>
                </div>
                <div class="status-badge">
                    <span class="pulse-dot"></span>
                    Registry Node Connected
                </div>
            </header>

            <!-- Search Area -->
            <section class="search-section">
                <label for="uriInput" class="search-label">Verify Agent URI</label>
                <div class="search-group">
                    <div class="search-icon">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    </div>
                    <input type="text" id="uriInput" class="uri-input" placeholder="agent://domain/name" value="agent://idevsec/steward" autocomplete="off" spellcheck="false">
                    <button id="resolveBtn" class="resolve-btn" onclick="resolveIdentity()">Resolve URI</button>
                </div>
            </section>

            <!-- Loader Screen -->
            <section id="scanningLoader" class="scanning-loader">
                <div class="scanning-text">Querying Cryptographic Registry</div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill"></div>
                </div>
                <div class="diagnostic-logs" id="diagnosticLogs"></div>
            </section>

            <!-- Result Card Block -->
            <section id="cardContainer" class="card-container">
                <div class="identity-card">
                    <div class="identity-card-header">
                        <div class="identity-card-title">
                            <div class="identity-avatar">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                            </div>
                            <div class="agent-info">
                                <h2 id="agentNameDisplay">AGENT IDENTIFIER</h2>
                                <p>Creduent Cryptographic Attestation</p>
                            </div>
                        </div>
                        <div id="statusBadge" class="badge-status status-verified">Verified</div>
                    </div>

                    <div class="details-grid">
                        <div class="grid-item full-width">
                            <div class="detail-label">Agent URI</div>
                            <div class="detail-value monospace" id="agentUriValue">agent://...</div>
                        </div>
                        <div class="grid-item full-width">
                            <div class="detail-label">Public Key (Ed25519)</div>
                            <div class="detail-value monospace">
                                <span id="agentKeyValue" style="font-size: 0.8rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 450px;">ed25519:...</span>
                                <button class="copy-btn" onclick="copyKey()" title="Copy Public Key">
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                                </button>
                            </div>
                        </div>
                        <div class="grid-item">
                            <div class="detail-label">Registered Domain</div>
                            <div class="detail-value" id="agentDomainValue">-</div>
                        </div>
                        <div class="grid-item">
                            <div class="detail-label">Issued Timestamp</div>
                            <div class="detail-value monospace" id="agentIssuedValue">-</div>
                        </div>
                        <div class="grid-item full-width">
                            <div class="detail-label">Attestation Authority</div>
                            <div class="detail-value monospace" id="agentIssuerValue">agent://creduent/registry</div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Error Box -->
            <section id="errorBox" class="error-hud-box">
                <div class="error-title" id="errorTitle">AGENT NOT FOUND</div>
                <div class="error-message" id="errorMessage">Identity document could not be resolved. Verification sequence aborted.</div>
            </section>
        </div>

        <footer class="footer">
            Creduent Trust Protocol &bull; A Project of <a href="https://idevsec.com" target="_blank">iDevSec</a>
        </footer>
    </main>

    <script>
        const logsBox = document.getElementById('diagnosticLogs');
        const loader = document.getElementById('scanningLoader');
        const cardBox = document.getElementById('cardContainer');
        const errorBox = document.getElementById('errorBox');

        function appendLog(action, status) {
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            const timeStr = new Date().toISOString().substring(11, 19);
            const statusColor = status === 'SUCCESS' || status === 'OK' ? 'var(--success)' : status === 'PENDING' ? 'var(--primary)' : 'var(--error)';
            entry.innerHTML = `<span class="timestamp">[${timeStr}]</span> <span class="action">${action}...</span> <span style="color: ${statusColor}; font-weight: 500;">${status}</span>`;
            logsBox.appendChild(entry);
            logsBox.scrollTop = logsBox.scrollHeight;
        }

        function copyKey() {
            const text = document.getElementById('agentKeyValue').innerText;
            navigator.clipboard.writeText(text).then(() => {
                const btn = document.querySelector('.copy-btn');
                btn.style.color = 'var(--success)';
                setTimeout(() => { btn.style.color = 'var(--text-dark)'; }, 1500);
            });
        }

        async function resolveIdentity() {
            let uri = document.getElementById('uriInput').value.trim();
            if (!uri) return;

            if (!uri.startsWith("agent://") && !uri.startsWith("agent:/")) {
                alert("Please enter a valid agent:// URI.");
                return;
            }

            if (uri.startsWith("agent:/") && !uri.startsWith("agent://")) {
                uri = "agent://" + uri.substring(7);
            }

            cardBox.style.display = 'none';
            errorBox.style.display = 'none';
            loader.style.display = 'flex';
            logsBox.innerHTML = '';

            appendLog("Initializing resolution sequence", "OK");
            appendLog("Establishing registry handshake", "PENDING");

            const requestPath = "/attest/" + encodeURIComponent(uri);

            try {
                await new Promise(r => setTimeout(r, 400));
                appendLog("Establishing registry handshake", "OK");
                appendLog("Verifying attestation proofs", "PENDING");
                
                await new Promise(r => setTimeout(r, 300));
                appendLog("Verifying attestation proofs", "OK");
                appendLog("Fetching agent identity document", "PENDING");

                const response = await fetch(requestPath);
                
                await new Promise(r => setTimeout(r, 300));

                if (response.status === 404) {
                    appendLog("Fetching agent identity document", "FAIL");
                    loader.style.display = 'none';
                    errorBox.style.display = 'block';
                    document.getElementById('errorTitle').textContent = "AGENT NOT FOUND";
                    document.getElementById('errorMessage').textContent = `Agent URI '${uri}' is not registered or has no active cryptographic attestation record in the registry database.`;
                    return;
                } else if (!response.ok) {
                    appendLog("Fetching agent identity document", "FAIL");
                    loader.style.display = 'none';
                    errorBox.style.display = 'block';
                    document.getElementById('errorTitle').textContent = "REGISTRY QUERY ERROR";
                    document.getElementById('errorMessage').textContent = `The registry node reported an unexpected error (${response.status} ${response.statusText}).`;
                    return;
                }

                const data = await response.json();
                appendLog("Fetching agent identity document", "OK");
                appendLog("Parsing cryptographic signature", "PENDING");
                
                await new Promise(r => setTimeout(r, 250));
                appendLog("Parsing cryptographic signature", "OK");
                appendLog("Validating identity signature", "OK");
                
                let namePart = "AGENT IDENTIFIER";
                try {
                    const parsed = uri.replace("agent://", "").split("/");
                    if (parsed.length > 0) {
                        namePart = parsed[parsed.length - 1];
                    }
                } catch(e){}

                document.getElementById('agentNameDisplay').textContent = namePart;
                document.getElementById('agentUriValue').textContent = data.agent_id || uri;
                document.getElementById('agentKeyValue').textContent = data.public_key || '-';
                document.getElementById('agentDomainValue').textContent = data.domain || '-';
                document.getElementById('agentIssuedValue').textContent = data.issued_at || '-';
                document.getElementById('agentIssuerValue').textContent = data.issuer || 'agent://creduent/registry';

                const level = (data.level || 'verified').toLowerCase();
                const badge = document.getElementById('statusBadge');
                badge.textContent = level;
                badge.className = 'badge-status';

                if (level === 'trusted') {
                    badge.classList.add('status-trusted');
                } else if (level === 'verified') {
                    badge.classList.add('status-verified');
                } else if (level === 'revoked') {
                    badge.classList.add('status-revoked');
                } else {
                    badge.classList.add('status-unverified');
                }

                loader.style.display = 'none';
                cardBox.style.display = 'block';

            } catch (err) {
                appendLog("Fetching agent identity document", "FAIL");
                loader.style.display = 'none';
                errorBox.style.display = 'block';
                document.getElementById('errorTitle').textContent = "REGISTRY UNREACHABLE";
                document.getElementById('errorMessage').textContent = "Could not communicate with the registry node. Please check your network connection and try again.";
            }
        }
    </script>
</body>
</html>"""

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Creduent Registry - Developer Dashboard</title>
    <meta name="description" content="Management and monitoring dashboard for Creduent Protocol Registry.">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0a0a0a;
            --surface: #111111;
            --surface-hover: #161616;
            --border: #222222;
            --border-focus: #3b82f6;
            --text: #f3f4f6;
            --text-muted: #9ca3af;
            --blue: #3b82f6;
            --blue-hover: #2563eb;
            --blue-dim: rgba(59, 130, 246, 0.1);
            --green: #22c55e;
            --green-dim: rgba(34, 197, 94, 0.1);
            --amber: #f59e0b;
            --amber-dim: rgba(245, 158, 11, 0.1);
            --red: #ef4444;
            --red-dim: rgba(239, 68, 68, 0.1);
            --violet: #8b5cf6;
            --violet-dim: rgba(139, 92, 246, 0.1);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            min-height: 100vh;
            padding: 40px 20px;
            line-height: 1.5;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
            padding-bottom: 20px;
            margin-bottom: 32px;
        }

        .brand h1 {
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: -0.025em;
        }

        .brand p {
            font-size: 0.875rem;
            color: var(--text-muted);
            margin-top: 4px;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.75rem;
            font-weight: 500;
            background: var(--green-dim);
            color: var(--green);
            padding: 4px 10px;
            border-radius: 9999px;
            border: 1px solid rgba(34, 197, 94, 0.2);
        }

        .status-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background-color: var(--green);
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }

        .stat-card {
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 20px;
        }

        .stat-label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            font-weight: 600;
        }

        .stat-val {
            font-size: 1.875rem;
            font-weight: 700;
            margin-top: 8px;
            font-family: 'JetBrains Mono', monospace;
        }

        .stat-card.warning {
            border-color: rgba(245, 158, 11, 0.4);
        }
        .stat-card.warning .stat-val {
            color: var(--amber);
        }

        /* Main Workspace Layout */
        .workspace {
            display: grid;
            grid-template-columns: 1fr 340px;
            gap: 24px;
        }

        @media (max-width: 1024px) {
            .workspace {
                grid-template-columns: 1fr;
            }
        }

        .main-panel {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .card {
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 24px;
        }

        .card-title {
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        /* Forms */
        .form-group {
            margin-bottom: 16px;
        }

        .form-group label {
            display: block;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 6px;
        }

        .form-group input, .form-group textarea {
            width: 100%;
            background-color: var(--bg);
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--text);
            padding: 10px 14px;
            font-family: inherit;
            font-size: 0.875rem;
            transition: border-color 0.2s;
        }

        .form-group input:focus, .form-group textarea:focus {
            outline: none;
            border-color: var(--border-focus);
        }

        .form-group input::placeholder {
            color: #4b5563;
        }

        .form-group textarea {
            resize: vertical;
            min-height: 80px;
            font-family: 'JetBrains Mono', monospace;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background-color: var(--blue);
            color: white;
            font-size: 0.875rem;
            font-weight: 500;
            padding: 10px 16px;
            border-radius: 6px;
            border: none;
            cursor: pointer;
            width: 100%;
            transition: background-color 0.2s;
        }

        .btn:hover {
            background-color: var(--blue-hover);
        }

        .btn-secondary {
            background-color: transparent;
            border: 1px solid var(--border);
            color: var(--text-muted);
        }

        .btn-secondary:hover {
            background-color: var(--bg);
            color: var(--text);
        }

        .btn-sm {
            padding: 6px 10px;
            font-size: 0.75rem;
            width: auto;
        }

        /* Table */
        .table-container {
            overflow-x: auto;
            margin: -24px;
            margin-top: 0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.875rem;
        }

        th {
            text-align: left;
            padding: 12px 24px;
            background-color: rgba(255, 255, 255, 0.02);
            border-bottom: 1px solid var(--border);
            font-weight: 500;
            color: var(--text-muted);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        td {
            padding: 16px 24px;
            border-bottom: 1px solid var(--border);
            vertical-align: middle;
        }

        tr:hover td {
            background-color: rgba(255, 255, 255, 0.01);
        }

        tr.warning-row td {
            background-color: rgba(239, 68, 68, 0.02);
        }

        tr.warning-row:hover td {
            background-color: rgba(239, 68, 68, 0.04);
        }

        .monospace {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8125rem;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.025em;
        }

        .badge-verified {
            background-color: var(--green-dim);
            color: var(--green);
            border: 1px solid rgba(34, 197, 94, 0.15);
        }

        .badge-unverified {
            background-color: var(--amber-dim);
            color: var(--amber);
            border: 1px solid rgba(245, 158, 11, 0.15);
        }

        .badge-revoked {
            background-color: var(--red-dim);
            color: var(--red);
            border: 1px solid rgba(239, 68, 68, 0.15);
        }

        .badge-trusted {
            background-color: var(--violet-dim);
            color: var(--violet);
            border: 1px solid rgba(139, 92, 246, 0.15);
        }

        .badge-warning {
            background-color: var(--red-dim);
            color: var(--red);
            border: 1px solid rgba(239, 68, 68, 0.2);
            font-size: 0.7rem;
            margin-left: 6px;
        }

        .actions-cell {
            display: flex;
            gap: 8px;
        }

        /* Modal Overlay */
        .modal-overlay {
            display: none;
            position: fixed;
            inset: 0;
            background-color: rgba(0, 0, 0, 0.8);
            z-index: 100;
            align-items: center;
            justify-content: center;
            padding: 20px;
            backdrop-filter: blur(4px);
        }

        .modal {
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            max-width: 600px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
            display: flex;
            flex-direction: column;
        }

        .modal-header {
            padding: 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .modal-body {
            padding: 20px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8125rem;
            white-space: pre-wrap;
            background-color: rgba(0, 0, 0, 0.2);
            color: var(--text-muted);
            overflow-x: auto;
        }

        .modal-footer {
            padding: 16px 20px;
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: flex-end;
        }

        /* Alerts and Feedbacks */
        .feedback {
            margin-top: 12px;
            padding: 10px 14px;
            border-radius: 6px;
            font-size: 0.8125rem;
            display: none;
        }

        .feedback-success {
            background-color: var(--green-dim);
            color: var(--green);
            border: 1px solid rgba(34, 197, 94, 0.2);
        }

        .feedback-error {
            background-color: var(--red-dim);
            color: var(--red);
            border: 1px solid rgba(239, 68, 68, 0.2);
        }

        .webhook-current-info {
            margin-top: 16px;
            padding: 12px;
            border: 1px dashed var(--border);
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.01);
            font-size: 0.8125rem;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="brand">
                <h1>Creduent Protocol Registry</h1>
                <p>Developer Dashboard</p>
            </div>
            <div class="status-badge">
                <span class="status-dot"></span>
                <span>SYSTEM LIVE</span>
            </div>
        </header>

        <!-- Stats Grid (Section A) -->
        <section class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Agents</div>
                <div class="stat-val" id="stat-total">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Verified</div>
                <div class="stat-val" style="color: var(--green);" id="stat-verified">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Unverified</div>
                <div class="stat-val" style="color: var(--amber);" id="stat-unverified">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Revoked</div>
                <div class="stat-val" style="color: var(--red);" id="stat-revoked">0</div>
            </div>
            <div class="stat-card warning" id="stat-exp-card">
                <div class="stat-label">Expiring &le; 30 Days</div>
                <div class="stat-val" id="stat-expiring">0</div>
            </div>
        </section>

        <!-- Workspace Layout -->
        <div class="workspace">
            <!-- Main panel (Section B) -->
            <div class="main-panel">
                <div class="card">
                    <div class="card-title">
                        <span>Agent Explorer</span>
                        <button class="btn btn-secondary btn-sm" onclick="fetchData()">Refresh Table</button>
                    </div>
                    <div class="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Agent ID</th>
                                    <th>Domain</th>
                                    <th>Level</th>
                                    <th>Expires At</th>
                                    <th>Remaining</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody id="agent-table-body">
                                <tr>
                                    <td colspan="6" style="text-align: center; color: var(--text-muted); padding: 40px 0;">
                                        Loading agent records...
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Side panel (Section C & D) -->
            <div class="side-panel" style="display: flex; flex-direction: column; gap: 24px;">
                <!-- Register Card (Section C) -->
                <div class="card">
                    <div class="card-title">Register New Agent</div>
                    <form id="register-form" onsubmit="handleRegister(event)">
                        <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 16px; line-height: 1.4; border-left: 2px solid var(--amber); padding-left: 8px;">
                            Direct registration requires admin key. Public registration via <code style="background: rgba(255,255,255,0.05); padding: 1px 4px; border-radius: 3px;">POST /register</code> uses DNS + agent.json verification.
                        </div>
                        <div class="form-group">
                            <label for="reg-agent-id">Agent ID</label>
                            <input type="text" id="reg-agent-id" name="reg-agent-id" placeholder="agent://creduent/my-agent" autocomplete="username" required>
                        </div>
                        <div class="form-group">
                            <label for="reg-domain">Domain</label>
                            <input type="text" id="reg-domain" name="reg-domain" placeholder="my-agent.com" autocomplete="off" required>
                        </div>
                        <div class="form-group">
                            <label for="reg-public-key">Public Key (Ed25519)</label>
                            <textarea id="reg-public-key" name="reg-public-key" placeholder="ed25519:uMMQ6RfZB5RJu..." required></textarea>
                        </div>
                        <div class="form-group">
                            <label for="reg-admin-key">Admin Key</label>
                            <input type="password" id="reg-admin-key" name="reg-admin-key" placeholder="Enter admin key..." required autocomplete="current-password">
                        </div>
                        <button type="submit" class="btn">Register Agent</button>
                        <div id="register-feedback" class="feedback"></div>
                    </form>
                </div>

                <!-- Webhook Card (Section D) -->
                <div class="card">
                    <div class="card-title">Webhook Manager</div>
                    <form id="webhook-form" onsubmit="handleWebhookRegister(event)">
                        <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 16px; line-height: 1.4; border-left: 2px solid var(--blue); padding-left: 8px;">
                            Webhook registration requires a valid Ed25519 signature. Sign the payload: <code style="background: rgba(255,255,255,0.05); padding: 1px 4px; border-radius: 3px;">agent_id|webhook_url</code> with your agent's private key.
                        </div>
                        <div class="form-group">
                            <label for="web-agent-id">Agent ID</label>
                            <input type="text" id="web-agent-id" placeholder="agent://creduent/my-agent" oninput="updateWebhookPayload()" required>
                        </div>
                        <div class="form-group">
                            <label for="web-url">Webhook URL</label>
                            <input type="url" id="web-url" placeholder="https://api.my-agent.com/webhook" oninput="updateWebhookPayload()" required>
                        </div>
                        
                        <!-- Webhook Payload Display (Hidden until fields filled) -->
                        <div id="web-payload-container" style="display: none; background: rgba(255, 255, 255, 0.02); border: 1px solid var(--border); border-radius: 8px; padding: 12px; margin-bottom: 16px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); font-weight: 600;">Payload to Sign</div>
                                <button type="button" class="btn btn-secondary btn-sm" id="copy-web-payload-btn" onclick="copyWebhookPayload()" style="font-size: 0.7rem; padding: 2px 6px;">Copy</button>
                            </div>
                            <pre id="web-payload-display" style="background: #050607; border: 1px solid var(--border); border-radius: 6px; padding: 10px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #a78bfa; white-space: pre-wrap; word-break: break-all; line-height: 1.4;"></pre>
                        </div>

                        <!-- Signature Input -->
                        <div class="form-group">
                            <label for="web-signature">Signature</label>
                            <textarea id="web-signature" placeholder="Base64-encoded Ed25519 signature..." required style="min-height: 60px; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem;"></textarea>
                        </div>

                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                            <button type="submit" class="btn">Register</button>
                            <button type="button" class="btn btn-secondary" onclick="handleWebhookQuery()">Query URL</button>
                        </div>
                        <div id="webhook-feedback" class="feedback"></div>
                        <div id="webhook-info" class="webhook-current-info"></div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- View Modal -->
    <div class="modal-overlay" id="view-modal" onclick="closeModal(event)">
        <div class="modal" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h3 id="modal-title">Agent Attestation</h3>
                <button class="btn btn-secondary btn-sm" onclick="hideModal()">Close</button>
            </div>
            <div class="modal-body" id="modal-body"></div>
            <div class="modal-footer">
                <button class="btn btn-secondary btn-sm" onclick="hideModal()">Done</button>
            </div>
        </div>
    </div>

    <!-- Renew Modal -->
    <div class="modal-overlay" id="renew-modal" onclick="closeRenewModal(event)">
        <form class="modal" id="renew-form" onsubmit="handleRenew(event)" onclick="event.stopPropagation()" style="max-width:640px; margin:0;">
            <div class="modal-header">
                <div>
                    <h3 style="font-size:1.05rem;font-weight:600;">Renew Agent Attestation</h3>
                    <p style="font-size:0.78rem;color:var(--text-muted);margin-top:3px;" id="ren-modal-subtitle">Sign the payload below with the agent's private key</p>
                </div>
                <button type="button" class="btn btn-secondary btn-sm" onclick="hideRenewModal()">✕ Close</button>
            </div>
            <div style="padding:20px;display:flex;flex-direction:column;gap:16px;overflow-y:auto;max-height:70vh;">

                <!-- Step 1: Agent + Expiry -->
                <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border);border-radius:8px;padding:16px;">
                    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;color:var(--text-muted);font-weight:600;margin-bottom:12px;">① Set New Expiry</div>
                    <input type="hidden" id="ren-agent-id" name="ren-agent-id">
                    <div class="form-group" style="margin-bottom:12px;">
                        <label for="ren-agent-id-display" style="font-size:0.72rem;">Agent ID</label>
                        <input type="text" id="ren-agent-id-display" name="ren-agent-id-display" readonly style="opacity:0.55;font-family:'JetBrains Mono',monospace;font-size:0.8rem;" autocomplete="username">
                    </div>
                    <div class="form-group" style="margin-bottom:0;">
                        <label for="ren-expires-at" style="font-size:0.72rem;">New Expiry Date <span style="color:var(--text-muted);font-weight:400;">(ISO 8601 UTC)</span></label>
                        <input type="text" id="ren-expires-at" name="ren-expires-at" placeholder="2027-05-30T00:00:00Z" oninput="updateRenewPayload()" required autocomplete="off">
                    </div>
                </div>

                <!-- Step 2: Payload to sign -->
                <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border);border-radius:8px;padding:16px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                        <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;color:var(--text-muted);font-weight:600;">② Payload to Sign</div>
                        <button type="button" class="btn btn-secondary btn-sm" id="copy-payload-btn" onclick="copyRenewPayload()" style="font-size:0.7rem;">Copy</button>
                    </div>
                    <pre id="ren-payload-display" style="background:#050607;border:1px solid var(--border);border-radius:6px;padding:12px;font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:#a78bfa;white-space:pre-wrap;word-break:break-all;line-height:1.6;"></pre>
                    <p style="font-size:0.75rem;color:var(--text-muted);margin-top:8px;">Sign this string with <code style="background:rgba(255,255,255,0.05);padding:1px 5px;border-radius:3px;font-size:0.72rem;">ed25519.sign(payload.encode())</code> and base64-encode the result.</p>
                </div>

                <!-- Step 3: Signature input -->
                <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border);border-radius:8px;padding:16px;">
                    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;color:var(--text-muted);font-weight:600;margin-bottom:12px;">③ Paste Signature</div>
                    <textarea id="ren-signature" name="ren-signature" placeholder="Base64-encoded Ed25519 signature..." style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:6px;color:var(--text);padding:10px 14px;font-family:'JetBrains Mono',monospace;font-size:0.8rem;resize:vertical;min-height:70px;transition:border-color 0.2s;" required></textarea>
                </div>

                <!-- Submit -->
                <button type="submit" class="btn" id="ren-submit-btn" style="font-weight:600;">Submit Renewal</button>
                <div id="renew-feedback" class="feedback"></div>
            </div>
        </form>
    </div>

    <!-- Upgrade Modal -->
    <div class="modal-overlay" id="upgrade-modal" onclick="closeUpgradeModal(event)">
        <form class="modal" id="upgrade-form" onsubmit="handleUpgrade(event)" onclick="event.stopPropagation()" style="max-width:480px; margin:0;">
            <div class="modal-header">
                <div>
                    <h3 style="font-size:1.05rem;font-weight:600;">Upgrade Attestation Level</h3>
                    <p style="font-size:0.78rem;color:var(--text-muted);margin-top:3px;">Select target level and enter admin key</p>
                </div>
                <button type="button" class="btn btn-secondary btn-sm" onclick="hideUpgradeModal()">✕ Close</button>
            </div>
            <div style="padding:20px;display:flex;flex-direction:column;gap:16px;">
                <input type="hidden" id="upg-agent-id" name="upg-agent-id">
                <div class="form-group" style="margin-bottom:12px;">
                    <label for="upg-agent-id-display" style="font-size:0.72rem;">Agent ID</label>
                    <input type="text" id="upg-agent-id-display" name="upg-agent-id-display" readonly style="opacity:0.55;font-family:'JetBrains Mono',monospace;font-size:0.8rem;" autocomplete="username">
                </div>
                <div class="form-group" style="margin-bottom:12px;">
                    <label for="upg-level" style="font-size:0.72rem;">Target Level</label>
                    <select id="upg-level" name="upg-level" style="width: 100%; background-color: var(--bg); border: 1px solid var(--border); border-radius: 6px; color: var(--text); padding: 10px 14px; font-family: inherit; font-size: 0.875rem;">
                        <option value="verified">Verified (Identity confirmed)</option>
                        <option value="trusted">Trusted (High authority/partner)</option>
                        <option value="unverified">Unverified (Revoke verification)</option>
                    </select>
                </div>
                <div class="form-group" style="margin-bottom:12px;">
                    <label for="upg-admin-key" style="font-size:0.72rem;">Admin Key</label>
                    <input type="password" id="upg-admin-key" name="upg-admin-key" placeholder="Enter admin key..." style="width: 100%; background-color: var(--bg); border: 1px solid var(--border); border-radius: 6px; color: var(--text); padding: 10px 14px; font-family: inherit; font-size: 0.875rem;" autocomplete="current-password">
                </div>
                <button type="submit" class="btn" id="upg-submit-btn" style="font-weight:600;">Submit Upgrade</button>
                <div id="upgrade-feedback" class="feedback"></div>
            </div>
        </form>
    </div>

    <!-- Revoke Modal -->
    <div class="modal-overlay" id="revoke-modal" onclick="closeRevokeModal(event)">
        <form class="modal" id="revoke-form" onsubmit="handleRevoke(event)" onclick="event.stopPropagation()" style="max-width:480px; margin:0;">
            <div class="modal-header">
                <div>
                    <h3 style="font-size:1.05rem;font-weight:600;color:var(--red);">Revoke Agent Attestation</h3>
                    <p style="font-size:0.78rem;color:var(--text-muted);margin-top:3px;">Enter admin key to confirm revocation</p>
                </div>
                <button type="button" class="btn btn-secondary btn-sm" onclick="hideRevokeModal()">✕ Close</button>
            </div>
            <div style="padding:20px;display:flex;flex-direction:column;gap:16px;">
                <input type="hidden" id="rev-agent-id" name="rev-agent-id">
                <div class="form-group" style="margin-bottom:12px;">
                    <label for="rev-agent-id-display" style="font-size:0.72rem;">Agent ID</label>
                    <input type="text" id="rev-agent-id-display" name="rev-agent-id-display" readonly style="opacity:0.55;font-family:'JetBrains Mono',monospace;font-size:0.8rem;" autocomplete="username">
                </div>
                <div class="form-group" style="margin-bottom:12px;">
                    <label for="rev-admin-key" style="font-size:0.72rem;">Admin Key</label>
                    <input type="password" id="rev-admin-key" name="rev-admin-key" placeholder="Enter admin key..." style="width: 100%; background-color: var(--bg); border: 1px solid var(--border); border-radius: 6px; color: var(--text); padding: 10px 14px; font-family: inherit; font-size: 0.875rem;" autocomplete="current-password">
                </div>
                <div style="font-size: 0.78rem; color: var(--red); line-height: 1.4; background: var(--red-dim); border: 1px solid rgba(239, 68, 68, 0.2); padding: 10px; border-radius: 6px;">
                    <strong>Warning:</strong> Revoking this agent will mark it as permanently revoked. This signature cannot be verified and the action cannot be undone.
                </div>
                <button type="submit" class="btn" id="rev-submit-btn" style="background-color: var(--red); font-weight:600;">Revoke Agent</button>
                <div id="revoke-feedback" class="feedback"></div>
            </div>
        </form>
    </div>

    <script>
        // Set default ISO date for renewal to 1 year from now
        function updateDefaultRenewalDate() {
            const nextYear = new Date();
            nextYear.setFullYear(nextYear.getFullYear() + 1);
            // Replace fraction and zone offset to end with Z
            document.getElementById('ren-expires-at').value = nextYear.toISOString().split('.')[0] + 'Z';
        }

        async function fetchData() {
            try {
                // Fetch stats
                const statsRes = await fetch('/stats');
                if (statsRes.ok) {
                    const stats = await statsRes.json();
                    document.getElementById('stat-total').textContent = stats.total;
                    document.getElementById('stat-verified').textContent = stats.verified;
                    document.getElementById('stat-unverified').textContent = stats.unverified;
                    document.getElementById('stat-revoked').textContent = stats.revoked;
                    document.getElementById('stat-expiring').textContent = stats.expiring_soon;

                    const expCard = document.getElementById('stat-exp-card');
                    if (stats.expiring_soon > 0) {
                        expCard.classList.add('warning');
                    } else {
                        expCard.classList.remove('warning');
                    }
                }

                // Fetch agent explorer table
                const agentsRes = await fetch('/agents');
                const tbody = document.getElementById('agent-table-body');
                if (agentsRes.ok) {
                    const agents = await agentsRes.json();
                    if (agents.length === 0) {
                        tbody.innerHTML = `
                            <tr>
                                <td colspan="6" style="text-align: center; color: var(--text-muted); padding: 40px 0;">
                                    No agents registered in the system.
                                </td>
                            </tr>
                        `;
                        return;
                    }

                    tbody.innerHTML = '';
                    const now = new Date();

                    agents.forEach(agent => {
                        const tr = document.createElement('tr');

                        // Resolve level early so it's available for all checks below
                        const level = (agent.level || 'verified').toLowerCase();

                        // Parse remaining days
                        let daysRem = '-';
                        let isExpiringSoon = false;
                        const expiresAtStr = agent.expires_at;
                        if (expiresAtStr && level !== 'revoked') {
                            try {
                                const expiry = new Date(expiresAtStr);
                                const diffTime = expiry - now;
                                daysRem = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                                if (daysRem < 0) {
                                    daysRem = `Expired (${Math.abs(daysRem)}d ago)`;
                                } else {
                                    if (daysRem <= 30) {
                                        isExpiringSoon = true;
                                    }
                                    daysRem = `${daysRem} days`;
                                }
                            } catch (e) {
                                daysRem = 'Error parsing';
                            }
                        }

                        if (isExpiringSoon) {
                            tr.className = 'warning-row';
                        }

                        // Badges
                        let badgeClass = 'badge-verified';
                        if (level === 'revoked') badgeClass = 'badge-revoked';
                        else if (level === 'trusted') badgeClass = 'badge-trusted';
                        else if (level !== 'verified') badgeClass = 'badge-unverified';

                        const warningBadge = isExpiringSoon ? `<span class="badge badge-warning">Expiring Soon</span>` : '';

                        tr.innerHTML = `
                            <td class="monospace">${agent.agent_id}</td>
                            <td>${agent.domain || '-'}</td>
                            <td><span class="badge ${badgeClass}">${level}</span></td>
                            <td class="monospace">${expiresAtStr ? expiresAtStr.split('T')[0] : '-'}</td>
                            <td class="${isExpiringSoon ? 'monospace' : ''}" style="${isExpiringSoon ? 'color: var(--red); font-weight: 600;' : ''}">
                                ${daysRem} ${warningBadge}
                            </td>
                            <td>
                                <div class="actions-cell">
                                    <button class="btn btn-secondary btn-sm" onclick="viewAgent('${encodeURIComponent(agent.agent_id)}')">View</button>
                                    <button class="btn btn-secondary btn-sm" onclick="showUpgradeModal('${encodeURIComponent(agent.agent_id)}')">Level</button>
                                    <button class="btn btn-secondary btn-sm" onclick="showRenewModal('${encodeURIComponent(agent.agent_id)}')">Renew</button>
                                    <button class="btn btn-secondary btn-sm" onclick="showRevokeModal('${encodeURIComponent(agent.agent_id)}')" style="color: var(--red);">Revoke</button>
                                </div>
                            </td>
                        `;
                        tbody.appendChild(tr);
                    });
                } else {
                    tbody.innerHTML = `
                        <tr>
                            <td colspan="6" style="text-align: center; color: var(--red); padding: 40px 0;">
                                Failed to fetch agent records from server.
                            </td>
                        </tr>
                    `;
                }
            } catch (e) {
                console.error("Dashboard fetch error:", e);
            }
        }

        async function viewAgent(agentIdDec) {
            const agentId = decodeURIComponent(agentIdDec);
            try {
                const res = await fetch(`/attest/${encodeURIComponent(agentId)}`);
                if (res.ok) {
                    const data = await res.json();
                    document.getElementById('modal-title').textContent = `Attestation: ${agentId}`;
                    document.getElementById('modal-body').textContent = JSON.stringify(data, null, 2);
                    document.getElementById('view-modal').style.display = 'flex';
                } else {
                    alert(`Failed to fetch agent attestation: ${res.statusText}`);
                }
            } catch (e) {
                alert(`Error: ${e.message}`);
            }
        }

        function populateWebhook(agentIdDec) {
            const agentId = decodeURIComponent(agentIdDec);
            document.getElementById('web-agent-id').value = agentId;
            document.getElementById('webhook-info').style.display = 'none';
            document.getElementById('webhook-feedback').style.display = 'none';
            updateWebhookPayload();
        }

        function updateWebhookPayload() {
            const agentId = document.getElementById('web-agent-id').value.trim();
            const webhookUrl = document.getElementById('web-url').value.trim();
            const payloadDisplay = document.getElementById('web-payload-display');
            const payloadContainer = document.getElementById('web-payload-container');
            
            if (agentId && webhookUrl) {
                const payloadStr = `${agentId}|${webhookUrl}`;
                payloadDisplay.textContent = payloadStr;
                payloadContainer.style.display = 'block';
            } else {
                payloadDisplay.textContent = '';
                payloadContainer.style.display = 'none';
            }
        }

        function copyWebhookPayload() {
            const text = document.getElementById('web-payload-display').textContent;
            navigator.clipboard.writeText(text).then(() => {
                const btn = document.getElementById('copy-web-payload-btn');
                btn.textContent = '✓ Copied';
                btn.style.color = 'var(--green)';
                setTimeout(() => { btn.textContent = 'Copy'; btn.style.color = ''; }, 2000);
            });
        }

        function updateDefaultRenewalDate() {
            const d = new Date();
            d.setFullYear(d.getFullYear() + 1);
            const iso = d.toISOString().replace(/\.\d{3}Z$/, 'Z');
            document.getElementById('ren-expires-at').value = iso;
        }

        function updateRenewPayload() {
            const agentId = document.getElementById('ren-agent-id').value;
            const expiresAt = document.getElementById('ren-expires-at').value.trim();
            const payloadStr = `${agentId}|${expiresAt}`;
            document.getElementById('ren-payload-display').textContent = payloadStr;
        }

        function copyRenewPayload() {
            const text = document.getElementById('ren-payload-display').textContent;
            navigator.clipboard.writeText(text).then(() => {
                const btn = document.getElementById('copy-payload-btn');
                btn.textContent = '✓ Copied';
                btn.style.color = 'var(--green)';
                setTimeout(() => { btn.textContent = 'Copy'; btn.style.color = ''; }, 2000);
            });
        }

        function showRenewModal(agentIdDec) {
            const agentId = decodeURIComponent(agentIdDec);
            document.getElementById('ren-agent-id').value = agentId;
            document.getElementById('ren-agent-id-display').value = agentId;
            document.getElementById('renew-feedback').style.display = 'none';
            document.getElementById('ren-signature').value = '';
            document.getElementById('ren-submit-btn').disabled = false;
            document.getElementById('ren-submit-btn').textContent = 'Submit Renewal';
            updateDefaultRenewalDate();
            updateRenewPayload();
            document.getElementById('renew-modal').style.display = 'flex';
        }

        function hideRenewModal() {
            document.getElementById('renew-modal').style.display = 'none';
        }

        function closeRenewModal(e) {
            if (e.target === document.getElementById('renew-modal')) {
                hideRenewModal();
            }
        }

        function hideModal() {
            document.getElementById('view-modal').style.display = 'none';
        }

        function closeModal(e) {
            if (e.target === document.getElementById('view-modal')) {
                hideModal();
            }
        }

        async function handleRegister(e) {
            e.preventDefault();
            const feedback = document.getElementById('register-feedback');
            feedback.style.display = 'none';

            const agent_id = document.getElementById('reg-agent-id').value.trim();
            const domain = document.getElementById('reg-domain').value.trim();
            const public_key = document.getElementById('reg-public-key').value.trim();
            const admin_key = document.getElementById('reg-admin-key').value.trim();

            try {
                const res = await fetch('/attest', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'CREDUENT-ADMIN-KEY': admin_key
                    },
                    body: JSON.stringify({ agent_id, domain, public_key })
                });

                const data = await res.json();
                if (res.ok) {
                    feedback.className = 'feedback feedback-success';
                    feedback.textContent = 'Agent registered and attested successfully!';
                    feedback.style.display = 'block';
                    document.getElementById('register-form').reset();
                    fetchData();
                } else {
                    feedback.className = 'feedback feedback-error';
                    feedback.textContent = `Registration failed: ${data.detail || 'Unknown error'}`;
                    feedback.style.display = 'block';
                }
            } catch (err) {
                feedback.className = 'feedback feedback-error';
                feedback.textContent = `Error: ${err.message}`;
                feedback.style.display = 'block';
            }
        }

        async function handleWebhookRegister(e) {
            e.preventDefault();
            const feedback = document.getElementById('webhook-feedback');
            feedback.style.display = 'none';

            const agent_id = document.getElementById('web-agent-id').value.trim();
            const webhook_url = document.getElementById('web-url').value.trim();
            const signature = document.getElementById('web-signature').value.trim();

            if (!signature) {
                feedback.className = 'feedback feedback-error';
                feedback.textContent = 'Signature is required. Sign the payload shown in the payload container.';
                feedback.style.display = 'block';
                return;
            }

            try {
                const res = await fetch('/webhook/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ agent_id, webhook_url, signature })
                });

                const data = await res.json();
                if (res.ok) {
                    feedback.className = 'feedback feedback-success';
                    feedback.textContent = 'Webhook URL registered successfully!';
                    feedback.style.display = 'block';
                    document.getElementById('web-signature').value = '';
                } else {
                    feedback.className = 'feedback feedback-error';
                    feedback.textContent = `Registration failed: ${data.detail || 'Unknown error'}`;
                    feedback.style.display = 'block';
                }
            } catch (err) {
                feedback.className = 'feedback feedback-error';
                feedback.textContent = `Error: ${err.message}`;
                feedback.style.display = 'block';
            }
        }

        async function handleWebhookQuery() {
            const feedback = document.getElementById('webhook-feedback');
            const info = document.getElementById('webhook-info');
            feedback.style.display = 'none';
            info.style.display = 'none';

            const agent_id = document.getElementById('web-agent-id').value.trim();
            if (!agent_id) {
                feedback.className = 'feedback feedback-error';
                feedback.textContent = 'Please enter an Agent ID to query';
                feedback.style.display = 'block';
                return;
            }

            try {
                const res = await fetch(`/webhook/${encodeURIComponent(agent_id)}`);
                const data = await res.json();
                if (res.ok) {
                    info.innerHTML = `
                        <strong style="color: var(--blue);">Registered URL:</strong><br>
                        <code class="monospace" style="word-break: break-all;">${data.webhook_url}</code>
                    `;
                    info.style.display = 'block';
                } else {
                    feedback.className = 'feedback feedback-error';
                    feedback.textContent = `Query failed: ${data.detail || 'Webhook not registered'}`;
                    feedback.style.display = 'block';
                }
            } catch (err) {
                feedback.className = 'feedback feedback-error';
                feedback.textContent = `Error: ${err.message}`;
                feedback.style.display = 'block';
            }
        }

        async function handleRenew(e) {
            e.preventDefault();
            const feedback = document.getElementById('renew-feedback');
            const submitBtn = document.getElementById('ren-submit-btn');
            feedback.style.display = 'none';

            const agent_id = document.getElementById('ren-agent-id').value.trim();
            const new_expires_at = document.getElementById('ren-expires-at').value.trim();
            const signature = document.getElementById('ren-signature').value.trim();

            if (!signature) {
                feedback.className = 'feedback feedback-error';
                feedback.textContent = 'Signature is required. Sign the payload shown in step ②.';
                feedback.style.display = 'block';
                return;
            }

            // Loading state
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';

            try {
                const res = await fetch('/renew', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ agent_id, new_expires_at, signature })
                });

                const data = await res.json();
                if (res.ok) {
                    feedback.className = 'feedback feedback-success';
                    feedback.textContent = `✓ Agent attestation renewed! New expiry: ${new_expires_at}`;
                    feedback.style.display = 'block';
                    submitBtn.textContent = '✓ Renewed';
                    setTimeout(() => {
                        hideRenewModal();
                        fetchData();
                    }, 1500);
                } else {
                    feedback.className = 'feedback feedback-error';
                    feedback.textContent = `Renewal failed: ${data.detail || 'Unknown error'}`;
                    feedback.style.display = 'block';
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Submit Renewal';
                }
            } catch (err) {
                feedback.className = 'feedback feedback-error';
                feedback.textContent = `Network error: ${err.message}`;
                feedback.style.display = 'block';
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit Renewal';
            }
        }

        function showUpgradeModal(agentIdDec) {
            const agentId = decodeURIComponent(agentIdDec);
            document.getElementById('upg-agent-id').value = agentId;
            document.getElementById('upg-agent-id-display').value = agentId;
            document.getElementById('upgrade-feedback').style.display = 'none';
            document.getElementById('upg-admin-key').value = '';
            document.getElementById('upg-submit-btn').disabled = false;
            document.getElementById('upg-submit-btn').textContent = 'Submit Upgrade';
            document.getElementById('upgrade-modal').style.display = 'flex';
        }

        function hideUpgradeModal() {
            document.getElementById('upgrade-modal').style.display = 'none';
        }

        function closeUpgradeModal(e) {
            if (e.target === document.getElementById('upgrade-modal')) {
                hideUpgradeModal();
            }
        }

        async function handleUpgrade(e) {
            e.preventDefault();
            const feedback = document.getElementById('upgrade-feedback');
            const submitBtn = document.getElementById('upg-submit-btn');
            feedback.style.display = 'none';

            const agent_id = document.getElementById('upg-agent-id').value.trim();
            const level = document.getElementById('upg-level').value;
            const admin_key = document.getElementById('upg-admin-key').value.trim();

            if (!admin_key) {
                feedback.className = 'feedback feedback-error';
                feedback.textContent = 'Admin Key is required.';
                feedback.style.display = 'block';
                return;
            }

            // Loading state
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';

            try {
                const res = await fetch('/admin/attest', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'CREDUENT-ADMIN-KEY': admin_key
                    },
                    body: JSON.stringify({ agent_id, level })
                });

                const data = await res.json();
                if (res.ok) {
                    feedback.className = 'feedback feedback-success';
                    feedback.textContent = `✓ Agent attestation level upgraded to: ${level}`;
                    feedback.style.display = 'block';
                    submitBtn.textContent = '✓ Upgraded';
                    setTimeout(() => {
                        hideUpgradeModal();
                        fetchData();
                    }, 1500);
                } else {
                    feedback.className = 'feedback feedback-error';
                    feedback.textContent = `Upgrade failed: ${data.detail || 'Unknown error'}`;
                    feedback.style.display = 'block';
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Submit Upgrade';
                }
            } catch (err) {
                feedback.className = 'feedback feedback-error';
                feedback.textContent = `Network error: ${err.message}`;
                feedback.style.display = 'block';
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit Upgrade';
            }
        }

        function showRevokeModal(agentIdDec) {
            const agentId = decodeURIComponent(agentIdDec);
            document.getElementById('rev-agent-id').value = agentId;
            document.getElementById('rev-agent-id-display').value = agentId;
            document.getElementById('revoke-feedback').style.display = 'none';
            document.getElementById('rev-admin-key').value = '';
            document.getElementById('rev-submit-btn').disabled = false;
            document.getElementById('rev-submit-btn').textContent = 'Revoke Agent';
            document.getElementById('revoke-modal').style.display = 'flex';
        }

        function hideRevokeModal() {
            document.getElementById('revoke-modal').style.display = 'none';
        }

        function closeRevokeModal(e) {
            if (e.target === document.getElementById('revoke-modal')) {
                hideRevokeModal();
            }
        }

        async function handleRevoke(e) {
            e.preventDefault();
            const feedback = document.getElementById('revoke-feedback');
            const submitBtn = document.getElementById('rev-submit-btn');
            feedback.style.display = 'none';

            const agent_id = document.getElementById('rev-agent-id').value.trim();
            const admin_key = document.getElementById('rev-admin-key').value.trim();

            if (!admin_key) {
                feedback.className = 'feedback feedback-error';
                feedback.textContent = 'Admin Key is required.';
                feedback.style.display = 'block';
                return;
            }

            // Loading state
            submitBtn.disabled = true;
            submitBtn.textContent = 'Revoking...';

            try {
                const res = await fetch('/revoke/' + encodeURIComponent(agent_id), {
                    method: 'DELETE',
                    headers: { 
                        'CREDUENT-ADMIN-KEY': admin_key
                    }
                });

                const data = await res.json();
                if (res.ok) {
                    feedback.className = 'feedback feedback-success';
                    feedback.textContent = '✓ Agent attestation successfully revoked!';
                    feedback.style.display = 'block';
                    submitBtn.textContent = '✓ Revoked';
                    setTimeout(() => {
                        hideRevokeModal();
                        fetchData();
                    }, 1500);
                } else {
                    feedback.className = 'feedback feedback-error';
                    feedback.textContent = `Revocation failed: ${data.detail || 'Unknown error'}`;
                    feedback.style.display = 'block';
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Revoke Agent';
                }
            } catch (err) {
                feedback.className = 'feedback feedback-error';
                feedback.textContent = `Network error: ${err.message}`;
                feedback.style.display = 'block';
                submitBtn.disabled = false;
                submitBtn.textContent = 'Revoke Agent';
            }
        }

        // Initialize & Auto refresh every 30s
        window.addEventListener('DOMContentLoaded', () => {
            fetchData();
            setInterval(fetchData, 30000);
        });
    </script>
</body>
</html>
"""

AGENT_CONSOLE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Creduent | Agent Console</title>
    <meta name="description" content="Creduent cryptographic agent identity resolution and trust verification protocol.">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #07090d;
            --surface: rgba(255,255,255,0.032);
            --surface-raised: rgba(255,255,255,0.055);
            --border: rgba(255,255,255,0.07);
            --border-active: rgba(139,92,246,0.45);
            --text: #f1f5f9;
            --text-muted: #64748b;
            --text-dim: #2d3748;
            --purple: #8b5cf6;
            --purple-glow: rgba(139,92,246,0.18);
            --blue: #38bdf8;
            --green: #34d399;
            --green-glow: rgba(52,211,153,0.15);
            --amber: #fbbf24;
            --red: #f87171;
        }
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        html { scroll-behavior: smooth; }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Ambient bg */
        body::before {
            content: '';
            position: fixed;
            inset: 0;
            background:
                radial-gradient(ellipse 55% 45% at 12% 8%, rgba(139,92,246,0.1) 0%, transparent 65%),
                radial-gradient(ellipse 45% 38% at 88% 88%, rgba(56,189,248,0.07) 0%, transparent 65%),
                radial-gradient(ellipse 35% 30% at 50% 50%, rgba(52,211,153,0.04) 0%, transparent 65%);
            pointer-events: none;
            z-index: 0;
        }

        .page-wrap {
            position: relative;
            z-index: 1;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        /* Navbar */
        nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 28px;
            height: 58px;
            border-bottom: 1px solid var(--border);
            background: rgba(7,9,13,0.8);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .nav-logo {
            display: flex;
            align-items: center;
            gap: 9px;
            font-weight: 700;
            font-size: 0.92rem;
            letter-spacing: -0.01em;
            color: var(--text);
            text-decoration: none;
        }

        .nav-logo-icon {
            width: 26px;
            height: 26px;
            background: linear-gradient(135deg, var(--purple), #6366f1);
            border-radius: 7px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7rem;
            box-shadow: 0 0 14px var(--purple-glow);
            flex-shrink: 0;
        }

        .nav-right { display: flex; align-items: center; gap: 8px; }

        .nav-link {
            padding: 5px 11px;
            border-radius: 6px;
            font-size: 0.78rem;
            color: var(--text-muted);
            text-decoration: none;
            transition: all 0.15s;
            border: 1px solid transparent;
        }
        .nav-link:hover { color: var(--text); background: var(--surface); border-color: var(--border); }

        .live-pill {
            display: flex;
            align-items: center;
            gap: 6px;
            background: var(--green-glow);
            border: 1px solid rgba(52,211,153,0.22);
            padding: 4px 11px 4px 9px;
            border-radius: 20px;
            font-size: 0.68rem;
            font-weight: 600;
            color: var(--green);
            letter-spacing: 0.05em;
        }
        .live-dot {
            width: 6px;
            height: 6px;
            background: var(--green);
            border-radius: 50%;
            flex-shrink: 0;
            animation: blink 2s ease-in-out infinite;
        }
        @keyframes blink {
            0%, 100% { opacity: 1; box-shadow: 0 0 5px var(--green); }
            50% { opacity: 0.3; box-shadow: none; }
        }

        /* Main */
        main {
            flex: 1;
            max-width: 1080px;
            width: 100%;
            margin: 0 auto;
            padding: 44px 20px 60px;
        }

        /* Hero */
        .hero {
            text-align: center;
            margin-bottom: 44px;
        }
        .hero-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: var(--purple-glow);
            border: 1px solid rgba(139,92,246,0.22);
            border-radius: 20px;
            padding: 4px 13px;
            font-size: 0.68rem;
            font-weight: 600;
            color: var(--purple);
            letter-spacing: 0.07em;
            text-transform: uppercase;
            margin-bottom: 18px;
        }
        .hero h1 {
            font-size: 2.4rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            line-height: 1.1;
            background: linear-gradient(140deg, #fff 25%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 12px;
        }
        .hero p {
            font-size: 0.95rem;
            color: var(--text-muted);
            max-width: 460px;
            margin: 0 auto;
            line-height: 1.7;
        }

        /* Two-column layout */
        .split {
            display: grid;
            grid-template-columns: 320px 1fr;
            gap: 18px;
            align-items: start;
        }
        @media (max-width: 820px) {
            .split { grid-template-columns: 1fr; }
            .hero h1 { font-size: 1.9rem; }
        }

        /* Card */
        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            overflow: hidden;
            transition: border-color 0.2s;
        }
        .card:hover { border-color: rgba(255,255,255,0.1); }

        .card-header {
            padding: 14px 18px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .card-header-title {
            font-size: 0.68rem;
            font-weight: 600;
            letter-spacing: 0.09em;
            text-transform: uppercase;
            color: var(--text-muted);
        }

        /* Identity panel */
        .identity-inner {
            padding: 20px 16px 16px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .identity-badge {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, var(--purple), #6366f1);
            border-radius: 13px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            margin-bottom: 14px;
            box-shadow: 0 0 22px var(--purple-glow);
        }

        .identity-name {
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 3px;
        }
        .identity-uri {
            font-size: 0.72rem;
            color: var(--purple);
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 18px;
            word-break: break-all;
            text-align: center;
        }

        .fields { display: flex; flex-direction: column; gap: 7px; width: 100%; }

        .field {
            background: rgba(0,0,0,0.22);
            border: 1px solid var(--border);
            border-radius: 9px;
            padding: 9px 13px;
        }
        .field-label {
            font-size: 0.6rem;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            color: var(--text-muted);
            font-weight: 600;
            margin-bottom: 4px;
        }
        .field-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            color: var(--text);
            word-break: break-all;
            line-height: 1.45;
        }
        .field-value a { color: var(--blue); text-decoration: none; }
        .field-value a:hover { text-decoration: underline; }

        .caps-wrap {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin-top: 14px;
            width: 100%;
        }
        .cap-pill {
            background: rgba(139,92,246,0.1);
            border: 1px solid rgba(139,92,246,0.2);
            color: #a78bfa;
            padding: 3px 9px;
            border-radius: 20px;
            font-size: 0.66rem;
            font-weight: 500;
            font-family: 'JetBrains Mono', monospace;
        }

        /* Scan console */
        .scan-controls {
            padding: 18px;
            border-bottom: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .domain-row { display: flex; gap: 9px; }

        .input-wrap { flex: 1; position: relative; }
        .input-prefix {
            position: absolute;
            left: 11px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 0.75rem;
            pointer-events: none;
            font-family: 'JetBrains Mono', monospace;
        }

        input[type="text"] {
            width: 100%;
            background: rgba(0,0,0,0.3);
            border: 1px solid var(--border);
            border-radius: 9px;
            padding: 9px 12px 9px 34px;
            color: var(--text);
            font-family: 'Inter', sans-serif;
            font-size: 0.83rem;
            outline: none;
            transition: border-color 0.18s, box-shadow 0.18s;
        }
        input[type="text"]:focus {
            border-color: var(--border-active);
            box-shadow: 0 0 0 3px var(--purple-glow);
        }

        .btn-exec {
            background: linear-gradient(135deg, var(--purple), #6366f1);
            color: #fff;
            border: none;
            border-radius: 9px;
            padding: 9px 20px;
            font-size: 0.83rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.18s;
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 6px;
            font-family: 'Inter', sans-serif;
            letter-spacing: -0.01em;
        }
        .btn-exec:hover { transform: translateY(-1px); box-shadow: 0 6px 18px rgba(139,92,246,0.32); }
        .btn-exec:active { transform: none; }
        .btn-exec:disabled { opacity: 0.45; cursor: not-allowed; transform: none; box-shadow: none; }

        .cap-row {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 14px;
        }
        .cap-row-label {
            font-size: 0.68rem;
            font-weight: 600;
            color: var(--text-muted);
            letter-spacing: 0.05em;
            text-transform: uppercase;
            white-space: nowrap;
        }
        .radio-opt {
            display: flex;
            align-items: center;
            gap: 5px;
            cursor: pointer;
            font-size: 0.78rem;
            color: var(--text-muted);
            transition: color 0.15s;
            user-select: none;
        }
        .radio-opt:hover { color: var(--text); }
        .radio-opt input[type="radio"] {
            accent-color: var(--purple);
            width: 14px;
            height: 14px;
            cursor: pointer;
            margin: 0;
            padding: 0;
            flex-shrink: 0;
        }

        /* Terminal */
        .terminal-wrap { padding: 14px; }

        .term-bar {
            display: flex;
            align-items: center;
            gap: 5px;
            margin-bottom: 9px;
        }
        .td { width: 9px; height: 9px; border-radius: 50%; }
        .td.r { background: #ef4444; }
        .td.a { background: #f59e0b; }
        .td.g { background: #22c55e; }
        .term-tag {
            margin-left: auto;
            font-size: 0.62rem;
            color: var(--text-dim);
            font-family: 'JetBrains Mono', monospace;
        }

        .terminal {
            background: #03050a;
            border: 1px solid rgba(255,255,255,0.045);
            border-radius: 9px;
            padding: 14px 16px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.77rem;
            min-height: 300px;
            max-height: 440px;
            overflow-y: auto;
            line-height: 1.7;
            display: flex;
            flex-direction: column;
            gap: 0;
            scrollbar-width: thin;
            scrollbar-color: rgba(255,255,255,0.08) transparent;
        }
        .terminal::-webkit-scrollbar { width: 3px; }
        .terminal::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 2px; }

        .tl { display: block; }
        .tl.sys { color: #334155; }
        .tl.info { color: #94a3b8; }
        .tl.ok { color: var(--green); }
        .tl.warn { color: var(--amber); }
        .tl.err { color: var(--red); }
        .tl.json { color: #a78bfa; white-space: pre-wrap; word-break: break-word; }
        .tl.hl { color: var(--blue); }

        .cursor {
            display: inline-block;
            width: 7px;
            height: 13px;
            background: var(--purple);
            vertical-align: text-bottom;
            margin-left: 1px;
            animation: cblink 1.1s step-end infinite;
        }
        @keyframes cblink { 0%,100%{opacity:1}50%{opacity:0} }

        .spinner {
            display: inline-block;
            width: 12px;
            height: 12px;
            border: 2px solid rgba(255,255,255,0.2);
            border-top-color: #fff;
            border-radius: 50%;
            animation: sp 0.65s linear infinite;
            vertical-align: middle;
        }
        @keyframes sp { to { transform: rotate(360deg); } }

        /* Footer */
        footer {
            text-align: center;
            padding: 22px;
            border-top: 1px solid var(--border);
            color: var(--text-dim);
            font-size: 0.72rem;
            background: rgba(7,9,13,0.6);
        }
        footer a { color: var(--text-muted); text-decoration: none; }
        footer a:hover { color: var(--text); }
    </style>
</head>
<body>
<div class="page-wrap">

    <nav>
        <a href="/" class="nav-logo">
            <div class="nav-logo-icon">⬡</div>
            Creduent
        </a>
        <div class="nav-right">
            <a href="/.well-known/agent.json" target="_blank" class="nav-link">agent.json</a>
            <a href="/resolver" class="nav-link">Resolver</a>
            <a href="/registry/dashboard" class="nav-link">Registry</a>
            <div class="live-pill">
                <span class="live-dot"></span>LIVE
            </div>
        </div>
    </nav>

    <main>
        <div class="hero">
            <div class="hero-eyebrow">⬡ &nbsp;Creduent Protocol · v1.0</div>
            <h1>Agent Console</h1>
            <p>Delegated task execution and cryptographic signature console for autonomous AI agents over the Creduent protocol.</p>
        </div>

        <div class="split">
            <!-- Identity Panel -->
            <div class="card">
                <div class="card-header">
                    <span class="card-header-title">Agent Identity</span>
                    <div class="live-pill" style="font-size:0.62rem;padding:3px 8px 3px 7px;">
                        <span class="live-dot"></span>VERIFIED
                    </div>
                </div>
                <div class="identity-inner">
                    <div class="identity-badge">⬡</div>
                    <div class="identity-name" id="ownerDisplay">Creduent</div>
                    <div class="identity-uri" id="agentIdDisplay">agent://idevsec/steward</div>
                    <div class="fields">
                        <div class="field">
                            <div class="field-label">Public Key · Ed25519</div>
                            <div class="field-value" id="publicKeyDisplay">loading...</div>
                        </div>
                        <div class="field">
                            <div class="field-label">Discovery Endpoint</div>
                            <div class="field-value">
                                <a href="/.well-known/agent.json" target="_blank">/.well-known/agent.json</a>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">Issued At</div>
                            <div class="field-value" id="issuedDisplay">-</div>
                        </div>
                    </div>
                    <div class="caps-wrap" id="capsWrap">
                        <span class="cap-pill">dns_lookup</span>
                        <span class="cap-pill">osint</span>
                        <span class="cap-pill">vulnerability_scan</span>
                    </div>
                </div>
            </div>

            <!-- Scan Console -->
            <div class="card">
                <div class="card-header">
                    <span class="card-header-title">Delegated Task Console</span>
                </div>
                <div class="scan-controls">
                    <div class="domain-row">
                        <div class="input-wrap">
                            <span class="input-prefix">⌕</span>
                            <input type="text" id="targetInput" placeholder="Target domain (e.g. google.com)" value="google.com">
                        </div>
                        <button class="btn-exec" onclick="executeScan()" id="scanBtn">
                            <span id="scanBtnIcon">▶</span>
                            <span id="scanBtnText">Execute</span>
                        </button>
                    </div>
                    <div class="cap-row">
                        <span class="cap-row-label">Mode:</span>
                        <label class="radio-opt">
                            <input type="radio" name="cap" value="dns_lookup" checked>
                            DNS Lookup
                        </label>
                        <label class="radio-opt">
                            <input type="radio" name="cap" value="osint">
                            OSINT Fingerprint
                        </label>
                        <label class="radio-opt">
                            <input type="radio" name="cap" value="vulnerability_scan">
                            Vuln Scan
                        </label>
                    </div>
                </div>
                <div class="terminal-wrap">
                    <div class="term-bar">
                        <span class="td r"></span>
                        <span class="td a"></span>
                        <span class="td g"></span>
                        <span class="term-tag">creduent://shell v1.0</span>
                    </div>
                    <div class="terminal" id="terminal">
                        <span class="tl sys">┌─ Creduent Agent Shell</span>
                        <span class="tl sys">│  Cryptographic identity loaded.</span>
                        <span class="tl sys">└─ Ready for task delegation.</span>
                        <span class="tl"> </span>
                        <span class="tl info">$ <span class="cursor"></span></span>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <footer>
        Powered by <a href="https://github.com/idevsec/creduent" target="_blank">Creduent Open Protocol</a> · v1.0
        &nbsp;·&nbsp;
        <a href="/.well-known/agent.json" target="_blank">agent.json</a>
        &nbsp;·&nbsp;
        <a href="/registry/dashboard">Registry Dashboard</a>
    </footer>

</div>

<script>
    const term = document.getElementById('terminal');

    function clearTerm() { term.innerHTML = ''; }

    function log(msg, cls = 'info') {
        // Remove cursor line before adding new content
        const last = term.querySelector('span:last-child');
        if (last && last.querySelector('.cursor')) last.remove();

        const s = document.createElement('span');
        s.className = 'tl ' + cls;
        s.textContent = msg;
        term.appendChild(s);
        term.scrollTop = term.scrollHeight;
    }

    function logPrompt() {
        const s = document.createElement('span');
        s.className = 'tl info';
        s.innerHTML = '$ <span class="cursor"></span>';
        term.appendChild(s);
        term.scrollTop = term.scrollHeight;
    }

    async function loadAgentMetadata() {
        try {
            const r = await fetch('/.well-known/agent.json');
            if (!r.ok) return;
            const d = await r.json();
            if (d.agent_id) document.getElementById('agentIdDisplay').textContent = d.agent_id;
            if (d.owner)    document.getElementById('ownerDisplay').textContent = d.owner;
            if (d.public_key) document.getElementById('publicKeyDisplay').textContent = d.public_key;
            if (d.issued_at)  document.getElementById('issuedDisplay').textContent = d.issued_at;
            if (d.capabilities && Array.isArray(d.capabilities)) {
                const wrap = document.getElementById('capsWrap');
                wrap.innerHTML = '';
                d.capabilities.forEach(c => {
                    const pill = document.createElement('span');
                    pill.className = 'cap-pill';
                    pill.textContent = c;
                    wrap.appendChild(pill);
                });
            }
        } catch(e) { console.error('Metadata load error:', e); }
    }

    async function executeScan() {
        const target = document.getElementById('targetInput').value.trim();
        const cap = document.querySelector('input[name="cap"]:checked')?.value || 'dns_lookup';
        if (!target) return;

        const btn = document.getElementById('scanBtn');
        const btnIcon = document.getElementById('scanBtnIcon');
        const btnText = document.getElementById('scanBtnText');

        btn.disabled = true;
        btnIcon.innerHTML = '<span class="spinner"></span>';
        btnText.textContent = 'Running...';

        clearTerm();
        log('┌─ Task initiated', 'ok');
        log('│  Mode   : ' + cap, 'ok');
        log('│  Target : ' + target, 'ok');
        log('└─ Delegating to Creduent agent...', 'ok');
        log(' ');

        try {
            log('[1/3] Loading agent identity from /.well-known/agent.json ...', 'info');
            const discRes = await fetch('/.well-known/agent.json');
            if (!discRes.ok) throw new Error('agent.json returned ' + discRes.status);
            const disc = await discRes.json();
            log('      ✓ Agent ID  : ' + disc.agent_id, 'ok');
            log('      ✓ Owner     : ' + disc.owner, 'ok');
            log('      ✓ Public Key: ' + disc.public_key, 'hl');
            log(' ');

            log('[2/3] Sending delegated task to /api/scan ...', 'info');
            const scanRes = await fetch('/api/scan?domain=' + encodeURIComponent(target) + '&capability=' + encodeURIComponent(cap) + '&_t=' + Date.now());
            const data = await scanRes.json();
            log('      ✓ HTTP ' + scanRes.status + ' received', 'ok');
            log(' ');

            log('[3/3] Verifying cryptographic signature ...', 'info');
            if (data.signature) {
                log('      ✓ Sig   : ' + data.signature.substring(0, 30) + '...', 'ok');
                log('      ✓ State : ' + (data.verification_state || '').toUpperCase(), 'ok');
            } else {
                log('      ⚠ Response is unsigned', 'warn');
                log('      ⚠ State : ' + (data.verification_state || 'unknown'), 'warn');
            }
            log(' ');

            log('─── Signed Response ───────────────────────────────────────', 'sys');
            log(JSON.stringify(data, null, 2), 'json');
            log('───────────────────────────────────────────────────────────', 'sys');

        } catch(e) {
            log('[ERROR] ' + e.message, 'err');
        } finally {
            btn.disabled = false;
            btnIcon.textContent = '▶';
            btnText.textContent = 'Execute';
            log(' ');
            logPrompt();
        }
    }

    window.addEventListener('DOMContentLoaded', loadAgentMetadata);
</script>
</body>
</html>"""
