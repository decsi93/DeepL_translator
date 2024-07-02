from tkinter import filedialog as fd

# Create a function to open the file dialog


def open_files():
    # Specify the file types
    filetypes = ('documents', '*.DOCX *.PPTX *.XLSX *.PDF *.HTML *.TXT *.STR')
    # Show the open file dialog allowing multiple file selection
    filenames = fd.askopenfilenames(filetypes=filetypes, initialdir="Raw\\")
    file_paths = []
    if filenames is not None:
        # Append each selected file path to the list
        for filename in filenames:
            file_paths.append(filename)

        return file_paths

    else:
        return None
