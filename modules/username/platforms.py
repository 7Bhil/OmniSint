import concurrent.futures
from typing import Dict, Any
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from core.console import console
from core.network import request as network_request

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
    "Imgur": "https://imgur.com/user/{}",
    "Flipboard": "https://flipboard.com/@{}",
    "SlideShare": "https://www.slideshare.net/{}",
    "Patreon": "https://www.patreon.com/{}",
    "BitBucket": "https://bitbucket.org/{}/",
    "TikTok": "https://www.tiktok.com/@{}",
    "Twitch": "https://www.twitch.org/{}",
    "Facebook": "https://www.facebook.com/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "WhatsApp": "https://wa.me/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Behance": "https://www.behance.net/{}",
    "Dribbble": "https://dribbble.com/{}",
    "Kaggle": "https://www.kaggle.com/{}",
    "StackOverflow": "https://stackoverflow.com/users/{}",
    "Quora": "https://www.quora.com/profile/{}",
    "Slack": "https://{}.slack.com",
    "Discord": "https://discord.com/users/{}",
    "Tumblr": "https://{}.tumblr.com",
    "Blogger": "https://{}.blogspot.com",
    "Wordpress": "https://{}.wordpress.com",
    "DailyMotion": "https://www.dailymotion.com/{}",
    "Mixcloud": "https://www.mixcloud.com/{}",
    "Last.fm": "https://www.last.fm/user/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "Etsy": "https://www.etsy.com/people/{}",
    "eBay": "https://www.ebay.com/usr/{}",
    "Amazon": "https://www.amazon.com/gp/profile/amzn1.account.{}",
    "TripAdvisor": "https://www.tripadvisor.com/members/{}",
    "Goodreads": "https://www.goodreads.com/{}",
    "Wattpad": "https://www.wattpad.com/user/{}",
    "Letterboxd": "https://letterboxd.com/{}",
    "MyAnimeList": "https://myanimelist.net/profile/{}",
    "Taringa": "https://www.taringa.net/{}",
    "ProductHunt": "https://www.producthunt.com/@{}",
    "AngelList": "https://angel.co/u/{}",
    "Codecademy": "https://www.codecademy.com/profiles/{}",
    "FreeCodeCamp": "https://www.freecodecamp.org/{}",
    "Exercism": "https://exercism.org/profiles/{}",
    "HackerRank": "https://www.hackerrank.com/{}",
    "LeetCode": "https://leetcode.com/{}",
    "CodeChef": "https://www.codechef.com/users/{}",
    "TopCoder": "https://www.topcoder.com/members/{}",
    "GeeksForGeeks": "https://auth.geeksforgeeks.org/user/{}/profile",
    "Codeforces": "https://codeforces.com/profile/{}",
    "Codewars": "https://www.codewars.com/users/{}",
    "HackerEarth": "https://www.hackerearth.com/@{}",
    "AtCoder": "https://atcoder.jp/users/{}",
    "SPOJ": "https://www.spoj.com/users/{}",
    "UVa": "https://uhunt.online/id/{}",
    "Poj": "http://poj.org/userstatus?user_id={}",
    "Aizu": "https://judge.u-aizu.ac.jp/onlinejudge/user.jsp?id={}",
    "Zoj": "https://zoj.pintia.cn/user/{}",
    "Timus": "https://timus.online/author.aspx?id={}",
    "LightOJ": "https://lightoj.com/user/{}",
    "Codefights": "https://codefights.com/profile/{}",
    "CheckiO": "https://py.checkio.org/user/{}/",
    "Codingame": "https://www.codingame.com/profile/{}",
    "ProjectEuler": "https://projecteuler.net/profile/{}.html",
    "AdventOfCode": "https://adventofcode.com/2023/leaderboard/private/view/{}",
    "Kattis": "https://open.kattis.com/users/{}",
    "HackThisSite": "https://www.hackthissite.org/user/view/{}",
    "RootMe": "https://www.root-me.org/{}",
    "TryHackMe": "https://tryhackme.com/p/{}",
    "HackTheBox": "https://app.hackthebox.com/users/{}",
    "CTFtime": "https://ctftime.org/user/{}",
    "Bugcrowd": "https://bugcrowd.com/{}",
    "HackerOne": "https://hackerone.com/{}",
    "Intigriti": "https://app.intigriti.com/profile/{}",
    "YesWeHack": "https://www.yeswehack.com/hunters/{}",
    "OpenBugBounty": "https://www.openbugbounty.org/bugbounty/{}/",
    "Pornhub": "https://www.pornhub.com/users/{}",
    "OnlyFans": "https://onlyfans.com/{}",
    "Chaturbate": "https://chaturbate.com/{}",
    "BongaCams": "https://bongacams.com/profile/{}",
    "Cam4": "https://www.cam4.com/{}",
    "Camsoda": "https://www.camsoda.com/{}",
    "MyFreeCams": "https://profiles.myfreecams.com/{}",
    "Stripchat": "https://stripchat.com/{}"
}

ADULT_PLATFORMS = [
    "Pornhub", "OnlyFans", "Chaturbate", "BongaCams", 
    "Cam4", "Camsoda", "MyFreeCams", "Stripchat"
]

