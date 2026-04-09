import os
import random
import requests
import json
import hashlib
from datetime import datetime, timedelta
from core.console import console

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]

CACHE_DIR = os.path.join(os.path.expanduser("~"), ".omnisint_cache")
PROXY_FILE = "proxies.txt"

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def get_proxy():
    """Load and return a random proxy from proxies.txt if it exists."""
    if not os.path.exists(PROXY_FILE):
        return None
    try:
        with open(PROXY_FILE, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        if not proxies:
            return None
        proxy = random.choice(proxies)
        # Assuming format is ip:port or user:pass@ip:port
        return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    except Exception:
        return None

def request(url, method="GET", use_cache=True, expiry_hours=12, **kwargs):
    """
    Centralized request handler with user-agent rotation, proxy support, and caching.
    """
    url_hash = hashlib.md5(url.encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{url_hash}.json")

    # 1. Check Cache
    if use_cache and os.path.exists(cache_path):
        try:
            with open(cache_path, "r") as f:
                cache_data = json.load(f)
                cached_time = datetime.fromisoformat(cache_data["timestamp"])
                if datetime.now() - cached_time < timedelta(hours=expiry_hours):
                    return cache_data["content"]
        except (Exception, json.JSONDecodeError):
            pass

    # 2. Setup Headers & Proxies
    headers = kwargs.get("headers", {})
    if "User-Agent" not in headers:
        headers["User-Agent"] = random.choice(USER_AGENTS)
    kwargs["headers"] = headers
    
    proxies = get_proxy()
    if proxies:
        kwargs["proxies"] = proxies

    # 3. Execute Request
    try:
        # Avoid hanging forever
        if "timeout" not in kwargs:
            kwargs["timeout"] = 10
            
        response = requests.request(method, url, **kwargs)
        
        result = {
            "status_code": response.status_code,
            "text": response.text,
            "url": response.url
        }

        # 4. Cache and Return
        if response.status_code == 200:
            if use_cache:
                with open(cache_path, "w") as f:
                    cache_content = {
                        "timestamp": datetime.now().isoformat(),
                        "content": result,
                        "original_url": url
                    }
                    json.dump(cache_content, f)
        return result
    except requests.RequestException as e:
        return {"status_code": 0, "text": "", "url": url, "error": str(e)}

def clear_cache():
    """Clear all cached requests."""
    for f in os.listdir(CACHE_DIR):
        os.remove(os.path.join(CACHE_DIR, f))
    console.print("[success]✓ Networking cache cleared.[/success]")
