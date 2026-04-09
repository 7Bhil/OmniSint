import json
import os
import html
from datetime import datetime
from core.console import console

def generate_mermaid_graph(target, results):
    escaped_target = html.escape(str(target))
    graph = ["graph TD"]
    graph.append(f"    T[Target: {escaped_target}]")
    
    for module, data in results.items():
        escaped_module = html.escape(str(module))
        m_id = escaped_module.replace(" ", "_")
        graph.append(f"    T --> {m_id}[Module: {escaped_module}]")
        
        # Visualize key findings as child nodes
        if isinstance(data, dict):
            # Check for discovered emails
            if "discovered_emails" in data:
                for email in data["discovered_emails"]:
                    escaped_email = html.escape(str(email))
                    e_id = escaped_email.replace("@", "_at_").replace(".", "_")
                    graph.append(f"    {m_id} -- discovered --> E_{e_id}[Email: {escaped_email}]")
            # Check for discovered names
            if "discovered_names" in data:
                for name in data["discovered_names"]:
                    escaped_name = html.escape(str(name))
                    n_id = escaped_name.replace(" ", "_")
                    graph.append(f"    {m_id} -- identity --> N_{n_id}[Name: {escaped_name}]")
            # Check for crypto wallets
            if "btc_info" in data or "eth_info" in data:
                graph.append(f"    {m_id} -- owner --> CW[Crypto Wallet]")
                
    return "\n".join(graph)

def export_results(target: str, domain_type: str, results: dict, format_type: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    escaped_target = html.escape(str(target))
    filename = f"omnisint_{domain_type}_{escaped_target.replace('/', '_')}_{timestamp}.{format_type}"
    
    os.makedirs('reports', exist_ok=True)
    filepath = os.path.join('reports', filename)
    
    if format_type == 'json':
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=4)
    elif format_type == 'html':
        mermaid_code = generate_mermaid_graph(target, results)
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>OmniSint Elite Report - {escaped_target}</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script>mermaid.initialize({{startOnLoad:true, theme:'dark'}});</script>
            <style>
                :root {{
                    --primary: #00ffd8;
                    --secondary: #bc00ff;
                    --bg: #050505;
                    --glass: rgba(255, 255, 255, 0.03);
                    --glass-border: rgba(255, 255, 255, 0.1);
                }}
                body {{
                    font-family: 'Inter', sans-serif;
                    background-color: var(--bg);
                    color: #ffffff;
                    margin: 0;
                    padding: 40px;
                    background: radial-gradient(circle at top right, #1a0033, transparent),
                                radial-gradient(circle at bottom left, #001a1a, transparent);
                    background-attachment: fixed;
                }}
                .container {{ max-width: 1100px; margin: 0 auto; }}
                header {{
                    background: var(--glass);
                    backdrop-filter: blur(12px);
                    border: 1px solid var(--glass-border);
                    padding: 30px;
                    border-radius: 24px;
                    margin-bottom: 40px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }}
                h1 {{ margin: 0; font-weight: 800; font-size: 2.5em; letter-spacing: -2px; color: var(--primary); }}
                .badge {{
                    background: var(--secondary);
                    padding: 5px 15px;
                    border-radius: 100px;
                    font-size: 0.8em;
                    font-weight: 600;
                    text-transform: uppercase;
                }}
                .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 40px; }}
                .stat-card {{
                    background: var(--glass);
                    backdrop-filter: blur(12px);
                    border: 1px solid var(--glass-border);
                    padding: 20px;
                    border-radius: 20px;
                    text-align: center;
                }}
                .stat-value {{ font-size: 1.5em; font-weight: 800; color: var(--primary); }}
                .stat-label {{ font-size: 0.8em; color: #888; text-transform: uppercase; margin-top: 5px; }}
                
                .graph-section {{
                    background: var(--glass);
                    border: 1px solid var(--glass-border);
                    border-radius: 24px;
                    padding: 40px;
                    margin-bottom: 40px;
                    text-align: center;
                    overflow: auto;
                }}
                .section-title {{ color: var(--primary); margin-bottom: 20px; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; }}

                .module-card {{
                    background: var(--glass);
                    backdrop-filter: blur(12px);
                    border: 1px solid var(--glass-border);
                    border-radius: 24px;
                    margin-bottom: 30px;
                    overflow: hidden;
                    transition: transform 0.3s ease;
                }}
                .module-card:hover {{ transform: translateY(-5px); border-color: var(--primary); }}
                .module-header {{
                    padding: 20px 30px;
                    background: rgba(255, 255, 255, 0.05);
                    border-bottom: 1px solid var(--glass-border);
                    font-weight: 600;
                    color: var(--primary);
                    display: flex;
                    align-items: center;
                }}
                .module-content {{ padding: 30px; }}
                pre {{
                    background: rgba(0,0,0,0.3);
                    padding: 20px;
                    border-radius: 12px;
                    font-size: 0.9em;
                    overflow-x: auto;
                    color: #00ffcc;
                    line-height: 1.5;
                }}
                footer {{ text-align: center; margin-top: 60px; color: #555; font-size: 0.8em; }}
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <div>
                        <h1>🧿 OmniSint <span style="color:#fff">Elite</span></h1>
                        <p style="color:#888; margin: 5px 0 0 0;">Intelligence Report for <strong>{escaped_target}</strong></p>
                    </div>
                    <div class="badge">Session Secure</div>
                </header>
        
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-value">{len(results)}</div>
                        <div class="stat-label">Modules Deployed</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{html.escape(str(domain_type).upper())}</div>
                        <div class="stat-label">Initial Pivot</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{datetime.now().strftime("%H:%M:%S")}</div>
                        <div class="stat-label">Generation Time</div>
                    </div>
                </div>
        
                <div class="graph-section">
                    <div class="section-title">🕸️ Intelligence Graph</div>
                    <div class="mermaid">
                        {mermaid_code}
                    </div>
                </div>
        """
        for module, data in results.items():
            html_content += f"""
            <div class="module-card">
                <div class="module-header">📡 MODULE: {html.escape(str(module).upper())}</div>
                <div class="module-content">
                    <pre>{html.escape(json.dumps(data, indent=4))}</pre>
                </div>
            </div>
            """
            
        html_content += f"""
                <footer>Generated by OmniSint v0.7 Elite • {datetime.now().strftime("%Y-%m-%d")} • Security Grade A+</footer>
            </div>
        </body>
        </html>
        """
        with open(filepath, 'w') as f:
            f.write(html_content)
            
        console.print(f"\n[success]💎 Elite Glassmorphism Report with Graph saved to: {filepath}[/success]")
