import trio
import httpx
import holehe.modules
from holehe.core import import_submodules
from typing import List, Dict, Any
from core.console import console
from core.network import get_proxy

async def check_email(email):
    out = []
    modules = import_submodules(holehe.modules)
    
    async def run_module(module, email, client, out):
        try:
            await module(email, client, out)
        except Exception:
            pass
            
    # Use Mozilla user agent to bypass some basic WAFs
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    }
    
    proxies = get_proxy()
    proxy_config = proxies.get("http") if proxies else None

    async with httpx.AsyncClient(headers=headers, timeout=15, proxies=proxy_config) as client:
        async with trio.open_nursery() as nursery:
            for module in modules:
                nursery.start_soon(run_module, module, email, client, out)
                
    return out

def run(email: str) -> Dict[str, Any]:
    console.print(f"\n[bold cyan]🚀 Deep Account Footprinting for '{email}'...[/bold cyan]")
    
    with console.status("[bold magenta]Scanning 120+ platforms (Proxy Enhanced)...[/bold magenta]", spinner="point"):
        results_list = trio.run(check_email, email)
        
    results: Dict[str, Any] = {"email": email, "found_accounts": []}
    found_count: int = 0
    
    for item in results_list:
        if item.get("exists") is True:
            name = item.get("name", "Unknown")
            console.print(f"[bold green]✔ ACCOUNT FOUND[/bold green] - [white]{name}[/white]")
            results["found_accounts"].append(name)
            found_count += 1
            
    if found_count > 0:
        console.print(f"\n[bold highlight]🏁 Footprinting complete![/bold highlight] The email is registered on [bold green]{found_count}[/bold green] platforms.")
    else:
        console.print(f"\n[bold yellow]🏁 Footprinting complete![/bold yellow] No accounts found or heavily rate-limited by providers.")
        
    return results
