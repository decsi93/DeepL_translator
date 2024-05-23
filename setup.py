from os import path, mkdir
from subprocess import run, PIPE, CalledProcessError
directories = ["Raw", "Done", ".In_progress"]


def check_prep(file_path):
    dir_path = fr"{file_path}"
    if not path.exists(dir_path):
        mkdir(dir_path)
        if file_path.startswith("."):
            set_hidden_attribute(dir_path)


def set_hidden_attribute(folder_path):
    try:
        # Ensure folder_path is a valid string and handle backslashes
        folder_path = folder_path.replace('\\', '\\\\')

        # Construct the command
        command = f'attrib +h "{folder_path}"'

        # Execute the command
        result = run(command, shell=True, check=True, text=True, stdout=PIPE, stderr=PIPE)

    except CalledProcessError as e:
        print(f"Error occurred: {e}")
        print("Output:", e.stdout)
        print("Error:", e.stderr)


for file_path in directories:
    check_prep(file_path)
