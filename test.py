from reportlab.pdfgen import canvas


def create_empty_pdf(filename, num_pages=1):
    """
    Creates a new PDF document with the specified filename and number of pages.

    Args:
        filename (str): The name of the PDF file to create.
        num_pages (int, optional): The number of empty pages to include in the PDF. Defaults to 1.
    """

    # Create a new PDF document
    if not filename.endswith(".pdf"):
        filename += ".pdf"

    c = canvas.Canvas(filename)

    # Add empty pages (if more than one)
    if num_pages > 1:
        for _ in range(1, num_pages):
            c.showPage()

    # Save the PDF
    c.save()
"""

for i in range(20):
    create_empty_pdf(filename=f"{i+1}", num_pages=1)
"""