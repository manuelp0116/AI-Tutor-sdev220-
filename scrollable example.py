import customtkinter as ctk

root = ctk.CTk

class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.msgboxes = []

        for value in self.values:
            msgbox = ctk.CTkTextbox(self, text=value, width=0, height=0)
            msgbox.grid(row=len(self.msgboxes), column=1, padx=20, pady=20, sticky="nsew")
            self.msgboxes.append(msgbox)

    def add_message(self, message):
        msgbox = ctk.CTkTextbox(self, text=message, width=0, height=0)
        msgbox.grid(row=len(self.msgboxes), column=1, padx=20, pady=20, sticky="nsew")
        self.msgboxes.append(msgbox)

class App:
    def __init__(self, window):
        super().__init__()
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)

        self.values = ["value 1", "value 2", "value 3", "value 4", "value 5", "value 6"]
        self.chatHistoryFrame = ScrollableFrame(window, values=self.values)
        self.chatHistoryFrame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.button = ctk.CTkButton(window, text="my button", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def button_callback(self):
        self.chatHistoryFrame.add_message("New message")

"<><><><><><><><><><><><><><><>  Custom Tkinter Window Settings <><><><><><><><><><><><><><><><><><>"

# Makes tkinter Dynamically Resizable
MIN_WIN_SIZE = (600, 480)  # Min window resolution (width/height)
MAX_WIN_SIZE = (1440, 1280)  # Max window resolution (width/height)

# I used the '*' character below to unpack the dimensions from the tuples 
# when passing them to the minsize and maxsize methods.

root.minsize(*MIN_WIN_SIZE) 
root.maxsize(*MAX_WIN_SIZE)

def_window_width = 800  # Default app width on app launch (width/height)
def_window_height = 600 # Default app height on app launch (width/height)

# Grabs the current default screen, height and width for use in centering.
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Sets the position of the window to the center of the screen upon first app launch
center_x = int(screen_width / 2 - def_window_width / 2)
center_y = int(screen_height / 2 - def_window_height / 2)
root.geometry(f'{def_window_width}x{def_window_height}+{center_x}+{center_y}')

app = App(root)
root.mainloop()
