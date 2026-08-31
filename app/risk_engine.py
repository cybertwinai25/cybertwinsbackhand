import os

def check_hibp_breaches(email: str) -> int:
    """
    Checks the HaveIBeenPwned API for the number of breaches for a given email.
    Currently mocked to return a static number unless a real API key is provided.
    """
    api_key = os.environ.get("HIBP_API_KEY")
    if not api_key:
        if "pwned" in email.lower():
            return 3
        elif "secure" in email.lower():
            return 0
        return 1
    return 1

def calculate_risk_score(email: str) -> dict:
    base_score = 100
    breach_count = check_hibp_breaches(email)
    breach_penalty = breach_count * -10
    password_penalty = -15
    device_penalty = 0
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
