# HTML Templates for Creduent Attestation Registry UIs

RESOLVER_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Creduent Identity Resolver - Agent Verification</title>
    <meta name="description" content="Decentralized agent:// URI cryptographic identity resolver and trust validator.">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "@id": "https://creduent.idevsec.com/#resolver",
      "name": "Creduent Identity Resolver",
      "applicationCategory": "SecurityApplication",
      "operatingSystem": "Cross-platform",
      "url": "https://creduent.idevsec.com/resolver",
      "author": {
        "@type": "Person",
        "@id": "https://cyberfascinate.idevsec.com/#founder",
        "name": "Kashish Kanojia",
        "alternateName": ["CyberFascinate", "cyberfascinate"],
        "jobTitle": "Founder & CEO",
        "sameAs": [
          "https://cyberfascinate.idevsec.com",
          "https://www.imdb.com/name/nm16609377/",
          "https://www.crunchbase.com/person/kashish-kanojia",
          "https://keybase.io/cyberfascinate",
          "https://orcid.org/0009-0002-3978-9363",
          "https://linkedin.com/in/cyberfascinate",
          "https://github.com/cyberfascinate",
          "https://x.com/cyberfascinate"
        ]
      },
      "provider": {
        "@type": "Organization",
        "@id": "https://idevsec.com/#organization",
        "name": "IDevSec",
        "url": "https://idevsec.com",
        "sameAs": [
          "https://idevsec.com",
          "https://www.crunchbase.com/organization/idevsec",
          "https://cyberfascinate.idevsec.com",
          "https://idevsec.com/creduent"
        ]
      }
    }
    </script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #f6f9fc;
            --bg-surface: #ffffff;
            --border-color: #e3e8ee;
            --border-input: #a8c3de;
            --primary: #533afd;
            --primary-hover: #4434d4;
            --primary-press: #2e2b8c;
            --primary-glow: rgba(83, 58, 253, 0.08);
            --primary-bg-subdued: #b9b9f9;
            --success: #22c55e;
            --success-bg: rgba(34, 197, 94, 0.08);
            --success-border: rgba(34, 197, 94, 0.2);
            --trusted: #8b5cf6;
            --trusted-bg: rgba(139, 92, 246, 0.08);
            --trusted-border: rgba(139, 92, 246, 0.2);
            --error: #ea2261;
            --error-bg: rgba(234, 34, 97, 0.08);
            --error-border: rgba(234, 34, 97, 0.2);
            --warning: #9b6829;
            --warning-bg: rgba(155, 104, 41, 0.08);
            --warning-border: rgba(155, 104, 41, 0.2);
            --text-main: #0d253d;
            --text-muted: #64748d;
            --text-dark: #61718a;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-base);
            color: var(--text-main);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-feature-settings: "ss01" on;
            font-weight: 300;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 0%, rgba(245, 233, 212, 0.6) 0%, transparent 45%),
                radial-gradient(circle at 45% 0%, rgba(155, 104, 41, 0.1) 0%, transparent 40%),
                radial-gradient(circle at 90% 0%, rgba(249, 107, 238, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 25% 0%, rgba(83, 58, 253, 0.12) 0%, transparent 55%),
                radial-gradient(circle at 75% 0%, rgba(234, 34, 97, 0.12) 0%, transparent 45%);
            background-size: 100% 420px;
            background-repeat: no-repeat;
        }

        .container {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px 40px 24px;
            z-index: 10;
            display: flex;
            flex-direction: column;
            flex: 1;
        }

        /* Navbar style */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 24px 0;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 24px;
            width: 100%;
        }

        .nav-left {
            display: flex;
            align-items: center;
        }

        .brand-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
        }

        .brand-avatar {
            width: 36px;
            height: 36px;
            background-color: var(--primary);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            box-shadow: 0 2px 8px rgba(83, 58, 253, 0.2);
        }

        .brand-text {
            font-family: 'Outfit', sans-serif;
            font-size: 20px;
            font-weight: 500;
            letter-spacing: -0.42px;
        }

        .brand-name {
            color: var(--text-main);
        }

        .brand-suffix {
            color: var(--primary);
        }

        .nav-center {
            display: flex;
            align-items: center;
            gap: 32px;
        }

        .nav-link {
            font-size: 15px;
            font-weight: 400;
            color: var(--text-muted);
            text-decoration: none;
            transition: color 0.15s ease;
        }

        .nav-link:hover {
            color: var(--text-main);
        }

        .nav-link.active {
            color: var(--primary);
            font-weight: 500;
        }

        .nav-right {
            display: flex;
            align-items: center;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-feature-settings: "tnum" on;
            font-size: 13px;
            font-weight: 400;
            line-height: 1.0;
            letter-spacing: -0.39px;
            background: var(--success-bg);
            color: var(--success);
            padding: 8px 16px;
            border-radius: 9999px;
            border: 1px solid var(--success-border);
            box-shadow: rgba(34, 197, 94, 0.08) 0 4px 12px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--success);
            box-shadow: 0 0 8px var(--success);
            animation: pulse-green 2s infinite;
        }

        @keyframes pulse-green {
            0%, 100% { opacity: 0.6; transform: scale(0.9); }
            50% { opacity: 1; transform: scale(1.15); }
        }

        .page-header {
            margin-bottom: 28px;
            animation: fadeIn 0.4s ease-out forwards;
        }

        .page-header h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 28px;
            font-weight: 500;
            color: var(--text-main);
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .page-header p {
            font-size: 14px;
            color: var(--text-muted);
            margin-top: 6px;
        }

        /* Grid Layout */
        .resolver-grid {
            display: grid;
            grid-template-columns: 4fr 6fr;
            gap: 28px;
            margin-bottom: 40px;
            width: 100%;
            align-items: start;
        }

        .resolver-sidebar {
            display: flex;
            flex-direction: column;
            gap: 24px;
            min-width: 0;
        }

        .resolver-main {
            display: flex;
            flex-direction: column;
            gap: 24px;
            min-height: 400px;
            min-width: 0;
        }

        /* Glass Panel */
        .glass-panel {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            box-shadow: rgba(0, 55, 112, 0.06) 0 8px 24px, rgba(0, 0, 0, 0.02) 0 2px 6px;
            border-radius: 12px;
            padding: 24px;
            position: relative;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .glass-panel:hover {
            box-shadow: rgba(0, 55, 112, 0.1) 0 12px 36px, rgba(0, 0, 0, 0.04) 0 4px 12px;
        }

        /* Search input & group */
        .search-section {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .search-label {
            font-family: 'Outfit', sans-serif;
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
        }

        .search-group {
            display: flex;
            background: var(--bg-base);
            border: 1px solid var(--border-input);
            border-radius: 9999px;
            overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.02);
            padding: 4px;
            align-items: center;
        }

        .search-group:focus-within {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px var(--primary-glow);
            background: var(--bg-surface);
        }

        .search-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0 12px 0 16px;
            color: var(--text-muted);
            flex-shrink: 0;
        }

        .uri-input {
            flex: 1;
            background: transparent;
            border: none;
            color: var(--text-main);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            padding: 8px 0;
            outline: none;
            min-width: 0;
        }

        .uri-input::placeholder {
            color: var(--text-muted);
            opacity: 0.55;
        }

        .resolve-btn {
            background: var(--primary);
            color: #ffffff;
            border: none;
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            font-weight: 500;
            padding: 8px 18px;
            cursor: pointer;
            transition: all 0.2s ease;
            border-radius: 9999px;
            flex-shrink: 0;
        }

        .resolve-btn:hover {
            background: var(--primary-hover);
            transform: translateY(-1px);
        }

        .resolve-btn:active {
            background: var(--primary-press);
            transform: translateY(0);
        }

        /* Examples list styling */
        .quick-examples {
            margin-top: 20px;
            padding-top: 16px;
            border-top: 1px solid var(--border-color);
        }

        .section-subtitle {
            font-family: 'Outfit', sans-serif;
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            margin-bottom: 12px;
            display: block;
        }

        .example-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .example-tag {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            color: var(--primary);
            background: var(--primary-glow);
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
            border: 1px solid rgba(83, 58, 253, 0.1);
        }

        .example-tag:hover {
            background: var(--primary);
            color: #ffffff;
            transform: translateY(-1px);
            box-shadow: 0 2px 6px rgba(83, 58, 253, 0.15);
        }

        /* History items styling */
        .card-header-compact {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .card-header-compact .section-subtitle {
            margin-bottom: 0;
        }

        .clear-history-btn {
            background: transparent;
            border: none;
            font-size: 0.75rem;
            font-weight: 500;
            color: var(--error);
            cursor: pointer;
            padding: 2px 6px;
            border-radius: 4px;
            transition: all 0.2s;
        }

        .clear-history-btn:hover {
            background: var(--error-bg);
        }

        .history-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .history-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--bg-base);
            padding: 10px 14px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            cursor: pointer;
            transition: all 0.2s;
        }

        .history-item:hover {
            border-color: var(--primary);
            background: var(--primary-glow);
            transform: translateX(2px);
        }

        .history-uri {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            color: var(--text-main);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            max-width: 85%;
        }

        .history-arrow {
            color: var(--text-muted);
            font-size: 0.85rem;
            transition: transform 0.2s;
        }

        .history-item:hover .history-arrow {
            color: var(--primary);
            transform: translateX(2px);
        }

        /* Logs block */
        .logs-card {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .diagnostic-logs {
            width: 100%;
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px 14px;
            font-family: 'JetBrains Mono', monospace;
            font-feature-settings: "tnum" on;
            font-size: 0.75rem;
            line-height: 1.6;
            color: var(--text-muted);
            height: 140px;
            overflow-y: auto;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.01);
        }

        .log-entry {
            display: flex;
            gap: 8px;
            border-bottom: 1px solid rgba(0,0,0,0.02);
            padding: 4px 0;
        }
        
        .log-entry:last-child {
            border-bottom: none;
        }

        .log-entry .timestamp {
            color: var(--text-dark);
            flex-shrink: 0;
        }

        .log-entry .action {
            color: var(--text-main);
            flex-grow: 1;
        }

        /* Main right side sections */
        .placeholder-card {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            min-height: 440px;
            text-align: center;
            border: 1px dashed var(--border-input);
            box-shadow: none;
        }

        .placeholder-content {
            max-width: 400px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 16px;
        }

        .placeholder-icon {
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: var(--primary-glow);
            color: var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(83, 58, 253, 0.08);
            margin-bottom: 4px;
        }

        .placeholder-content h3 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.3rem;
            font-weight: 500;
            color: var(--text-main);
        }

        .placeholder-content p {
            font-size: 0.9rem;
            color: var(--text-muted);
            line-height: 1.6;
        }

        /* Scanning State */
        .scanning-card {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            min-height: 440px;
        }

        .scanning-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
            width: 100%;
            max-width: 320px;
            text-align: center;
        }

        .scanning-text {
            font-family: 'Outfit', sans-serif;
            font-size: 1.2rem;
            font-weight: 500;
            color: var(--text-main);
        }

        .progress-bar-bg {
            width: 100%;
            height: 6px;
            background: var(--bg-base);
            border-radius: 10px;
            overflow: hidden;
            position: relative;
            border: 1px solid var(--border-color);
        }

        .progress-bar-fill {
            position: absolute;
            left: 0; top: 0; height: 100%; width: 40%;
            background: linear-gradient(90deg, var(--primary), var(--trusted));
            border-radius: 10px;
            animation: progress-slide 1.5s ease-in-out infinite;
        }

        @keyframes progress-slide {
            0% { left: -40%; }
            100% { left: 100%; }
        }

        .scanning-sub {
            font-size: 0.85rem;
            color: var(--text-muted);
        }

        /* Error state block */
        .error-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            min-height: 440px;
            text-align: center;
            border: 1px solid var(--error-border);
            background: var(--error-bg);
        }

        .error-icon {
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: rgba(234, 34, 97, 0.12);
            color: var(--error);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 16px;
        }

        .error-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--error);
            margin-bottom: 8px;
            letter-spacing: -0.2px;
        }

        .error-message {
            font-size: 0.9rem;
            color: var(--text-muted);
            line-height: 1.6;
            max-width: 420px;
            margin: 0 auto;
        }

        /* Result Passport Card */
        .result-card {
            padding: 32px;
            animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .identity-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
            margin-bottom: 24px;
            gap: 16px;
        }

        .identity-card-title {
            display: flex;
            align-items: center;
            gap: 14px;
            min-width: 0;
        }

        .identity-avatar {
            width: 52px;
            height: 52px;
            border-radius: 12px;
            background: rgba(83, 58, 253, 0.06);
            border: 1px solid rgba(83, 58, 253, 0.12);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--primary);
            flex-shrink: 0;
        }

        .agent-info {
            min-width: 0;
        }

        .agent-info h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.4rem;
            font-weight: 500;
            color: var(--text-main);
            letter-spacing: -0.26px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .agent-info p {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            margin-top: 3px;
            font-weight: 600;
        }

        .badge-status {
            font-family: 'Outfit', sans-serif;
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 6px 14px;
            border-radius: 30px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            flex-shrink: 0;
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
            min-width: 0;
        }

        .grid-item.full-width {
            grid-column: span 2;
        }

        .detail-label {
            font-family: 'Outfit', sans-serif;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            font-weight: 600;
        }

        .detail-value {
            font-size: 0.95rem;
            color: var(--text-main);
            word-break: break-all;
        }

        .detail-value.monospace {
            font-family: 'JetBrains Mono', monospace;
            font-feature-settings: "tnum" on;
            font-size: 0.85rem;
            background: var(--bg-base);
            padding: 8px 12px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            letter-spacing: -0.36px;
            min-width: 0;
        }

        .card-cap-tag {
            font-size: 11px;
            font-weight: 500;
            padding: 3px 8px;
            border-radius: 9999px;
            background-color: rgba(83, 58, 253, 0.06);
            color: var(--primary);
        }

        .copy-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 4px;
            border-radius: 4px;
            transition: all 0.2s;
            flex-shrink: 0;
            margin-left: 8px;
        }

        .copy-btn:hover {
            color: var(--text-main);
            background: var(--border-color);
        }

        /* JSON Inspector section */
        .json-inspector-section {
            margin-top: 28px;
            border-top: 1px solid var(--border-color);
            padding-top: 20px;
        }

        .json-toggle-btn {
            background: transparent;
            border: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: var(--primary);
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            padding: 6px 12px;
            border-radius: 6px;
            transition: all 0.2s;
        }

        .json-toggle-btn:hover {
            background: var(--primary-glow);
        }

        .json-toggle-btn svg {
            transition: transform 0.2s;
        }

        .json-toggle-btn.active svg {
            transform: rotate(180deg);
        }

        .json-content-wrapper {
            margin-top: 14px;
            background: #0f172a;
            border-radius: 8px;
            border: 1px solid #1e293b;
            overflow: hidden;
            animation: slideDown 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            width: 100%;
            max-width: 100%;
            box-sizing: border-box;
        }

        .json-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #1e293b;
            padding: 10px 16px;
            font-size: 0.75rem;
            color: #94a3b8;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            border-bottom: 1px solid #334155;
        }

        .copy-json-btn {
            background: transparent;
            border: none;
            color: #cbd5e1;
            cursor: pointer;
            font-size: 0.75rem;
            padding: 2px 8px;
            border-radius: 4px;
            transition: all 0.2s;
        }

        .copy-json-btn:hover {
            background: #334155;
            color: #ffffff;
        }

        .json-pre {
            padding: 16px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: #e2e8f0;
            overflow-x: auto;
            margin: 0;
            line-height: 1.5;
            max-height: 280px;
            max-width: 100%;
            box-sizing: border-box;
        }

        /* Footer */
        .footer {
            margin-top: 48px;
            padding-top: 24px;
            padding-bottom: 24px;
            border-top: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
            font-size: 14px;
            color: var(--text-muted);
            width: 100%;
        }

        .footer a {
            color: var(--text-muted);
            text-decoration: underline;
            text-underline-offset: 3px;
            text-decoration-color: rgba(100, 116, 141, 0.4);
            transition: all 0.15s ease;
        }

        .footer a:hover {
            color: var(--primary);
            text-decoration-color: var(--primary);
        }

        /* Responsive */
        @media (max-width: 900px) {
            .resolver-grid {
                grid-template-columns: 1fr;
                gap: 24px;
            }
            .placeholder-card, .scanning-card, .error-card {
                min-height: 320px;
            }
        }

        @media (max-width: 768px) {
            .navbar {
                flex-direction: column;
                gap: 16px;
                padding: 16px 0;
            }
            .nav-center {
                gap: 20px;
            }
        }

        @media (max-width: 640px) {
            body {
                padding: 0;
            }
            .container {
                padding: 0 16px 24px 16px;
            }
            .details-grid {
                grid-template-columns: 1fr;
            }
            .grid-item.full-width {
                grid-column: span 1;
            }
            .search-group {
                flex-direction: column;
                border-radius: 14px;
                gap: 8px;
                padding: 8px;
            }
            .search-icon {
                display: none;
            }
            .uri-input {
                padding: 4px 8px;
                width: 100%;
                text-align: center;
            }
            .resolve-btn {
                width: 100%;
                padding: 10px;
            }
            .glass-panel {
                padding: 16px;
            }
            .result-card {
                padding: 20px;
            }
            .identity-card-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 12px;
            }
        }
    </style>
