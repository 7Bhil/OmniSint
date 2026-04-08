import re
import json
from core.console import console
from core.plugins import load_plugins

# To avoid infinite loops of pivoting
def execute_module(domain, target, seen_entities):
    plugins = load_plugins(domain)
    module_results = {}
    for name, module in plugins.items():
        if hasattr(module, 'run'):
            try:
                result = module.run(target)
                if result:
                    module_results[f"{domain}_{name}_{target}"] = result
                    # Recursively analyze discoverd data from this pivot
                    recursive_results = analyze_and_pivot(result, target, seen_entities)
                    module_results.update(recursive_results)
            except Exception:
                pass
    return module_results

def analyze_and_pivot(raw_data: dict, current_target: str, seen_entities: set):
    """
    Takes dictionary output from any module, searches for emails, domains, phone numbers,
    and runs their respective modules if found.
    """
    data_str = json.dumps(raw_data)
    seen_entities.add(current_target.lower())
    
    pivot_results = {}
    
    # Simple regex to extract emails
    email_pattern = r'[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}'
    emails = set(re.findall(email_pattern, data_str))
    
    for email in emails:
        email = email.lower()
        if email not in seen_entities and not email.startswith('admin@') and not email.startswith('no-reply@'):
            console.print(f"\n[bold magenta]🔄 [Auto-Pivot] Discovered new Email Target: {email}[/bold magenta]")
            seen_entities.add(email)
            results = execute_module('email', email, seen_entities)
            pivot_results.update(results)
            
    return pivot_results
