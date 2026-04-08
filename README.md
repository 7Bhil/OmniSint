# 🧿 OmniSint Elite

**OmniSint Elite** is a next-generation, modular Open Source Intelligence (OSINT) suite designed for deep digital investigation. From username footprinting to automated cryptocurrency tracking, it provides a high-fidelity intelligence platform for elite investigators.

## 🚀 Key Features

- **Master Intelligence (`intel`)**: A unified command that auto-detects target types and runs full-spectrum scans.
- **Elite Glassmorphism Reports**: Premium, interactive HTML reports with modern aesthetics.
- **Auto-Pivot Engine**: Intelligent chaining of findings (emails, crypto wallets, etc.) to uncover linked identities automatically.
- **Crypto Wallet Intelligence**: Monitor BTC and ETH addresses, balances, and transaction history.
- **Data Breach Intelligence**: Integrated checks for public data leaks via HIBP.
- **Stealth Dorking**: Advanced deep-web search patterns via DuckDuckGo.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/7Bhil/OmniSint.git
   cd OmniSint
   ```

2. **Set up a virtual environment (Recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

OmniSint Elite uses a simple CLI interface powered by `Click`.

### The Master Command
The most powerful way to use OmniSint. It intelligently detects if the target is an email, username, domain, or phone number.
```bash
python3 main.py intel <target>
```

### Specific Commands
- **Username Scan**: `python3 main.py user <username>`
- **Domain Scan**: `python3 main.py domain <domain.com>`
- **Email Scan**: `python3 main.py email <email@example.com>`
- **Phone Scan**: `python3 main.py phone <+123456789>`

### Options
- `--export html`: Generate a premium Glassmorphism report (Default for `intel`).
- `--export json`: Generate a machine-readable JSON report.

## 💎 Elite Reporting
All reports are saved in the `reports/` directory. The Elite HTML reports are designed for professional presentation, featuring a modern dark UI with blur effects and typography.

## 🧩 Extensibility
OmniSint is built on a **Modular Plugin Architecture**. To add a new module:
1. Create a `.py` file in the appropriate category under `modules/` (e.g., `modules/username/`).
2. Implement a `run(target)` function that returns a dictionary.
3. OmniSint will automatically load and execute your module.

---
**Elite v0.5** • Designed for Advanced OSINT Engineers.
