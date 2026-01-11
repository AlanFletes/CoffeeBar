import os
import subprocess
from pathlib import Path
from typing import List, Optional, Dict
from . import registry_utils

class JdkManager:
    def __init__(self):
        self.common_paths = [
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Java"),
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Java"),
            os.path.join(os.environ.get("USERPROFILE"), ".jdks"),
            # Add Eclipse Adoptium / Temurin specific if needed, usually under Program Files/Eclipse Adoptium
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Eclipse Adoptium"),
        ]

    def find_jdks(self) -> List[Dict[str, str]]:
        """Scans common directories for JDK installations."""
        jdks = []
        for path_str in self.common_paths:
            if not os.path.exists(path_str):
                continue
            
            try:
                for entry in os.scandir(path_str):
                    if entry.is_dir():
                        jdk_path = entry.path
                        if self._is_valid_jdk(jdk_path):
                            version = self._get_jdk_version(jdk_path)
                            jdks.append({
                                "name": entry.name,
                                "path": jdk_path,
                                "version": version
                            })
            except PermissionError:
                continue
                
        return jdks

    def _is_valid_jdk(self, path: str) -> bool:
        """Checks if a directory looks like a JDK home."""
        # Simple check: existence of bin/java.exe and bin/javac.exe
        # JREs might not have javac, but for 'JDK' tool usually we want javac
        java_exe = os.path.join(path, "bin", "java.exe")
        return os.path.exists(java_exe)

    def _get_jdk_version(self, path: str) -> str:
        """Extracts version string from java.exe."""
        java_exe = os.path.join(path, "bin", "java.exe")
        try:
            # Run java -version and capture stderr (java version output goes to stderr mostly)
            result = subprocess.run(
                [java_exe, "-version"], 
                capture_output=True, 
                text=True, 
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            # Output is usually "java version '1.8.0_...'" or "openjdk 17.0.1 ..."
            output = result.stderr if result.stderr else result.stdout
            lines = output.splitlines()
            if lines:
                return lines[0] # Return the first line usually containing the version
        except Exception:
            return "Unknown"
        return "Unknown"

    def get_current_jdk(self) -> Optional[str]:
        """Returns the path of the current JAVA_HOME."""
        return registry_utils.get_env_variable("JAVA_HOME")

    def set_jdk(self, path: str):
        """Sets the JAVA_HOME and updates Path."""
        # 1. Set JAVA_HOME
        registry_utils.set_env_variable("JAVA_HOME", path)
        
        # 2. Ensure %JAVA_HOME%\bin is in Path
        # We add separate entry or ensure the reference exists. 
        # Best practice: Add "%JAVA_HOME%\bin" literal to path if registry allows, 
        # but Python's winreg might resolve it. 
        # Simpler approach: Check if we are using exact path or variable.
        # Ideally, we want the PATH to contain "%JAVA_HOME%\bin".
        
        target_path_entry = r"%JAVA_HOME%\bin"
        registry_utils.append_to_path(target_path_entry)
        
        print(f"Set JAVA_HOME to {path}")

    def add_search_path(self, path: str):
        if path not in self.common_paths:
            self.common_paths.append(path)
