import json
from bs4 import BeautifulSoup
from core.console import console
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Dict, Any, List
import urllib.parse
import re
import time
import random

from core.network import request as network_request

def search_duckduckgo(query: str):
    headers = {
        "Referer": "https://duckduckgo.com/"
    }
    
    url = "https://html.duckduckgo.com/html/"
    data = {"q": query}
    
    try:
        # random delay to look human
        time.sleep(random.uniform(0.5, 1.5))
        res = network_request(url, method="POST", headers=headers, data=data, timeout=10)
        
        if res.get("status_code") == 200:
            try:
                import lxml
                parser = "lxml"
            except ImportError:
                parser = "html.parser"
                
            soup = BeautifulSoup(res["text"], parser)
            results = []
            
            for result in soup.find_all('div', class_='result'):
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')
                
                if title_elem and snippet_elem:
                    results.append({
                        "title": title_elem.text.strip(),
                        "link": title_elem.get('href', ''),
                        "snippet": snippet_elem.text.strip()
                    })
            return results
    except Exception:
        pass
    return []

def run(phone_number: str) -> Dict[str, Any]:
    console.print(f"[info]Starting Advanced Stealth Dorking for '{phone_number}'...[/info]")
    results: Dict[str, Any] = {"phone_number": phone_number, "dork_hits": []}
    
    clean_number = re.sub(r'\D', '', phone_number)
    local_number = clean_number[3:] if len(clean_number) > 10 else clean_number
    
    # Advanced OSINT Dorks
    queries = [
        f'"{phone_number}"',
        f'"{clean_number}"',
        f'site:linkedin.com "{phone_number}" OR "{clean_number}" OR "{local_number}"',
        f'site:facebook.com "{phone_number}" OR "{clean_number}" OR "{local_number}"',
        f'site:instagram.com "{phone_number}" OR "{clean_number}"',
        f'site:twitter.com "{phone_number}" OR "{clean_number}"',
        f'site:pastebin.com "{phone_number}" OR "{clean_number}"'
    ]
    
    all_hits: List[Dict[str, str]] = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Injecting Dorks into Search Engines...", total=len(queries))
        
        for query in queries:
            progress.update(task, description=f"[cyan]Dorking: [white]{query}[/white]")
            hits = search_duckduckgo(query)
            for hit in hits:
                # Deduplicate by URL
                if not any(h['link'] == hit['link'] for h in all_hits):
                    all_hits.append(hit)
            progress.advance(task)
                
    if all_hits:
        console.print(f"\n[success][+] FOUND {len(all_hits)} Deep Web/Social Mentions![/success]")
        
        discovered_names = set()
        discovered_emails = set()
        
        # Regex for potential names: Capitalized words (2-3 words) often preceding or following phone indicators
        # This is a heuristic for OSINT
        name_patterns = [
            r'Owner:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'Contact:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s+-\s+LinkedIn',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s+on\s+Instagram'
        ]
        
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        for hit in all_hits:
            # Extract names
            for pattern in name_patterns:
                matches = re.finditer(pattern, hit['title'] + " " + hit['snippet'])
                for m in matches:
                    discovered_names.add(m.group(1))
            
            # Extract emails
            emails = re.findall(email_pattern, hit['snippet'] + " " + hit['title'])
            for e in emails:
                discovered_emails.add(e.lower())

        results["dork_hits"] = all_hits
        results["discovered_names"] = list(discovered_names)
        results["discovered_emails"] = list(discovered_emails)
        
        if discovered_names:
            console.print(f"  [info]👤 Potential Names Detected:[/info] [bold white]{', '.join(discovered_names)}[/bold white]")
        if discovered_emails:
            console.print(f"  [info]📧 Potential Emails Detected:[/info] [bold white]{', '.join(discovered_emails)}[/bold white]")
            
        for hit in all_hits[:5]:
            console.print(f"  [bold magenta]► {hit['title']}[/bold magenta]")
    else:
        console.print("[warning][-] This ghost number left zero open-source traces online.[/warning]")
        
    return results
