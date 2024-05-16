import tkinter as tk
window = tk.Tk()
check_box_status = tk.IntVar(value=1)
# cb = ""
flag = 1


def status():
    global check_box_status, flag  # Make sure the flag variable is also global

    check_box_status = tk.IntVar()
    check_box_status.set(1)
    # Create a checkbox widget and link it to the check_box_status variable
    checkbox = tk.Checkbutton(window, text="Check me", variable=check_box_status)
    checkbox.pack()

    # Bind a function to the checkbox "command" to update the flag
    def update_flag():
        global flag  # Access the global flag variable
        flag = check_box_status.get()  # Get the current checkbox state (0 or 1)

    checkbox.config(command=update_flag)


window.mainloop()
