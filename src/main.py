import os
import shutil
from copystatic import copy_files_recursive
from generate_page import generate_page, generate_pages_recursive
import sys

SOURCE_DIR = "static"
DEST_DIR = "docs"
CONTENT_DIR = "content"

FROM_PATH = "content/index.md"
TEMPLATE_PATH = "template.html"
DEST_HTML_PATH = "public/index.html"

def main():
    print("Initiating the site building process...")

    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    if os.path.exists(DEST_DIR):
        print(f"Deleting the old folder: {DEST_DIR}/")
        shutil.rmtree(DEST_DIR)

    print(f"Copying static files from {SOURCE_DIR}/ to {DEST_DIR}/...")
    copy_files_recursive(SOURCE_DIR, DEST_DIR)

    generate_pages_recursive(CONTENT_DIR, TEMPLATE_PATH, DEST_DIR, basepath)

    print("Build completed successfuly!")
    

if __name__ == "__main__":
    main()