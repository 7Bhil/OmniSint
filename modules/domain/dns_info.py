import socket
import json
from typing import Dict, Any
import whois
from core.console import console
from core.network import request as network_request

def get_ip_info(ip):
    try:
        # Using ip-api.com for quick IP info
        url = f"http://ip-api.com/json/{ip}"
        res = network_request(url, timeout=5)
        if res.get("status_code") == 200:
            data = json.loads(res["text"])
            if data.get("status") == "success":
                return {
                    "Country": data.get("country"),
                    "City": data.get("city"),
                    "ISP": data.get("isp"),
                    "Org": data.get("org")
                }
    except Exception:
        pass
    return None

def run(domain: str) -> Dict[str, Any]:
    console.print(f"[info]Starting DNS and IP Check for '{domain}'...[/info]")
    results: Dict[str, Any] = {"domain": domain}
    
    try:
        ip = socket.gethostbyname(domain)
        console.print(f"[success][+] IP Address resolved:[/success] {ip}")
        results["ip_address"] = ip
        
        info = get_ip_info(ip)
        if info:
            console.print("[info]IP Geolocation & ISP Info:[/info]")
            results["geolocation"] = info
            for key, value in info.items():
                console.print(f"  [dim]- {key}:[/dim] [white]{value}[/white]")
        else:
            console.print("[warning][-] Could not retrieve detailed IP info.[/warning]")
            results["geolocation"] = None
            
        console.print("[info]Querying WHOIS Data...[/info]")
        try:
            w = whois.whois(domain)
            results["whois"] = {"registrar": w.registrar, "creation_date": str(w.creation_date), "expiration_date": str(w.expiration_date)}
            console.print(f"  [dim]- Registrar:[/dim] [white]{w.registrar}[/white]")
            console.print(f"  [dim]- Created:[/dim] [white]{w.creation_date}[/white]")
            console.print(f"  [dim]- Expires:[/dim] [white]{w.expiration_date}[/white]")
        except Exception as e:
            console.print(f"[warning][-] WHOIS query failed: {e}[/warning]")
            
    except socket.gaierror:
        console.print(f"[danger][!] Failed to resolve IP for {domain}[/danger]")
        results["ip_address"] = "error"
        
    return results
