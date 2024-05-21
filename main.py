import tkinter as tk
from time import sleep
from datetime import datetime
from logging import basicConfig, getLogger, DEBUG
from deepl import Translator, DocumentTranslationException, DeepLException
from os import path, getcwd
from search import search, pdfs

# Initialize translator
translator = Translator("4ec2251b-bd81-4a7a-bcd4-cb9366d4e0bb:fx")
print(translator.get_usage())


def logger():
    # Configures basic logging to capture debug messages from the DeepL library.
    basicConfig()
    getLogger("DeepL").setLevel(DEBUG)


def translate():
    """
        Attempts to translate the provided PDF paths using the DeepL API.

        Handles DocumentTranslationException and DeepLException errors and logs them with timestamps.
    """
    global after_var, during_var, input_var
    try:
        logger()
        # Get the list of PDF paths from the search function (assuming it returns a list)
        paths = search(pdfs(input_var.get()))
        print(paths)
        for file_path in paths:
            finished = path.join(getcwd() + "\\Done\\HU_" + path.basename(file_path))

            sleep(1.5)

            translator.translate_document_from_filepath(input_path=file_path, output_path=finished,
                                                        target_lang="HU", formality="more")

    except DocumentTranslationException as error:
        doc_id = error.document_handle.document_id
        doc_key = error.document_handle.document_key
        after_var.set(f"Hiba történt feltöltés UTÁN: {error}, id: {doc_id}, key: {doc_key}")

        print(after_var.get())
        logs = open("error_logs.txt", "a")
        print(f"{after_var.get()}\t{datetime}", file=logs)  # Use datetime.now() for current time
        logs.close()

    except DeepLException as error:
        during_var.set(f"Hiba történt feltöltés KÖZBEN: {error}")
        print(during_var.get())
        logs = open("error_logs.txt", "a")
        print(f"{during_var}\t{datetime}", file=logs)
        logs.close()


def screen_size(parameter):
    """
        Gets the screen width or height using a hidden Tkinter window.

        Args:
            parameter: "w" for width, "h" for height.

        Returns:
            The screen width or height as an integer.
    """
    root = tk.Tk()
    root.withdraw()

    if parameter == "w":
        width = root.winfo_screenwidth()
        root.destroy()
        return width

    elif parameter == "h":
        height = root.winfo_screenheight()
        root.destroy()
        return height


# Create main window
window = tk.Tk()
window.title("DeepL Translator")
window.geometry(f"{screen_size("w")//2}x{screen_size("h")//4}")  # Use integer division for window size

# Input path section with labels and entry field
input_verification_label = tk.Label(window, text="Pontos vesszővel válaszd el a neveket", font=("ariel", 13))

input_label = tk.Label(window, text="Fordítandó PDF-ek teljes neve:", font=("ariel", 13))
input_label.pack()

input_var = tk.StringVar()
input_entry = tk.Entry(window, textvariable=input_var, width=(screen_size("w")//20), font=("airel", 12))
input_entry.pack()
input_verification_label.pack()

# Translate button
translate_button = tk.Button(window, text="Küldés", font=("airel", 14), command=translate,
                             height=screen_size("w")//350, width=screen_size("w")//200)
translate_button.pack()

# Error display (after)
after_var = tk.StringVar()
after_label = tk.Label(window, textvariable=after_var)
after_label.pack()

# Error display (during)
during_var = tk.StringVar()
during_label = tk.Label(window, textvariable=during_var)
during_label.pack()


# paths = search(pdfs(input_var.get()))


# Run the main event loop
window.mainloop()
