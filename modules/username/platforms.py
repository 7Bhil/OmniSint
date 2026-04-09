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

def check_platform(username, platform, url_template):
    url = url_template.format(username)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        
        # 1. Check for obvious 404
        if response.status_code == 404:
            return platform, url, False
            
        # 2. Site-specific content validation (soft 404 detection)
        # Many platforms return 200 OK even if the user is not found (SPAs like TikTok, Instagram, etc)
        content = response.text.lower()
        
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
                return platform, url, False
        
        import re
        title_match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
        title_text = title_match.group(1).strip() if title_match else ""

        # Platform specific tricky cases and precise title matches
        if platform == "Instagram":
            if "login" in response.url or title_text == "Instagram":
                return platform, url, False
        if platform == "LinkedIn" and "public-profile/in" not in response.url and "authwall" in response.url:
            return platform, url, False
        if platform == "Reddit" and ("wait for verification" in content or title_text == "Reddit - Dive into anything"):
            return platform, url, False
        if platform == "Steam" and "Error" in title_text:
            return platform, url, False
        if platform == "Imgur" and title_text == "Imgur: The magic of the Internet":
            return platform, url, False
        if platform == "DailyMotion" and title_text == "Dailymotion":
            return platform, url, False
        if platform == "TryHackMe" and title_text == "TryHackMe | Cyber Security Training":
            return platform, url, False
        if platform in ["Discord", "Kaggle", "HackerRank", "TryHackMe", "CodeChef", "Codingame", "HackTheBox", "RootMe", "HackThisSite", "Intigriti", "Aizu", "Taringa", "Telegram"]:
            # These are notorious for Soft 404s and anti-scraping
            if title_text == "" or title_text.lower() == platform.lower():
                return platform, url, False
            if username.lower() not in title_text.lower():
                return platform, url, False
            
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
                return platform, url, False
        
        if platform == "Wordpress" and "doesn" in content and "exist" in content:
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
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
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
