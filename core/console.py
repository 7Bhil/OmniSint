from rich.console import Console
from rich.theme import Theme

# Define custom themes for our OSINT tool
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red",
    "success": "bold green",
    "highlight": "bold yellow"
})

console = Console(theme=custom_theme)
