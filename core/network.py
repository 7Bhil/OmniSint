import random
import requests
import hashlib
from core.console import console
from core.config import Config
from core.proxy_manager import proxy_manager
from core.cache import cache_engine

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]

def request(url, method="GET", use_cache=True, expiry_hours=None, **kwargs):
    """
    Elite Request Handler v1.1.0
    Features: User-Agent Rotation, SQLite Caching, Cycling Proxies, Tor Support.
    """
    # 1. Check SQLite Cache
    cache_key = hashlib.md5(f"{method}:{url}:{json_stable(kwargs.get('params', {}))}".encode()).hexdigest()
    ttl = expiry_hours * 3600 if expiry_hours else Config.CACHE_TTL
    
    if use_cache:
        cached_result = cache_engine.get(cache_key, ttl)
        if cached_result:
            return cached_result

    # 2. Setup Headers & Proxies
    headers = kwargs.get("headers", {})
    if "User-Agent" not in headers:
        headers["User-Agent"] = random.choice(USER_AGENTS)
    kwargs["headers"] = headers
    
    # Get cycling proxy or Tor
    proxies = proxy_manager.get_proxy()
    if proxies:
        kwargs["proxies"] = proxies

    # 3. Execute Request
    try:
        if "timeout" not in kwargs:
            kwargs["timeout"] = Config.DEFAULT_TIMEOUT
            
        response = requests.request(method, url, **kwargs)
        
        result = {
            "status_code": response.status_code,
            "text": response.text,
            "url": response.url
        }

        # 4. Store in SQLite Cache if successful
        if response.status_code == 200 and use_cache:
            cache_engine.set(cache_key, result)
            
        return result
        
    except requests.RequestException as e:
        return {"status_code": 0, "text": "", "url": url, "error": str(e)}

def json_stable(d):
    import json
    return json.dumps(d, sort_keys=True)

def clear_cache():
    """Clear the SQLite networking cache."""
    cache_engine.clear()
    console.print("[success]✓ SQLite Networking cache cleared.[/success]")
