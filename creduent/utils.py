# NOTE: Sync with sdk/creduent/utils.py
import ipaddress
import socket
import requests
from fastapi import HTTPException
from urllib.parse import urlparse, urljoin

def is_private_ip(ip_str: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        return False

def safe_requests_get(url: str, timeout: int = 5, allow_private: bool = False) -> requests.Response:
    """
    Safe version of requests.get that prevents SSRF by blocking access
    to private IP ranges, including redirect targets, and pinning the IP.
    """
    from urllib.parse import urlunparse
    history = []
    current_url = url
    for _ in range(5):  # Follow max 5 redirects
        parsed = urlparse(current_url)
        host = parsed.netloc.split(':')[0]
        try:
            ip = socket.gethostbyname(host)
            if not allow_private and is_private_ip(ip):
                raise HTTPException(status_code=400, detail="Access to private IP ranges is blocked.")
        except socket.gaierror:
            # If DNS resolution fails here, let requests handle the connection error
            ip = None
            
        if ip:
            # Rewrite URL to use the resolved IP to prevent DNS Rebinding / TOCTOU
            port_suffix = f":{parsed.netloc.split(':')[1]}" if len(parsed.netloc.split(':')) > 1 else ""
            new_netloc = f"{ip}{port_suffix}"
            ip_url = urlunparse((parsed.scheme, new_netloc, parsed.path, parsed.params, parsed.query, parsed.fragment))
            headers = {"Host": host}
            
            verify_ssl = True
            if parsed.scheme == "https":
                verify_ssl = False
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                
            response = requests.get(ip_url, headers=headers, verify=verify_ssl, timeout=timeout, allow_redirects=False)
        else:
            response = requests.get(current_url, timeout=timeout, allow_redirects=False)
            
        if response.is_redirect:
            history.append(response)
            next_url = response.headers.get('location')
            if not next_url:
                break
            current_url = urljoin(current_url, next_url)
        else:
            response.history = history
            return response
            
    # Final request outside the loop
    parsed = urlparse(current_url)
    host = parsed.netloc.split(':')[0]
    try:
        ip = socket.gethostbyname(host)
        if not allow_private and is_private_ip(ip):
            raise HTTPException(status_code=400, detail="Access to private IP ranges is blocked.")
    except socket.gaierror:
        ip = None
        
    if ip:
        port_suffix = f":{parsed.netloc.split(':')[1]}" if len(parsed.netloc.split(':')) > 1 else ""
        new_netloc = f"{ip}{port_suffix}"
        ip_url = urlunparse((parsed.scheme, new_netloc, parsed.path, parsed.params, parsed.query, parsed.fragment))
        headers = {"Host": host}
        
        verify_ssl = True
        if parsed.scheme == "https":
            verify_ssl = False
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
        response = requests.get(ip_url, headers=headers, verify=verify_ssl, timeout=timeout, allow_redirects=False)
    else:
        response = requests.get(current_url, timeout=timeout, allow_redirects=False)
        
    response.history = history
    return response


def load_dotenv():
    """
    Manually loads .env.local or .env file from the project base directory
    into os.environ for local testing/development.
    """
    import os
    # Try to find base dir (where .env.local resides)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    for filename in ['.env.local', '.env']:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        if '=' in line:
                            key, val = line.split('=', 1)
                            key = key.strip()
                            val = val.strip()
                            # Strip quotes
                            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                                val = val[1:-1]
                            # Set and overwrite in environment
                            os.environ[key] = val
            except Exception as e:
                print(f"[-] Warning: Failed to load environment file {filename}: {e}")
