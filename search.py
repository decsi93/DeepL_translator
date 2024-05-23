from os import listdir, path, getcwd
from pymupdf import open as pdf_open
from subprocess import run
from platform import system
from time import sleep


def remove_trailing_semicolon(string_list):
    """
        Removes a trailing semicolon (';') from a string if it exists.

        Args:
            string_list: The string to check and potentially modify.

        Returns:
            The string with the trailing semicolon removed if it existed, otherwise the original string.
    """
    if string_list.endswith(';'):
        return string_list[:-1]  # Slice the string to remove the last character
    else:
        return string_list


def pdfs(file_names):
    """
        Processes a list of file names, handling trailing semicolons, adding missing '.pdf' extensions,
        ensuring uniqueness, and sorting the final list.

        Args:
            file_names: A string or list containing file names (potentially separated by semicolons).

        Returns:
            A sorted list of unique PDF file paths.
    """
    semicolon_counter = 0
    # Remove trailing semicolon if it exists
    file_names = (remove_trailing_semicolon(file_names))

    # Count semicolons to determine if separation is needed
    for file_name in file_names:
        for ch in file_name:
            if ch == ";":
                semicolon_counter += 1

    # Split on semicolons if there are multiple file names
    if ";" in file_names:
        file_names = file_names.split(";")
    else:
        # If no semicolons, convert the string to a list (assuming a single filename)
        file_names = [file_names]

    # Add '.pdf' extension if missing
    for file_name in file_names:
        if not file_name.endswith(".pdf"):
            file_names.remove(file_name)
            file_name = file_name + ".pdf"
            file_names.append(file_name)

    # Convert to set to ensure uniqueness, then back to list and sort
    file_names = set(file_names)
    file_names = list(file_names)

    return file_names


def search(search_keys: list):
    """
        Searches for PDF files in a specific directory based on a list of search keys.

        Args:
            search_keys: A list of file names or keywords to search for.

        Returns:
            A list of full paths to matching PDF files.
    """
    results = []
    source_pdfs = [f for f in listdir("Raw\\") if f.endswith(".pdf")]  # Get only PDF files

    for search_key in search_keys:
        for file_name in source_pdfs:
            if search_key in file_name:  # Check if search key is in the filename
                full_path = path.join(getcwd() + "\\Raw\\", file_name)
                found_in_done = search_key in listdir("Done\\")  # Check if exists in "Done\\"
                results.append(found_in_done)  # Append tuple with path and flag
                results.append(full_path)

    return results


def watermarking(pdf, watermark="watermark.png"):
    file = pdf_open(path.join(getcwd() + "\\.In_progress\\" + pdf))  # open a document

    for page_index in range(len(file)):  # iterate over pdf pages
        page = file[page_index]  # get the page
        # insert an image watermark from a file name to fit the page bounds
        page.insert_image(page.bound(), filename=watermark, overlay=True)

    file.save(path.join(getcwd() + "\\Done\\" + pdf))  # save the document with a new filename
    sleep(5)
    finished = path.join(getcwd() + "\\.In_progress\\" + pdf)
    remove_finished_temps(finished)


def remove_finished_temps(file_path):
    if system() == "Windows":
        run(['del', file_path], shell=True, check=True)
    else:
        run(['rm', file_path], check=True)


"""
test_files = 1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20; 
test_files = "1.pdf;2.pdf;3.pdf;5.pdf;6.pdf;7.pdf;9.pdf;10.pdf
;11.pdf;12.pdf;13.pdf;14.pdf;15.pdf;16.pdf;17.pdf;18.pdf;19.pdf;20.pdf;"

test_files = "a;b;c;d;e;f;g;"
print(pdfs(test_files))
"""
