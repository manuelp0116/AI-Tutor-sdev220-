import customtkinter as ctk # Import customtkinter module using a shortened version 'ctk'
from tkinter import messagebox # This is used to show a messagebox
import json, os, time
from PIL import Image # Import python image library for the button images
from ai import TutorGPT # The AI class

model = TutorGPT('history', 'college', 'learn')

root = ctk.CTk() # Create the app's customtkinter w\indow

title = ('AI Tutor') 

# This class is used to create a new scrollable frame. Once instantiated, the program can add mesages from both
# User and Assistant.
class scrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, senders):
        super().__init__()
        self.grid_columnconfigure(0, weight=1)
        self.senders = senders
        self.msgboxes = []
        self.row = 0

    def addChat(self, message, senders):
        for sender in senders:
            msgbox = ctk.CTkTextbox(self, text='')
            msgbox.grid(row=len(self.msgboxes), column=1, padx=20, pady=20, sticky="nsew")
            msgbox.config(state='disabled')
            self.msgboxes.append(msgbox)
            if sender == 'User':
                msgbox.insert("end", f"{Student.name}:{message}")
            elif sender == 'Assistant':
                response = model.complete()
                for chunk in response():
                    if chunk.endswith("."):
                        msgbox.insert('end', ".\n")
                        UI.update_textbox_height(20)
                        msgbox.update()
                        time.sleep(0.03)
                    else:
                        msgbox.configure(chunk)
                        msgbox.update()
                        time.sleep(0.03)
    
