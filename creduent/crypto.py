# NOTE: Sync with sdk/creduent/crypto.py
import jcs

def canonicalize(obj) -> str:
    """
    Canonicalize JSON object according to RFC 8785 (JCS) using the jcs library.
    Returns a UTF-8 string.
    """
    return jcs.canonicalize(obj).decode('utf-8')
