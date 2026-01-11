# ☕ CoffeeBar

**The elegant, lightweight JDK Manager for Windows, Linux & macOS.**

CoffeeBar allows you to switch between Java versions instantly, download new JDKs directly from Eclipse Adoptium, and manage your environment variables with style.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![PyPI](https://img.shields.io/pypi/v/coffeebar-jdk?style=flat-square&logo=pypi)
![Platform](https://img.shields.io/badge/Platform-Win%20|%20Linux%20|%20macOS-0078D6?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

*   **⚡ Instant Switching**: Change your `JAVA_HOME` and `Path` in seconds.
*   **📥 Integrated Downloader**: Download and install LTS JDKs (8, 11, 17, 21) directly from the app (powered by Eclipse Adoptium).
    *   *Auto-detects Apple Silicon (M1/M2/M3) vs Intel.*
*   **🚀 Smart Shell Refresh**:
    *   **Windows**: Updates current session via `refreshenv` (CMD/PS).
    *   **Linux/macOS**: Updates configuration via `.bashrc` / `.zshrc` integration.
*   **🎨 Dual Interface**:
    *   **GUI**: A beautiful "Dark Mode" graphical interface built with CustomTkinter.
    *   **CLI**: A robust command-line tool for power users.
*   **🔍 Auto-Discovery**: Automatically finds JDKs in `Program Files`, `.jdks` (IntelliJ), `/usr/lib/jvm`, `/Library/Java/JavaVirtualMachines` (macOS), etc.

---

## 🛠️ Installation

### 📦 PyPI (Recommended)
The easiest way to install on any platform:
```bash
pip install coffeebar-jdk
```

### 🪟 Windows (Manual)
1.  **Prerequisites**: Python 3 installed.
2.  Run `install.bat`.

### 🐧 Linux / 🍎 macOS (Manual)
1.  **Prerequisites**: Python 3 installed.
2.  Install `python3-tkinter` (Linux only, usually included in macOS/Windows).
    *   Debian/Ubuntu: `sudo apt-get install python3-tk`
3.  Run the installer:

```bash
chmod +x install.sh
./install.sh
```

**Post-Install (Linux/Mac):** Restart terminal or run `source ~/.bashrc` (or `.zshrc`).

---

## 📖 Usage

Once installed, use the `coffeebar` command globally.

### 💻 CLI Mode

| Action | Command | Description |
| :--- | :--- | :--- |
| **List JDKs** | `coffeebar list` | List available versions found in system paths. |
| **Switch** | `coffeebar use 17` | Switch `JAVA_HOME` (supports partial names). |
| **Install** | `coffeebar install 21` | Download LTS JDK from Adoptium. |
| **Current** | `coffeebar current` | Show active JDK. |
| **GUI** | `coffeebar` | Launch graphical interface. |

**Example:**
```bash
$ coffeebar use 17
Set JAVA_HOME to /usr/lib/jvm/temurin-17
[CoffeeBar] Environment updated.
```

### 🖥️ GUI Mode

Simply run `coffeebar` (or `python3 -m coffeebar.main`).

*   **Cross-platform**: Looks native on Windows, Linux (Gnome/KDE), and macOS.
*   **One-Click Install**: Downloads the correct `.tar.gz` or `.zip` for your OS and Architecture.

---

## ⚙️ How it works

*   **Windows**: Modifies `HKCU\Environment` and broadcasts changes.
*   **Linux/macOS**: Manages a lightweight file `~/.coffeebar_env` which is sourced by your shell configuration and uses simple shell aliases.

---

Made with ❤️ for developers.
