import customtkinter as ctk # Import customtkinter module using a shortened version 'ctk'
from tkinter import messagebox
import json, os, time
from PIL import Image # Import python image library for the button images

root = ctk.CTk() # Create the app's customtkinter window
response = 'This is the test for a message to print word by word. This will prove to Braden that it can work in the GUI.'

title = ('AI Tutor') 

class UI:
    def __init__(self, window):
        super().__init__()
        # set grid layout 1x2
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)
        self.currentTab = 'Student'
        self.quizChatWindows = []
        self.chatWindows = []
        self.msg = ''
        self.name = ''

        #####################################################################################################
        "<><><><><><><><><><><><><><><><><><><><>  Load Images   <><><><><><><><><><><><><><><><><><><><><>"
        #####################################################################################################

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.app_icon = ctk.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        
        #####################################################################################################
        "<><><><><><><><><><><><><><><>  Create Sidebar Frame with Tabs   <><><><><><><><><><><><><><><><><>"
        ##################################################################################################### 

        self.navbarFrame = ctk.CTkFrame(window, corner_radius=0,)
        self.navbarFrame.grid(row=0, column=0, sticky="nsew")
        self.navbarFrame.grid_rowconfigure(9, weight=1)

        self.navbarFrame_lbl = ctk.CTkLabel(self.navbarFrame, text="AI Tutor", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navbarFrame_lbl.grid(row=0, column=0, padx=40, pady=20)

        #####################################################################################################
        "<><><><><><><><><><><><><><>   Create Navbar Buttons in Sidebar Frame   <><><><><><><><><><><>><>"
        #####################################################################################################

        self.studentBtn_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        
        self.studentBtn = ctk.CTkButton(self.navbarFrame, corner_radius=0, height=40, border_spacing=10, text="Student",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.studentBtn_image, anchor="w", command=lambda: self.navbarEvent('Student', self.studentFrame))
        self.studentBtn.grid(row=1, column=0, sticky="ew")

        self.chatBtn_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        
        self.chatBtn = ctk.CTkButton(self.navbarFrame, corner_radius=0, height=40, border_spacing=10, text="Chat",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.chatBtn_image, anchor="w", command=lambda: self.navbarEvent('Chat', self.ChatFrame))
        self.chatBtn.grid(row=2, column=0, sticky="ew")

        self.quizBtn_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "quiz_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "quiz_light.png")), size=(20, 20))

        self.quizBtn = ctk.CTkButton(self.navbarFrame, corner_radius=0, height=40, border_spacing=10, text="Quiz",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.quizBtn_image, anchor="w", command=lambda: self.navbarEvent('Quiz', self.quizFrame))
        self.quizBtn.grid(row=3, column=0, sticky="ew")

        self.modeDropdown_lbl = ctk.CTkLabel(self.navbarFrame, text="Select a study \n mode below:")
        self.modeDropdown_lbl.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        self.modeDropdown = ctk.CTkOptionMenu(self.navbarFrame, values=["Learn", "Expand", "Quiz"])
        self.modeDropdown.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.dropdown_heading_lbl = ctk.CTkLabel(self.navbarFrame, text="Choose your subject \n and study level below:")
        self.dropdown_heading_lbl.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

        self.subjectDropdown = ctk.CTkOptionMenu(self.navbarFrame, values=["Math", "History", "Geography", "Health", "Science"])
        self.subjectDropdown.grid(row=7, column=0, padx=20, pady=10)

        self.lvlDropdown = ctk.CTkOptionMenu(self.navbarFrame, values=["Elementary", "Middle", "High", "College"])
        self.lvlDropdown.grid(row=8, column=0, padx=20, pady=10)

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navbarFrame, values=["Light", "Dark", "System"],)
        self.appearance_mode_menu.grid(row=9, column=0, padx=20, pady=15, sticky="s")

        #####################################################################################################
        "<><><><><><><><><><><><><><><><><><>   Create Student Frame   <><><><><><><><><><><><><><><><><><>"
        #####################################################################################################
        
        self.studentFrame = ctk.CTkFrame(window, corner_radius=0, fg_color="transparent")
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

        #####################################################################################################
        "<><><><><><><><><><><><><><><><><><>   Create Quiz Frame   <><><><><><><><><><><><><><><><><><><><>"
        #####################################################################################################
        
        self.quizFrame = ctk.CTkFrame(window, corner_radius=0, fg_color="transparent")
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
 
        # Create heading for dropdowns

        # Create dropdowns for subjects and levels

        #Create 'start learning' button
        self.start_button = ctk.CTkButton(self.studentFrame_widgets, text="Start Learning", command=lambda: self.start_app(), width=200)
        self.start_button.grid(row=6, column=1, padx=10, pady=20)

    def checkFields(self):
        if self.currentTab == 'Chat':
            while self.current_InputField.get() != '':
                self.askAI_btn.configure(state='normal')
            self.askAI_btn.configure(state='disabled')
        elif self.currentTab == 'Quiz':
            while self.chat_InputField.get() != '':
                self.createQuiz_btn.configure(state='normal')
            self.createQuiz_btn.configure(state='disabled')

        # select default frame
        self.navbarEvent("Student")

        "---- > Sample input that send's message to AI which then displays the AI's output and the user's input request in the chat history window.----"
        # Sample input = 'Teach me about the sun' 
        # self.mode: 'learn' 

    def setMode(self):
        return
    
    def loadQuiz(self, filename):
        with open(filename, "r") as file:
            self.quizData = json.load(file)
        
    # This function creates a new msgbox and adds the AI's output to the main Chat history screen
    def create_msgbox(self, mode): 
        self.ai_chatOutput = ctk.CTkTextbox(self.chatOutputWindow)
        self.ai_chatOutput.grid(row=len(self.ai_msgbox_list), column=1,)
        self.student_chatInput = ctk.CTkTextbox(self.chatOutputWindow)
        self.student_chatInput.grid(row=len(self.student_msgbox_list), column=3)
        self.ai_msgbox_chatList.append(self.ai_chatOutput)
        self.student_msgbox_list[mode].append(self.student_chatInput)
        # Makes responses read-only
        self.student_chatInput.configure(state='normal')
        self.ai_chatOutput.configure(state='disabled')
        return


    def addChat(self, response):
        # Add each character of the message one-by-one with a delay
        self.create_msgbox()
        for chunk in response:
            if chunk.endswith("."):
                self.ai_chatOutput.insert('end', ".\n")
                self.ai_chatOutput.update()
                time.sleep(0.03)
            else:
                self.ai_chatOutput.insert('end', chunk)
                self.ai_chatOutput.update()
                time.sleep(0.03)
            self.ai_responses.append(chunk)        
     
    def buttonEvent(self, name):
       name = self.name
       self.chatBtn.configure(fg_color=("gray75", "gray75") if name == "Home" else "transparent")
       self.quizBtn.configure(fg_color=("gray75", "gray75") if name == "Chat" else "transparent")
       self.studentBtn.configure(fg_color=("gray75", "gray75") if name == "Student" else "transparent")
       return
    
    # Get the response from the OpenAI API and display it in the AI response in the respective window
    def create_request(self, question):
        if self.checkFields():
            self.addChat(question)
        else:
            return

    def send_SR_input():
        print('send_SR_input')

    def get_TTS_output():
        print('get_TTS_output')

    def createQuiz(self):
        self.question_label = ctk.CTkLabel(self.quizContainer, text="Question")
        self.question_label.pack()


    def start_app(self):
        self.studentFrame.grid_forget()  # remove startupScreen frame
        self.chatFrame.grid(row=0, column=2, sticky="nsew")  # show main frame

    def back_event(self):
        self.chatFrame.grid_forget()  # remove main frame
        self.studentFrame.grid(row=0, column=0, sticky="nsew")  # show login frame

    def switchFrame(self, frame):
        if self.currentFrame != frame:
            self.currentFrame.grid_forget()
            self.currentFrame = frame
            frame.grid(row=0, column=1, sticky="nsew")
        else:
            pass

    def setCurrentScreen(self, name):
        self.currentTab = name
        root.title(f'{title} - {self.currentTab} screen') 

    def navbarEvent(self, name, frame):
        self.buttonEvent(name)
        # show selected frame
        self.switchFrame(frame)
        self.setCurrentScreen(name)

    def newChat(self):
        if self.chatWindows != []:
            self.currentChatWindow.grid_forget()
        else:
            self.chatOutputWindow = ctk.CTkScrollableFrame(self.currentFrame, corner_radius=0, fg_color="gray15")
        self.chatOutputWindow.grid(row=0, column=1, columnspan=4, sticky="nsew", padx=20, pady=10)
        self.switchChatWindow(self.chatOutputWindow)
        self.chatWindows.append(self.chatOutputWindow)

        # Create a scrollable frame to contain each the conversation between the user and the AI
        self.quiz_responseFrame = ctk.CTkScrollableFrame(self.quizCreationScreen, width=200, height=500, corner_radius=0, fg_color="gray15")
        self.quiz_responseFrame.grid(row=0, column=1, columnspan=4, sticky="ns", padx=20, pady=10)

    #####################################################################################################
    "<><><><><><><><><><><><><><>  Handler to creat a new Chat Frame  <><><><><><><><><><><><><><><><><>"
    #####################################################################################################
class scrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, msg):
        super().__init__()
        self.grid_columnconfigure(0, weight=1)
        self.msg = msg
        self.msgboxes = []

    def addMsgBox(self, value):
        for value in enumerate(self.values):
            msgbox = ctk.CTkTextbox(self, text=value)
            msgbox.grid(row=len(self.msgboxes), column=1, padx=20, pady=20, sticky="nsew")
            self.msgboxes.append(msgbox)
    
        self.chatFrame = ctk.CTkFrame(self.window, corner_radius=0, fg_color="transparent")
        self.chatFrame(self.window, width=400, height=500, corner_radius=0, fg_color="grey20")
        self.chatFrame.grid_rowconfigure(0, weight=1)
        self.chatFrame.grid_columnconfigure(1, weight=1)
        self.chatFrame.grid(row=0, column=1, columnspan=4, sticky="nsew", padx=20, pady=10)
        
        self.chatFrame_widgets = ctk.CTkFrame(self.chatFrame, corner_radius=0, fg_color="transparent")
        self.chatFrame_widgets.grid(row=0, column=1, columnspan=4, sticky="nsew", padx=20, pady=10)

        new_chat_btn = ctk.CTkButton(root, text="New Chat", command=self.newChat())
        new_chat_btn.pack()

        # Create a scrollable frame to contain each the conversation between the user and the AI
        self.chatOutputWindow = ctk.CTkScrollableFrame(self.chatFrame, corner_radius=0, fg_color="gray15")
        self.chatOutputWindow.grid(row=0, column=1, columnspan=4, sticky="nsew", padx=20, pady=10)

        # Create headings for UI elements
        self.primerPrompt = ctk.CTkLabel(self.chatFrame, text="Welcome to a revolutionary new learning \n experience powered by Open AI. Customize your results in the settings menu")

        # Create question input field
        self.chat_InputField = ctk.CTkEntry(self.chatFrame, placeholder_text="What can I help you with?", fg_color="transparent")
        self.askAI_btn = ctk.CTkButton(self.chatFrame, text="Ask AI", command=lambda: self.create_request(self.chat_InputField.get()))

        # Create speech recognition button
        self.speak_button = ctk.CTkButton(self.chatFrame, text="Speak", command=self.send_SR_input)

        # Pack all widgets into main window
        self.chat_InputField.grid(row=1, column=1, padx=5, pady=10, sticky='nsew')
        self.askAI_btn.grid(row=1, column=2, padx=5, pady=10, sticky='nsew')

    def switchChatWindow(self, instance):
        self.currentChatWindow = instance

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def newChat(self):
        values = ['Rainbow', 'Unicorn']
        self.scrollable_checkbox_frame = scrollableFrame(self, title="Values", values=values)
        
    
    def addMsg(self):
        self.chatHistoryFrame = self.scrollableFrame.addMsgbox(self.chatFrame, title="Values", )
        self.scrollableFrame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")


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
