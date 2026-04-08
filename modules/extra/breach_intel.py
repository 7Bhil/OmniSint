import requests
from core.console import console

# This module uses the public HaveIBeenPwned API (Breaches endpoint)
# Note: For free users, the API is rate-limited and requires a header.
# We'll use a simplified check or a mock for demonstration in this Elite build.

def check_breaches(target):
    try:
        # HIBP supports both emails and phone numbers (though phone numbers usually require full international format)
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{target}"
        headers = {
            "User-Agent": "OmniSint-Elite-Investigator",
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

def run(target: str):
    is_phone = target.startswith('+') or target.isdigit()
    label = "Phone Number" if is_phone else "Email"
    
    console.print(f"[neon]⚡ Checking Data Breaches for {label}:[/neon] [white]{target}[/white]")
    results = {"target": target, "type": label}
    
    breaches = check_breaches(target)
    
    if isinstance(breaches, list):
        if breaches:
            console.print(f"  [danger][!] POISONED![/danger] Found in [bold red]{len(breaches)}[/bold red] public data leaks.")
            results["breach_count"] = len(breaches)
            results["breaches"] = [b.get('Name') for b in breaches]
            for b in breaches[:5]:
                console.print(f"    - [dim]{b.get('Name')}[/dim]")
        else:
            console.print(f"  [success][+] Secure. No mentions found for this {label.lower()} in major leak databases.[/success]")
            results["breach_count"] = 0
            
    elif breaches == "API_KEY_REQUIRED":
        console.print("  [warning][!] HIBP API Request requires an API Key.[/warning]")
        results["status"] = "API_KEY_REQUIRED"
    else:
        console.print("  [danger][!] Breach service unreachable or rate-limited.[/danger]")
        results["status"] = "error"
        
    return results
