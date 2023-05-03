import customtkinter as ctk # Import customtkinter module using a shortened version 'ctk'
from tkinter import messagebox
import json, os, time
from PIL import Image # Import python image library for the button images


root = ctk.CTk() # Create the app's customtkinter window

title = ('AI Tutor') 

class UI(Quiz):
    def __init__(self, window):
        super().__init__()
        # set grid layout 1x2
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)
        self.currentTab = 'Home'

        #Load images
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.app_icon = ctk.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))

        ############################################ Create Sidebar widgets #########################################
        self.navbarFrame = ctk.CTkFrame(window, corner_radius=0,)
        self.navbarFrame.grid(row=0, column=0, sticky="nsew")
        self.navbarFrame.grid_rowconfigure(9, weight=1)

        self.navbarFrame_lbl = ctk.CTkLabel(self.navbarFrame, text="AI Tutor", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navbarFrame_lbl.grid(row=0, column=0, padx=40, pady=20)

        ############################################ Create Sidebar with tabs #######################################
        self.studentBtn_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        
        self.studentBtn = ctk.CTkButton(self.navbarFrame, corner_radius=0, height=40, border_spacing=10, text="Student",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.studentBtn_image, anchor="w", command=lambda: self.navbarEvent('Student'))
        self.studentBtn.grid(row=1, column=0, sticky="ew")

        self.chatBtn_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        
        self.chatBtn = ctk.CTkButton(self.navbarFrame, corner_radius=0, height=40, border_spacing=10, text="Chat",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.chatBtn_image, anchor="w", command=lambda: self.navbarEvent('Chat'))
        self.chatBtn.grid(row=2, column=0, sticky="ew")

        self.quizBtn_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "quiz_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "quiz_light.png")), size=(20, 20))

        self.quizBtn = ctk.CTkButton(self.navbarFrame, corner_radius=0, height=40, border_spacing=10, text="Quiz",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.quizBtn_image, anchor="w", command=lambda: self.navbarEvent('Quiz'))
        self.quizBtn.grid(row=3, column=0, sticky="ew")

        self.modeDropdown_lbl = ctk.CTkLabel(self.navbarFrame, text="Select a study \n mode below:")
        self.modeDropdown_lbl.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        self.modeDropdown = ctk.CTkOptionMenu(self.navbarFrame, values=["Learn", "Expand", "Quiz"], command=self.setMode())
        self.modeDropdown.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.dropdown_heading_lbl = ctk.CTkLabel(self.navbarFrame, text="Choose your subject \n and study level below:")
        self.dropdown_heading_lbl.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

        self.subjectDropdown = ctk.CTkOptionMenu(self.navbarFrame, values=["Math", "History", "Geography", "Health", "Science"])
        self.subjectDropdown.grid(row=7, column=0, padx=20, pady=10)

        self.lvlDropdown = ctk.CTkOptionMenu(self.navbarFrame, values=["Elementary", "Middle", "High", "College"])
        self.lvlDropdown.grid(row=8, column=0, padx=20, pady=10)

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navbarFrame, values=["Light", "Dark", "System"],)
        self.appearance_mode_menu.grid(row=9, column=0, padx=20, pady=15, sticky="s")
        
        ############################################ Create Student Frame #########################################
        self.studentFrame = ctk.CTkFrame(window, width=500, height=620, corner_radius=0, fg_color="transparent")
        self.studentFrame.grid(row=0, column=1, columnspan=4, sticky="nsew", padx=20, pady=10)
        self.studentFrame.grid_rowconfigure(0, weight=1)
        self.studentFrame.grid_columnconfigure(1, weight=1)

        self.studentFrame_widgets = ctk.CTkFrame(self.studentFrame, corner_radius=0, fg_color="transparent")
        self.studentFrame_widgets.grid(row=0, column=1, columnspan=4, sticky="nsew", padx=20, pady=10)

        self.appInfo_lbl = ctk.CTkLabel(self.studentFrame_widgets, text="Welcome to a revolutionary new learning \n experience powered by Open AI.",
                                                  font=ctk.CTkFont(size=20, weight="bold"))
        self.appInfo_lbl.grid(row=0, column=1, columnspan=4, padx=10, pady=10)

        self.userNameEntry_lbl = ctk.CTkLabel(self.studentFrame_widgets, text="Who am I tutoring today?",
                                                  font=ctk.CTkFont(size=20, weight="bold"))
        self.userNameEntry_lbl.grid(row=1, column=1, padx=10, pady=15)

        self.userNameEntry = ctk.CTkEntry(self.studentFrame_widgets, width=200, placeholder_text="Enter your first name:")
        self.userNameEntry.grid(row=2, column=1, padx=10, pady=(15))
        ############################################ Create Sidebar widgets #########################################

