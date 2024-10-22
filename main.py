import tkinter as tk
from file_dialog import open_files
from time import sleep
from datetime import datetime
from logging import basicConfig, getLogger, DEBUG
from deepl import Translator, DocumentTranslationException, DeepLException
from os import path, getcwd, listdir
from search import watermarking, remove_finished_temps
from threading import Thread

flag = False


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


# Initialize translator
translator = Translator("4ec2251b-bd81-4a7a-bcd4-cb9366d4e0bb:fx")
# translator = Translator("47a52ad7-61c7-4ed0-826f-6cb857f05e07:fx") maxed out 2024.07.01
# translator = Translator("3ef91913-d4dc-44d7-a09c-e3e38b434d6c:fx") maxed out 2024.07.01
# translator = Translator("")

print(translator.get_usage())


def logger():
    # Configures basic logging to capture debug messages from the DeepL library.
    basicConfig()
    getLogger("DeepL").setLevel(DEBUG)


def clear_temps():
    temps = listdir(".In_progress")
    for temp in temps:
        remove_finished_temps(".In_progress\\" + temp)


def translate():
    def task():
        """
            Attempts to translate the provided PDF paths using the DeepL API.

            Handles DocumentTranslationException and DeepLException errors and logs them with timestamps.
        """
        global after_var, during_var, flag
        flag = True

        try:
            logger()
            # Get the list of PDF paths from the search function (assuming it returns a list)
            paths = open_files()
            while paths is None:
                sleep(1)
            if paths is not None:
                print("Initiating")
                for file_path in paths:

                    # finished = path.join(getcwd() + "\\.In_progress\\HU_" + path.basename(file_path))
                    finished = path.join(getcwd() + "\\Done\\HU_" + path.basename(file_path))
                    sleep(1.5)
                    print("Translating")

                    translator.translate_document_from_filepath(input_path=file_path, output_path=finished,
                                                                target_lang="HU")

                    print("Translate Complete\n")
                    print(translator.get_usage())

                """processing = listdir(".In_progress\\")
                for item in processing:
                    watermarking(item)
"""
                sleep(1)
                # clear_temps()

                print("\nFinished\n")
                print(translator.get_usage())

        except DocumentTranslationException as error:
            handle_errors(error, "UTÁN")

        except DeepLException as error:
            handle_errors(error, "KÖZBEN")

    translation_thread = Thread(target=task)
    translation_thread.start()

    """status_thread = Thread(target=update_status())
    status_thread.start()
    """


def handle_errors(error, when):
    global flag
    flag = False
    if when == "UTÁN":
        doc_id = error.document_handle.document_id
        doc_key = error.document_handle.document_key
        after_var.set(f"Hiba történt feltöltés UTÁN: {error}")
        after = after_var.get()
        after += f"id: {doc_id}, key: {doc_key}"
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


# Input path section with labels and entry field
tk.Label(window, text="Válaszd ki a fordítandó dokumentumokat", font=("ariel", 13)).pack()

# Translate button
tk.Button(window, text="Tallózás", font=("airel", 14), command=translate, height=screen_size("w")//350,
          width=screen_size("w")//200).pack()


"""tk.Button(window, text="törlés", font=("airel", 14),
          command=clear_temps, height=screen_size("w")//175,
          width=screen_size("w")//100).pack()
"""

# Error display (after)
after_var = tk.StringVar()
tk.Label(window, textvariable=after_var).pack()

# Error display (during)
during_var = tk.StringVar()
tk.Label(window, textvariable=during_var).pack()

"""
class MockDocumentStatus:
    done = False
    seconds_remaining = 120


def update_status():
    global flag, MockDocumentStatus, doc_status

    def update_and_check():
        if not flag:
            return  # Exit if flag is False

        if not MockDocumentStatus.done:
            msg = f"{MockDocumentStatus.seconds_remaining} másodperc van hátra"
            doc_status.set(msg)  # Update the StringVar

            # Update the label text using tkinter.after() for UI thread
            window.after(0, lambda: doc_label.config(text=doc_status.get()))
            print(doc_status.get())

            MockDocumentStatus.seconds_remaining -= 2

            if MockDocumentStatus.seconds_remaining <= 0:
                MockDocumentStatus.done = True

        # Schedule the next update after 2 seconds (adjust as needed)
        if flag:
            Timer(2, update_and_check).start()

    # Start the initial update
    update_and_check()


doc_status = tk.StringVar()
doc_label = tk.Label(window, text="")
doc_label.pack()
"""

# Run the main event loop
window.mainloop()
