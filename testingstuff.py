import customtkinter as ctk
import time
from ai import TutorGPT

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = ctk.CTk()

model = TutorGPT("science", "high school", "quiz")

model.learnMode("how time affects space")

response = model.complete()

# response = 'This is the test for a message to print word by word. This will prove to Braden that it can work in the GUI.'

# def get_generator():
#     for chunk in response:
#          yield chunk

class UI:
    def __init__(self, window):

        window.grid_rowconfigure(0, weight=1)  # configure grid systemp
        window.grid_columnconfigure(0, weight=1)
        self.req_height = 10
        self.msg = ''
        self.chat_history = []
        ####################################### Create Chat Frame #####################################
        self.chat_frame = ctk.CTkFrame(window, corner_radius=0)
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(1, weight=1)
        self.chat_frame.grid(row=0, column=0, sticky="nsew")

        # Create a scrollable frame to contain each the conversation between the user and the AI
        self.chatHistory_frame = ctk.CTkScrollableFrame(self.chat_frame, corner_radius=0)
        self.chatHistory_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

        self.textBox = ctk.CTkTextbox(self.chatHistory_frame, height=20, width=100, corner_radius=0, wrap='word', activate_scrollbars=False)
        self.textBox.grid(row=0, column=0, sticky="nsew")
        
        # Create question input field
        self.chat_InputField = ctk.CTkEntry(self.chat_frame, placeholder_text="What can I help you with?", fg_color="transparent")
        self.askAI_btn = ctk.CTkButton(self.chat_frame, text="Ask AI", command=lambda: self.create_request(self.chat_InputField.get())) 
        
        self.chat_InputField.grid(row=1, column=1, padx=5, pady=10, sticky='nsew')
        self.askAI_btn.grid(row=1, column=2, padx=5, pady=10, sticky='nsew')

        self.startBtn = ctk.CTkButton(self.chat_frame, text='Start', command=lambda: self.type_msg())
        self.startBtn.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

    # def create_request(self):
        
    
    def type_msg(self):
        # Add each character of the message one-by-one with a delay
        # chunks = get_generator()
        chunks = response
        for chunk in chunks:
            if chunk.endswith("."):
                self.textBox.insert('end', ".\n") 
                self.update_textbox_height()
                time.sleep(0.01)
            else:
                self.textBox.insert('end', chunk, "\n")
            self.textBox.update()
            time.sleep(0.01)
    
    def update_textbox_height(self):
        # get the required height of the textbox
        self.req_height +=10
        # set the height of the textbox
        self.textBox.configure(height=self.req_height)
        #model.chat_history.append(self.response) # Add each new chat to the aray of this request[i++]

# configure the textbox to update its height when the text changes

#################################################################################
'------------------'"Tkinter window configuration"'------------------------'
#################################################################################

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

if __name__ == '__main__':
    app = UI(root)
    root.mainloop()