class controlPanel(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.checkboxes, self.radiobuttons, self.switches = [], [], []
        self.variable = ctk.StringVar(value="")
        self.switch_var = ctk.StringVar(value="")

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, pady=(10, 0), sticky="ew")

    def createCheckboxes(self):
        for i, value in enumerate(self.values):
            checkbox = ctk.CTkCheckBox(self, text=value)
            checkbox.grid(row=i+1, column=0, padx=10, pady=10, sticky="w")
            self.checkboxes.append(checkbox)
    
    def createRadioButtons(self):
        for i, value in enumerate(self.values):
            radiobutton = ctk.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i+1, column=0, padx=10, pady=10, sticky="w")
            self.radiobuttons.append(radiobutton)

    def createNewSwitches(self):
        for i, value in enumerate (self.values):
            switch_var = ctk.StringVar(value="on")
            switch = ctk.CTkSwitch(self, label=value, variable=switch_var, onvalue="on", offvalue="off")
            switch.grid(row=i+1, column=0, padx=10, pady=(0, 20))
            self.switches.append(switch)

    def getCheckboxes(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes
    
    def getSwitches(self):
        toggled_switches = []
        for switch in self.switches:
            if self.switch_var.get() == 'on':
                toggled_switches.append(switch.cget("text"))
        return toggled_switches

    def getRadioButtons(self):
        return self.variable.get()
    
class Student:
    def __init__(self):
        super().__init__()
        self.answer = ''
        self.chatInput = ''
        self.answers_correct = 0
        self.name = ''
        self.score = 0

# Quiz class. This class handles the quiz related variables.
    
class Quiz:
    def __init__(self, quiz_data):
        super().__init__()
        self.quiz_data = quiz_data
        self.quiz_length = len(self.quiz_data)
        self.quiz_type = ''
        self.current_question = ''
        self.correct_answer = ''
        self.options = ''
        self.question_index = 0
        Student.answers_correct = 0
        self.progress = 0
        self.max_score = 100
        self.display_question()

    def mapQuizData(self):
        self.current_question_data = self.quiz_data[self.question_index]
        vars = ['quiz_type', 'current_question', 'correct_answer']
        params = ['type', 'question', 'answer']
        for var, param in zip(vars, params):
            value = self.current_question_data[param]
            setattr(self, var, value)

    def create_widgets(self):
        self.mapQuizData()
        if self.quiz_type == 'Fill in the Blank':
            UI.question_label.configure(UI.quizContainer, text=Quiz.current_question, fg_color="gray30", corner_radius=6)
            UI.question_label.grid(row=1, column=0, sticky="ew")
            self.answer_entry = ctk.CTkEntry(self)
            self.answer_entry.grid(row=4, column=0, sticky="ew", padx=30)
        elif self.quiz_type == 'Multiple Choice':
            self.quiz_options = self.quiz_data[self.question_index]['options']
            self.multipleChoiceFrame = controlPanel(UI.quizContainer)
            self.multipleChoiceFrame.createRadioButtons(self.current_question, values=self.quiz_options)
            self.multipleChoiceFrame.grid(row=0, column=3, padx=40, pady=10, sticky="nsew")
        elif self.quiz_type == 'Multiple Answer':
            self.quiz_options = self.quiz_data[self.question_index]['options']
            self.multipleAnswerFrame = controlPanel(UI.quizContainer)
            self.multipleAnswerFrame.createCheckboxes(self.current_question, values=self.quiz_options)
            self.multipleAnswerFrame.grid(row=0, column=3, padx=40, pady=40, sticky="nsew")

    def display_question(self):
        self.create_widgets()

    def ignoreCaseSensitive(self, state):
        if state is True:
            Student.answer = Student.answer.lower()
            self.correct_answer = self.correct_answer.lower()
        else:
            return False

    def getStudentAnswers(self):
        # Get current question data
        if self.quiz_type == 'Fill in the Blank':
            # Get selected answers
            Student.answer = self.answer_entry.get()
            self.ignoreCaseSensitive(True)
            print(Student.answer, self.correct_answer)
        if self.quiz_type == 'Multiple Answer':
        # Get a set of selected answers
            Student.answer = self.multipleAnswerFrame.getCheckboxes()
        if self.quiz_type == 'Multiple Choice':
            # Get multiple choice answer as a set of selected answers
            Student.answer = self.multipleChoiceFrame.getRadioButtons()

    def submitAnswer(self):
        print('AI Response Here')
        # Send student response to AI
        model.complete()
        self.checkAnswer()

    def checkAnswer(self):
        self.getStudentAnswers()
            # Check if selected answers match correct answers
        if set(Student.answer) == set(self.correct_answer):
            Student.answers_correct += 1
            messagebox.showinfo("Result", "Correct!")
        else:
            messagebox.showinfo("Result", "Incorrect!")
        self.update_score()

    def nextQuestion(self):
        print('Go here?')
        self.question_index += 1
        if self.question_index == self.quiz_length:
            messagebox.showinfo("Score", f"You scored {Student.score}% out of {self.max_score}%")
            UI.switchFrame('quizResultsFrame')
            return
        self.display_question()

    def update_score(self):
        Student.score = ((Student.answers_correct / self.quiz_length) * 100)
        UI.score_lbl.configure(text=f'Score: {Student.score}')
        self.progress += (1 / self.quiz_length)
        UI.progress_bar.set(self.progress)
        self.nextQuestion()

# Create and run the quiz GUI
quiz_data = [
  {
    "type": "Multiple Answer",
    "question": "Which of the following are types of coral reefs? (Select all that apply)",
    "answer": ["Fringing", "Barrier", "Atoll"],
    "options": [
      "Fringing",
      "Barrier",
      "Atoll",
      "Patch"
    ]
  },
  {
    "type": "Multiple Choice",
    "question": "What is the most common type of shark?",
    "answer": "Blue shark",
    "options": [
      "Great white shark",
      "Tiger shark",
      "Hammerhead shark",
      "Blue shark"
    ]
  },
  {
    "type": "Multiple Choice",
    "question": "What percentage of the Earth's surface is covered by oceans?",
    "answer": "71%",
    "options": [
      "45%",
      "60%",
      "71%",
      "85%"
    ]
  },
  {
    "type": "Fill in the Blank",
    "question": "The deepest part of the ocean is called the _________.",
    "answer": "Challenger Deep"
  }
]

class UI:
    def __init__(self, window):
        super().__init__()
        # set grid layout 1x2
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)
        self.currentTab = 'Student'
        self.connectionStatus = ''
        self.chatWindows = []
        self.msg = ''
        # Quiz variable initialization:

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
                                                   image=self.chatBtn_image, anchor="w", command=lambda: self.navbarEvent('Chat', self.chatFrame))
        self.chatBtn.grid(row=2, column=0, sticky="ew")

        self.quizBtn_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "quiz_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "quiz_light.png")), size=(20, 20))

        self.quizBtn = ctk.CTkButton(self.navbarFrame, corner_radius=0, height=40, border_spacing=10, text="Quiz",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.quizBtn_image, anchor="w", command=lambda: self.navbarEvent('Quiz', self.quizFrame))
        self.quizBtn.grid(row=3, column=0, sticky="ew")

        self.modeDropdown_lbl = ctk.CTkLabel(self.navbarFrame, text="Select a study \n mode below:")
        self.modeDropdown_lbl.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        self.modeDropdown = ctk.CTkOptionMenu(self.navbarFrame, values=["Learn", "Expand"])
        self.modeDropdown.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.connectionStatus_lbl = ctk.CTkLabel(self.navbarFrame, textvariable=self.connectionStatus)
        self.connectionStatus_lbl.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navbarFrame, values=["Light", "Dark", "System"],)
        self.appearance_mode_menu.grid(row=9, column=0, padx=20, pady=15, sticky="s")

        #####################################################################################################
        "<><><><><><><><><><><><><><>  Handler to creat a new Chat Frame  <><><><><><><><><><><><><><><><><>"
        #####################################################################################################
        self.chatFrame = ctk.CTkFrame(window, corner_radius=0, fg_color="transparent")
        self.chatFrame.grid_rowconfigure(0, weight=1)
        self.chatFrame.grid_columnconfigure(1, weight=1)
        self.chatFrame.grid(row=0, column=1, columnspan=4, sticky="nsew", padx=20, pady=10)
        
        self.chatFrame_widgets = ctk.CTkFrame(self.chatFrame, corner_radius=0, fg_color="transparent")
        self.chatFrame_widgets.grid(row=0, column=1, columnspan=4, sticky="nsew", padx=20, pady=10)

        # Create question input field and add widgets into the chatFrame
        self.chat_input = ctk.CTkEntry(self.chatFrame, placeholder_text=f"{self.placeholder}", fg_color="transparent")
        self.chat_input.grid(row=1, column=1, padx=5, pady=10, sticky='nsew')
        self.askAI_btn = ctk.CTkButton(self.chatFrame, text="Ask AI", command=lambda: self.create_request(self.chat_input.get()))
        self.askAI_btn.grid(row=1, column=2, padx=5, pady=10, sticky='nsew')
        
        while model.connectionError == True:      
            self.connectionStatus=('Status: Connection error!, Retrying...')
            self.askAI_btn.configure(state='disabled')
            self.createQuiz_btn.configure(state='disabled')
        self.connectionStatus=('Status: Connected')
        self.askAI_btn.configure(state='normal')
        self.createQuiz_btn.configure(state='disabled')

        #####################################################################################################
        "<><><><><><><><><><><><><><><><><><>   Create Student Frame   <><><><><><><><><><><><><><><><><><>"
        #####################################################################################################
        self.studentFrame = ctk.CTkFrame(window, corner_radius=0, fg_color="transparent")
        self.studentFrame.grid(row=0, column=1, columnspan=4, sticky="nsew", padx=20, pady=10)
        self.studentFrame.grid_rowconfigure(3, weight=1)
        self.studentFrame.grid_columnconfigure(1, weight=1)

        self.studentFrame_widgets = ctk.CTkFrame(self.studentFrame, corner_radius=0, fg_color="transparent")
        self.studentFrame_widgets.grid(row=0, column=1, columnspan=4, sticky="nsew", padx=20, pady=10)

        self.appInfo_lbl = ctk.CTkLabel(self.studentFrame_widgets, text="Welcome to a revolutionary new learning \n experience powered by Open AI.",
                                                  font=ctk.CTkFont(size=20, weight="bold"))
        self.appInfo_lbl.grid(row=1, column=1, columnspan=4, padx=10, pady=10)

        self.userNameEntry_lbl = ctk.CTkLabel(self.studentFrame_widgets, text="Who am I tutoring today?",
                                                  font=ctk.CTkFont(size=20, weight="bold"))
        self.userNameEntry_lbl.grid(row=2, column=1, padx=10, pady=15)

        self.userNameEntry = ctk.CTkEntry(self.studentFrame_widgets, width=200, placeholder_text="Enter your first name:")
        self.userNameEntry.grid(row=3, column=1, padx=10, pady=(15))

        self.start_button = ctk.CTkButton(self.studentFrame_widgets, text="Start Learning", command=lambda: self.start_app(), width=200)
        self.start_button.grid(row=4, column=1, padx=10, pady=20)

        #####################################################################################################
        "<><><><><><><><><><><><><><><><><><>   Create Quiz Frame   <><><><><><><><><><><><><><><><><><><><>"
        #####################################################################################################
        self.quizFrame = ctk.CTkFrame(window, corner_radius=0, fg_color="transparent")
        self.quizFrame.grid_rowconfigure(4, weight=1)
        self.quizFrame.grid_columnconfigure(1, weight=1)
        self.quizFrame.grid(row=0, column=1, columnspan=4, sticky="nsew", padx=20, pady=10)
        self.quizCreationFrame = ctk.CTkFrame(self.quizFrame, corner_radius=0, fg_color="transparent")
        self.quizCreationFrame.grid(row=0, column=1, columnspan=4, sticky="nsew", padx=20, pady=10)
        self.quiz_subjectDropdown = ctk.CTkOptionMenu(self.quizCreationFrame, values=["Math", "History", "Geography", "Health", "Science"])
        self.quiz_subjectDropdown.grid(row=7, column=1, padx=20, pady=10)
        self.quiz_lvlDropdown = ctk.CTkOptionMenu(self.navbarFrame, values=["Elementary", "Middle", "High", "College"])
        self.quiz_lvlDropdown.grid(row=4, column=2, padx=20, pady=10)
        
        self.quiz_input = ctk.CTkEntry(self.quizFrame, placeholder_text=f"{self.placeholder}", fg_color="transparent")
        self.quiz_input.grid(row=1, column=1, padx=5, pady=10, sticky='nsew')
        self.createQuiz_btn = ctk.CTkButton(self.quizCreationFrame, text="Create a Quiz", command=lambda: self.createQuiz())
        self.createQuiz_btn.grid(row=1, column=2, padx=5, pady=10, sticky='nsew')
        self.quizContainerFrame = ctk.CTkFrame(self.quizFrame, corner_radius=0, fg_color="transparent")
        self.quizContainer.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)
        self.quizContainer = ctk.CTkFrame(self.quizContainerFrame, corner_radius=0, fg_color="transparent")
        self.quizContainer.grid(row=0, column=2, sticky="nsew", padx=20, pady=10)
        self.question_label = ctk.CTkLabel(self.quizContainer, text='')
        self.question_label.grid(row=0, column=0)
        self.score_lbl = ctk.CTkLabel(self.quizContainer, text='')
        self.score_lbl.grid(row=8, column=0,)
        self.submit_button = ctk.CTkButton(self.quizContainer, text='Submit', command=self.submitAnswer)
        self.submit_button.grid(row=5, column=0, sticky="nsew", pady=10, padx=40)
        self.progress_bar = ctk.CTkProgressBar(self.quizContainer)
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.grid(row=7, column=0, sticky="nsew", pady=10, padx=40)
        self.progress_bar.set(0)

    def createQuiz(self):
        self.switchFrame(frame=self.quizContainerFrame)

    def checkFields(self):
        if self.currentTab == 'Chat':
            while self.current_InputField.get() != '':
                self.askAI_btn.configure(state='normal')
            self.askAI_btn.configure(state='disabled')
        elif self.currentTab == 'Quiz':
            while self.quiz_input.get() != '':
                self.createQuiz_btn.configure(state='normal')
            self.createQuiz_btn.configure(state='disabled')

        # select default frame
        self.navbarEvent("Student")
     
    def tabEvent(self, name):
       name = self.name
       self.chatBtn.configure(fg_color=("gray75", "gray75") if name == "Home" else "transparent")
       self.quizBtn.configure(fg_color=("gray75", "gray75") if name == "Chat" else "transparent")
       self.studentBtn.configure(fg_color=("gray75", "gray75") if name == "Student" else "transparent")
       return
    
    # Get the response from the OpenAI API and display it in the AI response in the respective window
    def create_request(self):
        if self.checkFields():
            if self.chatWindows != []:
                self.currentChatWindow.grid_forget()
            else:
            # Create a scrollable frame to contain each the conversation between the user and the AI
                self.chatHistoryFrame = scrollableFrame(self.chatFrame)
                # Display the student's message and the AI's in the conversation
                self.chatHistoryFrame.addChat(message=Student.chatInput, senders=['User', 'Assistant'])
                self.chatWindows.append(self.chatHistoryFrame)
        else:
            return

    def start_app(self):
        self.studentFrame.grid_forget()  # remove startupScreen frame
        self.chatFrame.grid(row=0, column=1, sticky="nsew")  # show main frame

    def back_event(self):
        self.chatFrame.grid_forget()  # remove main frame
        self.studentFrame.grid(row=0, column=1, sticky="nsew")  # show login frame

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
        self.tabEvent(name)
        # show selected frame
        self.switchFrame(frame)
        self.setCurrentScreen(name)

    def newQuiz(self):
        response = model.complete()
        Quiz(response)

    '<><><><><><><><><><><> These functions set variables <><><><><><><><><><><> '
    def getCurrentDropdowns(self, dropdown):
        currentSubjectDropdown = dropdown
        currentGradeLevelDropdown = dropdown

    def setMode(self, mode):
        model.setMode(mode)

    def setMode(self, mode):
        model.setMode(mode)

    def setExcerpt(self, excerpt):
        model.addExcerpt(excerpt)

    def setSubjectLvl(self):
        subjectLvl = self.subjectLvlDropdown.get()

    def setGradeLvl(self):
        gradeLevel = self.gradeLevelDropdown.get()

    def getMode(self):
        mode = self.modeDropdown.get()

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

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
