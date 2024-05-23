import tkinter as tk
from time import sleep
from datetime import datetime
from logging import basicConfig, getLogger, DEBUG
from deepl import Translator, DocumentTranslationException, DeepLException
from os import path, getcwd, listdir
from search import search, pdfs, watermarking
from threading import Thread

flag = False


# Initialize translator
translator = Translator("4ec2251b-bd81-4a7a-bcd4-cb9366d4e0bb:fx")
print(translator.get_usage())


def logger():
    # Configures basic logging to capture debug messages from the DeepL library.
    basicConfig()
    getLogger("DeepL").setLevel(DEBUG)


def translate():
    def task():
        """
            Attempts to translate the provided PDF paths using the DeepL API.

            Handles DocumentTranslationException and DeepLException errors and logs them with timestamps.
        """
        global after_var, during_var, input_var, flag
        flag = True

        try:
            logger()
            # Get the list of PDF paths from the search function (assuming it returns a list)
            paths = search(pdfs(input_var.get()))
            for i in range(len(paths) - 1):
                if type(paths) is bool:
                    if not paths[i]:
                        finished = path.join(getcwd() + "\\.In_progress\\HU_" + path.basename(paths[i + 1]))

                        sleep(1.5)

                        translator.translate_document_from_filepath(input_path=paths[i + 1], output_path=finished,
                                                                    target_lang="HU")

                        processing = listdir(".In_progress\\")
                        for item in processing:
                            watermarking(item)

                    else:
                        tk.Label(window, text=f"Ez a dokumentum ({path.basename(paths[i + 1])}) már létezik!",
                                 font=("ariel", 13, "RED")).pack()

        except DocumentTranslationException as error:
            handle_errors(error, "UTÁN")

        except DeepLException as error:
            handle_errors(error, "KÖZBEN")

    translation_thread = Thread(target=task)
    translation_thread.start()
    status_thread = Thread(target=update_status())
    status_thread.start()


def handle_errors(error, when):
    global flag
    flag = False
    if when == "UTÁN":
        doc_id = error.document_handle.document_id
        doc_key = error.document_handle.document_key
        after_var.set(f"Hiba történt feltöltés UTÁN: {error}, id: {doc_id}, key: {doc_key}")
        after = after_var.get()
        print(after)
        logs = open("error_logs.txt", "a")
        print(f"{after}\t{datetime.now()}", file=logs)  # Use datetime.now() for current time
        logs.close()

    elif when == "KÖZBEN":
        during_var.set(f"Hiba történt feltöltés KÖZBEN: {error}")
        during = during_var.get()
        print(during)
        logs = open("error_logs.txt", "a")
        print(f"{during}\t{datetime.now()}", file=logs)
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

    root.destroy()


# Create main window
window = tk.Tk()
window.title("DeepL Translator")
window.geometry(f"{screen_size("w")//2}x{screen_size("h")//4}")  # Use integer division for window size

# Input path section with labels and entry field
tk.Label(window, text="Pontos vesszővel válaszd el a neveket", font=("ariel", 13)).pack()

tk.Label(window, text="Fordítandó PDF-ek teljes neve:", font=("ariel", 13)).pack()

input_var = tk.StringVar()
tk.Entry(window, textvariable=input_var, width=(screen_size("w")//20), font=("airel", 12)).pack()

# Translate button
tk.Button(window, text="Küldés", font=("airel", 14), command=translate, height=screen_size("w")//350,
          width=screen_size("w")//200).pack()


# Error display (after)
after_var = tk.StringVar()
tk.Label(window, textvariable=after_var).pack()

# Error display (during)
during_var = tk.StringVar()
tk.Label(window, textvariable=during_var).pack()


class MockDocumentStatus:
    done = False
    seconds_remaining = 120


DocumentStatus = MockDocumentStatus


def update_status():
    global flag
    while flag:
        sleep(2)
        if not DocumentStatus.done:
            msg = f"{DocumentStatus.seconds_remaining} másodperc van hátra"
            doc_status.set(msg)
            DocumentStatus.seconds_remaining -= 2
            if DocumentStatus.seconds_remaining <= 0:
                DocumentStatus.done = True
        if not flag:
            break


doc_status = tk.StringVar()
tk.Label(window, textvariable=doc_status).pack()


# Run the main event loop
window.mainloop()
