import os
import random
from itertools import cycle
from core.config import Config

class ProxyManager:
    """Handles proxy rotation and cycling."""
    
    def __init__(self):
        self.proxies = []
        self._load_proxies()
        self.proxy_cycle = cycle(self.proxies) if self.proxies else None

    def _load_proxies(self):
        if os.path.exists(Config.PROXY_FILE):
            try:
                with open(Config.PROXY_FILE, "r") as f:
                    self.proxies = [line.strip() for line in f if line.strip()]
            except Exception:
                pass

    def get_proxy(self):
        """Returns a proxy dict for 'requests' or None if no proxies available."""
        if Config.TOR_ENABLED:
            return {
                "http": "socks5h://127.0.0.1:9050",
                "https": "socks5h://127.0.0.1:9050"
            }
            
        if not self.proxy_cycle:
            return None
            
        proxy = next(self.proxy_cycle)
        if not proxy.startswith("http"):
            proxy = f"http://{proxy}"
            
        return {"http": proxy, "https": proxy}

# Global instance
proxy_manager = ProxyManager()
