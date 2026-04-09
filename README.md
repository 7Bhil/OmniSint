# 🧿 OmniSint Elite v1.1.0

**OmniSint Elite** is a professional-grade, modular Open Source Intelligence (OSINT) suite. v1.1.0 introduces industrial infrastructure: **Stealth 2.0**, **SQLite Caching**, and **Centralized Config**.

## 🚀 Key Features

- **Stealth Network 2.0**: Automatic proxy cycling and Tor support via `proxies.txt` to bypass anti-scraping filters.
- **Elite Caching Engine**: High-performance SQLite-driven cache for ultra-fast repeated investigations.
- **Power Configuration**: Centralized `.env` support for HIBP, Shodan, and Hunter.io API keys.
- **Master Intelligence (`intel`)**: A unified command that auto-detects target types and runs full-spectrum scans.
- **OmniCorrelator Engine**: AI-driven identity linkage across 120+ platforms with confidence scoring.
- **Elite Glassmorphism Reports**: Premium, interactive HTML reports with modern aesthetics.
- **Auto-Pivot Engine**: Intelligent chaining of findings to uncover linked identities automatically.
- **Crypto Wallet Intelligence**: Monitor BTC and ETH addresses, balances, and transaction history.
- **Stealth Dorking**: Advanced deep-web search patterns via DuckDuckGo.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/7Bhil/OmniSint.git
   cd OmniSint
   ```

2. **Setup Config:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

OmniSint Elite uses a simple CLI interface powered by `Click`.

### The Master Command
```bash
python3 main.py intel <target>
```

---
**Elite v1.1.0** • The Professional OSINT Standard.
