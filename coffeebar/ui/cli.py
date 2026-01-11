import typer
from rich.console import Console
import os
from rich.table import Table
from rich.panel import Panel
from coffeebar.core.jdk_manager import JdkManager
from coffeebar.core.jdk_downloader import JdkDownloader
from coffeebar.core import registry_utils
from pathlib import Path
from rich.progress import Progress
import sys

app = typer.Typer()
console = Console()
manager = JdkManager()
downloader = JdkDownloader()

@app.command()
def list():
    """List all available JDKs found in standard directories."""
    jdks = manager.find_jdks()
    current = manager.get_current_jdk()
    
    table = Table(title="Available JDKs")
    table.add_column("Status", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Version", style="green")
    table.add_column("Path", style="dim")

    for jdk in jdks:
        is_active = (current and os.path.normpath(current) == os.path.normpath(jdk["path"]))
        status = "-> (Current)" if is_active else ""
        style = "bold white" if is_active else None
        
        table.add_row(status, jdk["name"], jdk["version"], jdk["path"], style=style)

    console.print(table)

@app.command()
def current():
    """Show the currently active JAVA_HOME."""
    path = manager.get_current_jdk()
    if path:
        console.print(Panel(f"[bold green]{path}[/bold green]", title="Current JAVA_HOME"))
    else:
        console.print("[yellow]JAVA_HOME is not set.[/yellow]")

@app.command()
def use(path_or_name: str):
    """Set the JDK. You can provide a partial name or full path."""
    jdks = manager.find_jdks()
    
    # Try exact path match
    target = None
    for jdk in jdks:
        if jdk["path"].lower() == path_or_name.lower():
            target = jdk
            break
            
    # Try exact name match
    if not target:
        for jdk in jdks:
            if jdk["name"].lower() == path_or_name.lower():
                target = jdk
                break
    
    # Try partial name match
    if not target:
        matches = [jdk for jdk in jdks if path_or_name.lower() in jdk["name"].lower()]
        if len(matches) == 1:
            target = matches[0]
        elif len(matches) > 1:
            console.print(f"[red]Ambiguous name '{path_or_name}'. Matches: {', '.join(d['name'] for d in matches)}[/red]")
            return

    if target:
        manager.set_jdk(target["path"])
        console.print(f"[bold green]Successfully switched to {target['name']}[/bold green]")
        # Verification hint
        console.print("[dim]Note: Open a NEW terminal to see changes take effect.[/dim]")
    else:
        # If looked like a path and it exists, maybe force it?
        import os
        if os.path.exists(path_or_name) and manager._is_valid_jdk(path_or_name):
             manager.set_jdk(path_or_name)
             console.print(f"[bold green]Successfully set custom path to {path_or_name}[/bold green]")
        else:
            console.print(f"[red]Could not find JDK matching '{path_or_name}'[/red]")

@app.command()
def install(version: int = typer.Argument(..., help="Major Java version to install (e.g., 8, 11, 17, 21)")):
    """Download and install a JDK from Eclipse Adoptium."""
    
    if version not in downloader.get_supported_versions():
        console.print(f"[yellow]Version {version} is not in the LTS list {downloader.get_supported_versions()}. Trying anyway...[/yellow]")
    
    console.print(f"Fetching latest release info for Java {version} (Windows x64)...")
    release = downloader.get_latest_release(version)
    
    if not release:
        console.print("[red]Could not find release information![/red]")
        return
        
    console.print(f"Found: [cyan]{release['name']}[/cyan] ({release['size'] / 1024 / 1024:.2f} MB)")
    
    # Target directory: %UserProfile%/.jdks
    target_root = os.path.join(os.environ["USERPROFILE"], ".jdks")
    if not os.path.exists(target_root):
        os.makedirs(target_root)
        
    archive_path = os.path.join(target_root, release["filename"])
    
    # Download
    with Progress() as progress:
        task = progress.add_task("[green]Downloading...", total=release['size'])
        
        def update_progress(downloaded, total):
            progress.update(task, completed=downloaded)
            
        try:
            downloader.download_file(release['url'], archive_path, update_progress)
        except Exception as e:
            console.print(f"[red]Download failed: {e}[/red]")
            return

    console.print("Extracting...")
    # Use a specific folder name to avoid collisions or generic names
    # e.g. temurin-17.0.x
    folder_name = f"temurin-{release['name']}" # release['name'] often looks like 'jdk-17.0.10+7' which might be invalid chars for folder in some OS or just messy.
    # Safe name:
    import re
    safe_name = re.sub(r'[^a-zA-Z0-9\-\.]', '_', release['name'])
    folder_name = f"temurin-{safe_name}"

    try:
        final_path = downloader.install_jdk(archive_path, target_root, folder_name)
        console.print(f"[bold green]Installed successfully to: {final_path}[/bold green]")
        
        if typer.confirm("Do you want to set this as the active JDK now?"):
            manager.set_jdk(final_path)
            console.print(f"[bold green]Active JDK updated![/bold green]")
            console.print("[dim]Remember to restart your terminal.[/dim]")
            
    except Exception as e:
        console.print(f"[red]Installation failed: {e}[/red]")

@app.command()
def add_to_path():
    """Adds the CoffeeBar bin directory to the user's Path for easy access."""
    # Resolve bin directory relative to this file
    # src/ui/cli.py -> ... -> CoffeeBar -> bin
    base_dir = Path(__file__).parent.parent.parent
    bin_dir = base_dir / "bin"
    
    if not bin_dir.exists():
        console.print(f"[red]Could not find bin directory at {bin_dir}[/red]")
        return
        
    bin_path_str = str(bin_dir.absolute())
    
    try:
        registry_utils.append_to_path(bin_path_str, user=True)
        console.print(f"[bold green]Successfully added '{bin_path_str}' to your User Path.[/bold green]")
        console.print("[yellow]Please restart your terminal (close and open again) to use the 'coffeebar' command directly.[/yellow]")
    except Exception as e:
        console.print(f"[red]Failed to update Path: {e}[/red]")

if __name__ == "__main__":
    app()