class QuizFrame(ctk.CTkFrame):
    def __init__(self, window):
        super().__init__(window)
        self.quizFrame = ctk.CTkFrame(UI.window, corner_radius=0, fg_color="transparent")
        self.quizFrame.grid_columnconfigure(0, weight=1)
        self.quizFrame.grid_columnconfigure(1, weight=1)
        self.quizFrame.grid(row=0, column=1, columnspan=4, sticky="nsew", padx=20, pady=10)
        
        self.quizWindowContainer = ctk.CTkFrame(self.quizFrame, corner_radius=0, fg_color="transparent")
        self.quizWindowContainer.grid(row=0, column=1, columnspan=4, sticky="nsew", padx=20, pady=10)

        self.quizCreationScreen = ctk.CTkFrame(self.quizWindowContainer, corner_radius=0, fg_color="transparent")
        self.quizCreationScreen.grid(row=0, column=1, columnspan=4, sticky="nsew", padx=20, pady=10)

        self.createQuizBtn = ctk.CTkButton(self.quizCreationScreen, text="Create a Quiz", command=self.buttonEvent('Create Quiz'))

        self.quizContainer = ctk.CTkFrame(self.quizFrame, corner_radius=0, fg_color="transparent")
        self.quizContainer.grid(row=0, column=2, sticky="nsew", padx=20, pady=10)

        self.quizResultsContainer = ctk.CTkFrame(self.quizFrame, corner_radius=0, fg_color="transparent")
        self.quizResultsContainer.grid(row=0, column=1, columnspan=4, sticky="nsew", padx=20, pady=10)

        self.retryQuizBtn = self.createQuizBtn = ctk.CTkButton(self.quizCreationScreen, text="Create a Quiz", command=self.buttonEvent('Create Quiz'))


        # Create a scrollable frame to contain each the conversation between the user and the AI
        self.quiz_responseFrame = ctk.CTkScrollableFrame(self.quizCreationScreen, width=200, height=500, corner_radius=0, fg_color="gray15")
        self.quiz_responseFrame.grid(row=0, column=1, columnspan=4, sticky="ns", padx=20, pady=10)

class scrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, messages):
        super().__init__()
        self.grid_columnconfigure(0, weight=1)
        self.messages = messages
        self.msgboxes = []

    def createMsgBox(self, messages):
        for value in enumerate(self.messages):
            msgbox = ctk.CTkTextbox(self, text=value)
            msgbox.grid(row=len(self.msgboxes), column=1, padx=20, pady=20, sticky="nsew")
            self.msgboxes.append(msgbox)
            scrollableFrame()

    def submitQuiz(self, selectedChoice):


    def storeHistory(self, chat):
        for i in len(self.chatHistory):
            chat[i] = ctk.CTkButton(UI.chatHistoryWindow, command=lambda: self.switchFrame(chat[len(self.chatHistory)]))

    def display_Typing(self, response):
        self.createMsgbox()
        # Add each character of the message one-by-one with a delay
        subject = subjectDropdown.get()
        studyLvl = studyLvlDropdown.get()
        request = self.chat_input.get()
        self.chat_input.delete(0, "end")
        self.chat_box.insert("end", f"You: {request}")

    def processRequest(self):
        response = model.complete(subject, studyLvl, request)
            if chunk.endswith("."):
                self.ai_chatOutput.insert('end', ".\n")
                self.ai_chatOutput.update()
                time.sleep(0.03)
            else:
                self.ai_chatOutput.insert('end', chunk)
                self.ai_chatOutput.update()
                time.sleep(0.03)
            self.ai_responses.append(chunk)   

    def getGenerator(self, response):
        for chunk in response:
            yield chunk     

    def handle_modes(mode_list):
    }

    for mode in mode_list:
        function = modes.get(mode)
        if function is not None:
            function()
        else:
            print(f"Invalid mode: {mode}")

    #This function is designed to gather the tutor mode eg. 'Learn', 'Expand' 'Quiz'
    def houseKeeping (self, mode, subject, gradeLevel, config):
        model.setMode(mode)
        model.setSubject(subject)
        model.setGradeLevel(gradeLevel)
        model.setQuizConfiguration(config)

    getMode(self, mode)
        

    def getOpenFrame(self, frame):

        if self.currentFrame == self.quizCreationScreen:


class chatHistoryFrame:
    def __init__(self, chat):
        super().__init__()


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

# Sets the max and min size for each of the windows
if __name__ == "__main__":
    app = UI(root) # Creates an instance for the customtkinter window
    root.mainloop()
    
        


