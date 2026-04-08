import requests
from core.console import console

# This module uses the public HaveIBeenPwned API (Breaches endpoint)
# Note: For free users, the API is rate-limited and requires a header.
# We'll use a simplified check or a mock for demonstration in this Elite build.

def check_breaches(email):
    try:
        # Simplified public lookup via a secondary reliable source for OSINT
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        headers = {
            "User-Agent": "OmniSint-Elite-Investigator",
            # "hibp-api-key": "REDACTED" - User would normally provide this
        }
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return []
        elif response.status_code == 401:
            return "API_KEY_REQUIRED"
    except Exception:
        pass
    return None

def run(email: str):
    console.print(f"[neon]⚡ Checking Data Breaches for:[/neon] [white]{email}[/white]")
    results = {"email": email}
    
    breaches = check_breaches(email)
    
    if isinstance(breaches, list):
        if breaches:
            console.print(f"  [danger][!] POISONED![/danger] Found in [bold red]{len(breaches)}[/bold red] public data leaks.")
            results["breach_count"] = len(breaches)
            results["breaches"] = [b.get('Name') for b in breaches]
            for b in breaches[:5]:
                console.print(f"    - [dim]{b.get('Name')}[/dim]")
        else:
            console.print("  [success][+] Secure. No mentions found in major leak databases.[/success]")
            results["breach_count"] = 0
            
    elif breaches == "API_KEY_REQUIRED":
        # Graceful fallback/explanation for Elite version
        console.print("  [warning][!] HIBP API Request requires an API Key.[/warning]")
        console.print("  [dim]Skipping deep leak check...[/dim]")
        results["status"] = "API_KEY_REQUIRED"
    else:
        console.print("  [danger][!] Breach service unreachable or rate-limited.[/danger]")
        results["status"] = "error"
        
    return results
