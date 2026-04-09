import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    """Centralized configuration for API keys and global settings."""
    
    # OSINT API KEYS (Optional but recommended)
    HIBP_API_KEY    = os.getenv("HIBP_API_KEY", "")
    SHODAN_API_KEY  = os.getenv("SHODAN_API_KEY", "")
    HUNTER_API_KEY  = os.getenv("HUNTER_API_KEY", "")
    INTELX_API_KEY  = os.getenv("INTELX_API_KEY", "")
    
    # Network Settings
    TOR_ENABLED     = os.getenv("TOR_ENABLED", "false").lower() == "true"
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "15"))
    CACHE_TTL       = int(os.getenv("CACHE_TTL", "43200")) # 12 hours
    
    # Path Settings
    BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CACHE_DB  = os.path.join(os.path.expanduser("~"), ".omnisint_cache.db")
    PROXY_FILE = os.path.join(BASE_DIR, "proxies.txt")
