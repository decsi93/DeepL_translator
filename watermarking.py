from os import path, getcwd
from pymupdf import open as pdf_open
from subprocess import run
from platform import system


def file_type(file_name: str):
    watermarkable = [".docx", ".pptx", ".xlsx", ".pdf", ".html"]
    non_watermarkable = [".txt", ".srt", ".xlf", ".xliff"]
    flag = None
    for extension in watermarkable:
        if file_name.endswith(extension):
            flag = True
            file_suffix = extension
            break

    if flag is None:
        for extension in non_watermarkable:
            if file_name.endswith(extension):
                flag = False
                file_suffix = extension
                break

    return file_suffix, flag


def watermarking(document, extension, watermark="watermark.png"):
    if extension == ".pdf":
        file = pdf_open(path.join(getcwd() + "\\.In_progress\\" + document))  # open a document

        for page_index in range(len(file)):  # iterate over pdf pages
            page = file[page_index]  # get the page
            # insert an image watermark from a file name to fit the page bounds
            page.insert_image(page.bound(), filename=watermark, overlay=True)

        file.save(path.join(getcwd() + "\\Done\\" + document))  # save the document with a new filename

    if extension == ".docx":
        pass

    if extension == ".pptx":
        pass

    if extension == ".xlsx":
        pass

    if extension == ".html":
        pass


def remove_finished_temps(file_path):
    if system() == "Windows":
        run(['del', file_path], shell=True, check=True)
    else:
        run(['rm', file_path], check=True)
