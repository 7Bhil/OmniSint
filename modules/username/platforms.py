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
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        # 200 basically means found, 404 means not found.
        # This is a naive check. A true "next-gen" tool would check page content.
        if response.status_code == 200:
            return platform, url, True
        elif response.status_code == 404:
            return platform, url, False
        else:
            return platform, url, None 
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
