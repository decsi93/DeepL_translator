from os import listdir, path, getcwd
from reportlab.pdfgen import canvas


def pdfs(file_names):
    semicolon_counter = 0
    for ch in file_names:
        if ch == ";":
            semicolon_counter += 1

    if semicolon_counter > 0:
        file_names = file_names.split(";")
    else:
        list(file_names)

    search(file_names)


def search(search_key: list):
    for elements in search_key:
        pass
    source_pdfs = listdir("Raw\\")
    for file_name in source_pdfs:
        if search_key == file_name:
            return path.join(getcwd(), file_name)


def create_empty_pdf(filename, num_pages=1):
    """
    Creates a new PDF document with the specified filename and number of pages.

    Args:
        filename (str): The name of the PDF file to create.
        num_pages (int, optional): The number of empty pages to include in the PDF. Defaults to 1.
    """

    # Create a new PDF document
    if filename[-4:] != ".pdf":
        filename += ".pdf"

    c = canvas.Canvas(filename)

    # Add empty pages (if more than one)
    if num_pages > 1:
        for _ in range(1, num_pages):
            c.showPage()

    # Save the PDF
    c.save()


"""for i in range(20):
    create_empty_pdf(filename=f"{i+1}", num_pages=1)
"""

test_files = "1;2;3;5;6;7;9;10;11;12;13;14;15;16;17;18;19;20"
# pdfs(test_files)
