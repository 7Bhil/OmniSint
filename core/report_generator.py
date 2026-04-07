import json
import os
from datetime import datetime
from core.console import console

def export_results(target: str, domain_type: str, results: dict, format_type: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"omnisint_{domain_type}_{target}_{timestamp}.{format_type}"
    
    # Create reports directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)
    filepath = os.path.join('reports', filename)
    
    if format_type == 'json':
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=4)
    elif format_type == 'html':
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>OmniSint Report - {target}</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #ffffff; padding: 20px; }}
                h1 {{ color: #00bcd4; }}
                .module {{ background-color: #1e1e1e; padding: 15px; margin-bottom: 20px; border-radius: 8px; border-left: 4px solid #00bcd4; }}
                pre {{ background-color: #000; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                .success {{ color: #4CAF50; }}
                .danger {{ color: #F44336; }}
            </style>
        </head>
        <body>
            <h1>🧿 OmniSint Report</h1>
            <p><strong>Target:</strong> {target}</p>
            <p><strong>Type:</strong> {domain_type.capitalize()}</p>
            <p><strong>Date:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <hr>
        """
        for module, data in results.items():
            html_content += f"<div class='module'><h2>Module: {module}</h2>"
            html_content += f"<pre>{json.dumps(data, indent=4)}</pre></div>"
            
        html_content += """
        </body>
        </html>
        """
        with open(filepath, 'w') as f:
            f.write(html_content)
            
    console.print(f"\n[success]💾 Report saved to: {filepath}[/success]")
