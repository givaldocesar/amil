import os

def save_script(directory, file_name, data):
    path = os.path.join(directory, file_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(data))