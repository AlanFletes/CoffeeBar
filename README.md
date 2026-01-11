# CoffeeBar

A lightweight and elegant tool to manage Java JDK versions on Windows.

## Features
- **Switch JDKs**: Easily change the `JAVA_HOME` environment variable and update `Path`.
- **Auto-Discovery**: Automatically finds JDKs in common locations (e.g., `C:\Program Files\Java`, `%UserProfile%\.jdks`).
- **Dual Interface**:
    - **GUI**: Modern, dark-mode friendly graphical interface.
    - **CLI**: Fast command-line interface for scripting or quick switches.

## Installation

1. Install Python 3.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage - Best Practice (Wrappers)

To ensure that environment variables are updated in your **current** terminal session immediately, rely on the wrapper scripts in the `bin/` directory.

1.  Add `e:\MabeInternalTools\CoffeeBar\bin` to your system `Path`.
2.  Restart your terminal one last time.
3.  Use the `coffeebar` command directly:

```powershell
# Updates JAVA_HOME and refreshes current session
coffeebar use 17
```

*Note: The wrappers automatically detect if Chocolatey is installed and run `refreshenv` to update your current session.*

### Manual Usage (Python)

If you run via `python`, changes only apply to **new** terminals:

**GUI Mode:**
```bash
python -m src.main
```

### CLI Mode
Run with commands to use the CLI:

**List available JDKs:**
```bash
python -m src.main list
```

**Show current JDK:**
```bash
python -m src.main current
```

**Switch JDK:**
```bash
python -m src.main use <name_or_path>
# Example:
python -m src.main use 17
python -m src.main use "C:\MyJDKs\jdk-21"
```
