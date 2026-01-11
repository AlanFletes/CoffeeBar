import os
import winreg
import ctypes
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, LPVOID

HW_BROADCAST = 0xFFFF
WM_SETTINGCHANGE = 0x001A

def get_env_variable(name, user=True):
    """Retrieves an environment variable from the registry."""
    key = winreg.HKEY_CURRENT_USER if user else winreg.HKEY_LOCAL_MACHINE
    subkey = r"Environment" if user else r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    try:
        with winreg.OpenKey(key, subkey) as reg_key:
            value, _ = winreg.QueryValueEx(reg_key, name)
            return value
    except FileNotFoundError:
        return None

def set_env_variable(name, value, user=True):
    """Sets an environment variable in the registry."""
    key = winreg.HKEY_CURRENT_USER if user else winreg.HKEY_LOCAL_MACHINE
    subkey = r"Environment" if user else r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    
    with winreg.CreateKey(key, subkey) as reg_key:
        winreg.SetValueEx(reg_key, name, 0, winreg.REG_SZ, value)

    broadcast_settings_change()

def append_to_path(value, user=True):
    """Appends a value to the Path environment variable if not present."""
    current_path = get_env_variable("Path", user) or ""
    parts = [p.strip() for p in current_path.split(";") if p.strip()]
    
    # Check if value is already in path (case insensitive)
    if not any(p.lower() == value.lower() for p in parts):
        parts.append(value)
        new_path = ";".join(parts)
        # Use REG_EXPAND_SZ for Path to allow %variables%
        key = winreg.HKEY_CURRENT_USER if user else winreg.HKEY_LOCAL_MACHINE
        subkey = r"Environment" if user else r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        with winreg.CreateKey(key, subkey) as reg_key:
             winreg.SetValueEx(reg_key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        broadcast_settings_change()

def broadcast_settings_change():
    """Broadcasts a message to all top-level windows that settings have changed."""
    SendMessageTimeout = ctypes.windll.user32.SendMessageTimeoutW
    # lParam (4th arg) is polymorphic. For WM_SETTINGCHANGE it is a LPCWSTR (c_wchar_p).
    SendMessageTimeout.argtypes = [HWND, UINT, WPARAM, ctypes.c_wchar_p, UINT, UINT, LPVOID]
    SendMessageTimeout.restype = LPARAM
    
    # Notify apps of environment change
    SendMessageTimeout(HW_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", 0x0002, 5000, None)
