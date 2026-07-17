import os
import shutil

def copy_files_recursive(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        print(f"Creating destiny path: {dest_dir}")
        os.mkdir(dest_dir)

    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        print(f"Processing: {source_path} -> {dest_path}")

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            copy_files_recursive(source_path, dest_path)