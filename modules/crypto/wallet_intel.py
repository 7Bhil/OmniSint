import requests
from core.console import console

def get_btc_balance(address):
    try:
        url = f"https://blockchain.info/rawaddr/{address}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "balance_btc": data.get("final_balance", 0) / 100000000,
                "n_tx": data.get("n_tx"),
                "total_received": data.get("total_received", 0) / 100000000
            }
    except Exception:
        pass
    return None

def get_eth_balance(address):
    # Using a public block explorer API (simplified for demonstration)
    try:
        url = f"https://api.blockcypher.com/v1/eth/main/addrs/{address}/balance"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "balance_eth": data.get("balance", 0) / 10**18,
                "n_tx": data.get("n_tx"),
                "final_n_tx": data.get("final_n_tx")
            }
    except Exception:
        pass
    return None

def run(wallet_address: str):
    console.print(f"[neon]🔍 Analyzing Crypto Wallet:[/neon] [white]{wallet_address}[/white]")
    results = {"address": wallet_address}
    
    if wallet_address.startswith('1') or wallet_address.startswith('3') or wallet_address.startswith('bc1'):
        # Looks like BTC
        console.print("[dim]Detected: Bitcoin Address[/dim]")
        data = get_btc_balance(wallet_address)
        if data:
            results["btc_info"] = data
            console.print(f"  [success]💰 Balance:[/success] [bold white]{data['balance_btc']} BTC[/bold white]")
            console.print(f"  [info]📈 Total Transactions:[/info] {data['n_tx']}")
        else:
            console.print("[danger][!] Could not retrieve BTC data.[/danger]")
            
    elif wallet_address.startswith('0x'):
        # Looks like ETH
        console.print("[dim]Detected: Ethereum Address[/dim]")
        data = get_eth_balance(wallet_address)
        if data:
            results["eth_info"] = data
            console.print(f"  [success]💎 Balance:[/success] [bold white]{data['balance_eth']} ETH[/bold white]")
            console.print(f"  [info]📈 Total Transactions:[/info] {data['n_tx']}")
        else:
            console.print("[danger][!] Could not retrieve ETH data (API Limit or Invalid).[/danger]")
    else:
        console.print("[warning][-] Unknown or unsupported wallet format.[/warning]")
        
    return results
