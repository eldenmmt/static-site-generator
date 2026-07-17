import os
import shutil
from copystatic import copy_files_recursive

SOURCE_DIR = "static"
DEST_DIR = "public"

def main():
    print("Initiating the site building process...")

    if os.path.exists(DEST_DIR):
        print(f"Deleting the old folder: {DEST_DIR}/")
        shutil.rmtree(DEST_DIR)

    print(f"Copying static files from {SOURCE_DIR}/ to {DEST_DIR}/...")
    copy_files_recursive(SOURCE_DIR, DEST_DIR)

    print("Build completed successfuly!")
    

if __name__ == "__main__":
    main()