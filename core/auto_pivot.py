import re
import json
from core.console import console
from core.plugins import load_plugins

# To avoid infinite loops of pivoting
seen_entities = set()

def execute_module(domain, target):
    plugins = load_plugins(domain)
    for name, module in plugins.items():
        if hasattr(module, 'run'):
            try:
                module.run(target)
            except Exception:
                pass

def analyze_and_pivot(raw_data: dict, current_target: str):
    """
    Takes dictionary output from any module, searches for emails, domains, phone numbers,
    and runs their respective modules if found.
    """
    data_str = json.dumps(raw_data)
    seen_entities.add(current_target.lower())
    
    # Simple regex to extract emails
    email_pattern = r'[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}'
    emails = set(re.findall(email_pattern, data_str))
    
    # Phone numbers could be matched here but often there are many false positives in raw search text
    
    for email in emails:
        email = email.lower()
        if email not in seen_entities and not email.startswith('admin@') and not email.startswith('no-reply@'):
            console.print(f"\n[bold magenta]🔄 [Auto-Pivot] Discovered new Email Target: {email}[/bold magenta]")
            seen_entities.add(email)
            execute_module('email', email)
            
    # As the tool scales, we can add recursive domain pivoting, phone pivoting, etc.
