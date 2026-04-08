import click
from core.console import console
from core.plugins import load_plugins

@click.group()
def cli():
    """OmniSint - The Ultimate Modular OSINT Tool"""
    pass

from core.report_generator import export_results
from core.auto_pivot import analyze_and_pivot

@cli.command()
@click.argument('username')
@click.option('--export', type=click.Choice(['json', 'html']), help='Export results to a file')
def user(username, export):
    """Search for a username across multiple platforms."""
    console.print(f"[bold blue]🔍 Searching for username:[/bold blue] [bold white]{username}[/bold white]")
    plugins = load_plugins('username')
    
    if not plugins:
        console.print("[bold red]❌ No username modules loaded.[/bold red]")
        return
        
    all_results = {}
    seen_entities = set()
    for module_name, module in plugins.items():
        console.print(f"[dim]Running module: {module_name}[/dim]")
        if hasattr(module, 'run'):
            try:
                result = module.run(username)
                if result:
                    all_results[module_name] = result
            except Exception as e:
                console.print(f"[bold red]Error in module {module_name}: {e}[/bold red]")
                
    pivot_findings = analyze_and_pivot(all_results, username, seen_entities)
    all_results.update(pivot_findings)
                
    if export and all_results:
        export_results(username, 'username', all_results, export)

@cli.command()
@click.argument('domain_name')
@click.option('--export', type=click.Choice(['json', 'html']), help='Export results to a file')
def domain(domain_name, export):
    """Gather intel on a domain name (IP, DNS, Location)."""
    console.print(f"[bold blue]🌍 Gathering info for domain:[/bold blue] [bold white]{domain_name}[/bold white]")
    plugins = load_plugins('domain')
    
    if not plugins:
        console.print("[bold red]❌ No domain modules loaded.[/bold red]")
        return
        
    all_results = {}
    seen_entities = set()
    for module_name, module in plugins.items():
        console.print(f"[dim]Running module: {module_name}[/dim]")
        if hasattr(module, 'run'):
            try:
                result = module.run(domain_name)
                if result:
                    all_results[module_name] = result
            except Exception as e:
                console.print(f"[bold red]Error in module {module_name}: {e}[/bold red]")
                
    pivot_findings = analyze_and_pivot(all_results, domain_name, seen_entities)
    all_results.update(pivot_findings)
                
    if export and all_results:
        export_results(domain_name, 'domain', all_results, export)

@cli.command()
@click.argument('email_address')
@click.option('--export', type=click.Choice(['json', 'html']), help='Export results to a file')
def email(email_address, export):
    """Gather intel on an email address (DNS, spoofing, disposable check)."""
    console.print(f"[bold blue]📧 Gathering info for email:[/bold blue] [bold white]{email_address}[/bold white]")
    plugins = load_plugins('email')
    
    if not plugins:
        console.print("[bold red]❌ No email modules loaded.[/bold red]")
        return
        
    all_results = {}
    seen_entities = set()
    for module_name, module in plugins.items():
        console.print(f"[dim]Running module: {module_name}[/dim]")
        if hasattr(module, 'run'):
            try:
                result = module.run(email_address)
                if result:
                    all_results[module_name] = result
            except Exception as e:
                console.print(f"[bold red]Error in module {module_name}: {e}[/bold red]")
                
    pivot_findings = analyze_and_pivot(all_results, email_address, seen_entities)
    all_results.update(pivot_findings)
                
    if export and all_results:
        export_results(email_address, 'email', all_results, export)

@cli.command()
@click.argument('phone_number')
@click.option('--export', type=click.Choice(['json', 'html']), help='Export results to a file')
def phone(phone_number, export):
    """Gather intel on a phone number (Carrier, Region). Must include country code (e.g. +1)."""
    console.print(f"[bold blue]📱 Gathering info for phone:[/bold blue] [bold white]{phone_number}[/bold white]")
    plugins = load_plugins('phone')
    
    if not plugins:
        console.print("[bold red]❌ No phone modules loaded.[/bold red]")
        return
        
    all_results = {}
    seen_entities = set()
    for module_name, module in plugins.items():
        console.print(f"[dim]Running module: {module_name}[/dim]")
        if hasattr(module, 'run'):
            try:
                result = module.run(phone_number)
                if result:
                    all_results[module_name] = result
            except Exception as e:
                console.print(f"[bold red]Error in module {module_name}: {e}[/bold red]")
                
    pivot_findings = analyze_and_pivot(all_results, phone_number, seen_entities)
    all_results.update(pivot_findings)
                
    if export and all_results:
        export_results(phone_number, 'phone', all_results, export)

if __name__ == '__main__':
    console.print(f"[bold green]🧿 OmniSint v0.1[/bold green]")
    cli()
