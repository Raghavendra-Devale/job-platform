import os
import shutil
import glob

def copy_images():
    brain_dir = r"C:\Users\devale\.gemini\antigravity-ide\brain\973f0790-1de6-4dfa-a4cf-256b73929797"
    dest_dir = r"c:\Users\devale\Dev\Learning\job platform\assets\screenshots"
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created destination directory: {dest_dir}")
        
    mappings = {
        "admin_sync": "admin_sync.png",
        "profile_settings": "profile_settings.png",
        "resume_status": "resume_status.png",
        "recommendations": "recommendations.png",
        "dashboard": "dashboard.png"
    }
    
    for prefix, target_name in mappings.items():
        pattern = os.path.join(brain_dir, f"{prefix}_*.png")
        matching_files = glob.glob(pattern)
        
        if matching_files:
            # Get the latest matching file
            matching_files.sort(key=os.path.getmtime)
            src_file = matching_files[-1]
            dest_file = os.path.join(dest_dir, target_name)
            shutil.copy2(src_file, dest_file)
            print(f"Copied: {os.path.basename(src_file)} -> {target_name}")
        else:
            print(f"No file found starting with: {prefix}_ in {brain_dir}")

if __name__ == "__main__":
    copy_images()
