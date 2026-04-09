import click
from core.console import console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from core.plugins import load_plugins

@click.group()
def cli():
    """OmniSint - The Ultimate Modular OSINT Tool"""
    pass

from core.report_generator import export_results
from core.auto_pivot import analyze_and_pivot
from core.correlator import correlate_identities, display_correlations

@cli.command()
@click.argument('username')
@click.option('--18', 'adult_content', is_flag=True, default=False, help='Enable adult platform scanning (+18)')
@click.option('--export', type=click.Choice(['json', 'html']), help='Export results to a file')
def user(username, adult_content, export):
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
                if module_name == 'platforms':
                    result = module.run(username, adult_content=adult_content)
                else:
                    result = module.run(username)
                if result:
                    all_results[module_name] = result
            except Exception as e:
                console.print(f"[bold red]Error in module {module_name}: {e}[/bold red]")
                
    pivot_findings = analyze_and_pivot(all_results, username, seen_entities)
    all_results.update(pivot_findings)
    
    correlations = correlate_identities(all_results, username)
    display_correlations(correlations)
    all_results["correlations"] = correlations
                
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
    
    correlations = correlate_identities(all_results, domain_name)
    display_correlations(correlations)
    all_results["correlations"] = correlations
                
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
    
    correlations = correlate_identities(all_results, email_address)
    display_correlations(correlations)
    all_results["correlations"] = correlations
                
    if export and all_results:
        export_results(email_address, 'email', all_results, export)

@cli.command()
@click.argument('target')
@click.option('--18', 'adult_content', is_flag=True, default=False, help='Enable adult platform scanning (+18)')
@click.option('--export', type=click.Choice(['json', 'html']), default='html', help='Export results to a file')
def intel(target, adult_content, export):
    """MASTER SCAN: Intelligence aggregation across all domains."""
    console.print(Panel(f"[neon]🚀 Launching Master Intelligence Scan for:[/neon] [white]{target}[/white]", border_style="purple"))
    
    all_results = {}
    seen_entities = set()
    
    # Intelligent target type detection
    target_type = None
    if "@" in target: target_type = 'email'
    elif target.startswith('+') or target.isdigit(): target_type = 'phone'
    elif "." in target and not target.endswith('.'): target_type = 'domain'
    else: target_type = 'username'
    
    console.print(f"[dim]Detected Target Type: {target_type.upper()}[/dim]")
    
    plugins = load_plugins(target_type)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        scan_task = progress.add_task(f"[neon]Running {target_type} modules...", total=len(plugins))
        for name, module in plugins.items():
            progress.update(scan_task, description=f"[neon]Executing {name}...")
            if hasattr(module, 'run'):
                try:
                    if name == 'platforms':
                        res = module.run(target, adult_content=adult_content)
                    else:
                        res = module.run(target)
                    if res: all_results[name] = res
                except Exception as e:
                    console.print(f"[danger]Module {name} failed: {e}[/danger]")
            progress.advance(scan_task)

    # Trigger Elite Auto-Pivot
    console.print("[purple]🔄 Searching for linked identities (Auto-Pivot)...[/purple]")
    pivot_findings = analyze_and_pivot(all_results, target, seen_entities)
    all_results.update(pivot_findings)
    
    # Run OmniCorrelator
    correlations = correlate_identities(all_results, target)
    display_correlations(correlations)
    all_results["correlations"] = correlations
    
    if all_results:
        export_results(target, target_type, all_results, export)
    else:
        console.print("[warning][-] No intelligence gathered during the scan.[/warning]")

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
    
    correlations = correlate_identities(all_results, phone_number)
    display_correlations(correlations)
    all_results["correlations"] = correlations
                
    if export and all_results:
        export_results(phone_number, 'phone', all_results, export)

if __name__ == '__main__':
    from core.console import get_banner
    console.print(get_banner())
    cli()
