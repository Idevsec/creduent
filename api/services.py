import os
import sys
from datetime import datetime, timezone
from fastapi import HTTPException

# Add parent directory to path to allow importing from creduent package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from creduent.utils import is_private_ip, safe_requests_get, resolve_ips


def execute_agent_capabilities(domain: str, capability: str) -> dict:
    """
    Executes DNS, OSINT, or vulnerability scan tasks on a domain and returns findings.
    """
    domain = domain.strip().lower()
    if domain.startswith("http://"):
        domain = domain[7:]
    if domain.startswith("https://"):
        domain = domain[8:]
    domain = domain.split("/")[0]

    if capability not in ["dns_lookup", "osint", "vulnerability_scan"]:
        raise HTTPException(
            status_code=400, detail=f"Unsupported capability: {capability}"
        )

    results = {
        "domain": domain,
        "capability": capability,
        "scanned_at": datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "status": "pending",
    }

    # 1. DNS Lookup Capability
    if capability == "dns_lookup":
        try:
            ips = resolve_ips(domain)
            if not ips:
                raise Exception("No IP addresses resolved")
            for ip in ips:
                if is_private_ip(ip):
                    raise HTTPException(
                        status_code=400,
                        detail="Access to private IP ranges is blocked.",
                    )
            results.update({"status": "success", "ip": ips[0]})
        except HTTPException:
            raise
        except Exception as e:
            results.update({"status": "failed", "ip": None, "error": str(e)})

    # 2. OSINT Footprint Capability
    elif capability == "osint":
        # Get IP first
        try:
            ips = resolve_ips(domain)
            for ip in ips:
                if is_private_ip(ip):
                    raise HTTPException(
                        status_code=400,
                        detail="Access to private IP ranges is blocked.",
                    )
            ip_address = ips[0] if ips else None
        except HTTPException:
            raise
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

            results.update(
                {
                    "status": "success",
                    "ip": ip_address,
                    "server": server,
                    "powered_by": powered_by,
                    "status_code": response.status_code,
                    "redirects_count": redirects_count,
                    "final_url": final_url,
                }
            )
        except Exception as e:
            # Fallback to plain HTTP if HTTPS fails
            try:
                url = f"http://{domain}"
                response = safe_requests_get(url, timeout=5)
                headers = response.headers
                results.update(
                    {
                        "status": "success",
                        "ip": ip_address,
                        "server": headers.get("Server", "Unknown"),
                        "powered_by": headers.get("X-Powered-By", "None"),
                        "status_code": response.status_code,
                        "redirects_count": len(response.history),
                        "final_url": response.url,
                    }
                )
            except Exception as inner_e:
                results.update(
                    {
                        "status": "failed",
                        "ip": ip_address,
                        "error": f"HTTP request failed: {str(inner_e)}",
                    }
                )

    # 3. Vulnerability Grade Check Capability
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
            results.update(
                {
                    "status": "failed",
                    "error": "Could not connect to domain to run header-based vulnerability scan.",
                }
            )
        else:
            findings = []

            # HSTS Check
            if "Strict-Transport-Security" not in headers:
                findings.append(
                    {
                        "id": "missing_hsts",
                        "severity": "medium",
                        "description": "Strict-Transport-Security (HSTS) header is missing. Man-in-the-middle attacks possible.",
                    }
                )

            # Clickjacking Check
            if (
                "X-Frame-Options" not in headers
                and "frame-ancestors" not in headers.get("Content-Security-Policy", "")
            ):
                findings.append(
                    {
                        "id": "missing_x_frame_options",
                        "severity": "medium",
                        "description": "X-Frame-Options header is missing. Vulnerable to Clickjacking attacks.",
                    }
                )

            # CSP Check
            if "Content-Security-Policy" not in headers:
                findings.append(
                    {
                        "id": "missing_csp",
                        "severity": "high",
                        "description": "Content-Security-Policy (CSP) is not configured. High risk of XSS attacks.",
                    }
                )

            # MIME sniffing Check
            if "X-Content-Type-Options" not in headers:
                findings.append(
                    {
                        "id": "missing_x_content_type",
                        "severity": "low",
                        "description": "X-Content-Type-Options header is missing. Vulnerable to MIME-sniffing attacks.",
                    }
                )

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

            results.update(
                {
                    "status": "success",
                    "security_grade": grade,
                    "vulnerabilities_found": missing_count,
                    "findings": findings,
                }
            )

    return results
