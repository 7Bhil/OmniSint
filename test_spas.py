import requests

urls = {
    "DailyMotion": "https://www.dailymotion.com/thisuserdoesnotexist123456789",
    "Steam": "https://steamcommunity.com/id/thisuserdoesnotexist123456789",
    "Imgur": "https://imgur.com/user/thisuserdoesnotexist123456789",
    "Telegram": "https://t.me/thisuserdoesnotexist123456789",
    "Reddit": "https://www.reddit.com/user/thisuserdoesnotexist123456789",
    "Instagram": "https://www.instagram.com/thisuserdoesnotexist123456789/",
    "Discord": "https://discord.com/users/thisuserdoesnotexist123456789",
    "TryHackMe": "https://tryhackme.com/p/thisuserdoesnotexist123456789"
}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

for name, url in urls.items():
    try:
        r = requests.get(url, headers=headers, timeout=5)
        print(f"--- {name} [{r.status_code}] ---")
        if r.history:
            print(f"Redirected to: {r.url}")
        
        # Extract title
        import re
        title = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE)
        print("Title:", title.group(1) if title else "None")
        
        # Check snippet
        print("Snippet:", r.text[:100].replace('\n', ' '))
    except Exception as e:
        print(f"Error {name}: {e}")

