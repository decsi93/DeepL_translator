import tkinter as tk
from deepl import Translator, DocumentTranslationException, DeepLException
from datetime import datetime
from search import search
from logging import basicConfig, getLogger, DEBUG
flag = 1

def screen_size(parameter):
    root = tk.Tk()
    root.withdraw()

    if parameter == "width" or "w":
        width = root.winfo_screenwidth()
        root.destroy()
            return width

        elif parameter == "height" or "h":
            height = root.winfo_screenheight()
            root.destroy()
            return height

    # Create main window
    window = tk.Tk()
    window.title("DeepL Translator")
    window.geometry(f"{screen_size("w")//2}x{screen_size("h")//2}")

    # Input path
    print(flag)
    input_label = tk.Label(window, text="Fordítandó PDF-ek teljes neve:" if flag == 1 else "Fordítandó PDF teljes neve:")
    input_label.pack()
    input_var = tk.StringVar()
    input_entry = tk.Entry(window, textvariable=input_var)
    input_entry.pack()

    def update():
        global input_label
        if check_box_status.get():
            text = "Fordítandó PDF-ek teljes neve:"

        else:
            text = "Fordítandó PDF teljes neve:"
        window.mainloop()
        input_label = tk.Label(window, text=text)
        return input_label.pack()

    check_box_status = tk.IntVar(value=1)
    check_box = tk.Checkbutton(window, text="Több PDF fordítása", variable=check_box_status,
                               onvalue=1, offvalue=0, command=update)
    check_box.pack()

    # Output path
    output_label = tk.Label(window, text="Kimeneti file:")
    output_label.pack()
    output_var = tk.StringVar()
    output_entry = tk.Entry(window, textvariable=output_var)
    output_entry.pack()

    # Translate button
    translate_button = tk.Button(window, text="Küldés", command=translate)
    translate_button.pack()

    # Error display (after)
    after_var = tk.StringVar()
    after_label = tk.Label(window, textvariable=after_var)
    after_label.pack()

    # Error display (during)
    during_var = tk.StringVar()
    during_label = tk.Label(window, textvariable=during_var)
    during_label.pack()

    # Run the main event loop
    window.mainloop()


# Initialize translator
translator = Translator("4ec2251b-bd81-4a7a-bcd4-cb9366d4e0bb:fx")

after_var, during_var, input_var = tk.StringVar()


def logger():
    basicConfig()
    getLogger("DeepL").setLevel(DEBUG)


def translate():
    global after_var, during_var, input_var

    try:
        logger()
        translator.translate_document_from_filepath(input_path=search(input_var), output_path="Done\\",
                                                    target_lang="HU", formality="more")

    except DocumentTranslationException as error:
        doc_id = error.document_handle.document_id
        doc_key = error.document_handle.document_key
        after_var.set(f"Hiba történt feltöltés UTÁN: {error}, id: {doc_id}, key: {doc_key}")

        print(after_var.get())
        logs = open("error_logs.txt", "a")
        print(f"{after_var}\t{datetime}", file=logs)
        logs.close()

    except DeepLException as error:
        during_var.set(f"Hiba történt feltöltés KÖZBEN: {error}")
        print(during_var.get())

        logs = open("error_logs.txt", "a")

        print(f"{during_var}\t{datetime}", file=logs)
        logs.close()

tkinter()
