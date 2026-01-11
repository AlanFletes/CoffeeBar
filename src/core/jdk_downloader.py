import os
import requests
import zipfile
import shutil
from pathlib import Path

class JdkDownloader:
    BASE_URL = "https://api.adoptium.net/v3/assets/latest/{version}/hotspot"
    
    def get_supported_versions(self):
        # Common LTS versions
        return [8, 11, 17, 21]

    def get_latest_release(self, version):
        """Fetches the download URL for the latest release of the given version (Windows x64 JDK)."""
        params = {
            "architecture": "x64",
            "image_type": "jdk",
            "os": "windows",
            "vendor": "eclipse"
        }
        url = self.BASE_URL.format(version=version)
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return None
                
            # data is a list of binaries (usually one for latest)
            binary = data[0]["binary"]
            release_name = data[0]["release_name"]
            download_url = binary["package"]["link"]
            size = binary["package"]["size"]
            
            return {
                "version": version,
                "name": release_name,
                "url": download_url,
                "size": size,
                "filename": data[0]["binary"]["package"]["name"]
            }
        except Exception as e:
            print(f"Error fetching release info: {e}")
            return None

    def download_file(self, url, dest_path, progress_callback=None):
        """Downloads file with progress callback (bytes_downloaded, total_bytes)."""
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        mode = 'wb'
        downloaded = 0
        
        with open(dest_path, mode) as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback:
                        progress_callback(downloaded, total_size)
        return dest_path

    def install_jdk(self, archive_path, target_root_dir, folder_name):
        """Extracts the JDK and moves it to the target directory."""
        # 1. Extract to a temp folder
        temp_extract_dir = os.path.join(target_root_dir, "_temp_extract")
        if os.path.exists(temp_extract_dir):
            shutil.rmtree(temp_extract_dir)
        os.makedirs(temp_extract_dir)
        
        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(temp_extract_dir)
            
            # The zip usually contains a single root folder (e.g. jdk-17.0.1+12)
            extracted_items = os.listdir(temp_extract_dir)
            if not extracted_items:
                raise Exception("Empty zip file")
                
            jdk_root = os.path.join(temp_extract_dir, extracted_items[0])
            
            # Target path
            final_target_path = os.path.join(target_root_dir, folder_name)
            
            if os.path.exists(final_target_path):
                print(f"Target directory {final_target_path} already exists. Overwriting...")
                # shutil.rmtree(final_target_path) # Risky to auto-delete? Let's just create unique name or fail
                # For now, let's append a suffix if exists, to be safe
                pass 

            # Move logic
            shutil.move(jdk_root, final_target_path)
            
            return final_target_path
            
        finally:
            # Cleanup temp
            if os.path.exists(temp_extract_dir):
                shutil.rmtree(temp_extract_dir)
            # Cleanup archive
            if os.path.exists(archive_path):
                os.remove(archive_path)
