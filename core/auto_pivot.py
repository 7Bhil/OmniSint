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
    
    # Advanced Entity Extraction
    email_pattern = r'[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}'
    btc_pattern = r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b|bc1[a-z0-9]{39,59}\b'
    eth_pattern = r'\b0x[a-fA-F0-9]{40}\b'
    
    emails = set(re.findall(email_pattern, data_str))
    wallets = set(re.findall(btc_pattern, data_str)) | set(re.findall(eth_pattern, data_str))
    
    # Extract emails from discovered lists if present (from dorking/breaches)
    discovered_emails = raw_data.get("discovered_emails", [])
    for email in discovered_emails:
        email = email.lower()
        if email not in seen_entities:
            console.print(f"\n[purple]🔄 [Auto-Pivot] Pivoting on Discovered Email: {email}[/purple]")
            seen_entities.add(email)
            results = execute_module('email', email, seen_entities)
            pivot_results.update(results)

    # Extract names and trigger a 'username' style search as a proxy for identity
    discovered_names = raw_data.get("discovered_names", [])
    for name in discovered_names:
        clean_name = name.lower().replace(" ", "")
        if clean_name not in seen_entities:
            console.print(f"\n[purple]🔄 [Auto-Pivot] Pivoting on Discovered Name: {name}[/purple]")
            seen_entities.add(clean_name)
            # We use 'username' logic for name investigation (social accounts etc)
            results = execute_module('username', clean_name, seen_entities)
            pivot_results.update(results)

    return pivot_results
