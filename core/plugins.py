import os
import importlib.util
from .console import console

def load_plugins(domain: str):
    """
    Dynamically loads all python modules from a specific domain directory.
    Example: load_plugins('username') will load all .py files in modules/username/
    """
    plugins = {}
    
    # Calculate the path to the modules package based on this file's location
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(base_dir, 'modules', domain)
    
    if not os.path.exists(target_dir):
        console.print(f"[warning]Plugin directory not found: {target_dir}[/warning]")
        return plugins
        
    for filename in os.listdir(target_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            module_path = os.path.join(target_dir, filename)
            
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                    plugins[module_name] = module
                except Exception as e:
                    console.print(f"[danger]Failed to load plugin {module_name}: {e}[/danger]")
                    
    return plugins
