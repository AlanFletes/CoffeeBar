import sys
from coffeebar.ui import cli, gui

def main():
    if len(sys.argv) > 1:
        # Pass control to Typer CLI
        cli.app()
    else:
        # Launch GUI
        # Check if we can import customtkinter, else fail gracefully
        try:
            app = gui.CoffeeBarApp()
            app.mainloop()
        except ImportError as e:
            print(f"Error starting GUI: {e}")
            print("Running in CLI mode instead.")
            cli.app()

if __name__ == "__main__":
    main()
