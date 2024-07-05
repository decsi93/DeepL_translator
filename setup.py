# from itertools import product
from string import ascii_letters, digits, punctuation

ls = str(digits + ascii_letters + punctuation)
print(len(ls))

byt = 20497442737673217636335254372662635343505226212781934945547756536032971210714044111662233018898784996397633088879354537020160


prefixes = {
    "kilo": 0.001,
    "mega": 0.000_001,
    "giga": 0.000_000_001,
    "tera": 0.000_000_000_001,
    "peta": 1.000_000e-15,
    "exa": 1.000_000e-18,
    "zeta": 1.000_000e-21,
    "yota": 1.000_000e-24
}

# print(byt / giga)

# Define the base and the exponents
base = 94
first_exponent = 8
last_exponent = 63
number_of_terms = last_exponent - first_exponent + 1
common_ratio = base

# Calculate 94^8
a = base ** first_exponent

# Calculate 94^56
r_n = base ** number_of_terms

# Calculate the sum of the geometric series
S = a * (r_n - 1) // (common_ratio - 1)

for exponent in range(8, 21):
    size = base ** exponent
    for name, num in prefixes.items():
        print(f"{exponent}\t{size} in bytes")
        print(f"{exponent}\t{size * num} in {name}bytes\n")


"""from os import path, mkdir
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


"""
# SW: 2.0.32
# IP: 172.28.21.119
