from os import listdir, path, getcwd


def search(search_key):
    source_pdfs = listdir("Raw\\")
    for filename in source_pdfs:
        if search_key == filename:
            return path.join(getcwd(), filename)
