import os
import time
import requests

def check_hibp_breaches(email: str) -> int:
    """
    Checks the HaveIBeenPwned API for the number of breaches for a given email.
    Uses the real API if HIBP_API_KEY is provided, otherwise falls back to a
    demo-ready mock that varies based on email content.
    """
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
                breaches = response.json()
                return len(breaches)
            elif response.status_code == 404:
                return 0
            elif response.status_code == 429:
                if attempt < max_retries - 1:
                    retry_after = float(response.headers.get("Retry-After", 2))
                    time.sleep(retry_after)
                    continue
                else:
                    print("Error: HIBP API rate limit exceeded after retries.")
                    return 0
            elif response.status_code == 401:
                print("Error: HIBP API Key is invalid or unauthorized.")
                return 0
            else:
                print(f"Error checking HIBP API: HTTP {response.status_code}")
                return 0

        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            print(f"Exception checking HIBP API: {str(e)}")
            return 0

    return 0

def calculate_risk_score(email: str, device_info=None) -> dict:
    base_score = 100

    breach_count = check_hibp_breaches(email)
    breach_penalty = breach_count * -10

    password_penalty = -15

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
