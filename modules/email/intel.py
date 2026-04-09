import dns.resolver
from typing import List, Dict, Any
from core.console import console

DISPOSABLE_DOMAINS = [
    "mailinator.com", "10minutemail.com", "guerrillamail.com", "tempmail.com", "yopmail.com", "trashmail.com"
]

def check_disposable(domain: str) -> bool:
    return domain.lower() in DISPOSABLE_DOMAINS

def get_dns_records(domain: str, record_type: str):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [str(rdata) for rdata in answers]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout, dns.resolver.NoNameservers):
        return []

def run(email: str) -> Dict[str, Any]:
    console.print(f"[info]Starting Email OSINT for '{email}'...[/info]")
    results: Dict[str, Any] = {"email": email}
    
    if "@" not in email:
        console.print("[danger][!] Invalid email address.[/danger]")
        results["error"] = "Invalid email format"
        return results
        
    username, domain = email.split("@", 1)
    results["domain"] = domain
    results["username"] = username
    
    # 1. Check if disposable
    is_disposable = check_disposable(domain)
    if is_disposable:
        console.print("[danger][!] WARNING: This is a known disposable/temporary email domain![/danger]")
    else:
        console.print("[success][+] Not a known disposable email.[/success]")
    results["is_disposable"] = is_disposable
    
    # 2. Check MX Records (Does it receive mail?)
    console.print("[info]Checking Mail Exchange (MX) records...[/info]")
    mx_records = get_dns_records(domain, 'MX')
    if mx_records:
        primary_mx = mx_records[0].split()[-1]
        console.print(f"[success][+] MX Records Found: {len(mx_records)} detected (Primary: {primary_mx})[/success]")
        results["mx_records"] = mx_records
    else:
        console.print("[warning][-] No MX records found. This domain might not receive emails.[/warning]")
        results["mx_records"] = []
        
    # 3. Check TXT Records (SPF/DMARC)
    console.print("[info]Checking TXT/SPF records (Spoofing Protection)...[/info]")
    txt_records = get_dns_records(domain, 'TXT')
    spf_found = False
    for txt in txt_records:
        if "v=spf1" in txt:
            console.print(f"[success][+] SPF Record Found:[/success] {txt}")
            spf_found = True
            break
            
    if not spf_found:
        console.print("[dim][-] No explicit SPF record found.[/dim]")
        
    results["txt_records"] = txt_records
    results["spf_found"] = spf_found
    
    return results
