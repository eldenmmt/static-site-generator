import os
import shutil
from copystatic import copy_files_recursive
from generate_page import generate_page

SOURCE_DIR = "static"
DEST_DIR = "public"

FROM_PATH = "content/index.md"
TEMPLATE_PATH = "template.html"
DEST_HTML_PATH = "public/index.html"

def main():
    print("Initiating the site building process...")

    if os.path.exists(DEST_DIR):
        print(f"Deleting the old folder: {DEST_DIR}/")
        shutil.rmtree(DEST_DIR)

    print(f"Copying static files from {SOURCE_DIR}/ to {DEST_DIR}/...")
    copy_files_recursive(SOURCE_DIR, DEST_DIR)

    generate_page(FROM_PATH, TEMPLATE_PATH, DEST_HTML_PATH)

    print("Build completed successfuly!")
    

if __name__ == "__main__":
    main()