def check_platform(username, platform, url_template):
    url = url_template.format(username)
    res = network_request(url, timeout=5)
    
    status_code = res.get("status_code", 0)
    text = res.get("text", "")
    final_url = res.get("url", url)

    try:
        # 1. Check for obvious 404 or connection error
        if status_code == 0:
            return platform, url, None, None
        if status_code == 404:
            return platform, url, False, None
            
        # 2. Site-specific content validation (soft 404 detection)
        content = text.lower()
        
        # Global indicators of a non-existent profile
        not_found_indicators = [
            "page non trouvée", "not available", "plus disponible",
            "doesn't exist", "doesn’t exist", "nobody here", "not found",
            "page not found", "couldn't find", "account suspended",
            "user not found", "the page you're looking for isn't here",
            "This page doesn't exist", "Sorry, this page isn't available",
            "404 not found", "Oops! That page can't be found.",
            "error 404", "This user is no longer active",
            "has been suspended", "<title>404", "<title>Error 404",
            "profile not found", "page introuvable"
        ]
        
        for indicator in not_found_indicators:
            if indicator.lower() in content:
                return platform, url, False, None
        
        import re
        title_match = re.search(r'<title>(.*?)</title>', text, re.IGNORECASE)
        title_text = title_match.group(1).strip() if title_match else ""

        # Platform specific tricky cases and precise title matches
        if platform == "Instagram":
            if "login" in final_url or title_text == "Instagram":
                return platform, url, False, None
        if platform == "LinkedIn" and "public-profile/in" not in final_url and "authwall" in final_url:
            return platform, url, False, None
        if platform == "Reddit" and ("wait for verification" in content or title_text == "Reddit - Dive into anything"):
            return platform, url, False, None
        if platform == "Steam" and "Error" in title_text:
            return platform, url, False, None
        if platform == "Imgur" and title_text == "Imgur: The magic of the Internet":
            return platform, url, False, None
        if platform == "DailyMotion" and title_text == "Dailymotion":
            return platform, url, False, None
        if platform == "TryHackMe" and title_text == "TryHackMe | Cyber Security Training":
            return platform, url, False, None
        if platform in ["Discord", "Kaggle", "HackerRank", "TryHackMe", "CodeChef", "Codingame", "HackTheBox", "RootMe", "HackThisSite", "Intigriti", "Aizu", "Taringa", "Telegram"]:
            # These are notorious for Soft 404s and anti-scraping
            if title_text == "" or title_text.lower() == platform.lower():
                return platform, url, False, None
            if username.lower() not in title_text.lower():
                return platform, url, False, None
            
        # Catch generic titles for SPAs that always return 200 OK
        generic_spa_titles = {
            "OnlyFans": "OnlyFans",
            "Zoj": "ZOJ",
            "MyFreeCams": "MyFreeCams",
            "Cam4": "Cam4",
            "Mixcloud": "Mixcloud",
            "Wordpress": "WordPress.com"
        }
        
        if platform in generic_spa_titles:
            # If the title exactly matches the generic site title OR it doesn't contain the username
            if title_text == generic_spa_titles[platform] or title_text == "":
                return platform, url, False, None
        
        if platform == "Wordpress" and "doesn" in content and "exist" in content:
            return platform, url, False, None

            
        # 3. Fallback to status code if no specific rule matched
        if status_code == 200:
            # Successfully found! Let's extract metadata (Bio / True Name)
            import html
            extracted_bio = "No description available"
            desc_match = re.search(r'<meta\s+(?:name|property)=["\'](?:og:)?description["\']\s+content=["\'](.*?)["\']\s*/?>', text, re.IGNORECASE)
            if desc_match:
                # Clean up the bio (remove excessive whitespace, html entities, etc)
                raw_bio = html.unescape(desc_match.group(1).strip())
                # Truncate to avoid massive report bloat
                extracted_bio = (raw_bio[:200] + '...') if len(raw_bio) > 200 else raw_bio
                
            return platform, url, True, extracted_bio
            
        return platform, url, False, None
    except Exception:
        return platform, url, None, None

def run(username: str, adult_content: bool = False) -> Dict[str, Any]:
    console.print(f"[bold cyan]🚀 Launching concurrent username scan...[/bold cyan]")
    if adult_content:
        console.print("[bold red]🔞 [18+] Platforms ENABLED.[/bold red]")
    
    results: Dict[str, Any] = {}
    found_count = 0
    
    # Filter platforms based on adult content filter
    filtered_platforms = {}
    for name, url in PLATFORMS.items():
        if name in ADULT_PLATFORMS and not adult_content:
            continue
        filtered_platforms[name] = url
        
    total_platforms = len(filtered_platforms)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        task = progress.add_task(f"[cyan]Scanning {total_platforms} platforms...", total=total_platforms)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(check_platform, username, platform, url): platform for platform, url in filtered_platforms.items()}
            
            for future in concurrent.futures.as_completed(futures):
                platform = futures[future]
                try:
                    platform, url, exists, bio = future.result()
                    if exists is True:
                        progress.console.print(f"[bold green]✔ FOUND[/bold green] - [white]{platform}[/white]: {url}")
                        if bio and bio != "No description available":
                            progress.console.print(f"    [dim]↳ Bio: {bio}[/dim]")
                        results[platform] = {"status": "found", "url": url, "extracted_bio": bio}
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
