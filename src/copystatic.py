import os
from datetime import datetime
import shutil

def copy_static_to_dest(static_path, dest_path):
    with open("log.txt", "a") as file:
        file.write(f"\n{datetime.now()} - Application started.\n")

    clear_destination(dest_path) 
    copy_folder(static_path, dest_path)

def copy_folder(copy_path, dest_path):
    contents = os.listdir(copy_path)
    for item in contents:
        copy = os.path.join(copy_path, item)
        if not os.path.isfile(copy):            
            dest = os.path.join(dest_path, item)
            os.makedirs(dest, exist_ok=True)
            with open("log.txt", "a") as file:
                file.write(f"Directory: {dest} successfully created.\n")
            copy_folder(copy, dest)
            continue

        shutil.copy(copy, dest_path)
        with open("log.txt", "a") as file:
            file.write(f"File: {copy} successfully copied.\n")


def clear_destination(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))