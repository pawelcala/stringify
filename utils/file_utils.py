import os

from utils.log_utils import log_step


def find_files(path='.', filename_regex=None):
    found_files = []
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            list = find_files(filepath, filename_regex)
            found_files.extend(list)
        elif os.path.isfile(filepath):
            if filename_regex and filename.startswith(filename_regex):
                found_files.append(filepath)
            elif filename_regex is None:
                found_files.append(filepath)

    return found_files


def save_file(content, dir_name, file_name):
    current_dir = os.getcwd()
    try:
        os.makedirs(dir_name, exist_ok=True)
    except Exception:
        pass

    try:
        os.chdir(dir_name)
    except Exception:
        pass

    log_step("Saving file {}/{}".format(os.getcwd(), file_name))
    file = open(file_name, "w")
    file.write(content)
    file.close()
    os.chdir(current_dir)
