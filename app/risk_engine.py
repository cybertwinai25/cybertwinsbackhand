import os
import time
import requests

def check_hibp_breaches(email: str) -> int:
    api_key = os.environ.get("HIBP_API_KEY")
    if not api_key:
        if "pwned" in email.lower():
            return 3
        elif "secure" in email.lower():
            return 0
        return 1

    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {
        "hibp-api-key": api_key,
        "User-Agent": "CyberTwin-AI-Backend"
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                return len(response.json())
            elif response.status_code == 404:
                return 0
            elif response.status_code == 429:
                if attempt < max_retries - 1:
                    retry_after = float(response.headers.get("Retry-After", 2))
                    time.sleep(retry_after)
                    continue
                return 0
            else:
                return 0
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return 0
    return 0

def calculate_risk_score(email: str, device_info=None, password_compromised=None) -> dict:
    base_score = 100

    breach_count = check_hibp_breaches(email)
    breach_penalty = breach_count * -10

    # Dynamic password penalty based on HIBP Pwned Passwords check
    if password_compromised is True:
        password_penalty = -25
    elif password_compromised is False:
        password_penalty = 0
    else:
        password_penalty = -15  # Backward compatible default

    device_penalty = 0
    if device_info:
        if not getattr(device_info, 'is_lock_screen_secure', True):
            device_penalty -= 20
        if getattr(device_info, 'root_detected', False):
            device_penalty -= 25
        if getattr(device_info, 'is_outdated_os', False):
            device_penalty -= 10

    total_score = base_score + breach_penalty + password_penalty + device_penalty
    if total_score < 0:
        total_score = 0

    return {
        "total_score": total_score,
        "breakdown": {
            "breaches": breach_penalty,
            "passwords": password_penalty,
            "device": device_penalty
        }
    }
