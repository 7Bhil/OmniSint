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

def get_banner():
    banner = r"""
   ▄▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄   ▄▄ ▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄▄ 
  █       █  █▄█  █  █▄█  █   █       █   █  █▄█  █       █
  █   ▄   █       █       █   █  ▄▄▄▄▄█   █       █▄     ▄█
  █  █ █  █       █       █   █ █▄▄▄▄▄█   █       █ █   █  
  █  █▄█  █       █       █   █▄▄▄▄▄  █   █       █ █   █  
  █       █ ██▄██ █ ██▄██ █   █▄▄▄▄▄█ █   █ ██▄██ █ █   █  
  █▄▄▄▄▄▄▄█▄█   █▄█▄█   █▄█▄▄▄█▄▄▄▄▄▄▄█▄▄▄█▄█   █▄█▄█▄▄▄█  
    """
    return Panel(
        Text(banner, style="neon"),
        subtitle="[bold purple]OMNISINT ELITE v1.0.0[/bold purple]",
        border_style="purple",
        padding=(0, 2)
    )
