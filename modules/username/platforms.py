import requests
import concurrent.futures
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from core.console import console

PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Twitter": "https://twitter.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "GitLab": "https://gitlab.com/{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Spotify": "https://open.spotify.com/user/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Flickr": "https://www.flickr.com/people/{}",
    "Vimeo": "https://vimeo.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Disqus": "https://disqus.com/by/{}",
    "Medium": "https://medium.com/@{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "VK": "https://vk.com/{}",
    "About.me": "https://about.me/{}",
    "Imgur": "https://imgur.com/user/{}",
    "Flipboard": "https://flipboard.com/@{}",
    "SlideShare": "https://www.slideshare.net/{}",
    "Patreon": "https://www.patreon.com/{}",
    "BitBucket": "https://bitbucket.org/{}/"
}

def check_platform(username, platform, url_template):
    url = url_template.format(username)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        
        # 1. Check for obvious 404
        if response.status_code == 404:
            return platform, url, False
            
        # 2. Site-specific content validation (soft 404 detection)
        content = response.text.lower()
        if platform == "Instagram" and ("login" in response.url or "vrai nom" in content or "page non trouvée" in content or "not available" in content or "plus disponible" in content):
            return platform, url, False
        if platform == "Twitter" and ("doesn't exist" in content or "page non trouvée" in content):
            return platform, url, False
        if platform == "Reddit" and ("nobody here" in content or "page non trouvée" in content):
            return platform, url, False
        if platform == "GitHub" and "not found" in content:
            return platform, url, False
            
        # 3. Fallback to status code if no specific rule matched
        if response.status_code == 200:
            return platform, url, True
            
        return platform, url, False
    except requests.RequestException:
        return platform, url, None

def run(username: str):
    console.print(f"[bold cyan]🚀 Launching concurrent username scan...[/bold cyan]")
    results = {}
    found_count = 0
    total_platforms = len(PLATFORMS)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        task = progress.add_task(f"[cyan]Scanning {total_platforms} platforms...", total=total_platforms)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(check_platform, username, platform, url): platform for platform, url in PLATFORMS.items()}
            
            for future in concurrent.futures.as_completed(futures):
                platform = futures[future]
                try:
                    platform, url, exists = future.result()
                    if exists is True:
                        progress.console.print(f"[bold green]✔ FOUND[/bold green] - [white]{platform}[/white]: {url}")
                        results[platform] = {"status": "found", "url": url}
                        found_count += 1
                    elif exists is False:
                        # Don't clutter the beautiful UI with not found logs, just update progress
                        results[platform] = {"status": "not_found", "url": url}
                    else:
                        progress.console.print(f"[bold yellow]⚠ BLOCKED/ERROR[/bold yellow] - [white]{platform}[/white]")
                        results[platform] = {"status": "error", "url": url}
                except Exception as e:
                    results[platform] = {"status": "exception", "error": str(e)}
                
                progress.advance(task)
                
    console.print(f"\n[bold highlight]🏁 Scan complete![/bold highlight] Found on [bold green]{found_count}[/bold green] platforms.")
    return results
