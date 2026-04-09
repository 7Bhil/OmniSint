from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.text import Text

# Elite Neon Theme for OmniSint
custom_theme = Theme({
    "info": "bold cyan",
    "warning": "bold yellow",
    "danger": "bold red",
    "success": "bold green",
    "highlight": "bold magenta",
    "dim": "color(242)",
    "neon": "bold #00ffd8",
    "purple": "bold #bc00ff"
})

console = Console(theme=custom_theme)

from rich.table import Table

def display_intel_summary(all_results):
    if not all_results:
        return
        
    table = Table(title="💎 [bold highlight]Intelligence Summary[/bold highlight]", border_style="purple", show_header=True, header_style="bold magenta")
    table.add_column("Category", style="cyan")
    table.add_column("Result", style="white")
    
    # Extract Juicy Info
    found_accounts = []
    for m, res in all_results.items():
        if isinstance(res, dict):
            if "found_accounts" in res: found_accounts.extend(res["found_accounts"])
            elif m == "platforms":
                found_accounts.extend([p for p, d in res.items() if isinstance(d, dict) and d.get("status") == "found"])
    
    if found_accounts:
        table.add_row("Profiles Found", f"[bold green]{len(found_accounts)}[/bold green] platforms")
        
    # Check for breaches
    if "breach_intel" in all_results:
        breaches = all_results["breach_intel"].get("breaches", [])
        if breaches:
            table.add_row("Data Breaches", f"[bold red]⚠ {len(breaches)} leaks detected[/bold red]")
            
    # Check for wallets
    if "wallet_intel" in all_results:
        wallet = all_results["wallet_intel"]
        if "balance" in wallet or "eth_info" in wallet or "btc_info" in wallet:
            table.add_row("Crypto Wallet", "[bold yellow]Active Wallet Detected[/bold yellow]")

    if table.row_count > 0:
        console.print("\n")
        console.print(table)
        console.print("[dim]Check the HTML report for full correlation map and evidence.[/dim]\n")

def get_banner():
    # Vertical Gradient Colors: Matrix Green Palette (7 lines)
    colors = ["#00FF41", "#00F03C", "#00E137", "#00D232", "#00C32D", "#00B428", "#008F11"]
    
    # Original '::::' font style
    raw_banner = [
        r"      ::::::::  ::::     ::::  ::::    ::: :::::::::::  ::::::::  ::::::::::: ::::    ::: ::::::::::: ",
        r"     :+:    :+: +:+:+: :+:+:+  :+:+:   :+:     :+:     :+:    :+:     :+:     :+:+:   :+:     :+:     ",
        r"     +:+    +:+ +:+ +:+:+ +:+  :+:+:+  +:+     +:+     +:+            +:+     :+:+:+  +:+     +:+     ",
        r"     +#+    +:+ +#+  +:+  +#+  +#+ +:+ +#+     +#+     +#++:++#++     +#+     +#+ +:+ +#+     +#+     ",
        r"     +#+    +:+ +#+       +#+  +#+  +#+#+#     +#+            +#+     +#+     +#+  +#+#+#     +#+     ",
        r"     #+#    #+# #+#       #+#  #+#   #+#+#     #+#     #+#    #+#     +#+     #+#   #+#+#     #+#     ",
        r"      ########  ###       ###  ###    #### ###########  ########  ########### ###    ####     ###     "
    ]
    
    banner_markup = ""
    for i, line in enumerate(raw_banner):
        banner_markup += f"[attr=color({colors[i]})]{line}[/]\n"
        
    return Panel(
        Text.from_markup(banner_markup),
        subtitle="[bold green]OmniSint Elite v1.0.0[/bold green]",
        border_style="green",
        padding=(0, 2)
    )
