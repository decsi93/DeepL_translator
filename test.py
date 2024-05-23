from os import path, getcwd
import pymupdf
import os
import ctypes
import tqdm


def check_prep(path):
    if not os.path.exists(path):
        os.makedirs(path)
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ret = ctypes.windll.kernel32.SetFileAttributesW(path, FILE_ATTRIBUTE_HIDDEN)


path = "hello/ji"
check_prep(path)


def watermarking(pdf, watermark="watermark2.png"):
    file = pymupdf.open(pdf)  # open a document

    for page_index in range(len(file)):  # iterate over pdf pages
        page = file[page_index]  # get the page
        # insert an image watermark from a file name to fit the page bounds
        page.insert_image(page.bound(), filename=watermark, overlay=True)

    file.save("\\Done\\" + pdf)  # save the document with a new filename


def create_empty_pdf(filename, num_pages=2):
    """
    Creates a new PDF document with the specified filename and number of pages.

    Args:
        filename (str): The name of the PDF file to create.
        num_pages (int, optional): The number of empty pages to include in the PDF. Defaults to 1.
    """

    # Create a new PDF document
    if not filename.endswith(".pdf"):
        filename += ".pdf"
    """
    c = canvas.Canvas(filename)

    # Add empty pages (if more than one)
    if num_pages > 1:
        for _ in range(1, num_pages):
            c.showPage()

    # Save the PDF
    c.save()
    """

# create_empty_pdf("test.pdf")


"""

for i in range(20):
    create_empty_pdf(filename=f"{i+1}", num_pages=1)
"""