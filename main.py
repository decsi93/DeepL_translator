import tkinter as tk
from tkinter import *
from tkinter import ttk
from platform import system
from file_dialog import open_files
from time import sleep
from datetime import datetime
from logging import basicConfig, getLogger, DEBUG
from deepl import Translator, DocumentTranslationException, DeepLException
from os import path, getcwd, listdir, replace
from watermarking import watermarking, remove_finished_temps, file_type
from threading import Thread

flag = False


# Initialize translator
# translator = Translator(API_key_string)


try:
    print(translator.get_usage())
except EXCEPTION:
    pass
    # tk.Label(window, text="Nem elérhetőek a DeepL szerverei").pack()




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
                    finished = ""
                    if check_state():
                        finished = path.join(getcwd() + "\\.In_progress\\HU_" + path.basename(file_path))
                    elif not check_state():
                        finished = path.join(getcwd() + "\\Done\\HU_" + path.basename(file_path))

                    print("Translation has begun")

                    translator.translate_document_from_filepath(input_path=file_path, output_path=finished,
                                                                target_lang="HU")

                    print("Translation Completed\n")
                    print(translator.get_usage())

                if check_state():
                    processing = listdir(".In_progress\\")
                    for file in processing:

                        if file_type(file)[1]:
                            watermarking(document=file, extension=file_type(file)[0])

                        if file_type(file)[1]:
                            replace(f".In_progress\\{file}", getcwd() + f"\\Done\\{file}")

                    sleep(1)
                    clear_temps()

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
    global flag, after_var, during_var

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


def gui():
    def screen_size():
        """
            Gets the screen width and height using a tool from win32api.

            Returns:
                The screen width and height in a list.
        """

        if system() == "Windows":
            import ctypes

            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()

            return [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

        elif system() == "MacOS":
            import Quartz

            main_display = Quartz.CGMainDisplayID()

            return [Quartz.CGDisplayPixelsWide(main_display), Quartz.CGDisplayPixelsHigh(main_display)]

        elif system() == "Linux":
            import subprocess

            output = subprocess.check_output("xrandr | grep '*' | awk '{print $1}'", shell=True)
            resolution = output.decode().strip().split('x')

            return [int(resolution[0]), int(resolution[1])]

        else:
            return [1920, 1080]

    # Create main window
    window = tk.Tk()
    window.title("DeepL Translator")
    window.geometry(f"{screen_size()[0] // 2}x{screen_size()[1] // 2}")  # Use integer division for window size

    fonts = ("ariel", 15)
    global after_var, during_var
    tk.Label(window, text="Válaszd ki a fordítandó dokumentumokat", font=fonts).pack()
    tk.Label(window, text="\nHa bevan pipálva akkor vízjelet rak minden támogatott file típúsra", font=fonts).pack()

    def check_state():
        global check_box_value

        return check_box_value.get()

    check_box_value = BooleanVar(window, True)

    ttk.Checkbutton(window, variable=check_box_value, command=check_state, image=).pack()

    def selected_files():
        files = ""
        # show what files are selected
        tk.Label(window, text=files, font=fonts)
        pass

    # file dialog
    tk.Button(window, text="Tallózás", font=fonts, command=selected_files, height=screen_size()[1]//350,
              width=(screen_size()[0]//350)+5).pack()

    # Translate button
    tk.Button(window, text="Fordítás", font=fonts, command=translate, height=screen_size()[1]//350,
              width=(screen_size()[0]//350)+5).pack()

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


gui()
