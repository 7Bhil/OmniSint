# 🧿 OmniSint Elite v1.1.0

<p align="center">
  <b>The Professional-Grade OSINT Suite for Advanced Investigations.</b><br>
  <i>"Omnipresence. Omniscience. Synthesis."</i>
</p>

---

## 🚀 Pourquoi OmniSint Elite ?

OmniSint n'est pas un simple scraper de réseaux sociaux. C'est une **Plateforme d'Intelligence** qui connecte les points là où les autres outils s'arrêtent. En v1.1.0, il devient une arme de précision industrielle.

### 🧠 Les 3 Piliers de l'Élite

1.  **OmniCorrelator Engine** : Le cerveau. Il ne se contente pas de trouver des profils, il les analyse par intelligence croisée (Bios, Mails, Crypto) pour lier les identités avec un score de certitude algorithmique.
2.  **Stealth Layer 2.0 (Ghost)** : L'invisibilité. Rotation automatique d'User-Agents, cycling de proxies et support **Tor** (SOCKS5). Vous scannez sans jamais laisser de trace.
3.  **Auto-Pivot Dynamique** : La réaction en chaîne. Trouvez un mail dans une bio Instagram, et OmniSint lancera automatiquement un scan de fuites de données et de réseaux professionnels sur cette nouvelle piste.

---

## 🛠️ Installation Industrielle

```bash
# 1. Clone & Navigation
git clone https://github.com/7Bhil/OmniSint.git
cd OmniSint

# 2. Configuration (Indispensable)
cp .env.example .env
# Éditez .env avec vos clés HIBP, Shodan ou Hunter.io

# 3. Installation des dépendances
pip install -r requirements.txt
```

---

## 📖 Usage : L'Art de l'Enquête

OmniSint Elite est conçu pour être simple mais profond.

### 🧿 La Commande Master (Auto-Détection)
L'outil détecte intelligemment si vous lui donnez un mail, un pseudo, un domaine ou un téléphone.
```bash
python3 main.py intel <target>
```

### ⚡ Modules Spécifiques
- **Username** : `python3 main.py user <username>` (120+ plateformes)
- **Email** : `python3 main.py email <target@mail.com>` (Breaches & Presence)
- **Domain** : `python3 main.py domain <target.com>` (DNS, MX, WHOIS)
- **Phone** : `python3 main.py phone <+33xxxx...>` (Carrier & Dorking)
- **Crypto** : `python3 main.py crypto <address>` (BTC/ETH Tracking)

---

## 📊 Comparatif : Pourquoi nous sommes devant

| Fonctionnalité | Sherlock / Harvester | **OmniSint Elite** |
| :--- | :---: | :---: |
| **Rotation Proxy** | ❌ Manuel | ✅ **Auto-Cycle + Tor** |
| **Corrélation d'Identité** | ❌ Non | ✅ **Moteur Dédié** |
| **Auto-Pivot** | ❌ Non | ✅ **Récursif (Depth 3)** |
| **Cache Local** | ❌ Non | ✅ **SQLite High-Speed** |
| **Rapports Premium** | ❌ TXT/JSON | ✅ **Glassmorphism HTML** |

---

## ⚙️ Configuration Avancée

### 🛡️ Proxies (proxies.txt)
Ajoutez vos proxies (format `ip:port` ou `user:pass@ip:port`) dans `proxies.txt` pour activer la rotation automatique.

### 🔑 API Keys (.env)
Renseignez vos clés dans le fichier `.env` pour débloquer :
- **HIBP** : Analyse des fuites de données massives.
- **Hunter.io** : Recherche de mails corporate.
- **Shodan** : Analyse d'infrastructure profonde.

---

## 💎 Design & Esthétique
OmniSint utilise le thème **Matrix Green** pour sa console et des rapports HTML **Glassmorphism** pour une présentation irréprochable de vos enquêtes.

---
**Elite v1.1.0** • *Designed for Modern Intelligence Officers.* 🧿🛡️