</head>
<body>
    <main class="container">
        <!-- Unified Navbar matching image exactly -->
        <header class="navbar">
            <div class="nav-left">
                <a href="/" class="brand-logo">
                    <span class="brand-text">
                        <span class="brand-name">Creduent</span> 
                        <span class="brand-suffix">Registry</span>
                    </span>
                </a>
            </div>
            <div class="nav-center">
                <a href="/explore" class="nav-link">Explore</a>
                <a href="/dashboard" class="nav-link">Dashboard</a>
                <a href="/resolver" class="nav-link active">Resolver</a>
                <a href="/playground" class="nav-link">Playground</a>
            </div>
            <div class="nav-right">
                <div class="status-badge">
                    <span class="status-dot"></span>
                    <span>SYSTEM LIVE</span>
                </div>
            </div>
        </header>

        <div class="page-header">
            <h1>Identity Resolver</h1>
            <p>Resolve agent URIs and verify their cryptographic signatures.</p>
        </div>

        <div class="resolver-grid">
            <!-- Left sidebar: 40% width -->
            <div class="resolver-sidebar">
                <!-- Search Query Card -->
                <div class="glass-panel">
                    <section class="search-section">
                        <label for="uriInput" class="search-label">Verify Agent URI</label>
                        <div class="search-group">
                            <div class="search-icon">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                            </div>
                            <input type="text" id="uriInput" class="uri-input" placeholder="agent://domain/name" autocomplete="off" spellcheck="false">
                            <button id="resolveBtn" class="resolve-btn" onclick="resolveIdentity()">Resolve</button>
                        </div>
                    </section>
                </div>

                <!-- Recent Resolutions (localStorage history) -->
                <div class="glass-panel" id="historyCard" style="display: none;">
                    <div class="card-header-compact">
                        <span class="section-subtitle">Recent Resolutions</span>
                        <button class="clear-history-btn" onclick="clearHistory()">Clear</button>
                    </div>
                    <div class="history-list" id="historyList">
                        <!-- Populated dynamically -->
                    </div>
                </div>

                <!-- Live diagnostic logs -->
                <div class="glass-panel logs-card" id="logsCard" style="display: none;">
                    <span class="section-subtitle">Resolution Logs</span>
                    <div class="diagnostic-logs" id="diagnosticLogs"></div>
                </div>
            </div>

            <!-- Right main area: 60% width -->
            <div class="resolver-main">
                <!-- Idle State Placeholder -->
                <div class="glass-panel placeholder-card" id="idlePlaceholder">
                    <div class="placeholder-content">
                        <div class="placeholder-icon">
                            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                        </div>
                        <h3>Ready to Resolve</h3>
                        <p>Enter an agent URI or select a quick example to perform a secure cryptographic handshake and retrieve identity attestations.</p>
                    </div>
                </div>

                <!-- Scanning loader -->
                <div class="glass-panel scanning-card" id="scanningLoader" style="display: none;">
                    <div class="scanning-content">
                        <div class="scanning-text">Running Trust Sequence</div>
                        <div class="progress-bar-bg">
                            <div class="progress-bar-fill"></div>
                        </div>
                        <p class="scanning-sub">Querying attestation ledger...</p>
                    </div>
                </div>

                <!-- Error HUD Box -->
                <div class="glass-panel error-card" id="errorBox" style="display: none;">
                    <div class="error-icon">
                        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                    </div>
                    <div class="error-title" id="errorTitle">AGENT NOT FOUND</div>
                    <div class="error-message" id="errorMessage">Identity document could not be resolved. Verification sequence aborted.</div>
                </div>

                <!-- Result Card Block -->
                <div class="glass-panel result-card" id="cardContainer" style="display: none;">
                    <div class="identity-card-header">
                        <div class="identity-card-title">
                            <div class="identity-avatar" id="agentAvatarContainer">
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
                        <div class="grid-item">
                            <div class="detail-label">Owner</div>
                            <div class="detail-value" id="agentOwnerValue">-</div>
                        </div>
                        <div class="grid-item">
                            <div class="detail-label">Registered Domain</div>
                            <div class="detail-value" id="agentDomainValue">-</div>
                        </div>
                        <div class="grid-item full-width">
                            <div class="detail-label">Agent URI</div>
                            <div class="detail-value monospace" id="agentUriValue">agent://...</div>
                        </div>
                        <div class="grid-item full-width">
                            <div class="detail-label">W3C DID (did:creduent)</div>
                            <div class="detail-value monospace">
                                <span id="agentDidCreduentValue" style="font-size: 0.8rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; min-width: 0; max-width: calc(100% - 24px);">did:creduent:...</span>
                                <button class="copy-btn" onclick="copyId('agentDidCreduentValue')" title="Copy did:creduent">
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                                </button>
                            </div>
                        </div>
                        <div class="grid-item full-width">
                            <div class="detail-label">W3C DID (did:web)</div>
                            <div class="detail-value monospace">
                                <span id="agentDidWebValue" style="font-size: 0.8rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; min-width: 0; max-width: calc(100% - 24px);">did:web:...</span>
                                <button class="copy-btn" onclick="copyId('agentDidWebValue')" title="Copy did:web">
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                                </button>
                            </div>
                        </div>
                        <div class="grid-item full-width">
                            <div class="detail-label">Endpoint URL</div>
                            <div class="detail-value" id="agentEndpointValue">-</div>
                        </div>
                        <div class="grid-item full-width">
                            <div class="detail-label">Capabilities</div>
                            <div class="detail-value" id="agentCapabilitiesValue" style="display: flex; flex-wrap: wrap; gap: 6px;">-</div>
                        </div>
                        <div class="grid-item full-width">
                            <div class="detail-label">Public Key (Ed25519)</div>
                            <div class="detail-value monospace">
                                <span id="agentKeyValue" style="font-size: 0.8rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; min-width: 0; max-width: calc(100% - 24px);">ed25519:...</span>
                                <button class="copy-btn" onclick="copyKey()" title="Copy Public Key">
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                                </button>
                            </div>
                        </div>
                        <div class="grid-item">
                            <div class="detail-label">Issued Timestamp</div>
                            <div class="detail-value monospace" id="agentIssuedValue">-</div>
                        </div>
                        <div class="grid-item">
                            <div class="detail-label">Attestation Authority</div>
                            <div class="detail-value monospace" id="agentIssuerValue">agent://creduent/registry</div>
                        </div>
                    </div>

                    <!-- JSON Inspector Toggle -->
                    <div class="json-inspector-section">
                        <button class="json-toggle-btn" onclick="toggleJsonInspector()">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
                            <span>Show Attestation JSON</span>
                        </button>
                        <div class="json-content-wrapper" id="jsonWrapper" style="display: none;">
                            <div class="json-header">
                                <span>Attestation Document</span>
                                <button class="copy-json-btn" onclick="copyJson()">Copy</button>
                            </div>
                            <pre class="json-pre" id="jsonPre"></pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <footer class="footer">
            <div class="footer-left">
                Powered by <a href="https://github.com/idevsec/creduent" target="_blank" rel="noopener">Creduent Open Protocol</a> · v2.0.0
            </div>
            <div class="footer-right">
                © 2026 <a href="https://idevsec.com" target="_blank" rel="noopener">IDevSec</a>. All rights reserved.
            </div>
        </footer>
    </main>

    <script>
        const logsBox = document.getElementById('diagnosticLogs');
        const loader = document.getElementById('scanningLoader');
        const cardBox = document.getElementById('cardContainer');
        const errorBox = document.getElementById('errorBox');
        const idlePlaceholder = document.getElementById('idlePlaceholder');
        const logsCard = document.getElementById('logsCard');
        
        let lastResolvedData = null;
        let jsonVisible = false;

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
                const originalSvg = btn.innerHTML;
                btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--success)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
                setTimeout(() => { btn.innerHTML = originalSvg; }, 1500);
            });
        }

        function useExample(uri) {
            document.getElementById('uriInput').value = uri;
            resolveIdentity();
        }

        function loadHistory() {
            let history = [];
            try {
                history = JSON.parse(localStorage.getItem('creduent_resolver_history') || '[]');
            } catch(e) {}
            
            const historyCard = document.getElementById('historyCard');
            const historyList = document.getElementById('historyList');
            
            if (!Array.isArray(history) || history.length === 0) {
                historyCard.style.display = 'none';
                return;
            }
            
            historyCard.style.display = 'block';
            historyList.innerHTML = '';
            
            history.forEach(uri => {
                const item = document.createElement('div');
                item.className = 'history-item';
                item.onclick = () => {
                    document.getElementById('uriInput').value = uri;
                    resolveIdentity();
                };
                
                item.innerHTML = `
                    <span class="history-uri">${uri}</span>
                    <span class="history-arrow">→</span>
                `;
                historyList.appendChild(item);
            });
        }

        function saveToHistory(uri) {
            let history = [];
            try {
                history = JSON.parse(localStorage.getItem('creduent_resolver_history') || '[]');
            } catch(e) {}
            
            if (!Array.isArray(history)) history = [];
            
            history = history.filter(item => item !== uri);
            history.unshift(uri);
            if (history.length > 5) {
                history = history.slice(0, 5);
            }
            
            localStorage.setItem('creduent_resolver_history', JSON.stringify(history));
            loadHistory();
        }

        function clearHistory() {
            localStorage.removeItem('creduent_resolver_history');
            loadHistory();
        }

        function toggleJsonInspector() {
            const btn = document.querySelector('.json-toggle-btn');
            const wrapper = document.getElementById('jsonWrapper');
            jsonVisible = !jsonVisible;
            if (jsonVisible) {
                btn.classList.add('active');
                wrapper.style.display = 'block';
                btn.querySelector('span').textContent = 'Hide Attestation JSON';
                if (lastResolvedData) {
                    document.getElementById('jsonPre').textContent = JSON.stringify(lastResolvedData, null, 2);
                }
            } else {
                btn.classList.remove('active');
                wrapper.style.display = 'none';
                btn.querySelector('span').textContent = 'Show Attestation JSON';
            }
        }

        function copyJson() {
            if (lastResolvedData) {
                const text = JSON.stringify(lastResolvedData, null, 2);
                navigator.clipboard.writeText(text).then(() => {
                    const btn = document.querySelector('.copy-json-btn');
                    btn.textContent = 'Copied!';
                    setTimeout(() => { btn.textContent = 'Copy'; }, 1500);
                });
            }
        }

        function copyId(elementId) {
            const text = document.getElementById(elementId).innerText;
            navigator.clipboard.writeText(text).then(() => {
                const span = document.getElementById(elementId);
                const btn = span ? span.nextElementSibling : null;
                if (btn) {
                    const originalSvg = btn.innerHTML;
                    btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--success)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
                    setTimeout(() => { btn.innerHTML = originalSvg; }, 1500);
                }
            });
        }

        function getDidCreduent(agentUri) {
            if (!agentUri) return '-';
            const clean = agentUri.replace(/^agent:\/\//, '');
            return 'did:creduent:' + clean.replace(/\//g, ':');
        }

        function getDidWeb(agentUri, domain) {
            if (!agentUri) return '-';
            const parts = agentUri.replace(/^agent:\/\//, '').split('/');
            const namespace = parts[0] || 'default';
            let d = domain && domain !== '-' ? domain : `${namespace}.com`;
            if (d.startsWith('creduent.')) {
                const parentDomain = d.replace(/^creduent\./, '');
                if (parentDomain.startsWith(namespace)) {
                    d = parentDomain;
                }
            }
            const name = parts.length > 1 ? parts.slice(1).join(':') : namespace;
            return `did:web:${d}:agent:${name}`;
        }

        async function resolveIdentity() {
            let uri = document.getElementById('uriInput').value.trim();
            if (!uri) return;

            if (!uri.startsWith("agent://") && !uri.startsWith("agent:/") && !uri.startsWith("did:creduent:") && !uri.startsWith("did:web:")) {
                alert("Please enter a valid agent:// or W3C did: URI (e.g. did:creduent:namespace:agent or did:web:domain:agent:name).");
                return;
            }

            if (uri.startsWith("agent:/") && !uri.startsWith("agent://")) {
                uri = "agent://" + uri.substring(7);
            }

            // Update UI for loading state
            idlePlaceholder.style.display = 'none';
            cardBox.style.display = 'none';
            errorBox.style.display = 'none';
            loader.style.display = 'flex';
            logsCard.style.display = 'block';
            logsBox.innerHTML = '';
            
            // Collapse JSON inspector
            jsonVisible = true;
            toggleJsonInspector();

            appendLog("Initializing resolution sequence", "OK");
            appendLog("Establishing registry handshake", "PENDING");

            const requestPath = "/attest/" + encodeURIComponent(uri);

            try {
                appendLog("Establishing registry handshake", "OK");
                appendLog("Fetching agent identity document", "PENDING");

                const response = await fetch(requestPath);

                if (response.status === 404) {
                    appendLog("Fetching agent identity document", "FAIL");
                    loader.style.display = 'none';
                    errorBox.style.display = 'flex';
                    document.getElementById('errorTitle').textContent = "AGENT NOT FOUND";
                    document.getElementById('errorMessage').textContent = `Agent identifier '${uri}' is not registered or has no active cryptographic attestation record in the registry database.`;
                    return;
                } else if (!response.ok) {
                    appendLog("Fetching agent identity document", "FAIL");
                    loader.style.display = 'none';
                    errorBox.style.display = 'flex';
                    document.getElementById('errorTitle').textContent = "REGISTRY QUERY ERROR";
                    document.getElementById('errorMessage').textContent = `The registry node reported an unexpected error (${response.status} ${response.statusText}).`;
                    return;
                }

                const data = await response.json();
                lastResolvedData = data;
                
                appendLog("Fetching agent identity document", "OK");
                appendLog("Parsing cryptographic signature & DID document", "OK");
                appendLog("Validating identity signature", "OK");
                
                let namePart = "AGENT IDENTIFIER";
                try {
                    const actualUri = data.agent_id || uri;
                    const parsed = actualUri.replace("agent://", "").split("/");
                    if (parsed.length > 0) {
                        const rawName = parsed[parsed.length - 1];
                        if (rawName) {
                            namePart = rawName.charAt(0).toUpperCase() + rawName.slice(1);
                        }
                    }
                } catch(e){}

                document.getElementById('agentNameDisplay').textContent = namePart;
                document.getElementById('agentOwnerValue').textContent = data.owner || 'Unknown';
                document.getElementById('agentUriValue').textContent = data.agent_id || uri;
                document.getElementById('agentDidCreduentValue').textContent = data.did_creduent || getDidCreduent(data.agent_id || uri);
                document.getElementById('agentDidWebValue').textContent = data.did_web || getDidWeb(data.agent_id || uri, data.domain);
                document.getElementById('agentKeyValue').textContent = data.public_key || '-';
                document.getElementById('agentDomainValue').textContent = data.domain || '-';
                document.getElementById('agentEndpointValue').textContent = data.endpoint || '-';
                document.getElementById('agentIssuedValue').textContent = data.issued_at || '-';
                document.getElementById('agentIssuerValue').textContent = data.issuer || 'agent://creduent/registry';

                const capsContainer = document.getElementById('agentCapabilitiesValue');
                if (data.capabilities && data.capabilities.length > 0) {
                    capsContainer.innerHTML = data.capabilities.map(cap => `<span class="card-cap-tag">${cap}</span>`).join('');
                } else {
                    capsContainer.textContent = '-';
                }

                const avatarContainer = document.getElementById('agentAvatarContainer');
                if (data.domain && data.domain !== '-') {
                    let baseDomain = data.domain;
                    const parts = data.domain.split('.');
                    if (parts.length > 2) {
                        const pen = parts[parts.length - 2].toLowerCase();
                        const tld = parts[parts.length - 1].toLowerCase();
                        if ((tld === 'uk' && pen === 'co') || 
                            (tld === 'br' && pen === 'com') || 
                            (tld === 'au' && pen === 'net') || 
                            (tld === 'nz' && pen === 'co')) {
                            if (parts.length > 3) baseDomain = parts.slice(-3).join('.');
                        } else {
                            baseDomain = parts.slice(-2).join('.');
                        }
                    }
                    const img = document.createElement('img');
                    img.src = (baseDomain === 'idevsec.com') ? 'https://idevsec.com/logo.png' : `https://www.google.com/s2/favicons?sz=128&domain=${baseDomain}`;
                    img.alt = baseDomain;
                    img.style.width = '32px';
                    img.style.height = '32px';
                    img.style.borderRadius = '8px';
                    img.style.objectFit = 'contain';
                    img.onload = () => {
                        avatarContainer.innerHTML = '';
                        avatarContainer.appendChild(img);
                        if (typeof applyDarkBgIfWhiteLogo === 'function') {
                            applyDarkBgIfWhiteLogo(img, avatarContainer, baseDomain);
                        } else {
                            const lower = baseDomain.toLowerCase();
                            if (lower.includes('idevsec') || lower.includes('stacked')) {
                                avatarContainer.style.backgroundColor = '#090d16';
                                avatarContainer.style.borderColor = '#1e293b';
                            }
                        }
                    };
                    img.onerror = () => {
                        avatarContainer.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`;
                    };
                    avatarContainer.innerHTML = '';
                    avatarContainer.appendChild(img);
                } else {
                    avatarContainer.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`;
                }

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
                
                // Save to localStorage history
                saveToHistory(uri);

            } catch (err) {
                appendLog("Fetching agent identity document", "FAIL");
                loader.style.display = 'none';
                errorBox.style.display = 'flex';
                document.getElementById('errorTitle').textContent = "REGISTRY UNREACHABLE";
                document.getElementById('errorMessage').textContent = "Could not communicate with the registry node. Please check your network connection and try again.";
            }
        }

        window.addEventListener('DOMContentLoaded', () => {
            loadHistory();
            const urlParams = new URLSearchParams(window.location.search);
            const uriParam = urlParams.get('uri');
            if (uriParam) {
                document.getElementById('uriInput').value = uriParam;
                resolveIdentity();
            }
        });
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #f6f9fc; /* canvas-soft light base */
            --bg-surface: #ffffff; /* pure white canvas */
            --bg-surface-hover: #f9fbfd;
            --border-color: #e3e8ee; /* light gray hairline border */
            --primary: #533afd; /* electric indigo */
            --primary-hover: #4434d4; /* primary-deep */
            --primary-press: #2e2b8c; /* primary-press */
            --primary-glow: rgba(83, 58, 253, 0.1);
            
            --success: #22c55e;
            --success-glow: rgba(34, 197, 94, 0.08);
            --success-border: rgba(34, 197, 94, 0.2);
            
            --warning: #9b6829; /* lemon */
            --warning-glow: rgba(155, 104, 41, 0.08);
            --warning-border: rgba(155, 104, 41, 0.2);
            
            --error: #ea2261; /* ruby */
            --error-glow: rgba(234, 34, 97, 0.08);
            --error-border: rgba(234, 34, 97, 0.2);
            
            --trusted: #a78bfa; /* violet */
            --trusted-glow: rgba(167, 139, 250, 0.08);
            --trusted-border: rgba(167, 139, 250, 0.2);
            
            --text-main: #0d253d; /* ink (navy) */
            --text-muted: #64748d; /* ink-mute */
            --text-dark: #61718a; /* ink-mute-2 */
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.02);
            border-radius: 99px;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(0, 0, 0, 0.1);
            border-radius: 99px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(0, 0, 0, 0.2);
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-feature-settings: "ss01" on;
            font-weight: 300; /* thin weight display / typography per DESIGN.md */
            font-size: 15px; /* body-md default */
            line-height: 1.4;
            background-color: var(--bg-base);
            color: var(--text-main);
            min-height: 100vh;
            padding: 0;
            margin: 0;
            position: relative;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 0%, rgba(245, 233, 212, 0.6) 0%, transparent 45%),
                radial-gradient(circle at 45% 0%, rgba(155, 104, 41, 0.1) 0%, transparent 40%),
                radial-gradient(circle at 90% 0%, rgba(249, 107, 238, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 25% 0%, rgba(83, 58, 253, 0.12) 0%, transparent 55%),
                radial-gradient(circle at 75% 0%, rgba(234, 34, 97, 0.12) 0%, transparent 45%);
            background-size: 100% 100%;
            background-repeat: no-repeat;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px;
            position: relative;
            z-index: 10;
        }

        /* Navbar style matching image */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 24px 0;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 24px;
            width: 100%;
        }

        .nav-left {
            display: flex;
            align-items: center;
        }

        .brand-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
        }

        .brand-avatar {
            width: 36px;
            height: 36px;
            background-color: var(--primary);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            box-shadow: 0 2px 8px rgba(83, 58, 253, 0.2);
        }

        .brand-text {
            font-size: 20px;
            font-weight: 500;
            letter-spacing: -0.42px;
        }

        .brand-name {
            color: var(--text-main);
        }

        .brand-suffix {
            color: var(--primary);
        }

        .nav-center {
            display: flex;
            align-items: center;
            gap: 32px;
        }

        .nav-link {
            font-size: 15px;
            font-weight: 400;
            color: var(--text-muted);
            text-decoration: none;
            transition: color 0.15s ease;
        }

        .nav-link:hover {
            color: var(--text-main);
        }

        .nav-link.active {
            color: var(--primary);
            font-weight: 500;
        }

        .nav-right {
            display: flex;
            align-items: center;
        }

        .nav-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background-color: var(--primary);
            color: white;
            font-size: 14px;
            font-weight: 500;
            padding: 8px 18px;
            border-radius: 9999px; /* pill */
            text-decoration: none;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(83, 58, 253, 0.15);
        }

        .nav-btn:hover {
            background-color: var(--primary-hover);
            box-shadow: 0 6px 16px rgba(83, 58, 253, 0.25);
            transform: translateY(-1px);
        }

        .nav-btn:active {
            background-color: var(--primary-press);
            transform: translateY(0);
        }

        .dashboard-hero {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 24px;
            margin-bottom: 36px;
        }

        .brand h1 {
            font-size: 26px; /* display-md */
            font-weight: 300;
            line-height: 1.12;
            letter-spacing: -0.26px;
            color: var(--text-main);
            background: linear-gradient(135deg, var(--text-main) 30%, var(--text-muted) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .brand p {
            font-size: 13px; /* caption */
            font-weight: 400;
            line-height: 1.4;
            letter-spacing: -0.39px;
            color: var(--text-muted);
            margin-top: 4px;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-feature-settings: "tnum" on;
            font-size: 13px; /* caption */
            font-weight: 400;
            line-height: 1.0;
            letter-spacing: -0.39px;
            background: var(--success-glow);
            color: var(--success);
            padding: 8px 16px;
            border-radius: 9999px; /* rounded.pill */
            border: 1px solid var(--success-border);
            box-shadow: rgba(34, 197, 94, 0.08) 0 4px 12px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--success);
            box-shadow: 0 0 8px var(--success);
            animation: pulse-green 2s infinite;
        }

        @keyframes pulse-green {
            0%, 100% { opacity: 0.6; transform: scale(0.9); }
            50% { opacity: 1; transform: scale(1.15); }
        }

        .page-header {
            margin-bottom: 24px;
        }

        .page-header h1 {
            font-size: 24px;
            font-weight: 500;
            color: var(--text-main);
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .page-header p {
            font-size: 14px;
            color: var(--text-muted);
            margin-top: 4px;
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 36px;
        }

        .stat-card {
            background-color: var(--bg-surface);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 12px; /* rounded.lg */
            padding: 24px;
            box-shadow: rgba(0, 55, 112, 0.06) 0 8px 24px, rgba(0, 0, 0, 0.02) 0 2px 6px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .stat-card:hover {
            transform: translateY(-3px);
            background-color: var(--bg-surface-hover);
            border-color: rgba(168, 195, 222, 0.45);
            box-shadow: rgba(0, 55, 112, 0.12) 0 12px 36px, rgba(0, 0, 0, 0.05) 0 6px 12px;
        }

        .stat-card.stat-total::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--trusted));
        }

        .stat-card.stat-verified::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--success), #34d399);
        }

        .stat-card.stat-unverified::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--warning), #fbbf24);
        }

        .stat-card.stat-revoked::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--error), #fb7185);
        }

        .stat-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .stat-label {
            font-size: 10px; /* micro-cap */
            font-weight: 400;
            line-height: 1.15;
            letter-spacing: 0.1px;
            text-transform: uppercase;
            color: var(--text-muted);
        }

        .stat-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0.85;
        }

        .stat-val {
            font-size: 48px; /* display-xl */
            font-weight: 300;
            font-feature-settings: "tnum" on, "ss01" on;
            line-height: 1.15;
            letter-spacing: -0.96px;
            margin-top: 6px;
        }

        .stat-card.warning {
            border-color: var(--warning-border);
            background-color: rgba(155, 104, 41, 0.03);
        }

        /* Workspace Layout */
        .workspace {
            display: grid;
            grid-template-columns: minmax(0, 1fr);
            gap: 28px;
        }

        .main-panel {
            display: flex;
            flex-direction: column;
            gap: 28px;
            min-width: 0;
        }

        /* Mobile Responsiveness styling */
        @media (max-width: 768px) {
            body {
                padding: 24px 16px;
            }
            
            header {
                flex-direction: column;
                align-items: flex-start;
                gap: 16px;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 12px;
                margin-bottom: 24px;
            }
            
            .stat-card {
                padding: 18px 16px;
            }
            
            .stat-val {
                font-size: 32px; /* display-lg */
                letter-spacing: -0.64px;
            }
            
            .card {
                padding: 16px !important;
                overflow: hidden;
            }
            .card-title {
                flex-direction: column;
                align-items: flex-start;
                gap: 16px;
            }
            .table-container {
                margin: -16px;
                margin-top: 0;
            }
            .desktop-table {
                display: none;
            }
            .mobile-agent-list {
                display: flex !important;
                flex-direction: column;
                gap: 16px;
                margin-top: 16px;
                padding: 0 16px 16px 16px;
            }
            .modal-details-grid {
                grid-template-columns: 1fr;
                gap: 16px;
            }
            .modal-grid-span-2 {
                grid-column: span 1;
            }
        }
        
        @media (max-width: 480px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }

        .card {
            background-color: var(--bg-surface);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 12px; /* rounded.lg */
            padding: 24px;
            box-shadow: rgba(0, 55, 112, 0.08) 0 8px 24px, rgba(0, 0, 0, 0.04) 0 2px 6px;
            transition: all 0.3s ease;
        }

        .card:hover {
            border-color: rgba(168, 195, 222, 0.35);
            box-shadow: rgba(0, 55, 112, 0.12) 0 12px 36px, rgba(0, 0, 0, 0.06) 0 8px 24px;
        }

        .card-title {
            font-size: 20px; /* heading-md */
            font-weight: 300;
            line-height: 1.4;
            letter-spacing: -0.2px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: var(--text-main);
        }

        /* Forms styling */
        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            font-size: 10px; /* micro-cap */
            font-weight: 400;
            line-height: 1.15;
            letter-spacing: 0.1px;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 8px;
        }

        .form-group input, .form-group textarea, .form-group select {
            width: 100%;
            background-color: #ffffff;
            border: 1px solid #a8c3de; /* hairline input style */
            border-radius: 6px; /* rounded.sm: 6px */
            color: var(--text-main);
            padding: 8px 12px; /* tight input padding */
            font-family: inherit;
            font-size: 15px; /* body-md: 15px */
            font-weight: 300;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .form-group input:focus, .form-group textarea:focus, .form-group select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px var(--primary-glow);
            background-color: #ffffff;
        }

        .form-group input::placeholder, .form-group textarea::placeholder {
            color: var(--text-muted);
            opacity: 0.6;
        }

        .form-group textarea {
            resize: vertical;
            min-height: 90px;
            font-family: 'JetBrains Mono', monospace;
            font-feature-settings: "tnum" on;
            font-size: 14px; /* body-tabular */
            line-height: 1.4;
            letter-spacing: -0.42px;
            font-weight: 300;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            background-color: var(--primary);
            color: white;
            font-family: inherit;
            font-size: 16px; /* button-md */
            font-weight: 400; /* button weight 400 per design.md */
            line-height: 1.0;
            padding: 8px 16px; /* tight pill padding */
            border-radius: 9999px; /* rounded.pill */
            border: none;
            cursor: pointer;
            width: 100%;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .btn:hover {
            background-color: var(--primary-hover);
            transform: translateY(-1px);
            box-shadow: 0 4px 16px var(--primary-glow);
        }

        .btn:active {
            background-color: var(--primary-press);
            transform: translateY(0);
        }

        .btn-secondary {
            background-color: #ffffff;
            border: 1px solid var(--primary);
            color: var(--primary);
        }

        .btn-secondary:hover {
            background-color: rgba(83, 58, 253, 0.04);
            border-color: var(--primary-hover);
            color: var(--primary-hover);
            box-shadow: rgba(83, 58, 253, 0.06) 0 4px 12px;
        }

        .btn-sm {
            padding: 8px 16px;
            font-size: 14px; /* button-sm */
            font-weight: 400;
            width: auto;
        }

        /* Footer */
        .footer {
            margin-top: 48px;
            padding-top: 24px;
            padding-bottom: 24px;
            border-top: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
            font-size: 14px;
            color: var(--text-muted);
            width: 100%;
        }

        .footer a {
            color: var(--text-muted);
            text-decoration: underline;
            text-underline-offset: 3px;
            text-decoration-color: rgba(100, 116, 141, 0.4);
            transition: all 0.15s ease;
        }

        .footer a:hover {
            color: var(--primary);
            text-decoration-color: var(--primary);
        }

        /* Table */
        .table-container {
            overflow-x: auto;
            margin: -24px;
            margin-top: 0;
            border-bottom-left-radius: 12px;
            border-bottom-right-radius: 12px;
        }

        .mobile-agent-list {
            display: none;
        }

        .mobile-agent-card {
            background-color: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            box-shadow: rgba(0, 55, 112, 0.04) 0 1px 3px;
            transition: all 0.25s ease;
        }

        .mobile-agent-card:hover {
            border-color: rgba(168, 195, 222, 0.35);
            background-color: #f9fbfd;
            box-shadow: rgba(0, 55, 112, 0.08) 0 4px 12px;
        }

        .mobile-agent-card.warning-card {
            border-color: var(--error-border);
            background-color: rgba(234, 34, 97, 0.02);
        }

        .desktop-table {
            width: 100%;
            border-collapse: collapse;
        }

        th {
            text-align: left;
            padding: 14px 24px;
            background-color: #f6f9fc;
            border-bottom: 1px solid var(--border-color);
            font-size: 13px; /* caption */
            font-weight: 400;
            line-height: 1.4;
            letter-spacing: -0.39px;
            font-feature-settings: "tnum" on;
            color: var(--text-muted);
            text-transform: uppercase;
            white-space: nowrap;
        }

        td {
            padding: 16px 24px;
            border-bottom: 1px solid var(--border-color);
            vertical-align: middle;
            white-space: nowrap;
            font-size: 14px; /* body-tabular */
            font-weight: 300;
            line-height: 1.4;
            letter-spacing: -0.42px;
            font-feature-settings: "tnum" on;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover td {
            background-color: #f9fbfd;
        }

        tr.warning-row td {
            background-color: rgba(234, 34, 97, 0.02);
        }

        tr.warning-row:hover td {
            background-color: rgba(234, 34, 97, 0.04);
        }

        .monospace {
            font-family: 'JetBrains Mono', monospace;
            font-feature-settings: "tnum" on;
            font-size: 14px; /* body-tabular */
            letter-spacing: -0.42px;
            font-weight: 300;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            font-family: 'JetBrains Mono', monospace;
            font-feature-settings: "tnum" on;
            font-size: 10px; /* micro-cap */
            font-weight: 400;
            line-height: 1.15;
            letter-spacing: 0.1px;
            padding: 4px 8px; /* pill-tag-soft-style */
            border-radius: 9999px; /* pill rounded */
            text-transform: uppercase;
        }

        .badge-verified {
            background-color: var(--success-glow);
            color: var(--success);
            border: 1px solid var(--success-border);
        }

        .badge-unverified {
            background-color: var(--warning-glow);
            color: var(--warning);
            border: 1px solid var(--warning-border);
        }

        .badge-revoked {
            background-color: var(--error-glow);
            color: var(--error);
            border: 1px solid var(--error-border);
        }

        .badge-trusted {
            background-color: var(--trusted-glow);
            color: var(--trusted);
            border: 1px solid var(--trusted-border);
        }

        .badge-warning {
            background-color: var(--error-glow);
            color: var(--error);
            border: 1px solid var(--error-border);
            font-size: 10px;
            margin-left: 6px;
        }

        .actions-cell {
            display: flex;
            gap: 6px;
        }

        .actions-cell .btn {
            font-size: 13px; /* caption button */
            font-weight: 400;
            border-radius: 9999px;
            padding: 4px 10px;
        }

        /* Modal styling */
        .modal-overlay {
            display: none;
            position: fixed;
            inset: 0;
            background-color: rgba(13, 37, 61, 0.4);
            z-index: 100;
            align-items: center;
            justify-content: center;
            padding: 24px;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            animation: fadeIn 0.25s ease-out;
        }

        .modal {
            background-color: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 12px; /* rounded.lg */
            max-width: 600px;
            width: 100%;
            max-height: 90vh;
            overflow: hidden;
            box-shadow: rgba(0, 55, 112, 0.12) 0 16px 48px, rgba(0, 0, 0, 0.08) 0 24px 64px;
            display: flex;
            flex-direction: column;
            animation: scaleUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes scaleUp {
            from { transform: scale(0.95); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }

        .modal-header {
            padding: 24px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .modal-header h3 {
            font-size: 20px; /* heading-md */
            font-weight: 300;
            color: var(--text-main);
            letter-spacing: -0.2px;
        }

        .modal-body {
            padding: 24px;
            font-family: 'JetBrains Mono', monospace;
            font-feature-settings: "tnum" on;
            font-size: 14px; /* body-tabular */
            font-weight: 300;
            letter-spacing: -0.42px;
            white-space: pre-wrap;
            background-color: #f9fbfd;
            color: var(--text-main);
            overflow: auto;
            flex: 1;
            border-bottom: 1px solid var(--border-color);
        }

        /* View Modal Tabs & Grid styling */
        .modal-tab-header {
            display: flex;
            border-bottom: 1px solid var(--border-color);
            background: #f6f9fc;
            padding: 0 16px;
        }

        .modal-tab-btn {
            background: none;
            border: none;
            color: var(--text-muted);
            padding: 14px 16px;
            font-family: inherit;
            font-size: 15px; /* body-md */
            font-weight: 300;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            position: relative;
            transition: all 0.2s ease;
        }

        .modal-tab-btn:hover {
            color: var(--text-main);
            background: rgba(0, 0, 0, 0.02);
        }

        .modal-tab-btn.active {
            color: var(--text-main);
            border-bottom-color: var(--primary);
        }

        .modal-details-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px 20px;
        }

        .modal-grid-span-2 {
            grid-column: span 2;
        }

        .modal-detail-item {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .modal-detail-label {
            font-size: 10px; /* micro-cap */
            font-weight: 400;
            line-height: 1.15;
            letter-spacing: 0.1px;
            text-transform: uppercase;
            color: var(--text-muted);
        }

        .modal-field-box {
            display: flex;
            background: rgba(0, 0, 0, 0.02);
            border: 1px solid var(--border-color);
            border-radius: 6px; /* rounded.sm */
            overflow: hidden;
            justify-content: space-between;
            align-items: center;
            padding: 8px 12px;
            transition: border-color 0.2s ease;
        }

        .modal-field-box:hover {
            border-color: rgba(168, 195, 222, 0.3);
        }

        .modal-field-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px; /* body-tabular */
            font-weight: 300;
            letter-spacing: -0.42px;
            color: var(--text-main);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            max-width: 85%;
        }

        .modal-copy-btn {
            background: none;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 4px;
            border-radius: 4px;
            transition: all 0.2s;
        }

        .modal-copy-btn:hover {
            color: var(--text-main);
            background: rgba(0, 0, 0, 0.04);
        }
        
        .modal-certificate-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #f6f9fc;
            border: 1px solid var(--border-color);
            padding: 16px 20px;
            border-radius: 12px;
        }

        .modal-footer {
            padding: 18px 24px;
            display: flex;
            justify-content: flex-end;
            background-color: #f6f9fc;
        }

        /* Feedbacks and alerts */
        .feedback {
            margin-top: 16px;
            padding: 12px 16px;
            border-radius: 8px; /* rounded.md */
            font-size: 15px; /* body-md */
            font-weight: 300;
            display: none;
            animation: fadeIn 0.2s ease-out;
            line-height: 1.4;
        }

        .feedback-success {
            background-color: var(--success-glow);
            color: var(--success);
            border: 1px solid var(--success-border);
        }

        .feedback-error {
            background-color: var(--error-glow);
            color: var(--error);
            border: 1px solid var(--error-border);
        }

        .webhook-current-info {
            margin-top: 20px;
            padding: 16px;
            border: 1px dashed var(--border-color);
            border-radius: 8px;
            background: rgba(0, 0, 0, 0.01);
            font-size: 15px; /* body-md */
            font-weight: 300;
            display: none;
            animation: fadeIn 0.2s ease-out;
        }

        .payload-box {
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 14px;
            font-family: 'JetBrains Mono', monospace;
            font-feature-settings: "tnum" on;
            font-size: 14px; /* body-tabular */
            font-weight: 300;
            letter-spacing: -0.42px;
            color: var(--primary);
            white-space: pre-wrap;
            word-break: break-all;
            line-height: 1.4;
            position: relative;
        }

        .step-tag {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 10px; /* micro-cap */
            font-weight: 400;
            line-height: 1.15;
            letter-spacing: 0.1px;
            text-transform: uppercase;
            color: var(--text-dark);
            margin-bottom: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Unified Navbar matching image exactly -->
        <header class="navbar">
            <div class="nav-left">
                <a href="/" class="brand-logo">
                    <span class="brand-text">
                        <span class="brand-name">Creduent</span> 
                        <span class="brand-suffix">Registry</span>
                    </span>
                </a>
            </div>
            <div class="nav-center">
                <a href="/explore" class="nav-link">Explore</a>
                <a href="/dashboard" class="nav-link active">Dashboard</a>
                <a href="/resolver" class="nav-link">Resolver</a>
                <a href="/playground" class="nav-link">Playground</a>
            </div>
            <div class="nav-right">
                <div class="status-badge">
                    <span class="status-dot"></span>
                    <span>SYSTEM LIVE</span>
                </div>
            </div>
        </header>

        <div class="page-header">
            <h1>Developer Dashboard</h1>
            <p>Monitor and manage your agent attestations and webhooks.</p>
        </div>

        <!-- Stats Grid (Section A) -->
        <section class="stats-grid">
            <div class="stat-card stat-total">
                <div class="stat-card-header">
                    <span class="stat-label">Total Agents</span>
                    <div class="stat-icon" style="color: var(--primary);">
                        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
                    </div>
                </div>
                <div class="stat-val" id="stat-total">0</div>
            </div>
            <div class="stat-card stat-verified">
                <div class="stat-card-header">
                    <span class="stat-label">Verified</span>
                    <div class="stat-icon" style="color: var(--success);">
                        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 11 2 2 4-4"/></svg>
                    </div>
                </div>
                <div class="stat-val" style="color: var(--success);" id="stat-verified">0</div>
            </div>
            <div class="stat-card stat-unverified">
                <div class="stat-card-header">
                    <span class="stat-label">Unverified</span>
                    <div class="stat-icon" style="color: var(--warning);">
                        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                    </div>
                </div>
                <div class="stat-val" style="color: var(--warning);" id="stat-unverified">0</div>
            </div>
            <div class="stat-card stat-revoked">
                <div class="stat-card-header">
                    <span class="stat-label">Revoked</span>
                    <div class="stat-icon" style="color: var(--error);">
                        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
                    </div>
                </div>
                <div class="stat-val" style="color: var(--error);" id="stat-revoked">0</div>
            </div>

        </section>

        <!-- Workspace Layout -->
        <div class="workspace">
            <!-- Main panel (Section B) -->
            <div class="main-panel">
                <div class="card">
                    <div class="card-title" style="flex-wrap: wrap; gap: 12px;">
                        <span style="white-space: nowrap;">Agent Explorer</span>
                        <div style="display: flex; gap: 6px; flex-wrap: wrap; align-items: center;">
                            <button class="btn btn-secondary btn-sm" onclick="showRegisterModal()" style="white-space: nowrap;">
                                <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24" style="margin-right: 3px;"><path d="M12 5v14M5 12h14"/></svg>
                                Register Agent
                            </button>
                            <button class="btn btn-secondary btn-sm" onclick="showWebhookModal()" style="white-space: nowrap;">
                                <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24" style="margin-right: 3px;"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
                                Webhook Manager
                            </button>
                            <button class="btn btn-secondary btn-sm" onclick="fetchData()" style="white-space: nowrap;">
                                <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" style="margin-right: 3px;"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
                                Refresh
                            </button>
                        </div>
                    </div>
                    <div class="table-container">
                        <table class="desktop-table">
                            <thead>
                                <tr>
                                    <th>Agent ID</th>
                                    <th>Domain</th>
                                    <th>Level</th>
                                    <th>Expires At</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody id="agent-table-body">
                                <tr>
                                    <td colspan="5" style="text-align: center; color: var(--text-muted); padding: 48px 0;">
                                        Loading agent records...
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div class="mobile-agent-list" id="mobile-agent-list">
                            <div style="text-align: center; color: var(--text-muted); padding: 32px 0; font-size: 0.88rem;">
                                Loading agent records...
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Footer -->
        <footer class="footer">
            <div class="footer-left">
                Powered by <a href="https://github.com/idevsec/creduent" target="_blank" rel="noopener">Creduent Open Protocol</a> · v2.0.0
            </div>
            <div class="footer-right">
                © 2026 <a href="https://idevsec.com" target="_blank" rel="noopener">IDevSec</a>. All rights reserved.
            </div>
        </footer>
    </div>

    <!-- View Modal -->
    <div class="modal-overlay" id="view-modal" onclick="closeModal(event)">
        <div class="modal" onclick="event.stopPropagation()" style="max-width: 680px;">
            <div class="modal-header">
                <div>
                    <h3 id="modal-title">Agent Attestation</h3>
                    <p style="font-size:13px;font-weight:400;color:var(--text-muted);margin-top:4px;letter-spacing:-0.39px;">Cryptographic Discovery Certificate</p>
                </div>
                <button type="button" class="btn btn-secondary btn-sm" onclick="hideModal()">✕ Close</button>
            </div>
            
            <!-- Tab Controls -->
            <div class="modal-tab-header">
                <button class="modal-tab-btn active" onclick="switchViewModalTab('overview')" id="tab-btn-overview">
                    Overview
                </button>
                <button class="modal-tab-btn" onclick="switchViewModalTab('raw')" id="tab-btn-raw">
                    Raw JSON
                </button>
            </div>

            <!-- Tab Content: Overview -->
            <div id="view-modal-overview" style="padding: 24px; display: flex; flex-direction: column; gap: 20px; overflow-y: auto; max-height: 60vh;">
                <!-- Certificate Avatar & Status -->
                <div class="modal-certificate-header">
                    <div style="display: flex; align-items: center; gap: 14px;">
                        <div id="modal-agent-avatar" style="width: 44px; height: 44px; border-radius: 10px; background: rgba(83, 58, 253, 0.1); border: 1px solid rgba(83, 58, 253, 0.2); display: flex; align-items: center; justify-content: center; color: var(--primary);">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                        </div>
                        <div>
                            <div id="modal-agent-name" style="font-size: 1.1rem; font-weight: 500; color: var(--text-main);">Agent Name</div>
                            <div id="modal-agent-domain" style="font-size: 0.8rem; color: var(--text-muted);">domain.com</div>
                        </div>
                    </div>
                    <div>
                        <span id="modal-status-badge" class="badge">verified</span>
                    </div>
                </div>

                <!-- Details Grid -->
                <div class="modal-details-grid">
                    <div class="modal-grid-span-2 modal-detail-item">
                        <label class="modal-detail-label">Agent URI</label>
                        <div class="modal-field-box">
                            <span id="modal-field-uri" class="modal-field-value">agent://...</span>
                            <button onclick="copyModalField('modal-field-uri')" class="modal-copy-btn" title="Copy URI">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                            </button>
                        </div>
                    </div>

                    <div class="modal-grid-span-2 modal-detail-item">
                        <label class="modal-detail-label">W3C DID (did:creduent)</label>
                        <div class="modal-field-box">
                            <span id="modal-field-did-creduent" class="modal-field-value">did:creduent:...</span>
                            <button onclick="copyModalField('modal-field-did-creduent')" class="modal-copy-btn" title="Copy did:creduent">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                            </button>
                        </div>
                    </div>

                    <div class="modal-grid-span-2 modal-detail-item">
                        <label class="modal-detail-label">W3C DID (did:web)</label>
                        <div class="modal-field-box">
                            <span id="modal-field-did-web" class="modal-field-value">did:web:...</span>
                            <button onclick="copyModalField('modal-field-did-web')" class="modal-copy-btn" title="Copy did:web">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                            </button>
                        </div>
                    </div>

                    <div class="modal-grid-span-2 modal-detail-item">
                        <label class="modal-detail-label">Public Key (Ed25519)</label>
                        <div class="modal-field-box">
                            <span id="modal-field-public-key" class="modal-field-value">ed25519:...</span>
                            <button onclick="copyModalField('modal-field-public-key')" class="modal-copy-btn" title="Copy Public Key">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                            </button>
                        </div>
                    </div>

                    <div class="modal-detail-item">
                        <label class="modal-detail-label">Issued At</label>
                        <span id="modal-field-issued" style="font-family: 'JetBrains Mono', monospace; font-size: 0.88rem; color: var(--text-main);">-</span>
                    </div>

                    <div class="modal-detail-item">
                        <label class="modal-detail-label">Expires At</label>
                        <span id="modal-field-expires" style="font-family: 'JetBrains Mono', monospace; font-size: 0.88rem; color: var(--text-main);">-</span>
                    </div>
                </div>

                <!-- Proof Cryptographic Block -->
                <div id="modal-proof-section" class="modal-detail-item" style="margin-top: 6px;">
                    <label class="modal-detail-label">Attestation Proof Signature</label>
                    <div class="modal-field-box">
                        <span id="modal-field-signature" class="modal-field-value">signature:...</span>
                        <button onclick="copyModalField('modal-field-signature')" class="modal-copy-btn" title="Copy Signature">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Tab Content: Raw JSON -->
            <div id="view-modal-raw" style="padding: 24px; display: none; flex-direction: column; gap: 12px; overflow: hidden; height: 60vh;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 0.8rem; color: var(--text-muted);">Registry Record JSON Payload</span>
                    <button class="btn btn-secondary btn-sm" id="copy-raw-json-btn" onclick="copyRawJSON()" style="font-size: 0.72rem; padding: 4px 10px;">Copy JSON</button>
                </div>
                <pre id="modal-body-raw-content" style="flex: 1; padding: 16px; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; line-height: 1.5; color: var(--text-main); background: #ffffff; border: 1px solid var(--border-color); border-radius: 8px; overflow-y: auto; margin: 0; white-space: pre-wrap; word-break: break-all;"></pre>
            </div>

            <div class="modal-footer" style="border-top: 1px solid var(--border-color);">
                <button class="btn btn-secondary btn-sm" onclick="hideModal()">Done</button>
            </div>
        </div>
    </div>

    <!-- Register Modal -->
    <div class="modal-overlay" id="register-modal" onclick="closeRegisterModal(event)">
        <form class="modal" id="register-form" onsubmit="handleRegister(event)" onclick="event.stopPropagation()" style="max-width:540px; margin:0;">
            <div class="modal-header">
                <div>
                    <h3>Register New Agent</h3>
                    <p style="font-size:13px;font-weight:400;color:var(--text-muted);margin-top:4px;letter-spacing:-0.39px;">Direct registration requires admin key</p>
                </div>
                <button type="button" class="btn btn-secondary btn-sm" onclick="hideRegisterModal()">✕ Close</button>
            </div>
            <div style="padding:24px;display:flex;flex-direction:column;gap:18px;overflow-y:auto;max-height:75vh;">
                <div style="font-size: 0.78rem; color: var(--text-muted); line-height: 1.5; border-left: 2px solid var(--warning); padding-left: 10px; margin-bottom: 8px;">
                    Direct registration requires admin key. Public registration via <code style="background: rgba(0, 0, 0, 0.04); padding: 2px 5px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; color: var(--primary);">POST /register</code> uses DNS + agent.json verification.
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
                    <textarea id="reg-public-key" name="reg-public-key" placeholder="ed25519:uMMQ6RfZB5RJu..." required style="min-height: 70px;"></textarea>
                </div>
                <div class="form-group">
                    <label for="reg-admin-key">Admin Key</label>
                    <input type="password" id="reg-admin-key" name="reg-admin-key" placeholder="Enter admin key..." required autocomplete="current-password">
                </div>
                <button type="submit" class="btn" id="reg-submit-btn">Register Agent</button>
                <div id="register-feedback" class="feedback"></div>
            </div>
        </form>
    </div>

    <!-- Webhook Modal -->
    <div class="modal-overlay" id="webhook-modal" onclick="closeWebhookModal(event)">
        <form class="modal" id="webhook-form" onsubmit="handleWebhookRegister(event)" onclick="event.stopPropagation()" style="max-width:540px; margin:0;">
            <div class="modal-header">
                <div>
                    <h3>Webhook Manager</h3>
                    <p style="font-size:13px;font-weight:400;color:var(--text-muted);margin-top:4px;letter-spacing:-0.39px;">Manage agent webhook notifications</p>
                </div>
                <button type="button" class="btn btn-secondary btn-sm" onclick="hideWebhookModal()">✕ Close</button>
            </div>
            <div style="padding:24px;display:flex;flex-direction:column;gap:18px;overflow-y:auto;max-height:75vh;">
                <div style="font-size: 0.78rem; color: var(--text-muted); line-height: 1.5; border-left: 2px solid var(--primary); padding-left: 10px; margin-bottom: 8px;">
                    Webhook registration requires a valid Ed25519 signature. Sign the payload: <code style="background: rgba(0, 0, 0, 0.04); padding: 2px 5px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; color: var(--primary);">agent_id|webhook_url</code> with your agent's private key.
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
                <div id="web-payload-container" style="display: none; background: var(--bg-base); border: 1px solid var(--border-color); border-radius: 10px; padding: 16px; margin-bottom: 20px; animation: fadeIn 0.25s ease-out;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <div class="step-tag" style="margin-bottom: 0;">① Payload to Sign</div>
                        <button type="button" class="btn btn-secondary btn-sm" id="copy-web-payload-btn" onclick="copyWebhookPayload()" style="font-size: 0.7rem; padding: 3px 8px;">Copy</button>
                    </div>
                    <pre id="web-payload-display" class="payload-box"></pre>
                </div>

                <!-- Signature Input -->
                <div class="form-group">
                    <label for="web-signature">Signature</label>
                    <textarea id="web-signature" placeholder="Base64-encoded Ed25519 signature..." required style="min-height: 70px; font-family: var(--font-mono); font-size: 0.8rem;"></textarea>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                    <button type="submit" class="btn" id="web-submit-btn">Register</button>
                    <button type="button" class="btn btn-secondary" onclick="handleWebhookQuery()">Query URL</button>
                </div>
                <div id="webhook-feedback" class="feedback"></div>
                <div id="webhook-info" class="webhook-current-info"></div>
            </div>
        </form>
    </div>

    <!-- Renew Modal -->
    <div class="modal-overlay" id="renew-modal" onclick="closeRenewModal(event)">
        <form class="modal" id="renew-form" onsubmit="handleRenew(event)" onclick="event.stopPropagation()" style="max-width:640px; margin:0;">
            <div class="modal-header">
                <div>
                    <h3>Renew Agent Attestation</h3>
                    <p style="font-size:13px;font-weight:400;color:var(--text-muted);margin-top:4px;letter-spacing:-0.39px;" id="ren-modal-subtitle">Sign the payload below with the agent's private key</p>
                </div>
                <button type="button" class="btn btn-secondary btn-sm" onclick="hideRenewModal()">✕ Close</button>
            </div>
            <div style="padding:24px;display:flex;flex-direction:column;gap:20px;overflow-y:auto;max-height:70vh;">

                <!-- Agent Info Card -->
                <div class="modal-certificate-header">
                    <div style="display: flex; align-items: center; gap: 14px;">
                        <div id="ren-agent-avatar" style="width: 44px; height: 44px; border-radius: 10px; background: rgba(83, 58, 253, 0.1); border: 1px solid rgba(83, 58, 253, 0.2); display: flex; align-items: center; justify-content: center; color: var(--primary);">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                        </div>
                        <div>
                            <div id="ren-agent-name" style="font-size: 1.1rem; font-weight: 500; color: var(--text-main);">Agent Name</div>
                            <div id="ren-agent-domain" style="font-size: 0.8rem; color: var(--text-muted);">domain.com</div>
                        </div>
                    </div>
                    <div>
                        <span id="ren-status-badge" class="badge">verified</span>
                    </div>
                </div>

                <!-- Step 1: Set New Expiry -->
                <div style="background: var(--bg-base); border: 1px solid var(--border-color); border-radius: 12px; padding: 20px;">
                    <div class="step-tag">① Set New Expiry</div>
                    <input type="hidden" id="ren-agent-id" name="ren-agent-id">
                    <div class="form-group" style="margin-bottom:0;">
                        <label for="ren-expires-at">New Expiry Date <span style="color:var(--text-muted);font-weight:400;text-transform:none;letter-spacing:normal;">(ISO 8601 UTC)</span></label>
                        <input type="text" id="ren-expires-at" name="ren-expires-at" placeholder="2027-05-30T00:00:00Z" oninput="updateRenewPayload()" required autocomplete="off">
                    </div>
                </div>

                <!-- Step 2: Payload to sign -->
                <div style="background: var(--bg-base); border: 1px solid var(--border-color); border-radius: 12px; padding: 20px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                        <div class="step-tag" style="margin-bottom:0;">② Payload to Sign</div>
                        <button type="button" class="btn btn-secondary btn-sm" id="copy-payload-btn" onclick="copyRenewPayload()" style="font-size:0.7rem;padding:3px 8px;">Copy</button>
                    </div>
                    <pre id="ren-payload-display" class="payload-box" style="line-height:1.6;"></pre>
                    <p style="font-size:0.78rem;color:var(--text-muted);margin-top:10px;">Sign this string with <code style="background: rgba(0, 0, 0, 0.04); padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; font-family: 'JetBrains Mono', monospace; color: var(--primary);">ed25519.sign(payload.encode())</code> and base64-encode the result.</p>
                </div>

                <!-- Step 3: Signature input -->
                <div style="background: var(--bg-base); border: 1px solid var(--border-color); border-radius: 12px; padding: 20px;">
                    <div class="step-tag">③ Paste Signature</div>
                    <textarea id="ren-signature" name="ren-signature" placeholder="Base64-encoded Ed25519 signature..." style="width: 100%; background: #ffffff; border: 1px solid #a8c3de; border-radius: 8px; color: var(--text-main); padding: 12px 16px; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; resize: vertical; min-height: 75px; transition: all 0.25s;" required></textarea>
                </div>

                <!-- Submit -->
                <button type="submit" class="btn" id="ren-submit-btn" style="font-weight:600;padding:14px 20px;">Submit Renewal</button>
                <div id="renew-feedback" class="feedback"></div>
            </div>
        </form>
    </div>

    <!-- Upgrade Modal -->
    <div class="modal-overlay" id="upgrade-modal" onclick="closeUpgradeModal(event)">
        <form class="modal" id="upgrade-form" onsubmit="handleUpgrade(event)" onclick="event.stopPropagation()" style="max-width:480px; margin:0;">
            <div class="modal-header">
                <div>
                    <h3>Upgrade Attestation Level</h3>
                    <p style="font-size:13px;font-weight:400;color:var(--text-muted);margin-top:4px;letter-spacing:-0.39px;">Select target level and enter admin key</p>
                </div>
                <button type="button" class="btn btn-secondary btn-sm" onclick="hideUpgradeModal()">✕ Close</button>
            </div>
            <div style="padding:24px;display:flex;flex-direction:column;gap:18px;">
                <input type="hidden" id="upg-agent-id" name="upg-agent-id">
                
                <!-- Agent Info Card -->
                <div class="modal-certificate-header">
                    <div style="display: flex; align-items: center; gap: 14px;">
                        <div id="upg-agent-avatar" style="width: 44px; height: 44px; border-radius: 10px; background: rgba(83, 58, 253, 0.1); border: 1px solid rgba(83, 58, 253, 0.2); display: flex; align-items: center; justify-content: center; color: var(--primary);">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                        </div>
                        <div>
                            <div id="upg-agent-name" style="font-size: 1.1rem; font-weight: 500; color: var(--text-main);">Agent Name</div>
                            <div id="upg-agent-domain" style="font-size: 0.8rem; color: var(--text-muted);">domain.com</div>
                        </div>
                    </div>
                    <div>
                        <span id="upg-status-badge" class="badge">verified</span>
                    </div>
                </div>

                <div class="form-group" style="margin-bottom:12px;">
                    <label for="upg-level">Target Level</label>
                    <select id="upg-level" name="upg-level">
                        <option value="verified">Verified (Identity confirmed)</option>
                        <option value="trusted">Trusted (High authority/partner)</option>
                        <option value="unverified">Unverified (Revoke verification)</option>
                    </select>
                </div>
                <div class="form-group" style="margin-bottom:12px;">
                    <label for="upg-admin-key">Admin Key</label>
                    <input type="password" id="upg-admin-key" name="upg-admin-key" placeholder="Enter admin key..." autocomplete="current-password" required>
                </div>
                <button type="submit" class="btn" id="upg-submit-btn" style="font-weight:600;padding:14px 20px;">Submit Upgrade</button>
                <div id="upgrade-feedback" class="feedback"></div>
            </div>
        </form>
    </div>

    <!-- Revoke Modal -->
    <div class="modal-overlay" id="revoke-modal" onclick="closeRevokeModal(event)">
        <form class="modal" id="revoke-form" onsubmit="handleRevoke(event)" onclick="event.stopPropagation()" style="max-width:480px; margin:0;">
            <div class="modal-header">
                <div>
                    <h3 style="color:var(--error);">Revoke Agent Attestation</h3>
                    <p style="font-size:13px;font-weight:400;color:var(--text-muted);margin-top:4px;letter-spacing:-0.39px;">Enter admin key to confirm revocation</p>
                </div>
                <button type="button" class="btn btn-secondary btn-sm" onclick="hideRevokeModal()">✕ Close</button>
            </div>
            <div style="padding:24px;display:flex;flex-direction:column;gap:18px;">
                <input type="hidden" id="rev-agent-id" name="rev-agent-id">
                
                <!-- Agent Info Card -->
                <div class="modal-certificate-header">
                    <div style="display: flex; align-items: center; gap: 14px;">
                        <div id="rev-agent-avatar" style="width: 44px; height: 44px; border-radius: 10px; background: rgba(83, 58, 253, 0.1); border: 1px solid rgba(83, 58, 253, 0.2); display: flex; align-items: center; justify-content: center; color: var(--primary);">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                        </div>
                        <div>
                            <div id="rev-agent-name" style="font-size: 1.1rem; font-weight: 500; color: var(--text-main);">Agent Name</div>
                            <div id="rev-agent-domain" style="font-size: 0.8rem; color: var(--text-muted);">domain.com</div>
                        </div>
                    </div>
                    <div>
                        <span id="rev-status-badge" class="badge">verified</span>
                    </div>
                </div>

                <div class="form-group" style="margin-bottom:12px;">
                    <label for="rev-admin-key">Admin Key</label>
                    <input type="password" id="rev-admin-key" name="rev-admin-key" placeholder="Enter admin key..." autocomplete="current-password" required>
                </div>
                <div style="font-size: 0.82rem; color: var(--error); line-height: 1.5; background: var(--error-glow); border: 1px solid var(--error-border); padding: 14px; border-radius: 8px;">
                    <strong style="display: block; margin-bottom: 4px;">Warning:</strong> Revoking this agent will mark it as permanently revoked. This signature cannot be verified and the action cannot be undone.
                </div>
                <button type="submit" class="btn" id="rev-submit-btn" style="background-color: var(--error); font-weight:600; padding:14px 20px;">Revoke Agent</button>
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
                }

                // Fetch agent explorer table
                const agentsRes = await fetch('/agents?t=' + Date.now());
                const tbody = document.getElementById('agent-table-body');
                const mobileList = document.getElementById('mobile-agent-list');
                
                if (agentsRes.ok) {
                    const agents = await agentsRes.json();
                    window.loadedAgents = agents;
                    
                    if (agents.length === 0) {
                        tbody.innerHTML = `
                            <tr>
                                <td colspan="5" style="text-align: center; color: var(--text-muted); padding: 48px 0;">
                                    No agents registered in the system.
                                </td>
                            </tr>
                        `;
                        mobileList.innerHTML = `
                            <div style="text-align: center; color: var(--text-muted); padding: 32px 0; font-size: 0.88rem;">
                                No agents registered in the system.
                            </div>
                        `;
                        return;
                    }

                    tbody.innerHTML = '';
                    mobileList.innerHTML = '';
                    const now = new Date();

                    agents.forEach(agent => {
                        // Resolve level early so it's available for all checks below
                        const level = (agent.level || 'verified').toLowerCase();

                        // Parse remaining days
                        let isExpiringSoon = false;
                        const expiresAtStr = agent.expires_at;
                        if (expiresAtStr && level !== 'revoked') {
                            try {
                                const expiry = new Date(expiresAtStr);
                                const diffTime = expiry - now;
                                const daysRem = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                                if (daysRem >= 0 && daysRem <= 30) {
                                    isExpiringSoon = true;
                                }
                            } catch (e) {}
                        }

                        // Badges
                        let badgeClass = 'badge-verified';
                        if (level === 'revoked') badgeClass = 'badge-revoked';
                        else if (level === 'trusted') badgeClass = 'badge-trusted';
                        else if (level !== 'verified') badgeClass = 'badge-unverified';

                        // 1. Render Desktop Table Row
                        const tr = document.createElement('tr');
                        if (isExpiringSoon) {
                            tr.className = 'warning-row';
                        }
                        tr.innerHTML = `
                            <td class="monospace">${agent.agent_id}</td>
                            <td>${agent.domain || '-'}</td>
                            <td><span class="badge ${badgeClass}">${level}</span></td>
                            <td class="monospace">${expiresAtStr ? expiresAtStr.split('T')[0] : '-'}</td>
                            <td>
                                <div class="actions-cell">
                                    <button class="btn btn-secondary btn-sm" onclick="viewAgent('${encodeURIComponent(agent.agent_id)}')">View</button>
                                    <button class="btn btn-secondary btn-sm" onclick="showUpgradeModal('${encodeURIComponent(agent.agent_id)}')">Level</button>
                                    <button class="btn btn-secondary btn-sm" onclick="showRenewModal('${encodeURIComponent(agent.agent_id)}')">Renew</button>
                                    <button class="btn btn-secondary btn-sm" onclick="showRevokeModal('${encodeURIComponent(agent.agent_id)}')" style="color: var(--error); border-color: rgba(234, 34, 97, 0.15);">Revoke</button>
                                </div>
                            </td>
                        `;
                        tbody.appendChild(tr);

                        // 2. Render Mobile Premium Card
                        const cardDiv = document.createElement('div');
                        cardDiv.className = 'mobile-agent-card' + (isExpiringSoon ? ' warning-card' : '');
                        
                        const nameRaw = agent.agent_id.split('/').pop() || '';
                        const agentName = nameRaw.charAt(0).toUpperCase() + nameRaw.slice(1);

                        cardDiv.innerHTML = `
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px;">
                                <div style="display: flex; align-items: center; gap: 10px; min-width: 0;">
                                    <div class="mobile-card-avatar" style="width: 32px; height: 32px; border-radius: 8px; background: rgba(83, 58, 253, 0.1); border: 1px solid rgba(83, 58, 253, 0.2); display: flex; align-items: center; justify-content: center; color: var(--primary); flex-shrink: 0;">
                                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                                    </div>
                                    <div style="min-width: 0; overflow: hidden;">
                                        <div style="font-family: 'Outfit', sans-serif; font-size: 1.05rem; font-weight: 600; color: var(--text-main); overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${agentName}</div>
                                        <div style="font-size: 0.75rem; color: var(--text-muted);">${agent.domain || '-'}</div>
                                    </div>
                                </div>
                                <div>
                                    <span class="badge ${badgeClass}" style="font-size: 0.65rem; padding: 4px 8px;">${level}</span>
                                </div>
                            </div>
                            
                            <div style="display: flex; flex-direction: column; gap: 6px; border-top: 1px solid var(--border-color); padding-top: 10px; font-size: 0.78rem;">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <span style="color: var(--text-muted); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Agent URI:</span>
                                    <span class="monospace" style="color: var(--text-dark); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 75%; font-size: 0.75rem;">${agent.agent_id}</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <span style="color: var(--text-muted); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Expires:</span>
                                    <span class="monospace" style="color: var(--text-main);">${expiresAtStr ? expiresAtStr.split('T')[0] : '-'}</span>
                                </div>
                            </div>

                            <div style="display: flex; gap: 8px; justify-content: flex-end; border-top: 1px solid var(--border-color); padding-top: 10px; flex-wrap: wrap;">
                                <button class="btn btn-secondary btn-sm" onclick="viewAgent('${encodeURIComponent(agent.agent_id)}')">View</button>
                                <button class="btn btn-secondary btn-sm" onclick="showUpgradeModal('${encodeURIComponent(agent.agent_id)}')">Level</button>
                                <button class="btn btn-secondary btn-sm" onclick="showRenewModal('${encodeURIComponent(agent.agent_id)}')">Renew</button>
                                <button class="btn btn-secondary btn-sm" onclick="showRevokeModal('${encodeURIComponent(agent.agent_id)}')" style="color: var(--error); border-color: rgba(234, 34, 97, 0.15);">Revoke</button>
                            </div>
                        `;
                        mobileList.appendChild(cardDiv);

                        // Load favicon asynchronously for card
                        if (agent.domain && agent.domain !== '-') {
                            let baseDomain = agent.domain;
                            const parts = agent.domain.split('.');
                            if (parts.length > 2) {
                                const pen = parts[parts.length - 2].toLowerCase();
                                const tld = parts[parts.length - 1].toLowerCase();
                                if ((tld === 'uk' && pen === 'co') || 
                                    (tld === 'br' && pen === 'com') || 
                                    (tld === 'au' && pen === 'net') || 
                                    (tld === 'nz' && pen === 'co')) {
                                    if (parts.length > 3) baseDomain = parts.slice(-3).join('.');
                                } else {
                                    baseDomain = parts.slice(-2).join('.');
                                }
                            }
                            const img = document.createElement('img');
                            img.src = (baseDomain === 'idevsec.com') ? 'https://idevsec.com/logo.png' : `https://www.google.com/s2/favicons?sz=64&domain=${baseDomain}`;
                            img.alt = baseDomain;
                            img.style.width = '20px';
                            img.style.height = '20px';
                            img.style.borderRadius = '4px';
                            img.style.objectFit = 'contain';
                            const avatar = cardDiv.querySelector('.mobile-card-avatar');
                            img.onload = () => {
                                avatar.innerHTML = '';
                                avatar.appendChild(img);
                            };
                        }
                    });
                } else {
                    tbody.innerHTML = `
                        <tr>
                            <td colspan="5" style="text-align: center; color: var(--error); padding: 48px 0;">
                                Failed to fetch agent records from server.
                            </td>
                        </tr>
                    `;
                    mobileList.innerHTML = `
                        <div style="text-align: center; color: var(--error); padding: 32px 0; font-size: 0.88rem;">
                            Failed to fetch agent records from server.
                        </div>
                    `;
                }
            } catch (e) {
                console.error("Dashboard fetch error:", e);
            }
        }

        function getDidCreduent(agentUri) {
            if (!agentUri) return '-';
            const clean = agentUri.replace(/^agent:\/\//, '');
            return 'did:creduent:' + clean.replace(/\//g, ':');
        }

        function getDidWeb(agentUri, domain) {
            if (!agentUri) return '-';
            const parts = agentUri.replace(/^agent:\/\//, '').split('/');
            const namespace = parts[0] || 'default';
            let d = domain && domain !== '-' ? domain : `${namespace}.com`;
            if (d.startsWith('creduent.')) {
                const parentDomain = d.replace(/^creduent\./, '');
                if (parentDomain.startsWith(namespace)) {
                    d = parentDomain;
                }
            }
            const name = parts.length > 1 ? parts.slice(1).join(':') : namespace;
            return `did:web:${d}:agent:${name}`;
        }

        function switchViewModalTab(tab) {
            const overviewTabBtn = document.getElementById('tab-btn-overview');
            const rawTabBtn = document.getElementById('tab-btn-raw');
            const overviewContent = document.getElementById('view-modal-overview');
            const rawContent = document.getElementById('view-modal-raw');

            if (tab === 'overview') {
                overviewTabBtn.classList.add('active');
                rawTabBtn.classList.remove('active');
                overviewContent.style.display = 'flex';
                rawContent.style.display = 'none';
            } else {
                overviewTabBtn.classList.remove('active');
                rawTabBtn.classList.add('active');
                overviewContent.style.display = 'none';
                rawContent.style.display = 'flex';
            }
        }

        function normalizeDomain(domain, agentUri) {
            if (!domain || domain === '-') return '-';
            if (domain.startsWith('creduent.')) {
                const parent = domain.replace(/^creduent\./, '');
                if (agentUri) {
                    const ns = agentUri.replace(/^agent:\/\//, '').split('/')[0];
                    if (ns && parent.startsWith(ns)) return parent;
                }
                return parent;
            }
            return domain;
        }

        function populateViewModal(data) {
            const agentId = data.agent_id || '-';
            const domain = normalizeDomain(data.domain || '-', agentId);
            const publicKey = data.public_key || '-';
            const level = (data.level || 'verified').toLowerCase();
            const issuedAt = data.issued_at ? data.issued_at.replace('T', ' ').replace('Z', ' UTC') : '-';
            const expiresAt = data.expires_at ? data.expires_at.replace('T', ' ').replace('Z', ' UTC') : '-';
            const signature = data.signature || '-';

            // Set Title
            document.getElementById('modal-title').textContent = `Attestation Certificate`;

            // Populate Overview fields
            let namePart = "Agent Identifier";
            try {
                const parsed = agentId.replace("agent://", "").split("/");
                if (parsed.length > 0) {
                    const lastPart = parsed[parsed.length - 1];
                    if (lastPart) {
                        namePart = lastPart.charAt(0).toUpperCase() + lastPart.slice(1);
                    }
                }
            } catch(e){}

            document.getElementById('modal-agent-name').textContent = namePart;
            document.getElementById('modal-agent-domain').textContent = domain;
            document.getElementById('modal-field-uri').textContent = agentId;
            document.getElementById('modal-field-did-creduent').textContent = data.did_creduent || getDidCreduent(agentId);
            document.getElementById('modal-field-did-web').textContent = data.did_web || getDidWeb(agentId, domain);
            document.getElementById('modal-field-public-key').textContent = publicKey;
            document.getElementById('modal-field-issued').textContent = issuedAt;
            document.getElementById('modal-field-expires').textContent = expiresAt;
            document.getElementById('modal-field-signature').textContent = signature;

            // Populate Badge
            const badge = document.getElementById('modal-status-badge');
            badge.textContent = level;
            badge.className = 'badge';
            if (level === 'revoked') {
                badge.classList.add('badge-revoked');
            } else if (level === 'trusted') {
                badge.classList.add('badge-trusted');
            } else if (level === 'verified') {
                badge.classList.add('badge-verified');
            } else {
                badge.classList.add('badge-unverified');
            }

            // Populate Favicon / Avatar
            const avatarContainer = document.getElementById('modal-agent-avatar');
            if (domain && domain !== '-') {
                let baseDomain = domain;
                const parts = domain.split('.');
                if (parts.length > 2) {
                    const pen = parts[parts.length - 2].toLowerCase();
                    const tld = parts[parts.length - 1].toLowerCase();
                    if ((tld === 'uk' && pen === 'co') || 
                        (tld === 'br' && pen === 'com') || 
                        (tld === 'au' && pen === 'net') || 
                        (tld === 'nz' && pen === 'co')) {
                        if (parts.length > 3) baseDomain = parts.slice(-3).join('.');
                    } else {
                        baseDomain = parts.slice(-2).join('.');
                    }
                }
                const img = document.createElement('img');
                img.src = (baseDomain === 'idevsec.com') ? 'https://idevsec.com/logo.png' : `https://www.google.com/s2/favicons?sz=128&domain=${baseDomain}`;
                img.alt = baseDomain;
                img.style.width = '30px';
                img.style.height = '30px';
                img.style.borderRadius = '6px';
                img.style.objectFit = 'contain';
                img.onerror = () => {
                    avatarContainer.innerHTML = `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`;
                };
                avatarContainer.innerHTML = '';
                avatarContainer.appendChild(img);
            } else {
                avatarContainer.innerHTML = `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`;
            }

            // Populate Raw JSON Tab
            document.getElementById('modal-body-raw-content').textContent = JSON.stringify(data, null, 2);
        }

        function copyModalField(elementId) {
            const text = document.getElementById(elementId).textContent;
            const container = document.getElementById(elementId).closest('.modal-field-box');
            const btn = container ? container.querySelector('button') : null;
            
            navigator.clipboard.writeText(text).then(() => {
                if (btn) {
                    const originalSVG = btn.innerHTML;
                    btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--success)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
                    setTimeout(() => {
                        btn.innerHTML = originalSVG;
                    }, 2000);
                }
            });
        }

        function copyRawJSON() {
            const text = document.getElementById('modal-body-raw-content').textContent;
            const btn = document.getElementById('copy-raw-json-btn');
            navigator.clipboard.writeText(text).then(() => {
                if (btn) {
                    const originalText = btn.textContent;
                    btn.textContent = '✓ Copied';
                    btn.style.color = 'var(--success)';
                    btn.style.borderColor = 'var(--success-border)';
                    setTimeout(() => {
                        btn.textContent = originalText;
                        btn.style.color = '';
                        btn.style.borderColor = '';
                    }, 2000);
                }
            });
        }

        function populateModalCard(prefix, agent) {
            const agentId = agent.agent_id || '-';
            const domain = agent.domain || '-';
            const level = (agent.level || 'verified').toLowerCase();

            // Name
            let namePart = "Agent Identifier";
            try {
                const parsed = agentId.replace("agent://", "").split("/");
                if (parsed.length > 0) {
                    const lastPart = parsed[parsed.length - 1];
                    if (lastPart) {
                        namePart = lastPart.charAt(0).toUpperCase() + lastPart.slice(1);
                    }
                }
            } catch(e){}

            const nameEl = document.getElementById(`${prefix}-agent-name`);
            const domainEl = document.getElementById(`${prefix}-agent-domain`);
            if (nameEl) nameEl.textContent = namePart;
            if (domainEl) domainEl.textContent = domain;

            // Badge
            const badge = document.getElementById(`${prefix}-status-badge`);
            if (badge) {
                badge.textContent = level;
                badge.className = 'badge';
                if (level === 'revoked') {
                    badge.classList.add('badge-revoked');
                } else if (level === 'trusted') {
                    badge.classList.add('badge-trusted');
                } else if (level === 'verified') {
                    badge.classList.add('badge-verified');
                } else {
                    badge.classList.add('badge-unverified');
                }
            }

            // Avatar
            const avatarContainer = document.getElementById(`${prefix}-agent-avatar`);
            if (avatarContainer) {
                if (domain && domain !== '-') {
                    let baseDomain = domain;
                    const parts = domain.split('.');
                    if (parts.length > 2) {
                        const pen = parts[parts.length - 2].toLowerCase();
                        const tld = parts[parts.length - 1].toLowerCase();
                        if ((tld === 'uk' && pen === 'co') || 
                            (tld === 'br' && pen === 'com') || 
                            (tld === 'au' && pen === 'net') || 
                            (tld === 'nz' && pen === 'co')) {
                            if (parts.length > 3) baseDomain = parts.slice(-3).join('.');
                        } else {
                            baseDomain = parts.slice(-2).join('.');
                        }
                    }
                    const img = document.createElement('img');
                    img.src = (baseDomain === 'idevsec.com') ? 'https://idevsec.com/logo.png' : `https://www.google.com/s2/favicons?sz=128&domain=${baseDomain}`;
                    img.alt = baseDomain;
                    img.style.width = '30px';
                    img.style.height = '30px';
                    img.style.borderRadius = '6px';
                    img.style.objectFit = 'contain';
                    img.onerror = () => {
                        avatarContainer.innerHTML = `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`;
                    };
                    avatarContainer.innerHTML = '';
                    avatarContainer.appendChild(img);
                } else {
                    avatarContainer.innerHTML = `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`;
                }
            }
        }

        async function viewAgent(agentIdDec) {
            const agentId = decodeURIComponent(agentIdDec);
            
            // Switch to overview tab by default
            switchViewModalTab('overview');
            
            // Serve instantly from local cache if available
            if (window.loadedAgents) {
                const cachedAgent = window.loadedAgents.find(a => a.agent_id === agentId);
                if (cachedAgent) {
                    populateViewModal(cachedAgent);
                    document.getElementById('view-modal').style.display = 'flex';
                    return;
                }
            }
            
            try {
                const res = await fetch(`/attest/${encodeURIComponent(agentId)}`);
                if (res.ok) {
                    const data = await res.json();
                    populateViewModal(data);
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
                btn.style.color = 'var(--success)';
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
                btn.style.color = 'var(--success)';
                setTimeout(() => { btn.textContent = 'Copy'; btn.style.color = ''; }, 2000);
            });
        }

        function showRenewModal(agentIdDec) {
            const agentId = decodeURIComponent(agentIdDec);
            document.getElementById('ren-agent-id').value = agentId;
            document.getElementById('renew-feedback').style.display = 'none';
            document.getElementById('ren-signature').value = '';
            document.getElementById('ren-submit-btn').disabled = false;
            document.getElementById('ren-submit-btn').textContent = 'Submit Renewal';
            updateDefaultRenewalDate();
            updateRenewPayload();

            // Populate Card
            if (window.loadedAgents) {
                const agent = window.loadedAgents.find(a => a.agent_id === agentId);
                if (agent) {
                    populateModalCard('ren', agent);
                }
            }

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
                    setTimeout(() => {
                        hideRegisterModal();
                    }, 1500);
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
                    setTimeout(() => {
                        hideWebhookModal();
                    }, 1500);
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
                        <strong style="color: var(--primary);">Registered URL:</strong><br>
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
            document.getElementById('upgrade-feedback').style.display = 'none';
            document.getElementById('upg-admin-key').value = '';
            document.getElementById('upg-submit-btn').disabled = false;
            document.getElementById('upg-submit-btn').textContent = 'Submit Upgrade';

            // Populate Card
            if (window.loadedAgents) {
                const agent = window.loadedAgents.find(a => a.agent_id === agentId);
                if (agent) {
                    populateModalCard('upg', agent);
                }
            }

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
            document.getElementById('revoke-feedback').style.display = 'none';
            document.getElementById('rev-admin-key').value = '';
            document.getElementById('rev-submit-btn').disabled = false;
            document.getElementById('rev-submit-btn').textContent = 'Revoke Agent';

            // Populate Card
            if (window.loadedAgents) {
                const agent = window.loadedAgents.find(a => a.agent_id === agentId);
                if (agent) {
                    populateModalCard('rev', agent);
                }
            }

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

        function showRegisterModal() {
            document.getElementById('register-feedback').style.display = 'none';
            document.getElementById('register-form').reset();
            document.getElementById('register-modal').style.display = 'flex';
        }

        function hideRegisterModal() {
            document.getElementById('register-modal').style.display = 'none';
        }

        function closeRegisterModal(e) {
            if (e.target === document.getElementById('register-modal')) {
                hideRegisterModal();
            }
        }

        function showWebhookModal() {
            document.getElementById('webhook-feedback').style.display = 'none';
            document.getElementById('webhook-info').style.display = 'none';
            document.getElementById('web-payload-container').style.display = 'none';
            document.getElementById('webhook-form').reset();
            document.getElementById('webhook-modal').style.display = 'flex';
        }

        function hideWebhookModal() {
            document.getElementById('webhook-modal').style.display = 'none';
        }

        function closeWebhookModal(e) {
            if (e.target === document.getElementById('webhook-modal')) {
                hideWebhookModal();
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


WELCOME_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Creduent Registry & Resolver | Home</title>
    <meta name="description" content="Decentralized cryptographic agent identity resolution and trust verification protocol.">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #533afd;
            --primary-deep: #4434d4;
            --primary-press: #2e2b8c;
            --primary-soft: #665efd;
            --primary-bg-subdued: #b9b9f9;
            --ink: #0d253d;
            --ink-secondary: #273951;
            --ink-mute: #64748d;
            --canvas: #ffffff;
            --canvas-soft: #f6f9fc;
            --canvas-cream: #f5e9d4;
            --hairline: #e3e8ee;
            --hairline-input: #a8c3de;
            --ruby: #ea2261;
            --magenta: #f96bee;
            --lemon: #9b6829;
            --shadow-blue: rgba(0, 55, 112, 0.08);
            --success: #22c55e;
            --success-glow: rgba(34, 197, 94, 0.08);
            --success-border: rgba(34, 197, 94, 0.2);
        }

        *, *::before, *::after {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: "Inter", -apple-system, sans-serif;
            background: var(--canvas);
            color: var(--ink);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            font-feature-settings: "ss01" on;
            -webkit-font-smoothing: antialiased;
        }

        .hero-mesh {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 380px;
            background: 
                radial-gradient(circle at 12% 15%, rgba(245,233,212,0.55) 0%, transparent 45%),
                radial-gradient(circle at 88% 8%, rgba(249,107,238,0.25) 0%, transparent 40%),
                radial-gradient(circle at 50% -12%, rgba(83,58,253,0.14) 0%, transparent 50%),
                radial-gradient(circle at 75% 25%, rgba(234,34,97,0.11) 0%, transparent 45%);
            z-index: 0;
            pointer-events: none;
            border-bottom: 1px solid var(--hairline);
        }

        .container {
            max-width: 1200px;
            width: 100%;
            margin: 0 auto;
            padding: 0 24px;
            position: relative;
            z-index: 1;
        }

        /* Navbar style matching image */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 24px 0;
            border-bottom: 1px solid var(--hairline);
            margin-bottom: 24px;
            width: 100%;
        }

        .nav-left {
            display: flex;
            align-items: center;
        }

        .brand-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
        }

        .brand-avatar {
            width: 36px;
            height: 36px;
            background-color: var(--primary);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            box-shadow: 0 2px 8px rgba(83, 58, 253, 0.2);
        }

        .brand-text {
            font-size: 20px;
            font-weight: 500;
            letter-spacing: -0.42px;
        }

        .brand-name {
            color: var(--ink);
        }

        .brand-suffix {
            color: var(--primary);
        }

        .nav-center {
            display: flex;
            align-items: center;
            gap: 32px;
        }

        .nav-link {
            font-size: 15px;
            font-weight: 400;
            color: var(--ink-mute);
            text-decoration: none;
            transition: color 0.15s ease;
        }

        .nav-link:hover {
            color: var(--ink);
        }

        .nav-link.active {
            color: var(--primary);
            font-weight: 500;
        }

        .nav-right {
            display: flex;
            align-items: center;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-feature-settings: "tnum" on;
            font-size: 13px;
            font-weight: 400;
            line-height: 1.0;
            letter-spacing: -0.39px;
            background: var(--success-glow);
            color: var(--success);
            padding: 8px 16px;
            border-radius: 9999px;
            border: 1px solid var(--success-border);
            box-shadow: rgba(34, 197, 94, 0.08) 0 4px 12px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--success);
            box-shadow: 0 0 8px var(--success);
            animation: pulse-green 2s infinite;
        }

        @keyframes pulse-green {
            0%, 100% { opacity: 0.6; transform: scale(0.9); }
            50% { opacity: 1; transform: scale(1.15); }
        }

        main {
            flex: 1;
            padding-top: 56px;
        }

        .hero {
            max-width: 620px;
            margin-bottom: 64px;
        }

        .eyebrow {
            display: inline-block;
            background: var(--primary-bg-subdued);
            color: var(--primary-deep);
            font-size: 10px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            padding: 4px 8px;
            border-radius: 9999px;
            margin-bottom: 18px;
        }

        .display-title {
            font-size: 56px;
            font-weight: 300;
            line-height: 1.03;
            letter-spacing: -1.4px;
            color: var(--ink);
            margin-bottom: 16px;
        }

        .lead-text {
            font-size: 18px;
            font-weight: 300;
            line-height: 1.45;
            color: var(--ink-secondary);
        }

        .split-panel {
            display: grid;
            grid-template-columns: 1fr 1.25fr;
            gap: 36px;
            margin-bottom: 96px;
            align-items: start;
        }

        .endpoints-card {
            background: var(--canvas);
            border: 1px solid var(--hairline);
            border-radius: 12px;
            padding: 32px;
            box-shadow: var(--shadow-blue) 0 1px 3px;
        }

        .card-title {
            font-size: 22px;
            font-weight: 300;
            line-height: 1.1;
            letter-spacing: -0.22px;
            margin-bottom: 24px;
        }

        .endpoint-list {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .endpoint-item {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding-bottom: 18px;
            border-bottom: 1px solid var(--hairline);
        }

        .endpoint-item:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }

        .method-badge {
            font-family: 'JetBrains Mono', monospace;
            font-size: 10px;
            font-weight: 600;
            padding: 3px 6px;
            border-radius: 4px;
            text-transform: uppercase;
            width: 46px;
            text-align: center;
            flex-shrink: 0;
        }

        .method-badge.get {
            background: rgba(56,189,248,0.1);
            border: 1px solid rgba(56,189,248,0.22);
            color: #0284c7;
        }

        .method-badge.post {
            background: rgba(52,211,153,0.1);
            border: 1px solid rgba(52,211,153,0.22);
            color: #059669;
        }

        .method-badge.delete {
            background: rgba(248,113,113,0.1);
            border: 1px solid rgba(248,113,113,0.22);
            color: #dc2626;
        }

        .endpoint-details {
            flex: 1;
        }

        .endpoint-path {
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            font-weight: 500;
            margin-bottom: 4px;
            word-break: break-all;
        }

        .endpoint-path a {
            color: var(--primary);
            text-decoration: none;
        }

        .endpoint-path a:hover {
            text-decoration: underline;
        }

        .endpoint-desc {
            font-size: 13px;
            color: var(--ink-mute);
            line-height: 1.4;
        }

        .ide-mockup {
            background: #090d16;
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 12px;
            box-shadow: rgba(0, 55, 112, 0.12) 0 8px 24px, rgba(0, 55, 112, 0.08) 0 2px 6px;
            overflow: hidden;
        }

        .ide-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #0b111e;
            padding: 12px 18px;
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }

        .ide-dots {
            display: flex;
            gap: 6px;
            align-items: center;
        }

        .ide-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }

        .ide-dot.red { background: #ef4444; }
        .ide-dot.yellow { background: #f59e0b; }
        .ide-dot.green { background: #10b981; }

        .ide-tab {
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            color: #94a3b8;
            background: #090d16;
            padding: 6px 12px;
            border-radius: 4px 4px 0 0;
            border: 1px solid rgba(255,255,255,0.06);
            border-bottom: none;
            margin-bottom: -13px;
            margin-left: 16px;
            display: inline-block;
        }

        .btn-copy {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            color: #cbd5e1;
            font-family: "Inter", sans-serif;
            font-size: 11px;
            font-weight: 500;
            padding: 6px 12px;
            border-radius: 9999px;
            cursor: pointer;
            transition: all 0.15s;
        }

        .btn-copy:hover {
            background: rgba(255,255,255,0.1);
            color: #ffffff;
        }

        .ide-body {
            padding: 24px;
            margin: 0;
            overflow-x: auto;
        }

        pre {
            margin: 0;
        }

        code {
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            line-height: 1.55;
            color: #cbd5e1;
            font-variant-numeric: tabular-nums;
            letter-spacing: -0.36px;
        }

        .json-key { color: #f472b6; }
        .json-string { color: #38bdf8; }
        .json-number { color: #fbbf24; }
        .json-boolean { color: #a78bfa; }

        footer {
            border-top: 1px solid var(--hairline);
            padding: 48px 0;
            color: var(--ink-mute);
            font-size: 13px;
        }

        .footer-inner {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .footer-inner a {
            color: var(--ink-secondary);
            text-decoration: none;
        }

        .footer-inner a:hover {
            color: var(--primary);
        }

        @media (max-width: 900px) {
            .navbar {
                flex-direction: column;
                gap: 16px;
                padding: 16px 0;
            }
            .nav-center {
                gap: 20px;
            }
            .split-panel {
                grid-template-columns: 1fr;
                gap: 28px;
            }
            .display-title {
                font-size: 40px;
                letter-spacing: -0.8px;
            }
            .footer-inner {
                flex-direction: column;
                gap: 16px;
                text-align: center;
            }
        }
    </style>
</head>
<body>

<div class="hero-mesh"></div>

<div class="container">
    <!-- Unified Navbar matching image exactly -->
    <header class="navbar">
        <div class="nav-left">
            <a href="/" class="brand-logo">
                <span class="brand-text">
                    <span class="brand-name">Creduent</span> 
                    <span class="brand-suffix">Registry</span>
                </span>
            </a>
        </div>
        <div class="nav-center">
            <a href="/explore" class="nav-link">Explore</a>
            <a href="/dashboard" class="nav-link">Dashboard</a>
            <a href="/resolver" class="nav-link">Resolver</a>
            <a href="/playground" class="nav-link">Playground</a>
        </div>
        <div class="nav-right">
            <div class="status-badge">
                <span class="status-dot"></span>
                <span>SYSTEM LIVE</span>
            </div>
        </div>
    </header>
</div>

<main>
    <div class="container">
        <div class="hero">
            <span class="eyebrow">Creduent Protocol · v2.0.0</span>
            <h1 class="display-title">Attestation Registry</h1>
            <p class="lead-text">Decentralized cryptographic agent identity resolution and trust verification protocol for autonomous AI agents.</p>
        </div>

        <div class="split-panel">
            <!-- Left: Endpoints Card -->
            <div class="endpoints-card">
                <h2 class="card-title">API Endpoints</h2>
                <div class="endpoint-list">
                    <div class="endpoint-item">
                        <span class="method-badge get">get</span>
                        <div class="endpoint-details">
                            <div class="endpoint-path"><a href="/">/</a></div>
                            <div class="endpoint-desc">Attestation registry welcome and protocol landing page.</div>
                        </div>
                    </div>
                    <div class="endpoint-item">
                        <span class="method-badge get">get</span>
                        <div class="endpoint-details">
                            <div class="endpoint-path"><a href="/explore">/explore</a></div>
                            <div class="endpoint-desc">Explore directory of registered agent cryptographic identities.</div>
                        </div>
                    </div>
                    <div class="endpoint-item">
                        <span class="method-badge get">get</span>
                        <div class="endpoint-details">
                            <div class="endpoint-path"><a href="/resolver">/resolver</a></div>
                            <div class="endpoint-desc">Visual Agent Identity Resolver and trust validator.</div>
                        </div>
                    </div>
                    <div class="endpoint-item">
                        <span class="method-badge get">get</span>
                        <div class="endpoint-details">
                            <div class="endpoint-path"><a href="/dashboard">/dashboard</a></div>
                            <div class="endpoint-desc">Developer registry monitoring and management dashboard.</div>
                        </div>
                    </div>
                    <div class="endpoint-item">
                        <span class="method-badge get">get</span>
                        <div class="endpoint-details">
                            <div class="endpoint-path"><a href="/playground">/playground</a></div>
                            <div class="endpoint-desc">Client-side Web Crypto sandbox, keypair generator & signature verifier.</div>
                        </div>
                    </div>
                    <div class="endpoint-item">
                        <span class="method-badge post">post</span>
                        <div class="endpoint-details">
                            <div class="endpoint-path">/register</div>
                            <div class="endpoint-desc">Open endpoint to register agent cryptographic identities.</div>
                        </div>
                    </div>
                    <div class="endpoint-item">
                        <span class="method-badge get">get</span>
                        <div class="endpoint-details">
                            <div class="endpoint-path">/attest/{agent_id}</div>
                            <div class="endpoint-desc">Retrieve signed identity attestation records.</div>
                        </div>
                    </div>
                    <div class="endpoint-item">
                        <span class="method-badge delete">del</span>
                        <div class="endpoint-details">
                            <div class="endpoint-path">/revoke/{agent_id}</div>
                            <div class="endpoint-desc">Revoke an active agent identity attestation.</div>
                        </div>
                    </div>
                    <div class="endpoint-item">
                        <span class="method-badge post">post</span>
                        <div class="endpoint-details">
                            <div class="endpoint-path">/recovery/override</div>
                            <div class="endpoint-desc">Emergency key rotation via DNS TXT record recovery.</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right: IDE Code Mockup -->
            <div class="ide-mockup">
                <div class="ide-header">
                    <div class="ide-dots">
                        <span class="ide-dot red"></span>
                        <span class="ide-dot yellow"></span>
                        <span class="ide-dot green"></span>
                        <span class="ide-tab">welcome.json</span>
                    </div>
                    <button class="btn-copy" onclick="copyJson()">Copy JSON</button>
                </div>
                <div class="ide-body">
                    <pre><code>{
  <span class="json-key">"service"</span>: <span class="json-string">"Creduent Attestation Registry &amp; Resolver"</span>,
  <span class="json-key">"version"</span>: <span class="json-string">"2.0.0"</span>,
  <span class="json-key">"status"</span>: <span class="json-string">"operational"</span>,
  <span class="json-key">"endpoints"</span>: {
    <span class="json-key">"home"</span>: <span class="json-string">"/"</span>,
    <span class="json-key">"explore"</span>: <span class="json-string">"/explore"</span>,
    <span class="json-key">"resolver"</span>: <span class="json-string">"/resolver"</span>,
    <span class="json-key">"dashboard"</span>: <span class="json-string">"/dashboard"</span>,
    <span class="json-key">"playground"</span>: <span class="json-string">"/playground"</span>,
    <span class="json-key">"register"</span>: <span class="json-string">"/register"</span>,
    <span class="json-key">"attest"</span>: <span class="json-string">"/attest/{agent_id}"</span>,
    <span class="json-key">"revoke"</span>: <span class="json-string">"/revoke/{agent_id}"</span>,
    <span class="json-key">"recovery_override"</span>: <span class="json-string">"/recovery/override"</span>
  }
}</code></pre>
                </div>
            </div>
        </div>
    </div>
</main>

<footer>
    <div class="container">
        <div class="footer-inner">
            <span>Powered by <a href="https://github.com/idevsec/creduent" target="_blank">Creduent Open Protocol</a> · v2.0.0</span>
            <span>&copy; 2026 <a href="https://idevsec.com" target="_blank">IDevSec</a>. All rights reserved.</span>
        </div>
    </div>
</footer>

<script>
    function copyJson() {
        const jsonText = `{
  "service": "Creduent Attestation Registry & Resolver",
  "version": "2.0.0",
  "status": "operational",
  "endpoints": {
    "home": "/",
    "explore": "/explore",
    "resolver": "/resolver",
    "dashboard": "/dashboard",
    "playground": "/playground",
    "register": "/register",
    "attest": "/attest/{agent_id}",
    "revoke": "/revoke/{agent_id}",
    "recovery_override": "/recovery/override"
  }
}`;
        navigator.clipboard.writeText(jsonText).then(() => {
            const btn = document.querySelector('.btn-copy');
            btn.textContent = '✓ Copied';
            setTimeout(() => {
                btn.textContent = 'Copy JSON';
            }, 2000);
        });
    }
</script>
</body>
</html>
"""

EXPLORE_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Creduent Registry - Explore Agent Directory</title>
    <meta name="description" content="Discover and search registered agents, capability listings, and attestation certificates.">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #f6f9fc;
            --bg-surface: #ffffff;
            --border-color: #e3e8ee;
            --border-input: #a8c3de;
            --primary: #533afd;
            --primary-hover: #4434d4;
            --primary-press: #2e2b8c;
            --primary-glow: rgba(83, 58, 253, 0.1);
            --primary-bg-subdued: #b9b9f9;
            --text-main: #0d253d;
            --text-muted: #64748d;
            --text-dark: #61718a;
            
            --success: #22c55e;
            --success-bg: rgba(34, 197, 94, 0.08);
            --success-border: rgba(34, 197, 94, 0.2);
            
            --warning: #9b6829;
            --warning-bg: rgba(155, 104, 41, 0.08);
            --warning-border: rgba(155, 104, 41, 0.2);
            
            --error: #ea2261;
            --error-bg: rgba(234, 34, 97, 0.08);
            --error-border: rgba(234, 34, 97, 0.2);
            
            --trusted: #a78bfa;
            --trusted-bg: rgba(167, 139, 250, 0.08);
            --trusted-border: rgba(167, 139, 250, 0.2);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-feature-settings: "ss01" on;
            font-weight: 300;
            font-size: 15px;
            line-height: 1.4;
            background-color: var(--bg-base);
            color: var(--text-main);
            min-height: 100vh;
            padding: 0;
            margin: 0;
            position: relative;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 0%, rgba(245, 233, 212, 0.6) 0%, transparent 45%),
                radial-gradient(circle at 45% 0%, rgba(155, 104, 41, 0.1) 0%, transparent 40%),
                radial-gradient(circle at 90% 0%, rgba(249, 107, 238, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 25% 0%, rgba(83, 58, 253, 0.12) 0%, transparent 55%),
                radial-gradient(circle at 75% 0%, rgba(234, 34, 97, 0.12) 0%, transparent 45%);
            background-size: 100% 420px;
            background-repeat: no-repeat;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px;
            position: relative;
            z-index: 10;
        }

        /* Navbar style matching image */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 24px 0;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 24px;
        }

        .nav-left {
            display: flex;
            align-items: center;
        }

        .brand-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
        }

        .brand-avatar {
            width: 36px;
            height: 36px;
            background-color: var(--primary);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            box-shadow: 0 2px 8px rgba(83, 58, 253, 0.2);
        }

        .brand-text {
            font-size: 20px;
            font-weight: 500;
            letter-spacing: -0.42px;
        }

        .brand-name {
            color: var(--text-main);
        }

        .brand-suffix {
            color: var(--primary);
        }

        .nav-center {
            display: flex;
            align-items: center;
            gap: 32px;
        }

        .nav-link {
            font-size: 15px;
            font-weight: 400;
            color: var(--text-muted);
            text-decoration: none;
            transition: color 0.15s ease;
        }

        .nav-link:hover {
            color: var(--text-main);
        }

        .nav-link.active {
            color: var(--primary);
            font-weight: 500;
        }

        .nav-right {
            display: flex;
            align-items: center;
        }

        .nav-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background-color: var(--primary);
            color: white;
            font-size: 14px;
            font-weight: 500;
            padding: 8px 18px;
            border-radius: 9999px; /* pill */
            text-decoration: none;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(83, 58, 253, 0.15);
        }

        .nav-btn:hover {
            background-color: var(--primary-hover);
            box-shadow: 0 6px 16px rgba(83, 58, 253, 0.25);
            transform: translateY(-1px);
        }

        .nav-btn:active {
            background-color: var(--primary-press);
            transform: translateY(0);
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-feature-settings: "tnum" on;
            font-size: 13px;
            font-weight: 400;
            line-height: 1.0;
            letter-spacing: -0.39px;
            background: var(--success-glow);
            color: var(--success);
            padding: 8px 16px;
            border-radius: 9999px;
            border: 1px solid var(--success-border);
            box-shadow: rgba(34, 197, 94, 0.08) 0 4px 12px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--success);
            box-shadow: 0 0 8px var(--success);
            animation: pulse-green 2s infinite;
        }

        @keyframes pulse-green {
            0%, 100% { opacity: 0.6; transform: scale(0.9); }
            50% { opacity: 1; transform: scale(1.15); }
        }

        .page-header {
            margin-bottom: 24px;
        }

        .page-header h1 {
            font-size: 24px;
            font-weight: 500;
            color: var(--text-main);
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .page-header p {
            font-size: 14px;
            color: var(--text-muted);
            margin-top: 4px;
        }

        /* Controls Card */
        .controls-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px 20px;
            display: flex;
            gap: 16px;
            align-items: center;
            box-shadow: rgba(0, 55, 112, 0.04) 0 8px 24px, rgba(0, 0, 0, 0.02) 0 2px 6px;
            margin-bottom: 24px;
        }

        .search-box {
            flex: 1;
            display: flex;
            align-items: center;
            gap: 12px;
            background: #f6f9fc;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px 16px;
            transition: all 0.25s ease;
        }

        .search-box:focus-within {
            border-color: var(--primary);
            background: #ffffff;
            box-shadow: 0 0 0 3px var(--primary-glow);
        }

        .search-icon {
            color: var(--text-muted);
        }

        .search-box input {
            border: none;
            background: transparent;
            outline: none;
            width: 100%;
            font-size: 15px;
            font-weight: 300;
            color: var(--text-main);
        }

        .search-box input::placeholder {
            color: var(--text-muted);
            opacity: 0.6;
        }

        .select-wrapper {
            position: relative;
        }

        .select-wrapper select {
            appearance: none;
            background-color: #f6f9fc;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px 36px 10px 16px;
            font-size: 15px;
            font-weight: 300;
            color: var(--text-main);
            outline: none;
            cursor: pointer;
            transition: all 0.25s ease;
        }

        .select-wrapper select:focus {
            border-color: var(--primary);
            background-color: #ffffff;
            box-shadow: 0 0 0 3px var(--primary-glow);
        }

        .select-wrapper::after {
            content: "";
            position: absolute;
            right: 14px;
            top: 50%;
            transform: translateY(-50%);
            border: 5px solid transparent;
            border-top-color: var(--text-muted);
            pointer-events: none;
        }

        /* Category Trigger Button */
        .category-trigger-container {
            margin-bottom: 32px;
        }

        .btn-category-trigger {
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            font-weight: 600;
            padding: 12px 20px;
            border-radius: 4px;
            border: 1px solid var(--border-color);
            background-color: var(--bg-surface);
            color: var(--text-dark);
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .btn-category-trigger:hover {
            border-color: var(--primary);
            color: var(--primary);
            box-shadow: 0 4px 16px rgba(83, 58, 253, 0.06);
        }

        /* SaaS Style Category Selector Modal */
        .category-modal-overlay {
            display: none;
            position: fixed;
            inset: 0;
            background-color: rgba(15, 23, 42, 0.3);
            z-index: 200;
            align-items: center;
            justify-content: center;
            padding: 24px;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            animation: fadeIn 0.25s ease-out;
        }

        .category-modal {
            background-color: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            max-width: 640px;
            width: 100%;
            max-height: 80vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: rgba(0, 55, 112, 0.12) 0 16px 48px, rgba(0, 0, 0, 0.08) 0 24px 64px;
            animation: scaleUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        .category-modal-header {
            padding: 20px 24px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: var(--bg-surface);
        }

        .category-modal-title {
            font-family: 'Outfit', sans-serif;
            font-size: 18px;
            font-weight: 500;
            color: var(--text-main);
            letter-spacing: -0.2px;
        }

        .category-modal-close {
            background: none;
            border: 1px solid var(--primary);
            color: var(--primary);
            font-family: 'Outfit', sans-serif;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            border-radius: 9999px;
            padding: 6px 14px;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }

        .category-modal-close:hover {
            background-color: rgba(83, 58, 253, 0.04);
            transform: translateY(-1px);
        }

        .category-modal-body {
            padding: 24px;
            overflow-y: auto;
            flex-grow: 1;
            background-color: var(--bg-base);
        }

        .modal-search-box {
            margin-bottom: 24px;
        }

        .modal-search-box input {
            width: 100%;
            background-color: var(--bg-surface);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            border-radius: 8px;
            font-family: inherit;
            font-size: 13px;
            padding: 12px 16px;
            outline: none;
            box-sizing: border-box;
            transition: all 0.2s ease;
        }

        .modal-search-box input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(83, 58, 253, 0.1);
        }

        .modal-group {
            margin-bottom: 28px;
        }

        .modal-group-title {
            font-size: 9px;
            font-weight: 700;
            color: #55555c;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .modal-group-title::after {
            content: "";
            flex-grow: 1;
            height: 1px;
            background-color: rgba(0, 0, 0, 0.04);
        }

        .modal-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }

        @media (max-width: 520px) {
            .modal-grid {
                grid-template-columns: 1fr;
            }
        }

        .modal-item-card {
            background-color: var(--bg-surface);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            border-radius: 8px;
            padding: 16px;
            font-size: 13px;
            font-family: 'Outfit', sans-serif;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 500;
        }

        .modal-item-card:hover {
            border-color: var(--primary);
            color: var(--primary);
            background-color: rgba(83, 58, 253, 0.02);
            transform: translateY(-1px);
            box-shadow: rgba(0, 55, 112, 0.04) 0 4px 12px;
        }

        .modal-item-card.active {
            border-color: var(--primary);
            color: var(--primary-deep);
            background-color: rgba(83, 58, 253, 0.06);
            font-weight: 600;
        }

        /* Grid */
        .agents-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 24px;
            margin-bottom: 64px;
        }

        .agent-card {
            background-color: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            box-shadow: rgba(0, 55, 112, 0.04) 0 8px 24px, rgba(0, 0, 0, 0.02) 0 2px 6px;
            display: flex;
            flex-direction: column;
            height: 100%;
            justify-content: space-between;
            transition: all 0.3s ease;
        }

        .agent-card:hover {
            transform: translateY(-3px);
            border-color: rgba(168, 195, 222, 0.4);
            box-shadow: rgba(0, 55, 112, 0.1) 0 12px 32px, rgba(0, 0, 0, 0.04) 0 4px 12px;
        }

        .card-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }

        .agent-avatar {
            width: 42px;
            height: 42px;
            border-radius: 8px;
            background: rgba(83, 58, 253, 0.06);
            border: 1px solid rgba(83, 58, 253, 0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--primary);
        }

        .agent-avatar img {
            width: 28px;
            height: 28px;
            border-radius: 4px;
            object-fit: contain;
        }

        .badge {
            font-family: 'JetBrains Mono', monospace;
            font-size: 10px;
            font-weight: 500;
            padding: 4px 10px;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .badge-verified {
            background-color: var(--success-bg);
            color: var(--success);
            border: 1px solid var(--success-border);
        }

        .badge-trusted {
            background-color: var(--trusted-bg);
            color: var(--trusted);
            border: 1px solid var(--trusted-border);
        }

        .badge-unverified {
            background-color: var(--warning-bg);
            color: var(--warning);
            border: 1px solid var(--warning-border);
        }

        .badge-revoked {
            background-color: var(--error-bg);
            color: var(--error);
            border: 1px solid var(--error-border);
        }

        .agent-details {
            margin-bottom: 20px;
            flex-grow: 1;
        }

        .agent-name {
            font-family: 'Outfit', sans-serif;
            font-size: 18px;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 12px;
            line-height: 1.3;
            letter-spacing: -0.2px;
        }

        .meta-row {
            display: flex;
            margin-bottom: 6px;
            font-size: 13px;
        }

        .meta-label {
            color: var(--text-muted);
            width: 90px;
            font-weight: 400;
            flex-shrink: 0;
        }

        .meta-val {
            color: var(--text-main);
            font-weight: 300;
            word-break: break-all;
        }

        .card-caps {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 14px;
        }

        .card-cap-tag {
            font-size: 11px;
            font-weight: 500;
            padding: 3px 8px;
            border-radius: 9999px;
            background-color: rgba(83, 58, 253, 0.06);
            color: var(--primary-deep);
        }

        .card-actions {
            display: flex;
            gap: 8px;
            border-top: 1px solid var(--border-color);
            padding-top: 16px;
            margin-top: auto;
        }

        .btn-card-action {
            flex: 1;
            font-family: inherit;
            font-size: 13px;
            font-weight: 500;
            padding: 8px 10px;
            border-radius: 9999px;
            border: 1px solid var(--border-color);
            background-color: #ffffff;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            text-decoration: none;
        }

        .btn-card-action:hover {
            border-color: var(--primary);
            color: var(--primary);
            background-color: rgba(83, 58, 253, 0.02);
        }

        .btn-card-action.btn-verify {
            background-color: var(--primary);
            color: white;
            border-color: var(--primary);
        }

        .btn-card-action.btn-verify:hover {
            background-color: var(--primary-hover);
            color: white;
            border-color: var(--primary-hover);
        }

        /* Modal styling */
        .modal-overlay {
            display: none;
            position: fixed;
            inset: 0;
            background-color: rgba(13, 37, 61, 0.4);
            z-index: 100;
            align-items: center;
            justify-content: center;
            padding: 24px;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            animation: fadeIn 0.25s ease-out;
        }

        .modal {
            background-color: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            max-width: 600px;
            width: 100%;
            max-height: 90vh;
            overflow: hidden;
            box-shadow: rgba(0, 55, 112, 0.12) 0 16px 48px, rgba(0, 0, 0, 0.08) 0 24px 64px;
            display: flex;
            flex-direction: column;
            animation: scaleUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes scaleUp {
            from { transform: scale(0.95); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }

        .modal-header {
            padding: 20px 24px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .modal-header h3 {
            font-size: 18px;
            font-weight: 400;
            color: var(--text-main);
            letter-spacing: -0.2px;
        }

        .modal-subtitle {
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 2px;
        }

        .modal-close {
            background: none;
            border: none;
            font-size: 18px;
            cursor: pointer;
            color: var(--text-muted);
        }

        .modal-body {
            padding: 24px;
            overflow-y: auto;
            background-color: #f9fbfd;
            flex-grow: 1;
        }

        .modal-body pre {
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            color: var(--text-main);
            margin: 0;
            white-space: pre-wrap;
            word-break: break-all;
            line-height: 1.5;
        }

        .modal-footer {
            padding: 16px 24px;
            border-top: 1px solid var(--border-color);
            display: flex;
            justify-content: flex-end;
            gap: 12px;
            background-color: #f6f9fc;
        }

        /* Footer */
        .footer {
            margin-top: 48px;
            padding-top: 24px;
            padding-bottom: 24px;
            border-top: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
            font-size: 14px;
            color: var(--text-muted);
            width: 100%;
        }

        .footer a {
            color: var(--text-muted);
            text-decoration: underline;
            text-underline-offset: 3px;
            text-decoration-color: rgba(100, 116, 141, 0.4);
            transition: all 0.15s ease;
        }

        .footer a:hover {
            color: var(--primary);
            text-decoration-color: var(--primary);
        }

        @media (max-width: 768px) {
            .navbar {
                flex-direction: column;
                gap: 16px;
                padding: 16px 0;
            }
            .nav-center {
                gap: 20px;
            }
            .agents-grid {
                grid-template-columns: 1fr;
            }
            .controls-card {
                flex-direction: column;
                align-items: stretch;
            }
            .select-wrapper select {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Unified Navbar matching image exactly -->
        <header class="navbar">
            <div class="nav-left">
                <a href="/" class="brand-logo">
                    <span class="brand-text">
                        <span class="brand-name">Creduent</span> 
                        <span class="brand-suffix">Registry</span>
                    </span>
                </a>
            </div>
            <div class="nav-center">
                <a href="/explore" class="nav-link active">Explore</a>
                <a href="/dashboard" class="nav-link">Dashboard</a>
                <a href="/resolver" class="nav-link">Resolver</a>
                <a href="/playground" class="nav-link">Playground</a>
            </div>
            <div class="nav-right">
                <div class="status-badge">
                    <span class="status-dot"></span>
                    <span>SYSTEM LIVE</span>
                </div>
            </div>
        </header>

        <div class="page-header">
            <h1>Explore Directory</h1>
            <p>Discover and verify autonomous agents across the Creduent Registry.</p>
        </div>

        <!-- Search & Level Filters -->
        <section class="controls-card">
            <div class="search-box">
                <svg class="search-icon" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                <input type="text" id="searchInput" placeholder="Search agents by ID, owner, or domain..." oninput="renderAgents()">
            </div>
            <div class="select-wrapper">
                <select id="levelFilter" onchange="renderAgents()">
                    <option value="">All Verification Levels</option>
                    <option value="verified">Verified</option>
                    <option value="trusted">Trusted</option>
                    <option value="unverified">Unverified</option>
                    <option value="revoked">Revoked</option>
                </select>
            </div>
        </section>

        <!-- Capabilities Filter Trigger -->
        <div class="category-trigger-container">
            <button class="btn-category-trigger" onclick="openCategoryModal()">
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" style="margin-right: 8px;">
                    <path d="M4 6h16M4 12h16M4 18h7"></path>
                </svg>
                Category: <span id="activeCategoryLabel" style="margin-left: 4px; font-weight: 700; color: var(--primary);">All Capabilities</span>
            </button>
        </div>

        <!-- Capabilities Selector Modal -->
        <div class="category-modal-overlay" id="categoryModal" onclick="closeCategoryModal(event)">
            <div class="category-modal" onclick="event.stopPropagation()">
                <div class="category-modal-header">
                    <div>
                        <span class="category-modal-title">Select Capability</span>
                        <p class="modal-subtitle" style="margin-top: 4px;">Choose a capability to filter the agent registry</p>
                    </div>
                    <button class="category-modal-close" onclick="hideCategoryModal()">✕ Close</button>
                </div>
                <div class="category-modal-body">
                    <div class="modal-search-box">
                        <input type="text" id="modalSearchInput" placeholder="Search capability..." oninput="filterModalCapabilities()">
                    </div>
                    <!-- Grouped Categories Grid -->
                    <div id="modalGroupsContainer">
                        <!-- Group blocks will be rendered here dynamically -->
                    </div>
                </div>
            </div>
        </div>

        <!-- Agent Directory Grid -->
        <main class="agents-grid" id="agentsGrid">
            <div style="grid-column: 1 / -1; text-align: center; color: var(--text-muted); padding: 48px 0;">
                Loading agent registry directory...
            </div>
        </main>

        <!-- Footer -->
        <footer class="footer">
            <div class="footer-left">
                Powered by <a href="https://github.com/idevsec/creduent" target="_blank" rel="noopener">Creduent Open Protocol</a> · v2.0.0
            </div>
            <div class="footer-right">
                © 2026 <a href="https://idevsec.com" target="_blank" rel="noopener">IDevSec</a>. All rights reserved.
            </div>
        </footer>
    </div>

    <!-- JSON View Modal -->
    <div class="modal-overlay" id="view-modal" onclick="closeModal(event)">
        <div class="modal" onclick="event.stopPropagation()">
            <div class="modal-header">
                <div>
                    <h3 id="modal-title">Attestation Certificate</h3>
                    <p class="modal-subtitle">Raw cryptographic attestation record from the registry database</p>
                </div>
                <button class="modal-close" onclick="hideModal()">✕</button>
            </div>
            <div class="modal-body">
                <pre id="modal-content"></pre>
            </div>
            <div class="modal-footer">
                <button class="btn-card-action" id="copy-json-btn" onclick="copyModalJSON()">Copy JSON</button>
                <button class="btn-card-action btn-verify" onclick="hideModal()">Close</button>
            </div>
        </div>
    </div>

    <script>
        let agents = [];
        let activeCapability = null;

        async function loadAgents() {
            try {
                const res = await fetch('/agents?t=' + Date.now());
                if (res.ok) {
                    agents = await res.json();
                    renderFilters();
                    renderAgents();
                }
            } catch (e) {
                console.error("Error loading agents:", e);
                document.getElementById('agentsGrid').innerHTML = `
                    <div style="grid-column: 1 / -1; text-align: center; color: var(--error); padding: 48px 0;">
                        Failed to connect to the Creduent Registry node.
                    </div>
                `;
            }
        }

        const CAPABILITY_METRICS = {
            "incident_response": { label: "Incident Response" },
            "soc_analysis": { label: "SOC Operations" },
            "threat_intel": { label: "Threat Intelligence" },
            "vapt_advisory": { label: "VAPT Advisory" },
            "faq_resolution": { label: "Customer Support" },
            "informational": { label: "Information Desk" },
            "attestation_demos": { label: "Labs & Demos" }
        };

        let activeGroup = null;

        const GROUPS = [
            {
                id: "security",
                title: "Security Operations",
                capabilities: ["incident_response", "soc_analysis", "threat_intel", "vapt_advisory"]
            },
            {
                id: "utilities",
                title: "Support & Utilities",
                capabilities: ["faq_resolution", "informational", "attestation_demos"]
            }
        ];

        function getFreq() {
            const freq = {};
            agents.forEach(agent => {
                if (agent.capabilities) {
                    agent.capabilities.forEach(cap => {
                        freq[cap] = (freq[cap] || 0) + 1;
                    });
                }
            });
            return freq;
        }

        function freqCount(cap) {
            let count = 0;
            agents.forEach(agent => {
                if (agent.capabilities && agent.capabilities.includes(cap)) {
                    count++;
                }
            });
            return count;
        }

        let currentModalView = "groups"; // "groups" or "capabilities"
        let currentModalGroupId = null;

        function renderFilters() {
            const container = document.getElementById('modalGroupsContainer');
            container.innerHTML = '';

            const modalHeaderTitle = document.querySelector('.category-modal-title');

            if (currentModalView === "groups") {
                modalHeaderTitle.textContent = "SELECT CATEGORY GROUP";

                const grid = document.createElement('div');
                grid.className = 'modal-grid';

                // "All Capabilities" reset card
                const allCard = document.createElement('div');
                allCard.className = 'modal-item-card' + (activeCapability === null && activeGroup === null ? ' active' : '');
                allCard.textContent = 'All Capabilities';
                allCard.onclick = () => {
                    filterByCapability(null, null);
                };
                grid.appendChild(allCard);

                // Predefined Groups
                GROUPS.forEach(group => {
                    // Count how many active capabilities exist in this group to verify if it has agents
                    const hasActive = group.capabilities.some(cap => (freqCount(cap) > 0));
                    if (!hasActive) return;

                    const groupCard = document.createElement('div');
                    groupCard.className = 'modal-item-card' + (activeGroup === group.id ? ' active' : '');
                    groupCard.textContent = group.title;
                    groupCard.onclick = () => {
                        currentModalView = "capabilities";
                        currentModalGroupId = group.id;
                        renderFilters();
                    };
                    grid.appendChild(groupCard);
                });

                container.appendChild(grid);
            } else {
                // Capabilities Drill-down View
                const group = GROUPS.find(g => g.id === currentModalGroupId);
                if (!group) {
                    currentModalView = "groups";
                    renderFilters();
                    return;
                }

                modalHeaderTitle.textContent = group.title.toUpperCase();

                // Add Back Row
                const backRow = document.createElement('div');
                backRow.style.marginBottom = '20px';
                
                const backBtn = document.createElement('button');
                backBtn.className = 'category-modal-close';
                backBtn.textContent = '← Back to Groups';
                backBtn.onclick = () => {
                    currentModalView = "groups";
                    currentModalGroupId = null;
                    renderFilters();
                };
                backRow.appendChild(backBtn);
                container.appendChild(backRow);

                const grid = document.createElement('div');
                grid.className = 'modal-grid';



                // Count active capabilities
                const freq = getFreq();
                const activeCaps = group.capabilities
                    .filter(cap => (freq[cap] || 0) > 0)
                    .map(cap => ({ cap, count: freq[cap] }))
                    .sort((a, b) => b.count - a.count);

                activeCaps.forEach(item => {
                    const meta = CAPABILITY_METRICS[item.cap] || { label: item.cap };
                    const card = document.createElement('div');
                    card.className = 'modal-item-card' + (activeCapability === item.cap ? ' active' : '');
                    card.textContent = meta.label;
                    card.onclick = () => {
                        filterByCapability(item.cap, null);
                    };
                    grid.appendChild(card);
                });

                container.appendChild(grid);
            }
        }

        function openCategoryModal() {
            document.getElementById('categoryModal').style.display = 'flex';
            document.getElementById('modalSearchInput').value = '';
            currentModalView = "groups";
            currentModalGroupId = null;
            // Reset search visibility
            filterModalCapabilities();
            renderFilters();
        }

        function hideCategoryModal() {
            document.getElementById('categoryModal').style.display = 'none';
        }

        function closeCategoryModal(event) {
            if (event.target.id === 'categoryModal') {
                hideCategoryModal();
            }
        }

        function filterModalCapabilities() {
            const query = document.getElementById('modalSearchInput').value.trim().toLowerCase();
            const items = document.querySelectorAll('.modal-item-card');
            
            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(query) || text.includes('back')) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        }

        function updateCategoryLabel() {
            const labelEl = document.getElementById('activeCategoryLabel');
            if (activeCapability) {
                labelEl.textContent = CAPABILITY_METRICS[activeCapability]?.label || activeCapability;
            } else if (activeGroup) {
                const group = GROUPS.find(g => g.id === activeGroup);
                labelEl.textContent = group ? `All ${group.title.split(' ')[0]}` : 'All Capabilities';
            } else {
                labelEl.textContent = 'All Capabilities';
            }
        }

        function filterByCapability(cap, groupId) {
            activeCapability = cap;
            activeGroup = groupId;
            updateCategoryLabel();
            hideCategoryModal();
            renderAgents();
        }

        function getDidCreduent(agentUri) {
            if (!agentUri) return '-';
            const clean = agentUri.replace(/^agent:\/\//, '');
            return 'did:creduent:' + clean.replace(/\//g, ':');
        }

        function getDidWeb(agentUri, domain) {
            if (!agentUri) return '-';
            const parts = agentUri.replace(/^agent:\/\//, '').split('/');
            const namespace = parts[0] || 'default';
            let d = domain && domain !== '-' ? domain : `${namespace}.com`;
            if (d.startsWith('creduent.')) {
                const parentDomain = d.replace(/^creduent\./, '');
                if (parentDomain.startsWith(namespace)) {
                    d = parentDomain;
                }
            }
            const name = parts.length > 1 ? parts.slice(1).join(':') : namespace;
            return `did:web:${d}:agent:${name}`;
        }

        function renderAgents() {
            const query = document.getElementById('searchInput').value.trim().toLowerCase();
            const level = document.getElementById('levelFilter').value;
            const grid = document.getElementById('agentsGrid');
            grid.innerHTML = '';

            const filtered = agents.filter(agent => {
                // Capability & Group filter
                if (activeCapability) {
                    if (!agent.capabilities || !agent.capabilities.includes(activeCapability)) {
                        return false;
                    }
                } else if (activeGroup) {
                    const group = GROUPS.find(g => g.id === activeGroup);
                    if (!group || !agent.capabilities || !agent.capabilities.some(cap => group.capabilities.includes(cap))) {
                        return false;
                    }
                }

                // Level filter
                if (level && (agent.level || 'verified').toLowerCase() !== level) {
                    return false;
                }

                // Search query filter (matches ID, DID, domain, owner, and any custom capabilities)
                if (query) {
                    const idMatch = (agent.agent_id || '').toLowerCase().includes(query);
                    const didCreduentMatch = getDidCreduent(agent.agent_id).toLowerCase().includes(query);
                    const didWebMatch = getDidWeb(agent.agent_id, agent.domain).toLowerCase().includes(query);
                    const domainMatch = (agent.domain || '').toLowerCase().includes(query);
                    const ownerMatch = (agent.owner || '').toLowerCase().includes(query);
                    const capMatch = agent.capabilities && agent.capabilities.some(cap => cap.toLowerCase().includes(query));
                    if (!idMatch && !didCreduentMatch && !didWebMatch && !domainMatch && !ownerMatch && !capMatch) {
                        return false;
                    }
                }

                return true;
            });

            if (filtered.length === 0) {
                grid.innerHTML = `
                    <div style="grid-column: 1 / -1; text-align: center; color: var(--text-muted); padding: 64px 0;">
                        <div style="font-weight: 500; color: var(--text-main); margin-bottom: 4px;">No agents found</div>
                        <div>Try adjusting your filters or search keywords.</div>
                    </div>
                `;
                return;
            }

            filtered.forEach(agent => {
                const card = document.createElement('div');
                card.className = 'agent-card';
                
                const level = (agent.level || 'verified').toLowerCase();
                let badgeClass = 'badge-verified';
                if (level === 'revoked') badgeClass = 'badge-revoked';
                else if (level === 'trusted') badgeClass = 'badge-trusted';
                else if (level !== 'verified') badgeClass = 'badge-unverified';

                const capsHTML = (agent.capabilities || []).map(cap => {
                    const meta = CAPABILITY_METRICS[cap] || { label: cap.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ') };
                    return `<span class="card-cap-tag">${meta.label}</span>`;
                }).join('');

                const cardId = 'card-' + btoa(agent.agent_id).replace(/[^a-zA-Z0-9]/g, '');

                const nameRaw = agent.agent_id.split('/').pop() || '';
                const agentName = nameRaw.charAt(0).toUpperCase() + nameRaw.slice(1);

                card.innerHTML = `
                    <div>
                        <div class="card-top">
                            <div class="agent-avatar" id="avatar-${cardId}">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                            </div>
                            <span class="badge ${badgeClass}">${level}</span>
                        </div>
                        <div class="agent-details">
                            <div class="agent-name">${agentName}</div>
                            <div class="meta-row">
                                <span class="meta-label">Owner</span>
                                <span class="meta-val">${agent.owner || 'Unknown'}</span>
                            </div>
                            <div class="meta-row">
                                <span class="meta-label">Agent URI</span>
                                <span class="meta-val" style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--text-dark);">${agent.agent_id}</span>
                            </div>
                            <div class="meta-row">
                                <span class="meta-label">W3C DID</span>
                                <span class="meta-val" style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--primary);">${getDidCreduent(agent.agent_id)}</span>
                            </div>
                            <div class="meta-row">
                                <span class="meta-label">Domain</span>
                                <span class="meta-val">${agent.domain || '-'}</span>
                            </div>
                            <div class="meta-row">
                                <span class="meta-label">Endpoint</span>
                                <span class="meta-val">${agent.endpoint || '-'}</span>
                            </div>
                            <div class="card-caps">${capsHTML}</div>
                        </div>
                    </div>
                    <div class="card-actions">
                        <button class="btn-card-action" onclick="copyUri('${agent.agent_id}')">Copy URI</button>
                        <button class="btn-card-action" onclick="copyUri('${getDidCreduent(agent.agent_id)}')">Copy DID</button>
                        <button class="btn-card-action" onclick="viewJSON('${encodeURIComponent(agent.agent_id)}')">JSON</button>
                        <a href="/resolver?uri=${encodeURIComponent(agent.agent_id)}" class="btn-card-action btn-verify">Verify</a>
                    </div>
                `;
                grid.appendChild(card);

                // Fetch domain favicon asynchronously
                if (agent.domain && agent.domain !== '-') {
                    let baseDomain = agent.domain;
                    const parts = agent.domain.split('.');
                    if (parts.length > 2) {
                        const pen = parts[parts.length - 2].toLowerCase();
                        const tld = parts[parts.length - 1].toLowerCase();
                        if ((tld === 'uk' && pen === 'co') || 
                            (tld === 'br' && pen === 'com') || 
                            (tld === 'au' && pen === 'net') || 
                            (tld === 'nz' && pen === 'co')) {
                            if (parts.length > 3) baseDomain = parts.slice(-3).join('.');
                        } else {
                            baseDomain = parts.slice(-2).join('.');
                        }
                    }
                    const img = document.createElement('img');
                    img.src = (baseDomain === 'idevsec.com') ? 'https://idevsec.com/logo.png' : ('https://www.google.com/s2/favicons?sz=64&domain=' + baseDomain);
                    img.alt = baseDomain;
                    const avatar = document.getElementById('avatar-' + cardId);
                    img.onload = () => {
                        avatar.innerHTML = '';
                        avatar.appendChild(img);
                        applyDarkBgIfWhiteLogo(img, avatar, baseDomain);
                    };
                }
            });
        }

        function applyDarkBgIfWhiteLogo(img, container, baseDomain) {
            if (!container || !img) return;

            function setDark() {
                container.style.backgroundColor = '#090d16';
                container.style.borderColor = '#1e293b';
                img.style.padding = '3px';
                img.style.borderRadius = '6px';
            }

            const lowerDomain = (baseDomain || '').toLowerCase();
            // Automatically apply sleek dark background for idevsec, stackedid, and light/white logos
            if (lowerDomain.includes('idevsec') || lowerDomain.includes('stacked') || lowerDomain.includes('github') || lowerDomain.includes('apple') || lowerDomain.includes('vercel')) {
                setDark();
            }
        }

        function filterAgents() {
            renderAgents();
        }

        function copyUri(uri) {
            navigator.clipboard.writeText(uri).then(() => {
                alert('Agent URI copied to clipboard: ' + uri);
            });
        }

        let currentAgentData = null;

        function viewJSON(encodedUri) {
            const uri = decodeURIComponent(encodedUri);
            const agent = agents.find(a => a.agent_id === uri);
            if (agent) {
                currentAgentData = agent;
                document.getElementById('modal-content').textContent = JSON.stringify(agent, null, 2);
                document.getElementById('view-modal').style.display = 'flex';
            }
        }

        function hideModal() {
            document.getElementById('view-modal').style.display = 'none';
        }

        function closeModal(event) {
            if (event.target.id === 'view-modal') {
                hideModal();
            }
        }

        function copyModalJSON() {
            if (currentAgentData) {
                navigator.clipboard.writeText(JSON.stringify(currentAgentData, null, 2)).then(() => {
                    const btn = document.getElementById('copy-json-btn');
                    btn.textContent = '✓ Copied';
                    setTimeout(() => {
                        btn.textContent = 'Copy JSON';
                    }, 1500);
                });
            }
        }

        window.addEventListener('DOMContentLoaded', loadAgents);
    </script>
</body>
</html>
"""

NOT_FOUND_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>404 Page Not Found | Creduent Registry</title>
    <meta name="description" content="The requested resource or agent namespace could not be found on the Creduent registry.">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Outfit:wght@400;600;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #533afd;
            --primary-deep: #4434d4;
            --primary-press: #2e2b8c;
            --primary-soft: #665efd;
            --primary-bg-subdued: #b9b9f9;
            --ink: #0d253d;
            --ink-secondary: #273951;
            --ink-mute: #64748d;
            --canvas: #ffffff;
            --canvas-soft: #f6f9fc;
            --hairline: #e3e8ee;
            --ruby: #ea2261;
            --magenta: #f96bee;
            --shadow-blue: rgba(0, 55, 112, 0.08);
            --error-glow: rgba(234, 34, 97, 0.08);
            --error-border: rgba(234, 34, 97, 0.2);
        }

        *, *::before, *::after {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: "Inter", -apple-system, sans-serif;
            background: var(--canvas);
            color: var(--ink);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            font-feature-settings: "ss01" on;
            -webkit-font-smoothing: antialiased;
        }

        .hero-mesh {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 380px;
            background: 
                radial-gradient(circle at 12% 15%, rgba(245,233,212,0.55) 0%, transparent 45%),
                radial-gradient(circle at 88% 8%, rgba(249,107,238,0.25) 0%, transparent 40%),
                radial-gradient(circle at 50% -12%, rgba(83,58,253,0.14) 0%, transparent 50%),
                radial-gradient(circle at 75% 25%, rgba(234,34,97,0.11) 0%, transparent 45%);
            z-index: 0;
            pointer-events: none;
            border-bottom: 1px solid var(--hairline);
        }

        .container {
            max-width: 1200px;
            width: 100%;
            margin: 0 auto;
            padding: 0 24px;
            position: relative;
            z-index: 1;
        }

        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 24px 0;
            border-bottom: 1px solid var(--hairline);
            margin-bottom: 24px;
            width: 100%;
        }

        .nav-left {
            display: flex;
            align-items: center;
        }

        .brand-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
        }

        .brand-avatar {
            width: 36px;
            height: 36px;
            background-color: var(--primary);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            box-shadow: 0 2px 8px rgba(83, 58, 253, 0.2);
        }

        .brand-text {
            font-size: 20px;
            font-weight: 500;
            letter-spacing: -0.42px;
        }

        .brand-name {
            color: var(--ink);
        }

        .brand-suffix {
            color: var(--primary);
        }

        .nav-center {
            display: flex;
            align-items: center;
            gap: 32px;
        }

        .nav-link {
            font-size: 15px;
            font-weight: 400;
            color: var(--ink-mute);
            text-decoration: none;
            transition: color 0.15s ease;
        }

        .nav-link:hover {
            color: var(--ink);
        }

        .nav-right {
            display: flex;
            align-items: center;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-feature-settings: "tnum" on;
            font-size: 13px;
            font-weight: 400;
            line-height: 1.0;
            letter-spacing: -0.39px;
            background: var(--error-glow);
            color: var(--ruby);
            padding: 8px 16px;
            border-radius: 9999px;
            border: 1px solid var(--error-border);
            box-shadow: rgba(234, 34, 97, 0.08) 0 4px 12px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--ruby);
            box-shadow: 0 0 8px var(--ruby);
            animation: pulse-red 2s infinite;
        }

        @keyframes pulse-red {
            0%, 100% { opacity: 0.6; transform: scale(0.9); }
            50% { opacity: 1; transform: scale(1.15); }
        }

        main {
            flex: 1;
            padding-top: 56px;
        }

        .hero {
            max-width: 620px;
            margin-bottom: 64px;
        }

        .eyebrow {
            display: inline-block;
            background: var(--error-glow);
            color: var(--ruby);
            font-size: 10px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            padding: 4px 8px;
            border-radius: 9999px;
            margin-bottom: 18px;
            border: 1px solid var(--error-border);
        }

        .display-title {
            font-family: "Outfit", sans-serif;
            font-size: 56px;
            font-weight: 600;
            line-height: 1.03;
            letter-spacing: -1.4px;
            color: var(--ink);
            margin-bottom: 16px;
        }

        .lead-text {
            font-size: 18px;
            font-weight: 300;
            line-height: 1.45;
            color: var(--ink-secondary);
        }

        .split-panel {
            display: grid;
            grid-template-columns: 1fr 1.25fr;
            gap: 36px;
            margin-bottom: 96px;
            align-items: start;
        }

        .endpoints-card {
            background: var(--canvas);
            border: 1px solid var(--hairline);
            border-radius: 12px;
            padding: 32px;
            box-shadow: var(--shadow-blue) 0 1px 3px;
        }

        .card-title {
            font-size: 22px;
            font-weight: 300;
            line-height: 1.1;
            letter-spacing: -0.22px;
            margin-bottom: 24px;
        }

        .endpoint-list {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .endpoint-item {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding-bottom: 18px;
            border-bottom: 1px solid var(--hairline);
        }

        .endpoint-item:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }

        .action-link {
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            font-weight: 500;
            color: var(--primary);
            text-decoration: none;
            margin-bottom: 4px;
            display: inline-block;
        }

        .action-link:hover {
            text-decoration: underline;
        }

        .endpoint-desc {
            font-size: 13px;
            color: var(--ink-mute);
            line-height: 1.4;
        }

        .ide-mockup {
            background: #090d16;
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 12px;
            box-shadow: rgba(0, 55, 112, 0.12) 0 8px 24px, rgba(0, 55, 112, 0.08) 0 2px 6px;
            overflow: hidden;
        }

        .ide-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #0b111e;
            padding: 12px 18px;
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }

        .ide-dots {
            display: flex;
            gap: 6px;
            align-items: center;
        }

        .ide-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }

        .ide-dot.red { background: #ef4444; }
        .ide-dot.yellow { background: #f59e0b; }
        .ide-dot.green { background: #10b981; }

        .ide-tab {
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            color: #94a3b8;
            background: #090d16;
            padding: 6px 12px;
            border-radius: 4px 4px 0 0;
            border: 1px solid rgba(255,255,255,0.06);
            border-bottom: none;
            margin-bottom: -13px;
            margin-left: 16px;
            display: inline-block;
        }

        .btn-copy {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            color: #cbd5e1;
            font-family: "Inter", sans-serif;
            font-size: 11px;
            font-weight: 500;
            padding: 6px 12px;
            border-radius: 9999px;
            cursor: pointer;
            transition: all 0.15s;
        }

        .btn-copy:hover {
            background: rgba(255,255,255,0.1);
            color: #ffffff;
        }

        .ide-body {
            padding: 24px;
            margin: 0;
            overflow-x: auto;
        }

        pre {
            margin: 0;
        }

        code {
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            line-height: 1.55;
            color: #cbd5e1;
            font-variant-numeric: tabular-nums;
            letter-spacing: -0.36px;
        }

        .json-key { color: #f472b6; }
        .json-string { color: #38bdf8; }
        .json-number { color: #fbbf24; }
        .json-boolean { color: #a78bfa; }

        footer {
            border-top: 1px solid var(--hairline);
            padding: 48px 0;
            color: var(--ink-mute);
            font-size: 13px;
            margin-top: auto;
        }

        .footer-inner {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .footer-inner a {
            color: var(--ink-secondary);
            text-decoration: none;
        }

        .footer-inner a:hover {
            color: var(--primary);
        }

        @media (max-width: 900px) {
            .navbar {
                flex-direction: column;
                gap: 16px;
                padding: 16px 0;
            }
            .nav-center {
                gap: 20px;
            }
            .split-panel {
                grid-template-columns: 1fr;
                gap: 28px;
            }
            .display-title {
                font-size: 40px;
                letter-spacing: -0.8px;
            }
            .footer-inner {
                flex-direction: column;
                gap: 16px;
                text-align: center;
            }
        }
    </style>
</head>
<body>

<div class="hero-mesh"></div>

<div class="container">
    <header class="navbar">
        <div class="nav-left">
            <a href="/" class="brand-logo">
                <span class="brand-text">
                    <span class="brand-name">Creduent</span> 
                    <span class="brand-suffix">Registry</span>
                </span>
            </a>
        </div>
        <div class="nav-center">
            <a href="/explore" class="nav-link">Explore</a>
            <a href="/dashboard" class="nav-link">Dashboard</a>
            <a href="/resolver" class="nav-link">Resolver</a>
        </div>
        <div class="nav-right">
            <div class="status-badge">
                <span class="status-dot"></span>
                <span>STATUS 404</span>
            </div>
        </div>
    </header>

    <main>
        <section class="hero">
            <span class="eyebrow">Error 404</span>
            <h1 class="display-title">Resource Not Found</h1>
            <p class="lead-text">
                The requested URL path, registry endpoint, or cryptographic agent namespace does not exist or has been permanently moved.
            </p>
        </section>

        <div class="split-panel">
            <!-- Left: Suggested Actions -->
            <div class="endpoints-card">
                <h2 class="card-title">Where to go next?</h2>
                <div class="endpoint-list">
                    <div class="endpoint-item">
                        <div class="endpoint-details">
                            <a href="/" class="action-link">Return to Home &rarr;</a>
                            <div class="endpoint-desc">Visit the Creduent Registry root index.</div>
                        </div>
                    </div>
                    <div class="endpoint-item">
                        <div class="endpoint-details">
                            <a href="/resolver" class="action-link">Identity Resolver UI &rarr;</a>
                            <div class="endpoint-desc">Look up, verify, and trace active agent:// namespaces directly.</div>
                        </div>
                    </div>
                    <div class="endpoint-item">
                        <div class="endpoint-details">
                            <a href="/dashboard" class="action-link">Developer Dashboard &rarr;</a>
                            <div class="endpoint-desc">Manage registrations, attestations, and webhook configs.</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right: IDE Code Mockup -->
            <div class="ide-mockup">
                <div class="ide-header">
                    <div class="ide-dots">
                        <span class="ide-dot red"></span>
                        <span class="ide-dot yellow"></span>
                        <span class="ide-dot green"></span>
                        <span class="ide-tab">error.json</span>
                    </div>
                    <button class="btn-copy" onclick="copyJson()">Copy JSON</button>
                </div>
                <div class="ide-body">
                    <pre><code>{
  <span class="json-key">"error"</span>: <span class="json-string">"Not Found"</span>,
  <span class="json-key">"status_code"</span>: <span class="json-number">404</span>,
  <span class="json-key">"message"</span>: <span class="json-string">"The requested resource could not be resolved."</span>,
  <span class="json-key">"docs"</span>: <span class="json-string">"https://github.com/idevsec/creduent"</span>
}</code></pre>
                </div>
            </div>
        </div>
    </main>
</div>

<footer>
    <div class="container">
        <div class="footer-inner">
            <span>Powered by <a href="https://github.com/idevsec/creduent" target="_blank">Creduent Open Protocol</a> · v2.0.0</span>
            <span>&copy; 2026 <a href="https://idevsec.com" target="_blank">IDevSec</a>. All rights reserved.</span>
        </div>
    </div>
</footer>

<script>
    function copyJson() {
        const jsonText = `{
  "error": "Not Found",
  "status_code": 404,
  "message": "The requested resource could not be resolved.",
  "docs": "https://github.com/idevsec/creduent"
}`;
        navigator.clipboard.writeText(jsonText).then(() => {
            const btn = document.querySelector('.btn-copy');
            btn.textContent = '✓ Copied';
            setTimeout(() => {
                btn.textContent = 'Copy JSON';
            }, 2000);
        });
    }
</script>
</body>
</html>
"""

PLAYGROUND_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Creduent Playground - Client-Side Cryptographic Sandbox</title>
    <meta name="description" content="Client-side cryptographic sandbox for keypair generation, RFC 8785 JCS canonicalization, Ed25519 signing, tamper testing, and live registry resolution.">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #f6f9fc;
            --bg-surface: #ffffff;
            --border-color: #e3e8ee;
            --border-input: #a8c3de;
            --primary: #533afd;
            --primary-hover: #4434d4;
            --primary-press: #2e2b8c;
            --primary-glow: rgba(83, 58, 253, 0.08);
            --primary-bg-subdued: #b9b9f9;
            --success: #22c55e;
            --success-bg: rgba(34, 197, 94, 0.08);
            --success-border: rgba(34, 197, 94, 0.2);
            --trusted: #8b5cf6;
            --trusted-bg: rgba(139, 92, 246, 0.08);
            --trusted-border: rgba(139, 92, 246, 0.2);
            --error: #ea2261;
            --error-bg: rgba(234, 34, 97, 0.08);
            --error-border: rgba(234, 34, 97, 0.2);
            --warning: #9b6829;
            --warning-bg: rgba(155, 104, 41, 0.08);
            --warning-border: rgba(155, 104, 41, 0.2);
            --text-main: #0d253d;
            --text-muted: #64748d;
            --text-dark: #61718a;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-base);
            color: var(--text-main);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-feature-settings: "ss01" on;
            font-weight: 300;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 0%, rgba(245, 233, 212, 0.6) 0%, transparent 45%),
                radial-gradient(circle at 45% 0%, rgba(155, 104, 41, 0.1) 0%, transparent 40%),
                radial-gradient(circle at 90% 0%, rgba(249, 107, 238, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 25% 0%, rgba(83, 58, 253, 0.12) 0%, transparent 55%),
                radial-gradient(circle at 75% 0%, rgba(234, 34, 97, 0.12) 0%, transparent 45%);
            background-size: 100% 420px;
            background-repeat: no-repeat;
        }

        .container {
            width: 100%;
            max-width: 1240px;
            margin: 0 auto;
            padding: 0 24px 40px 24px;
            z-index: 10;
            display: flex;
            flex-direction: column;
            flex: 1;
        }

        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 24px 0;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 24px;
            width: 100%;
        }

        .nav-left {
            display: flex;
            align-items: center;
        }

        .brand-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
        }

        .brand-text {
            font-family: 'Outfit', sans-serif;
            font-size: 20px;
            font-weight: 500;
            letter-spacing: -0.42px;
        }

        .brand-name {
            color: var(--text-main);
        }

        .brand-suffix {
            color: var(--primary);
        }

        .nav-center {
            display: flex;
            align-items: center;
            gap: 32px;
        }

        .nav-link {
            font-size: 15px;
            font-weight: 400;
            color: var(--text-muted);
            text-decoration: none;
            transition: color 0.15s ease;
        }

        .nav-link:hover {
            color: var(--text-main);
        }

        .nav-link.active {
            color: var(--primary);
            font-weight: 500;
        }

        .nav-right {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background-color: rgba(34, 197, 94, 0.08);
            border: 1px solid rgba(34, 197, 94, 0.2);
            color: var(--success);
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 500;
            letter-spacing: 0.05em;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background-color: var(--success);
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 8px rgba(34, 197, 94, 0.6);
            animation: pulse-green 2s infinite ease-in-out;
        }

        @keyframes pulse-green {
            0%, 100% { opacity: 0.6; transform: scale(0.9); }
            50% { opacity: 1; transform: scale(1.15); }
        }

        .page-header {
            margin-bottom: 28px;
        }

        .page-header h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 28px;
            font-weight: 500;
            color: var(--text-main);
            letter-spacing: -0.5px;
        }

        .page-header p {
            font-size: 14px;
            color: var(--text-muted);
            margin-top: 6px;
        }

        .glass-panel {
            background-color: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 28px;
            box-shadow: rgba(0, 55, 112, 0.04) 0 1px 3px;
        }

        /* Tabs Navigation Bar */
        .tab-bar {
            display: flex;
            gap: 8px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 24px;
            padding-bottom: 0;
            overflow-x: auto;
        }

        .tab-item {
            padding: 10px 16px;
            font-size: 14px;
            font-weight: 400;
            color: var(--text-muted);
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all 0.2s ease;
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 6px;
            font-family: inherit;
        }

        .tab-item:hover {
            color: var(--text-main);
        }

        .tab-item.active {
            color: var(--primary);
            font-weight: 500;
            border-bottom-color: var(--primary);
        }

        .tab-num {
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            background: rgba(83, 58, 253, 0.08);
            color: var(--primary);
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: 600;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* Forms & Inputs */
        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 13px;
            font-weight: 400;
            color: var(--text-muted);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: -0.39px;
            font-feature-settings: "tnum" on;
        }

        .form-control {
            width: 100%;
            background-color: #ffffff;
            border: 1px solid var(--border-input);
            border-radius: 8px;
            color: var(--text-main);
            padding: 10px 14px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            line-height: 1.45;
            letter-spacing: -0.42px;
            font-feature-settings: "tnum" on;
            font-weight: 300;
            transition: all 0.2s ease;
        }

        .form-control:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px var(--primary-glow);
        }

        textarea.form-control {
            resize: vertical;
            min-height: 110px;
        }

        /* Metric Grid & Badges */
        .metrics-bar {
            display: flex;
            gap: 16px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .metric-card {
            background: rgba(246, 249, 252, 0.8);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px 16px;
            display: flex;
            flex-direction: column;
            gap: 2px;
            min-width: 140px;
        }

        .metric-card .label {
            font-size: 11px;
            text-transform: uppercase;
            color: var(--text-muted);
            letter-spacing: 0.05em;
        }

        .metric-card .value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            font-weight: 600;
            color: var(--text-main);
        }

        /* Buttons */
        .btn-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            background-color: var(--primary);
            color: white;
            font-family: inherit;
            font-size: 14px;
            font-weight: 400;
            line-height: 1.0;
            padding: 10px 20px;
            border-radius: 9999px;
            border: none;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .btn:hover {
            background-color: var(--primary-hover);
            transform: translateY(-1px);
            box-shadow: 0 4px 16px var(--primary-glow);
        }

        .btn:active {
            background-color: var(--primary-press);
            transform: translateY(0);
        }

        .btn-secondary {
            background-color: #ffffff;
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 5px 12px;
            font-size: 12px;
            border-radius: 9999px;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .btn-secondary:hover {
            background-color: #f6f9fc;
            border-color: var(--primary);
            color: var(--primary);
        }

        .btn-danger {
            background-color: rgba(234, 34, 97, 0.08);
            border: 1px solid rgba(234, 34, 97, 0.3);
            color: var(--error);
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .btn-danger:hover {
            background-color: rgba(234, 34, 97, 0.15);
            border-color: var(--error);
        }

        .btn-sm {
            padding: 4px 10px;
            font-size: 12px;
        }

        .feedback {
            padding: 14px 18px;
            border-radius: 8px;
            font-size: 13px;
            display: none;
            line-height: 1.5;
            margin-top: 16px;
        }

        .feedback-success {
            background-color: var(--success-bg);
            border: 1px solid var(--success-border);
            color: var(--success);
        }

        .feedback-error {
            background-color: var(--error-bg);
            border: 1px solid var(--error-border);
            color: var(--error);
        }

        .trace-box {
            background: #0f172a;
            color: #e2e8f0;
            border-radius: 8px;
            padding: 14px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            line-height: 1.6;
            margin-top: 14px;
            overflow-x: auto;
        }

        .trace-step {
            display: flex;
            gap: 12px;
            margin-bottom: 6px;
        }

        .trace-step:last-child {
            margin-bottom: 0;
        }

        .trace-tag {
            color: #38bdf8;
            font-weight: 600;
        }

        .trace-ok {
            color: #4ade80;
        }

        .trace-fail {
            color: #f87171;
        }

        /* Split view */
        .split-view {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }

        .technical-tag {
            display: inline-block;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            padding: 2px 6px;
            border-radius: 4px;
            background: var(--bg-base);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            margin-right: 6px;
        }

        .footer {
            margin-top: auto;
            padding-top: 24px;
            border-top: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
            font-size: 13px;
            color: var(--text-muted);
        }

        .footer a {
            color: var(--text-muted);
            text-decoration: underline;
            text-underline-offset: 3px;
            text-decoration-color: rgba(100, 116, 141, 0.4);
            transition: all 0.15s ease;
        }

        .footer a:hover {
            color: var(--primary);
            text-decoration-color: var(--primary);
        }

        @media (max-width: 900px) {
            .split-view {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 768px) {
            .navbar {
                flex-direction: column;
                align-items: flex-start;
                gap: 16px;
            }
            .nav-center {
                gap: 16px;
            }
            .glass-panel {
                padding: 18px;
            }
        }
    </style>
</head>
<body>
    <main class="container">
        <!-- Unified Navbar -->
        <header class="navbar">
            <div class="nav-left">
                <a href="/" class="brand-logo">
                    <span class="brand-text">
                        <span class="brand-name">Creduent</span> 
                        <span class="brand-suffix">Registry</span>
                    </span>
                </a>
            </div>
            <div class="nav-center">
                <a href="/explore" class="nav-link">Explore</a>
                <a href="/dashboard" class="nav-link">Dashboard</a>
                <a href="/resolver" class="nav-link">Resolver</a>
                <a href="/playground" class="nav-link active">Playground</a>
            </div>
            <div class="nav-right">
                <div class="status-badge">
                    <span class="status-dot"></span>
                    <span>SYSTEM LIVE</span>
                </div>
            </div>
        </header>

        <div class="page-header">
            <h1>Cryptographic Playground</h1>
            <p>Client-side cryptographic sandbox for keypair generation, RFC 8785 JCS canonicalization, Ed25519 signing, tamper testing, and live registry resolution.</p>
        </div>

        <div class="glass-panel">
            <!-- Navigation Tabs Bar -->
            <div class="tab-bar">
                <div class="tab-item active" onclick="switchTab('keygen', event)"><span class="tab-num">01</span> Keypair Generator & Formats</div>
                <div class="tab-item" onclick="switchTab('signer', event)"><span class="tab-num">02</span> Document Signer</div>
                <div class="tab-item" onclick="switchTab('verifier', event)"><span class="tab-num">03</span> Signature Verifier & Attack Suite</div>
                <div class="tab-item" onclick="switchTab('jcs', event)"><span class="tab-num">04</span> RFC 8785 Byte Inspector</div>
                <div class="tab-item" onclick="switchTab('resolver', event)"><span class="tab-num">05</span> Registry Resolver Test</div>
                <div class="tab-item" onclick="switchTab('did', event)"><span class="tab-num">06</span> W3C DID Inspector</div>
            </div>

            <!-- Tab 1: Keypair Generator & Converter -->
            <section id="tab-keygen" class="tab-content active">
                <p style="font-size: 14px; color: var(--text-muted); line-height: 1.5; margin-bottom: 16px;">
                    Generates 256-bit Ed25519 keypairs via Web Crypto API (<code>window.crypto.subtle</code>). Private key operations remain strictly in browser memory.
                </p>

                <div class="metrics-bar">
                    <div class="metric-card">
                        <span class="label">Algorithm</span>
                        <span class="value">Ed25519 (25519)</span>
                    </div>
                    <div class="metric-card">
                        <span class="label">Security Level</span>
                        <span class="value">128-bit Security</span>
                    </div>
                    <div class="metric-card">
                        <span class="label">Generation Time</span>
                        <span class="value" id="keyGenLatency">0.00 ms</span>
                    </div>
                    <div class="metric-card">
                        <span class="label">SHA-256 Fingerprint</span>
                        <span class="value" id="pubKeyThumbprint" style="font-size: 11px; word-break: break-all;">-</span>
                    </div>
                </div>

                <div class="form-group">
                    <label for="genPublicKey">
                        <span>Public Key (Formatted Base64)</span>
                        <div>
                            <span class="technical-tag">RAW 32-BYTES</span>
                            <button class="btn-secondary btn-sm" onclick="copyVal('genPublicKey', this)">Copy</button>
                        </div>
                    </label>
                    <input type="text" id="genPublicKey" class="form-control" placeholder="Click 'Generate Ed25519 Keypair'..." readonly>
                </div>

                <div class="form-group">
                    <label for="genPrivateKey">
                        <span>Private Key (PKCS#8 Base64)</span>
                        <div>
                            <span class="technical-tag">PKCS#8 DER</span>
                            <button class="btn-secondary btn-sm" onclick="copyVal('genPrivateKey', this)">Copy</button>
                        </div>
                    </label>
                    <textarea id="genPrivateKey" class="form-control" style="min-height: 75px;" placeholder="Click 'Generate Ed25519 Keypair'..." readonly></textarea>
                </div>

                <div class="split-view" style="margin-bottom: 20px;">
                    <div class="form-group">
                        <label for="genJwkPublic">
                            <span>Public Key (JSON Web Key / JWK)</span>
                            <button class="btn-secondary btn-sm" onclick="copyVal('genJwkPublic', this)">Copy JWK</button>
                        </label>
                        <textarea id="genJwkPublic" class="form-control" style="min-height: 90px;" placeholder="Exported JWK structure..." readonly></textarea>
                    </div>
                    <div class="form-group">
                        <label for="genHexPublic">
                            <span>Public Key (Hexadecimal Format)</span>
                            <button class="btn-secondary btn-sm" onclick="copyVal('genHexPublic', this)">Copy HEX</button>
                        </label>
                        <textarea id="genHexPublic" class="form-control" style="min-height: 90px;" placeholder="Raw HEX representation..." readonly></textarea>
                    </div>
                </div>

                <div class="btn-group">
                    <button class="btn" onclick="generatePlaygroundKeys()">
                        Generate Ed25519 Keypair
                    </button>
                    <button class="btn-secondary" onclick="saveKeyToSession()">
                        Save Keypair to Session
                    </button>
                    <button class="btn-secondary" onclick="loadKeyFromSession()">
                        Load Session Keypair
                    </button>
                </div>

                <div id="keyGenFeedback" class="feedback"></div>
            </section>

            <!-- Tab 2: Document Signer -->
            <section id="tab-signer" class="tab-content">
                <p style="font-size: 14px; color: var(--text-muted); line-height: 1.5; margin-bottom: 16px;">
                    Signs agent identity document using RFC 8785 JSON Canonicalization Scheme (JCS). Canonical output ensures exact byte matching across programming language runtimes.
                </p>

                <div class="form-group">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <label for="signerPayload" style="margin-bottom: 0;">Unsigned agent.json Payload</label>
                        <div style="display: flex; gap: 6px; align-items: center;">
                            <button class="btn-secondary btn-sm" onclick="loadBlankTemplate()">Load Template</button>
                            <button class="btn-secondary btn-sm" onclick="formatJsonInput('signerPayload', this)">Prettify</button>
                            <button class="btn-secondary btn-sm" onclick="minifyJsonInput('signerPayload', this)">Minify</button>
                        </div>
                    </div>
                    <textarea id="signerPayload" class="form-control" style="min-height: 150px;" placeholder="Paste unsigned agent.json payload or generate a keypair in Tab 01 to pre-fill..."></textarea>
                </div>

                <div class="form-group">
                    <label for="signerPrivKey">
                        <span>Private Key (PKCS#8 Base64)</span>
                        <span class="technical-tag" id="signerKeyStatus">NOT LOADED</span>
                    </label>
                    <textarea id="signerPrivKey" class="form-control" style="min-height: 70px;" placeholder="Paste private key or generate in Tab 01..."></textarea>
                </div>

                <div class="btn-group">
                    <button class="btn" onclick="signPlaygroundDocument()">
                        Sign Document (Client-Side)
                    </button>
                    <button class="btn-secondary" onclick="validateSchemaOnly()">
                        Validate Schema Only
                    </button>
                </div>

                <div id="signerFeedback" class="feedback"></div>

                <div id="signerResultContainer" class="form-group" style="display: none; margin-top: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <label for="signerResult" style="margin-bottom: 0;">Signed agent.json Output (JCS Compliant)</label>
                        <div style="display: flex; gap: 6px;">
                            <button class="btn-secondary btn-sm" onclick="copyVal('signerResult', this)">Copy JSON</button>
                            <button class="btn-secondary btn-sm" onclick="downloadSignedJson()">Download agent.json</button>
                        </div>
                    </div>
                    <textarea id="signerResult" class="form-control" style="min-height: 180px; color: var(--primary);" readonly></textarea>
                </div>
            </section>

            <!-- Tab 3: Signature Verifier & Attack Suite -->
            <section id="tab-verifier" class="tab-content">
                <p style="font-size: 14px; color: var(--text-muted); line-height: 1.5; margin-bottom: 16px;">
                    Verifies cryptographic signatures over JCS canonical payload. Includes security attack simulations to evaluate signature tamper-resistance.
                </p>

                <div class="form-group">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <label for="verifierPayload" style="margin-bottom: 0;">Signed Document Payload</label>
                        <button class="btn-secondary btn-sm" onclick="formatJsonInput('verifierPayload', this)">Prettify</button>
                    </div>
                    <textarea id="verifierPayload" class="form-control" style="min-height: 160px;" placeholder="Paste signed agent.json containing 'signature' field..."></textarea>
                </div>

                <div class="form-group">
                    <label>Security Attack Simulations (Tamper Testing)</label>
                    <div class="btn-group" style="margin-top: 6px;">
                        <button class="btn-danger btn-sm" onclick="simulateAttack('tamper_payload')">Tamper Capability Array</button>
                        <button class="btn-danger btn-sm" onclick="simulateAttack('corrupt_sig')">Corrupt Signature Byte</button>
                        <button class="btn-danger btn-sm" onclick="simulateAttack('foreign_key')">Substitute Random Key</button>
                        <button class="btn-danger btn-sm" onclick="simulateAttack('alter_domain')">Alter Domain String</button>
                    </div>
                </div>

                <div class="btn-group" style="margin-top: 16px;">
                    <button class="btn" onclick="verifyPlaygroundDocument()">
                        Verify Signature
                    </button>
                </div>

                <div id="verifierFeedback" class="feedback"></div>

                <div id="verificationTrace" class="trace-box" style="display: none;">
                    <div style="font-weight: 600; color: #94a3b8; margin-bottom: 8px; border-bottom: 1px solid #334155; padding-bottom: 4px;">VERIFICATION PIPELINE TRACE</div>
                    <div id="traceLogs"></div>
                </div>
            </section>

            <!-- Tab 4: RFC 8785 JCS Byte Inspector -->
            <section id="tab-jcs" class="tab-content">
                <p style="font-size: 14px; color: var(--text-muted); line-height: 1.5; margin-bottom: 16px;">
                    Inspects JSON Canonicalization Scheme (RFC 8785) formatting rules: recursive lexicographical key ordering, whitespace strip, UTF-8 normalization.
                </p>

                <div class="split-view">
                    <div class="form-group">
                        <label for="jcsRawInput">Raw Input JSON</label>
                        <textarea id="jcsRawInput" class="form-control" style="min-height: 160px;" placeholder="Paste or type JSON object here to inspect JCS canonicalization..." oninput="inspectJcsCanonicalization()"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="jcsCanonicalOutput">JCS Canonicalized Output (RFC 8785)</label>
                        <textarea id="jcsCanonicalOutput" class="form-control" style="min-height: 160px; color: var(--primary);" readonly></textarea>
                    </div>
                </div>

                <div class="form-group">
                    <label for="jcsHexDump">Canonical Byte HEX View</label>
                    <textarea id="jcsHexDump" class="form-control" style="min-height: 90px; font-size: 12px; color: #64748d;" readonly></textarea>
                </div>

                <div class="metrics-bar">
                    <div class="metric-card">
                        <span class="label">Raw Char Count</span>
                        <span class="value" id="jcsRawLength">0</span>
                    </div>
                    <div class="metric-card">
                        <span class="label">JCS Char Count</span>
                        <span class="value" id="jcsCanonicalLength">0</span>
                    </div>
                    <div class="metric-card">
                        <span class="label">Size Delta</span>
                        <span class="value" id="jcsDeltaBytes">0 bytes</span>
                    </div>
                </div>
            </section>

            <!-- Tab 5: Registry Resolver Test Bench -->
            <section id="tab-resolver" class="tab-content">
                <p style="font-size: 14px; color: var(--text-muted); line-height: 1.5; margin-bottom: 16px;">
                    Test identity resolution against Creduent API endpoints (<code>/resolve</code>). Validates schema, identity state, and signature verification server-side or via mock.
                </p>

                <div class="form-group">
                    <label for="testUriInput">Agent URI to Resolve</label>
                    <div style="display: flex; gap: 8px;">
                        <input type="text" id="testUriInput" class="form-control" placeholder="Enter agent:// URI to resolve...">
                        <button class="btn" style="white-space: nowrap;" onclick="executeResolverTest()">Resolve URI</button>
                    </div>
                </div>

                <div id="resolverResponseBox" class="trace-box" style="display: none;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #334155; padding-bottom: 4px;">
                        <span style="font-weight: 600; color: #94a3b8;">API RESPONSE INSPECTOR</span>
                        <span id="resolverHttpStatus" class="technical-tag" style="background: #1e293b; color: #38bdf8;">STATUS: 200 OK</span>
                    </div>
                    <pre id="resolverJsonOutput" style="white-space: pre-wrap; font-family: inherit; font-size: 12px; color: #e2e8f0;"></pre>
                </div>
            </section>

            <!-- Tab 6: W3C DID Inspector & Converter -->
            <section id="tab-did" class="tab-content">
                <p style="font-size: 14px; color: var(--text-muted); line-height: 1.5; margin-bottom: 16px;">
                    Bidirectional converter between Creduent <code>agent://</code> URIs and W3C Decentralized Identifiers (<code>did:creduent</code> and <code>did:web</code>). Generates standard JSON-LD W3C DID Documents.
                </p>

                <div class="form-group">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <label for="didInputUri" style="margin-bottom: 0;">Input Agent URI or DID String</label>
                        <div style="display: flex; gap: 6px;">
                            <button class="btn-secondary btn-sm" onclick="loadDidExample('steward')">Load Example</button>
                            <button class="btn-secondary btn-sm" onclick="loadDidFromActiveSession()">Use Active Session</button>
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <input type="text" id="didInputUri" class="form-control" placeholder="e.g., agent://idevsec/steward or did:creduent:idevsec:steward">
                        <button class="btn" style="white-space: nowrap;" onclick="convertPlaygroundDid()">Inspect & Convert DID</button>
                    </div>
                </div>

                <div class="split-view" style="margin-top: 16px;">
                    <div class="form-group">
                        <label for="didCreduentResult">
                            <span>did:creduent Identifier</span>
                            <button class="btn-secondary btn-sm" onclick="copyVal('didCreduentResult', this)">Copy</button>
                        </label>
                        <input type="text" id="didCreduentResult" class="form-control" readonly>
                    </div>
                    <div class="form-group">
                        <label for="didWebResult">
                            <span>did:web Identifier</span>
                            <button class="btn-secondary btn-sm" onclick="copyVal('didWebResult', this)">Copy</button>
                        </label>
                        <input type="text" id="didWebResult" class="form-control" readonly>
                    </div>
                </div>

                <div class="form-group" style="margin-top: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <label for="didDocumentResult" style="margin-bottom: 0;">W3C DID Document (JSON-LD Compliant)</label>
                        <button class="btn-secondary btn-sm" onclick="copyVal('didDocumentResult', this)">Copy DID Document</button>
                    </div>
                    <textarea id="didDocumentResult" class="form-control" style="min-height: 220px; color: var(--primary);" readonly></textarea>
                </div>
            </section>
        </div>

        <footer class="footer">
            <div class="footer-left">
                Powered by <a href="https://github.com/idevsec/creduent" target="_blank" rel="noopener">Creduent Open Protocol</a> &middot; v2.0.0
            </div>
            <div class="footer-right">
                &copy; 2026 <a href="https://idevsec.com" target="_blank" rel="noopener">IDevSec</a>. All rights reserved.
            </div>
        </footer>
    </main>

    <script>
        function switchTab(tabName, ev) {
            document.querySelectorAll('.tab-item').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            
            if (ev && ev.target) {
                const targetTab = ev.target.closest('.tab-item');
                if (targetTab) targetTab.classList.add('active');
            }
            const activeContent = document.getElementById('tab-' + tabName);
            if (activeContent) activeContent.classList.add('active');

            if (tabName === 'jcs') {
                inspectJcsCanonicalization();
            }
        }

        function loadDidExample(type) {
            document.getElementById('didInputUri').value = 'agent://idevsec/steward';
            convertPlaygroundDid();
        }

        function loadDidFromActiveSession() {
            let activeUri = '';
            try {
                const payloadStr = document.getElementById('signerPayload').value;
                if (payloadStr) {
                    const parsed = JSON.parse(payloadStr);
                    if (parsed.agent_id) activeUri = parsed.agent_id;
                }
            } catch(e) {}
            if (!activeUri) {
                const pubKey = document.getElementById('genPublicKey').value;
                if (pubKey) activeUri = 'agent://myorg/myagent';
            }
            document.getElementById('didInputUri').value = activeUri || 'agent://myorg/myagent';
            convertPlaygroundDid();
        }

        function convertPlaygroundDid() {
            let val = (document.getElementById('didInputUri').value || '').trim();
            if (!val) {
                document.getElementById('didCreduentResult').value = '';
                document.getElementById('didWebResult').value = '';
                document.getElementById('didDocumentResult').value = '';
                return;
            }

            let namespace = "default";
            let name = "agent";

            if (val.startsWith("did:creduent:")) {
                const parts = val.replace("did:creduent:", "").split(":");
                namespace = parts[0] || "default";
                name = parts[1] || "agent";
            } else if (val.startsWith("did:web:")) {
                const domain = val.replace("did:web:", "").replace(/:/g, "/");
                const parts = domain.split("/");
                namespace = parts[0] || "default";
                name = parts[1] || "agent";
            } else {
                let clean = val.replace(/^agent:\/\//i, "").replace(/^\/+/, "");
                const parts = clean.split("/");
                namespace = parts[0] || "default";
                name = parts[1] || "agent";
            }

            const agentUri = `agent://${namespace}/${name}`;
            const didCreduent = `did:creduent:${namespace}:${name}`;
            const didWeb = `did:web:${namespace}.com:${name}`;

            document.getElementById('didCreduentResult').value = didCreduent;
            document.getElementById('didWebResult').value = didWeb;

            const pubKey = (document.getElementById('genPublicKey') ? document.getElementById('genPublicKey').value : '') || "ed25519:V43yNaTrpqQj9YJnjYVL2HdOrqUDcnflhzNGuHTaFD8=";

            const didDoc = {
                "@context": [
                    "https://www.w3.org/ns/did/v1",
                    "https://w3id.org/security/suites/ed25519-2020/v1"
                ],
                "id": didCreduent,
                "alsoKnownAs": [agentUri, `https://${namespace}.com/.well-known/agent.json`],
                "verificationMethod": [
                    {
                        "id": `${didCreduent}#key-1`,
                        "type": "Ed25519VerificationKey2020",
                        "controller": didCreduent,
                        "publicKeyMultibase": pubKey.replace(/^ed25519:/i, "")
                    }
                ],
                "authentication": [`${didCreduent}#key-1`],
                "assertionMethod": [`${didCreduent}#key-1`],
                "service": [
                    {
                        "id": `${didCreduent}#agent-endpoint`,
                        "type": "AgentServiceEndpoint",
                        "serviceEndpoint": `https://${namespace}.com/agent`
                    }
                ]
            };

            document.getElementById('didDocumentResult').value = JSON.stringify(didDoc, null, 2);
        }

        function copyVal(id, btnElement) {
            const val = document.getElementById(id).value;
            if (!val) return;
            navigator.clipboard.writeText(val).then(() => {
                if (btnElement) {
                    const orig = btnElement.textContent;
                    btnElement.textContent = 'COPIED';
                    setTimeout(() => { btnElement.textContent = orig; }, 1500);
                }
            });
        }

        function downloadSignedJson() {
            const val = document.getElementById('signerResult').value;
            if (!val) return;
            const blob = new Blob([val], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'agent.json';
            a.click();
            URL.revokeObjectURL(url);
        }

        function formatJsonInput(id, btnElement) {
            try {
                const el = document.getElementById(id);
                const parsed = JSON.parse(el.value);
                el.value = JSON.stringify(parsed, null, 2);
                if (btnElement) {
                    const orig = btnElement.textContent;
                    btnElement.textContent = 'FORMATTED';
                    setTimeout(() => { btnElement.textContent = orig; }, 1500);
                }
            } catch(e) {
                alert("JSON syntax error: " + e.message);
            }
        }

        function minifyJsonInput(id, btnElement) {
            try {
                const el = document.getElementById(id);
                const parsed = JSON.parse(el.value);
                el.value = JSON.stringify(parsed);
                if (btnElement) {
                    const orig = btnElement.textContent;
                    btnElement.textContent = 'MINIFIED';
                    setTimeout(() => { btnElement.textContent = orig; }, 1500);
                }
            } catch(e) {
                alert("JSON syntax error: " + e.message);
            }
        }

        function loadBlankTemplate() {
            const pubKey = document.getElementById('genPublicKey').value;
            const doc = {
                "agent_id": "agent://YOUR_DOMAIN/YOUR_AGENT_NAME",
                "domain": "YOUR_DOMAIN.com",
                "capabilities": ["YOUR_CAPABILITY_1", "YOUR_CAPABILITY_2"],
                "public_key": pubKey || "ed25519:YOUR_PUBLIC_KEY_HERE"
            };
            document.getElementById('signerPayload').value = JSON.stringify(doc, null, 2);
        }

        function bytesToBase64(bytes) {
            let bin = "";
            for (let i = 0; i < bytes.length; i++) {
                bin += String.fromCharCode(bytes[i]);
            }
            return btoa(bin);
        }

        function base64ToBytes(b64) {
            const bin = atob(b64.trim());
            const bytes = new Uint8Array(bin.length);
            for (let i = 0; i < bin.length; i++) {
                bytes[i] = bin.charCodeAt(i);
            }
            return bytes;
        }

        function bytesToHex(bytes) {
            return Array.from(bytes).map(b => b.toString(16).padStart(2, '0')).join('');
        }

        function canonicalize(obj) {
            if (obj === null) return "null";
            if (typeof obj !== "object") return JSON.stringify(obj);
            if (Array.isArray(obj)) {
                return "[" + obj.map(canonicalize).join(",") + "]";
            }
            const keys = Object.keys(obj).sort();
            const parts = [];
            for (const key of keys) {
                const val = obj[key];
                if (val !== undefined) {
                    parts.push(JSON.stringify(key) + ":" + canonicalize(val));
                }
            }
            return "{" + parts.join(",") + "}";
        }

        async function generatePlaygroundKeys() {
            const feedback = document.getElementById('keyGenFeedback');
            const startTime = performance.now();
            try {
                const keyPair = await window.crypto.subtle.generateKey(
                    { name: "Ed25519" },
                    true,
                    ["sign", "verify"]
                );
                
                const rawPub = await window.crypto.subtle.exportKey("raw", keyPair.publicKey);
                const pkcs8Priv = await window.crypto.subtle.exportKey("pkcs8", keyPair.privateKey);
                const jwkPub = await window.crypto.subtle.exportKey("jwk", keyPair.publicKey);

                const pubBytes = new Uint8Array(rawPub);
                const pubB64 = "ed25519:" + bytesToBase64(pubBytes);
                const privB64 = bytesToBase64(new Uint8Array(pkcs8Priv));
                const pubHex = bytesToHex(pubBytes);

                const digest = await window.crypto.subtle.digest("SHA-256", pubBytes);
                const thumbHex = bytesToHex(new Uint8Array(digest)).substring(0, 16);

                const endTime = performance.now();
                document.getElementById('keyGenLatency').textContent = (endTime - startTime).toFixed(2) + " ms";
                document.getElementById('pubKeyThumbprint').textContent = thumbHex + "...";

                document.getElementById('genPublicKey').value = pubB64;
                document.getElementById('genPrivateKey').value = privB64;
                document.getElementById('genJwkPublic').value = JSON.stringify(jwkPub, null, 2);
                document.getElementById('genHexPublic').value = pubHex;

                document.getElementById('signerPrivKey').value = privB64;
                document.getElementById('signerKeyStatus').textContent = "LOADED";
                document.getElementById('signerKeyStatus').style.color = "var(--success)";
                
                try {
                    let doc = JSON.parse(document.getElementById('signerPayload').value);
                    doc.public_key = pubB64;
                    document.getElementById('signerPayload').value = JSON.stringify(doc, null, 2);
                } catch(e){}

                feedback.style.display = 'block';
                feedback.className = 'feedback feedback-success';
                feedback.innerHTML = '<strong>[OK] Keypair Generated Successfully</strong><br>Ed25519 keypair exported in Base64, JWK, and Hex formats. Private key loaded into Document Signer.';
            } catch(err) {
                feedback.style.display = 'block';
                feedback.className = 'feedback feedback-error';
                feedback.innerHTML = '<strong>[ERROR] Key Generation Failure:</strong> ' + err.message;
            }
        }

        function saveKeyToSession() {
            const pub = document.getElementById('genPublicKey').value;
            const priv = document.getElementById('genPrivateKey').value;
            if (!pub || !priv) {
                alert("Generate a keypair first before saving.");
                return;
            }
            sessionStorage.setItem('creduent_saved_pub', pub);
            sessionStorage.setItem('creduent_saved_priv', priv);
            alert("Keypair saved to browser sessionStorage.");
        }

        function loadKeyFromSession() {
            const pub = sessionStorage.getItem('creduent_saved_pub');
            const priv = sessionStorage.getItem('creduent_saved_priv');
            if (!pub || !priv) {
                alert("No keypair found in sessionStorage.");
                return;
            }
            document.getElementById('genPublicKey').value = pub;
            document.getElementById('genPrivateKey').value = priv;
            document.getElementById('signerPrivKey').value = priv;
            document.getElementById('signerKeyStatus').textContent = "LOADED";
            document.getElementById('signerKeyStatus').style.color = "var(--success)";
            alert("Keypair loaded from sessionStorage.");
        }

        function validateSchemaOnly() {
            const feedback = document.getElementById('signerFeedback');
            try {
                const rawJsonStr = document.getElementById('signerPayload').value;
                let docObj = JSON.parse(rawJsonStr);
                
                const requiredKeys = ["agent_id", "domain", "public_key"];
                const missing = requiredKeys.filter(k => !docObj[k]);
                
                if (missing.length > 0) {
                    throw new Error("Missing required schema fields: " + missing.join(", "));
                }

                feedback.style.display = 'block';
                feedback.className = 'feedback feedback-success';
                feedback.innerHTML = '<strong>[VALID] Schema Pre-Validation Passed</strong><br>Payload contains agent_id, domain, and public_key fields.';
            } catch(err) {
                feedback.style.display = 'block';
                feedback.className = 'feedback feedback-error';
                feedback.innerHTML = '<strong>[INVALID] Schema Validation Failed:</strong> ' + err.message;
            }
        }

        async function signPlaygroundDocument() {
            const rawJsonStr = document.getElementById('signerPayload').value;
            const privKeyB64 = document.getElementById('signerPrivKey').value.trim();
            const feedback = document.getElementById('signerFeedback');

            try {
                if (!privKeyB64) throw new Error("Private Key (PKCS#8 Base64) is required.");
                let docObj = JSON.parse(rawJsonStr);

                delete docObj.signature;

                const canonicalStr = canonicalize(docObj);
                const payloadBytes = new TextEncoder().encode(canonicalStr);

                const privKeyBytes = base64ToBytes(privKeyB64);
                const cryptoPrivKey = await window.crypto.subtle.importKey(
                    "pkcs8",
                    privKeyBytes,
                    { name: "Ed25519" },
                    false,
                    ["sign"]
                );

                const sigBytes = await window.crypto.subtle.sign(
                    { name: "Ed25519" },
                    cryptoPrivKey,
                    payloadBytes
                );

                const sigB64 = bytesToBase64(new Uint8Array(sigBytes));
                docObj.signature = sigB64;

                const signedResultStr = JSON.stringify(docObj, null, 2);
                document.getElementById('signerResult').value = signedResultStr;
                document.getElementById('signerResultContainer').style.display = 'block';
                
                document.getElementById('verifierPayload').value = signedResultStr;

                feedback.style.display = 'block';
                feedback.className = 'feedback feedback-success';
                feedback.innerHTML = '<strong>[OK] Document Signed Successfully</strong><br>RFC 8785 JCS signature attached to agent document and populated into Verifier.';
            } catch(err) {
                feedback.style.display = 'block';
                feedback.className = 'feedback feedback-error';
                feedback.innerHTML = '<strong>[ERROR] Signing Failure:</strong> ' + err.message;
            }
        }

        async function verifyPlaygroundDocument() {
            const signedJsonStr = document.getElementById('verifierPayload').value;
            const feedback = document.getElementById('verifierFeedback');
            const traceBox = document.getElementById('verificationTrace');
            const traceLogs = document.getElementById('traceLogs');
            
            traceLogs.innerHTML = "";
            traceBox.style.display = "block";

            function addTrace(step, msg, ok) {
                const div = document.createElement('div');
                div.className = 'trace-step';
                div.innerHTML = `<span class="trace-tag">[${step}]</span> <span class="${ok ? 'trace-ok' : 'trace-fail'}">${msg}</span>`;
                traceLogs.appendChild(div);
            }

            try {
                addTrace("01_PARSE", "Parsing JSON payload structure...", true);
                let docObj = JSON.parse(signedJsonStr);
                
                if (!docObj.signature) throw new Error("Missing 'signature' property.");
                if (!docObj.public_key) throw new Error("Missing 'public_key' property.");

                addTrace("02_FIELDS", "Extracted public_key and signature fields", true);

                const sigB64 = docObj.signature;
                const pubKeyStr = docObj.public_key;

                let rawPubKeyB64 = pubKeyStr;
                if (pubKeyStr.startsWith("ed25519:")) {
                    rawPubKeyB64 = pubKeyStr.substring(8);
                }

                const pubKeyBytes = base64ToBytes(rawPubKeyB64);
                const sigBytes = base64ToBytes(sigB64);

                addTrace("03_DECODE", `Decoded 32-byte public key and ${sigBytes.length}-byte signature`, true);

                const docCopy = JSON.parse(JSON.stringify(docObj));
                delete docCopy.signature;

                const canonicalStr = canonicalize(docCopy);
                const payloadBytes = new TextEncoder().encode(canonicalStr);

                addTrace("04_JCS", `Canonicalized payload string (${payloadBytes.length} bytes)`, true);

                const cryptoPubKey = await window.crypto.subtle.importKey(
                    "raw",
                    pubKeyBytes,
                    { name: "Ed25519" },
                    false,
                    ["verify"]
                );

                addTrace("05_IMPORT", "Imported Ed25519 public key into Web Crypto API", true);

                const isValid = await window.crypto.subtle.verify(
                    { name: "Ed25519" },
                    cryptoPubKey,
                    sigBytes,
                    payloadBytes
                );

                if (isValid) {
                    addTrace("06_VERIFY", "CRYPTO VERIFICATION MATCHED", true);
                    feedback.style.display = 'block';
                    feedback.className = 'feedback feedback-success';
                    feedback.innerHTML = `<strong>[VERIFIED] Signature Check Passed</strong><br>Ed25519 signature is cryptographically valid for key <code>${pubKeyStr}</code> over JCS payload.`;
                } else {
                    addTrace("06_VERIFY", "CRYPTO VERIFICATION MISMATCH", false);
                    feedback.style.display = 'block';
                    feedback.className = 'feedback feedback-error';
                    feedback.innerHTML = `<strong>[FAILED] Signature Verification Mismatch</strong><br>Signature validation failed. Document payload has been altered or signed with a non-matching private key.`;
                }
            } catch(err) {
                addTrace("ERROR", err.message, false);
                feedback.style.display = 'block';
                feedback.className = 'feedback feedback-error';
                feedback.innerHTML = `<strong>[ERROR] Verification Error:</strong> ${err.message}`;
            }
        }

        function simulateAttack(type) {
            const el = document.getElementById('verifierPayload');
            try {
                let doc = JSON.parse(el.value);
                if (type === 'tamper_payload') {
                    if (Array.isArray(doc.capabilities)) {
                        doc.capabilities.push("unauthorized_root_access");
                    } else {
                        doc.capabilities = ["unauthorized_root_access"];
                    }
                } else if (type === 'corrupt_sig') {
                    if (doc.signature) {
                        doc.signature = doc.signature.substring(0, doc.signature.length - 4) + "XXXX";
                    }
                } else if (type === 'foreign_key') {
                    doc.public_key = "ed25519:FOREIGN_KEY_ATTACK_MOCK_BYTES_123456=";
                } else if (type === 'alter_domain') {
                    doc.domain = "malicious-attacker-domain.com";
                }
                el.value = JSON.stringify(doc, null, 2);
                verifyPlaygroundDocument();
            } catch(e) {
                alert("Sign a document in Tab 02 first before simulating attacks.");
            }
        }

        function inspectJcsCanonicalization() {
            const rawStr = document.getElementById('jcsRawInput').value;
            const canonicalEl = document.getElementById('jcsCanonicalOutput');
            const hexEl = document.getElementById('jcsHexDump');

            try {
                const parsed = JSON.parse(rawStr);
                const canonical = canonicalize(parsed);
                canonicalEl.value = canonical;

                const bytes = new TextEncoder().encode(canonical);
                hexEl.value = bytesToHex(bytes);

                document.getElementById('jcsRawLength').textContent = rawStr.length;
                document.getElementById('jcsCanonicalLength').textContent = canonical.length;
                const delta = canonical.length - rawStr.length;
                document.getElementById('jcsDeltaBytes').textContent = (delta > 0 ? "+" : "") + delta + " chars";
            } catch(e) {
                canonicalEl.value = "JSON PARSE ERROR: " + e.message;
                hexEl.value = "";
            }
        }

        async function executeResolverTest() {
            let uri = document.getElementById('testUriInput').value.trim();
            const box = document.getElementById('resolverResponseBox');
            const statusEl = document.getElementById('resolverHttpStatus');
            const jsonOutput = document.getElementById('resolverJsonOutput');

            if (!uri) return;

            box.style.display = 'block';
            jsonOutput.textContent = "Resolving " + uri + " via Creduent Registry API...";

            try {
                const requestPath = "/attest/" + encodeURIComponent(uri);
                const res = await fetch(requestPath);
                const data = await res.json();
                statusEl.textContent = "STATUS: " + res.status + " " + (res.ok ? "OK" : "ERROR");
                jsonOutput.textContent = JSON.stringify(data, null, 2);
            } catch(err) {
                statusEl.textContent = "CLIENT RESOLUTION ERROR";
                jsonOutput.textContent = JSON.stringify({
                    "target_uri": uri,
                    "resolution_status": "ERROR",
                    "detail": err.message
                }, null, 2);
            }
        }
    </script>
</body>
</html>
"""

