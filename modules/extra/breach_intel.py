import json
from typing import Dict, Any
from core.console import console
from core.network import request as network_request

# This module uses the public HaveIBeenPwned API (Breaches endpoint)
# Note: For free users, the API is rate-limited and requires a header.
# We'll use a simplified check or a mock for demonstration in this Elite build.

from core.config import Config

def check_breaches(target):
    try:
        # HIBP supports both emails and phone numbers
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{target}"
        headers = {}
        if Config.HIBP_API_KEY:
            headers["hibp-api-key"] = Config.HIBP_API_KEY
            
        res = network_request(url, headers=headers, timeout=5)
        
        status_code = res.get("status_code", 0)
        
        if status_code == 200:
            return json.loads(res["text"])
        elif status_code == 404:
            return []
        elif status_code == 401:
            return "API_KEY_REQUIRED"
    except Exception:
        pass
    return None

def run(target: str) -> Dict[str, Any]:
    is_phone = target.startswith('+') or target.isdigit()
    label = "Phone Number" if is_phone else "Email"
    
    console.print(f"[neon]⚡ Checking Data Breaches for {label}:[/neon] [white]{target}[/white]")
    results: Dict[str, Any] = {"target": target, "type": label}
    
    breaches = check_breaches(target)
    
    if isinstance(breaches, list):
        if breaches:
            console.print(f"  [danger][!] POISONED![/danger] Found in [bold red]{len(breaches)}[/bold red] public data leaks.")
            results["breach_count"] = len(breaches)
            # Limit display to first 5
            display_breaches = breaches[:5] if isinstance(breaches, list) else []
            for b in display_breaches:
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
