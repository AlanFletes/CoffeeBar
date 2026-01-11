# ☕ CoffeeBar

**The elegant, lightweight JDK Manager for Windows.**

CoffeeBar allows you to switch between Java versions instantly, download new JDKs directly from Eclipse Adoptium, and manage your environment variables with style.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=flat-square&logo=windows)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

*   **⚡ Instant Switching**: Change your `JAVA_HOME` and `Path` in seconds.
*   **📥 Integrated Downloader**: Download and install LTS JDKs (8, 11, 17, 21) directly from the app (powered by Eclipse Adoptium).
*   **🚀 Smart Shell Refresh**: Updates your *current* terminal session immediately (supports CMD & PowerShell / Chocolatey `refreshenv`).
*   **🎨 Dual Interface**:
    *   **GUI**: A beautiful "Dark Mode" graphical interface built with CustomTkinter.
    *   **CLI**: A robust command-line tool for power users.
*   **🔍 Auto-Discovery**: Automatically finds JDKs in `Program Files`, `%UserProfile%\.jdks` (IntelliJ), and custom paths.

---

## 🛠️ Installation

1.  **Prerequisites**: Ensure you have [Python 3](https://www.python.org/downloads/) installed.
2.  **Clone/Download** this repository.
3.  **Run the Installer**:
    Double-click `install.bat`
    
    *This script will install dependencies and add the global `coffeebar` command to your system.*

---

## 📖 Usage

Once installed, you can use the `coffeebar` command anywhere.

### 💻 CLI Mode (Command Line)

| Action | Command | Description |
| :--- | :--- | :--- |
| **List JDKs** | `coffeebar list` | Show all detected Java versions. |
| **Switch** | `coffeebar use 17` | Switch to a specific version (supports partial names). |
| **Install** | `coffeebar install 21` | Download and install a new JDK version. |
| **Current** | `coffeebar current` | Show the active `JAVA_HOME`. |
| **GUI** | `coffeebar` | Launch the graphical interface. |

**Example:**
```powershell
PS C:\> coffeebar use 17
[CoffeeBar] Chocolatey detected. Refreshing environment...
Successfully switched to sapmachine-17.0.10
```

### 🖥️ GUI Mode

Simply run:
```powershell
coffeebar
```
Or launch via `python -m src.main` if you haven't run the installer.

*   **List & Switch**: Click "Set Active" on any JDK card.
*   **Download**: Click **"⬇ Install JDK"** to fetch new versions.
*   **Add Path**: Manually scan other folders for portable JDKs.

---

## ⚙️ Technical Details

*   **Environment**: Modifies User Environment Variables (`HKCU\Environment`).
*   **Session Refresh**: Uses a wrapper strategy (`bin/coffeebar.cmd` and `bin/coffeebar.ps1`) to inject variable changes into the parent process, so you don't have to restart your terminal.
*   **Location**: JDKs are installed to `%UserProfile%\.jdks`, compatible with IntelliJ IDEA.

---

Made with ❤️ for developers.
