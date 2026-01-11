import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
from coffeebar.core.jdk_manager import JdkManager
from coffeebar.core.jdk_downloader import JdkDownloader

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class DownloadWindow(ctk.CTkToplevel):
    def __init__(self, master, on_complete):
        super().__init__(master)
        self.title("Download JDK")
        self.geometry("400x350")
        self.on_complete = on_complete
        self.downloader = JdkDownloader()
        
        # Center the window
        self.update_idletasks()
        width = 400
        height = 350
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        self.lbl = ctk.CTkLabel(self, text="Select Java Version (Eclipse Temurin):", font=("Roboto", 14))
        self.lbl.pack(pady=(20, 10))
        
        self.version_var = ctk.StringVar(value="17")
        self.combo = ctk.CTkComboBox(self, values=[str(v) for v in self.downloader.get_supported_versions()], variable=self.version_var)
        self.combo.pack(pady=10)
        
        self.btn_download = ctk.CTkButton(self, text="Download & Install", command=self.start_download)
        self.btn_download.pack(pady=20)
        
        self.progress = ctk.CTkProgressBar(self)
        self.progress.pack(pady=10, padx=40, fill="x")
        self.progress.set(0)
        
        self.status_lbl = ctk.CTkLabel(self, text="")
        self.status_lbl.pack(pady=5)

    def start_download(self):
        version = int(self.version_var.get())
        self.btn_download.configure(state="disabled")
        threading.Thread(target=self.run_download, args=(version,), daemon=True).start()

    def run_download(self, version):
        self.update_status(f"Fetching info for Java {version}...", 0)
        release = self.downloader.get_latest_release(version)
        if not release:
            self.update_status("Error: Could not find release.", 0)
            self.after(0, lambda: self.btn_download.configure(state="normal"))
            return
            
        self.update_status(f"Downloading {release['name']}...", 0)
        
        target_root = os.path.join(os.environ["USERPROFILE"], ".jdks")
        if not os.path.exists(target_root):
            os.makedirs(target_root)
        
        # Ensure regex is imported or handled
        import re
        safe_name = re.sub(r'[^a-zA-Z0-9\-\.]', '_', release['name'])
        filename = f"{safe_name}.zip"
        archive_path = os.path.join(target_root, filename)
        
        def progress_cb(downloaded, total):
            pct = downloaded / total
            self.after(0, lambda: self.progress.set(pct))
            
        try:
            self.downloader.download_file(release['url'], archive_path, progress_cb)
            
            self.update_status("Extracting...", 1.0)
            
            folder_name = f"temurin-{safe_name}"
            
            self.downloader.install_jdk(archive_path, target_root, folder_name)
            
            self.update_status("Done!", 1.0)
            self.after(0, self.finish)
        except Exception as e:
            self.update_status(f"Error: {str(e)[:50]}...", 0)
            self.after(0, lambda: self.btn_download.configure(state="normal"))

    def update_status(self, text, progress_val=None):
        self.after(0, lambda: self.status_lbl.configure(text=text))
        if progress_val is not None:
             self.after(0, lambda: self.progress.set(progress_val))
        
    def finish(self):
        messagebox.showinfo("Success", "JDK Installed Successfully!")
        self.destroy()
        self.on_complete()

class JdkFrame(ctk.CTkFrame):
    def __init__(self, master, jdk, is_active, on_select):
        super().__init__(master)
        self.jdk = jdk
        self.on_select = on_select

        # Layout
        self.grid_columnconfigure(0, weight=1)
        
        # Colors
        bg_color = "transparent" if not is_active else ("#3B8ED0", "#1F6AA5") # Accent color if active
        self.configure(fg_color=bg_color)

        self.lbl_name = ctk.CTkLabel(self, text=jdk["name"], font=("Roboto", 16, "bold"))
        self.lbl_name.grid(row=0, column=0, sticky="w", padx=10, pady=(10,0))

        self.lbl_version = ctk.CTkLabel(self, text=jdk["version"], font=("Roboto", 12))
        self.lbl_version.grid(row=1, column=0, sticky="w", padx=10, pady=(0,10))
        
        self.lbl_path = ctk.CTkLabel(self, text=jdk["path"], font=("Roboto", 10), text_color="gray")
        self.lbl_path.grid(row=2, column=0, sticky="w", padx=10, pady=(0,10))

        btn_text = "Active" if is_active else "Set Active"
        state = "disabled" if is_active else "normal"
        self.btn_action = ctk.CTkButton(self, text=btn_text, state=state, command=self.select_jdk)
        self.btn_action.grid(row=0, column=1, rowspan=3, padx=10, sticky="e")
        
        # Corner radius for elegance
        self.configure(corner_radius=10)

    def select_jdk(self):
        self.on_select(self.jdk["path"])

class CoffeeBarApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.manager = JdkManager()
        
        self.title("CoffeeBar - Java Manager")
        self.geometry("600x500")
        
        # Header
        self.header = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.header.pack(fill="x", padx=0, pady=0)
        
        self.lbl_title = ctk.CTkLabel(self.header, text="☕ CoffeeBar", font=("Roboto", 24, "bold"))
        self.lbl_title.pack(side="left", padx=20, pady=15)

        self.btn_scan = ctk.CTkButton(self.header, text="Add search path", command=self.add_path, width=120)
        self.btn_scan.pack(side="right", padx=10, pady=15)
        
        self.btn_download = ctk.CTkButton(self.header, text="⬇ Install JDK", command=self.open_download_window, width=120)
        self.btn_download.pack(side="right", padx=10, pady=15)
        
        self.btn_refresh = ctk.CTkButton(self.header, text="Refresh", command=self.refresh_list, width=80)
        self.btn_refresh.pack(side="right", padx=10, pady=15)

        # Content
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Available JDKs")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.status_bar = ctk.CTkLabel(self, text="Ready", anchor="w")
        self.status_bar.pack(fill="x", side="bottom", padx=20, pady=5)
        
        self.refresh_list()

    def refresh_list(self):
        # Clear existing
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        jdks = self.manager.find_jdks()
        current_jdk = self.manager.get_current_jdk()
        
        if not jdks:
            ctk.CTkLabel(self.scroll_frame, text="No JDKs found in standard locations.").pack(pady=20)
        
        for jdk in jdks:
            is_active = False
            if current_jdk and os.path.normpath(current_jdk) == os.path.normpath(jdk["path"]):
                is_active = True
                
            frame = JdkFrame(self.scroll_frame, jdk, is_active, self.set_active_jdk)
            frame.pack(fill="x", expand=True, padx=5, pady=5)
            
    def set_active_jdk(self, path):
        try:
            self.manager.set_jdk(path)
            self.status_bar.configure(text=f"Set JAVA_HOME to {path}")
            self.refresh_list()
            messagebox.showinfo("Success", "JAVA_HOME updated successfully!\nNote: Restart terminals to see changes.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_download_window(self):
        DownloadWindow(self, self.refresh_list)

    def add_path(self):
        path = filedialog.askdirectory()
        if path:
            self.manager.add_search_path(path)
            self.refresh_list()
            
if __name__ == "__main__":
    app = CoffeeBarApp()
    app.mainloop()
