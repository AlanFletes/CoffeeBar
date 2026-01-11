import os
from pathlib import Path

def get_shell_config_file():
    """Determines the appropriate shell configuration file (.bashrc, .zshrc)."""
    shell = os.environ.get("SHELL", "")
    home = Path.home()
    
    if "zsh" in shell:
        return home / ".zshrc"
    else:
        # Default to bashrc for bash or others
        return home / ".bashrc"

def set_env_variable(name, value):
    """Sets an environment variable by updating the shell config file."""
    config_file = get_shell_config_file()
    
    # We will use a dedicated block for CoffeeBar in the config file
    # to avoid messing up manual configurations.
    
    # Strategy: Maintain a ~/.coffeebar_env file and source it in .bashrc/.zshrc
    # This is safer and cleaner than regexing .bashrc every time.
    
    env_file = Path.home() / ".coffeebar_env"
    
    # Write the variable to the env file
    content = ""
    if env_file.exists():
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        # Filter out existing definition of this var
        for line in lines:
            if not line.startswith(f"export {name}="):
                content += line
    
    content += f'\nexport {name}="{value}"\n'
    
    # Ensure PATH includes JAVA_HOME/bin
    if name == "JAVA_HOME":
        if "export PATH=$JAVA_HOME/bin:$PATH" not in content:
            content += 'export PATH=$JAVA_HOME/bin:$PATH\n'

    with open(env_file, 'w') as f:
        f.write(content)

    # Ensure env file is sourced in config file
    _ensure_sourced(config_file, env_file)

def _ensure_sourced(config_file, env_file):
    """Ensures the env_file is sourced in the config_file."""
    source_cmd = f'[ -f "{env_file}" ] && source "{env_file}"'
    
    if not config_file.exists():
        # Create if doesn't exist
        with open(config_file, 'w') as f:
            f.write(f"\n# CoffeeBar\n{source_cmd}\n")
        return

    with open(config_file, 'r') as f:
        content = f.read()
        
    if str(env_file) not in content and env_file.name not in content: # check for absolute or relative
        with open(config_file, 'a') as f:
            f.write(f"\n# CoffeeBar configuration\n{source_cmd}\n")

def get_env_variable(name):
    """
    Tries to read the variable from the current environment or the .coffeebar_env file.
    Note: Reading from file is tricky without sourcing. We prioritize os.environ.
    """
    return os.environ.get(name)
