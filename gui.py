# Program name:       Brain Spark
# Author:             Charles 'Nuke' Phillips, Chloe Moor, Manuel Padres, Braden Shrum 
# Version:            version 1.0
# Last revision date: 5/13/2023
# The objective of this program is to tutor a user through the use of AI
# Each time a user communicates with the AI, they can learn about a certain subject for a particular gradeLevel.
# Additionally, the student can create a interactive quiz with four radio buttons.
# Finally, it saves the Quiz to a JSON file.

import customtkinter as ctk # Import customtkinter module using a shortened version 'ctk'
from tkinter import messagebox # This is used to show a messagebox
import json, os, time
from PIL import Image # Import python image library for the button images
from ai import TutorGPT # The AI class
from dataclasses import dataclass
from textwrap import dedent
from storageSolutions import StorageSolutions

# File that runs storage logic

# This allows the AI to generate
def get_generator():
    response=model.complete()
    for chunk in response:
        yield chunk

def get_quiz():
    response=model.complete()
    for part in response:
        print(f'{part}')
        yield part

model = TutorGPT(mode='Learn')

stgsol = StorageSolutions()
root = ctk.CTk() # Create the app's customtkinter window
title = ('AI Tutor') # Title of the app

subject_list = ["History", "Math", "Science", "Literature", "Business/Law", "Physics", "Art"]
gradeLevel_list = ["Elementary school", "Middle school", "Secondary school", "College/University"]

# This class is used to create a new scrollable frame. Once instantiated, the program can add mesages from both
# User and Assistant.
class scrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.msgboxes = []
        self.req_height = 10

    # This function gets the student message and creates new message boxes inside of the conversationFrame
    def addMsg(self, msg):
        senders=['User', 'Assistant'] #User is the Student and Assisistant is the AI
        for sender in senders:
            msgbox = ctk.CTkTextbox(self, height=10, wrap="word", activate_scrollbars=False)
            self.msgboxes.append(msgbox)
            if sender == 'User':
                msgbox.grid(row=len(self.msgboxes), column=0, padx=5, pady=5, sticky="nsew")
                msgbox.insert("end", msg)
                msgbox.configure(state='disabled')
            elif sender == 'Assistant': # If sender is Assistant, add 'TutorGPT:' to the sender header
                msgbox.grid(row=len(self.msgboxes), column=0, padx=5, pady=5, sticky="nsew")
                msgbox.insert("end", f"{root.title}: " "\n")
                chunks = get_generator()
                for chunk in chunks:    # A for loop to iterate through each chunk and type into the current messagebox
                    if any(chunk.endswith(char) for char in ['.', '?', '!']):
                        punct_marks = ['.', '?', '!']
                        for mark in punct_marks:
                            if chunk.endswith(f'{mark}'):
                                msgbox.insert('end', f"{mark}\n")
                         # Increment the height of the textbox in real-time
                        msgbox.update()
                        self.req_height +=15
                        msgbox.configure(height=self.req_height)
                        time.sleep(0.03)
                    else:
                        msgbox.insert('end', chunk)
                        msgbox.update()
                        self.req_height +=4
                        msgbox.configure(height=self.req_height)
                        time.sleep(0.03)
                msgbox.configure(state='disabled')
                self.req_height=0


# This class is used to create the radiobuttons and set the current quiz question as the title.
class createRadioButtons(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_rowconfigure(8, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = ctk.StringVar(value="")

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            radiobutton = ctk.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i+1, column=0, padx=10, pady=10, sticky="w")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()

# This class holds the variables that pertain to the student
@dataclass
class Student:
    answers = []
    msg = ''
    msg_list = []
    answers_correct = 0
    name = ''
    score = 0.0

class UI:
    def __init__(self, window):
        # set grid layout 1x2
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)
        self.connectionStatus = 'Connection Status:'
        self.chatWindows = []
        self.navbarLink = ''
        self.placeholder=''
        self.selectedChatSubjectLevel = ctk.StringVar(value='Subject:')
        self.selectedChatGradeLevel = ctk.StringVar(value='Grade Level:')
        self.selectedQuizSubjectLevel = ctk.StringVar(value='Subject:')
        self.selectedQuizGradeLevel = ctk.StringVar(value='Grade Level:')
        self.selectedMode = ctk.StringVar(value='Tutor Mode:')

        #####################################################################################################
        "<><><><><><><><><><><><><><><><><><><><>  Load Images   <><><><><><><><><><><><><><><><><><><><><>"
        #####################################################################################################
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.app_icon = ctk.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "brain_spark_logo.png")), size=(108, 108))

        #####################################################################################################
        "<><><><><><><><><><><><><><><>  Create Sidebar Frame with Tabs   <><><><><><><><><><><><><><><><><>"
        #####################################################################################################
        self.navbarFrame = ctk.CTkFrame(window, corner_radius=0,)
        self.navbarFrame.grid(row=0, column=0, sticky="nsew")
        self.navbarFrame.grid_rowconfigure(9, weight=1)

        self.navbarFrame_lbl = ctk.CTkLabel(self.navbarFrame, text="", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=30, weight="bold"))
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

        self.settingsBtn_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "settings_icon_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "settings_icon_light.png")), size=(20, 20))

        self.quizBtn_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "quiz_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "quiz_light.png")), size=(20, 20))

        self.quizBtn = ctk.CTkButton(self.navbarFrame, corner_radius=0, height=40, border_spacing=10, text="Quiz",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.quizBtn_image, anchor="w", command=lambda: self.navbarEvent('Quiz', self.quizFrame))
        self.quizBtn.grid(row=3, column=0, sticky="ew")

        self.connectionStatusHeader_lbl = ctk.CTkLabel(self.navbarFrame, text=f"{self.connectionStatus}")
        self.connectionStatusHeader_lbl.grid(row=8, column=0, padx=20, pady=10, sticky="s")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navbarFrame, values=["Light", "Dark", "System"],)
        self.appearance_mode_menu.grid(row=9, column=0, padx=20, pady=15, sticky="s")

        #####################################################################################################
        "<><><><><><><><><><><><><><>  Create Chat Frame  <><><><><><><><><><><><><><><><><>"
        #####################################################################################################
        
        self.chatFrame = ctk.CTkFrame(window, corner_radius=0, fg_color="transparent")
        self.chatFrame.grid_rowconfigure(0, weight=1)
        self.chatFrame.grid_columnconfigure(1, weight=1)
        self.chatFrame.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)

        self.chatFrameWidgets = ctk.CTkFrame(self.chatFrame, corner_radius=0, fg_color="transparent")
        self.chatFrameWidgets.grid_rowconfigure(1, weight=1)
        self.chatFrameWidgets.grid_columnconfigure(3, weight=1)
        self.chatFrameWidgets.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

        self.chatWindow = ctk.CTkFrame(self.chatFrameWidgets, corner_radius=0, fg_color="transparent")
        self.chatWindow.grid_rowconfigure(1, weight=1)
        self.chatWindow.grid_columnconfigure(0, weight=1)
        self.chatWindow.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.chatSettingsFrame = ctk.CTkFrame(self.chatFrameWidgets, corner_radius=0, fg_color="transparent")
        self.chatSettingsFrame.grid_rowconfigure(3, weight=1)
        self.chatSettingsFrame.grid_columnconfigure(1, weight=1)
        self.chatSettingsFrame.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)
        self.chat_dropdown_heading_lbl = ctk.CTkLabel(self.chatSettingsFrame, text="\n \n                 Choose your subject \n and study level below:")
        self.chat_dropdown_heading_lbl.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.chat_subjectDropdown = ctk.CTkOptionMenu(self.chatSettingsFrame, values=["Math", "History", "Geography", "Health", "Science"], command=self.setSubject, variable=self.selectedChatSubjectLevel)
        self.chat_subjectDropdown.grid(row=2, column=0, padx=20, pady=10)
        self.chat_gradeLevelDropdown = ctk.CTkOptionMenu(self.chatSettingsFrame, values=["Elementary", "Middle", "High", "College"], command=self.setGrade, variable=self.selectedChatGradeLevel)
        self.chat_gradeLevelDropdown.grid(row=2, column=1, padx=20, pady=10)
        self.hideChatSettingsBtn = ctk.CTkButton(self.chatSettingsFrame, text="Hide Settings", command=lambda: self.chatSettingsFrame.grid_forget())
        self.hideChatSettingsBtn.grid(row=3, column=1, padx=10, pady=10)
        self.chatSettingsFrame.grid_forget()

        self.chatSettingsBtn = ctk.CTkButton(self.chatFrameWidgets, corner_radius=0, height=10, width=10, border_spacing=10, text="Chat Settings",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.settingsBtn_image, anchor="nw", command=lambda: self.switchPanel(panel=self.chatSettingsFrame))
        self.chatSettingsBtn.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        self.newChatBtn = ctk.CTkButton(self.chatFrameWidgets, corner_radius=0, height=10, width=10, border_spacing=10, text="Chat Settings",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.studentBtn_image, anchor="nw", command=lambda: self.newChat())
        self.chatSettingsBtn.grid(row=0, column=1, padx=5, pady=5, sticky='nw')

        self.chatSettingsFrame.grid_forget()  # remove chat settings frame

        self.modeDropdown = ctk.CTkOptionMenu(self.chatFrameWidgets, width=15, values=["Learn", "Expand"], command=self.setMode, variable=self.selectedMode)
        self.modeDropdown.grid(row=2, column=0, padx=10, pady=10, sticky="s")
        # Create question input field and add widgets into the chatFrame
        self.chat_input = ctk.CTkEntry(self.chatFrameWidgets, placeholder_text=f"{self.placeholder}", fg_color="transparent")
        self.chat_input.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        self.askAI_btn = ctk.CTkButton(self.chatFrameWidgets, text="Ask AI", font=ctk.CTkFont(size=15, weight="bold"), command=lambda: self.create_request(msg=self.chat_input.get()))
        self.askAI_btn.grid(row=2, column=2, padx=10, pady=10, sticky="s")

        #####################################################################################################
        "<><><><><><><><><><><><><><><><><><>   Create Student Frame   <><><><><><><><><><><><><><><><><><>"
        #####################################################################################################
        self.studentFrame = ctk.CTkFrame(window, corner_radius=0, fg_color="transparent")
        self.studentFrame.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)
        self.studentFrame.grid_rowconfigure(5, weight=1)
        self.studentFrame.grid_columnconfigure(1, weight=1)

        self.appInfo_lbl = ctk.CTkLabel(
            self.studentFrame,
            text="Welcome to a revolutionary new learning \n experience powered by Open AI.",
            font=ctk.CTkFont(size=20, weight="bold"))
        self.appInfo_lbl.grid(row=2, column=1, padx=10, pady=50)

        self.buttonSub_frame = ctk.CTkFrame(self.studentFrame, corner_radius=0, fg_color="transparent")
        self.buttonSub_frame.grid(row=4, column=1, padx=10, pady=10, sticky="n")

        self.intro_text = f"""\
We're here to help you with your learning. If you need help with a subject, \
click on "Ask AI" to go to our chat window. You can ask our AI anything! \
Are you ready to test yourself? Our "Quiz Generator" will create a multiple choice \
test for you on a topic of your choice.\n\nWhat would you like to do?
        """
        self.choose_lbl = ctk.CTkLabel(
            self.studentFrame,
            wraplength=500,
            text=self.intro_text,
            font=ctk.CTkFont(size=20))
        self.choose_lbl.grid(row=3, column=1, padx=10, pady=10, sticky="n")

        self.chooseAI_button = ctk.CTkButton(
            self.buttonSub_frame,
            height=40,
            width=150,
            text="Ask AI",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=lambda: self.navbarEvent("Chat", self.chatFrame))
        self.chooseAI_button.grid(row=1, column=0, padx=10)

        self.chooseQuiz_button = ctk.CTkButton(
            self.buttonSub_frame,
            height=40,
            width=150,
            text="Quiz Generator",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=lambda: self.navbarEvent("Quiz", self.quizFrame))
        self.chooseQuiz_button.grid(row=1, column=1, padx=10)

        #####################################################################################################
        "<><><><><><><><><><><><><><><><><><>   Create Quiz Frame   <><><><><><><><><><><><><><><><><><><><>"
        #####################################################################################################
        self.quizFrame = ctk.CTkFrame(window, corner_radius=0, fg_color="transparent")
        self.quizFrame.grid_rowconfigure(0, weight=1)
        self.quizFrame.grid_columnconfigure(1, weight=1)
        self.quizFrame.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)

        # Create Quiz Results Frame. This allows a student to view what the correct answers were. 
        self.quizFrame_header = ctk.CTkLabel(
            self.quizFrame,
            text="Quiz Generator",
            font=ctk.CTkFont(size=20, weight="bold"))
        self.quizFrame_header.grid(
            row=0, column=1, columnspan=2, padx=10, pady=10, sticky="n")

        self.quizFrame_subheader = ctk.CTkLabel(
            self.quizFrame,
            text=f"Let's test your knowledge!\n\nPlease select a subject and a study level, then enter a topic.The quiz will be 10 questions long and multiple choice. Click \"Create Quiz\" when you're ready to start.",
            font=ctk.CTkFont(size=20),
            wraplength=500)
        self.quizFrame_subheader.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

        self.quizFrame_subframe = ctk.CTkFrame(self.quizFrame, corner_radius=0, fg_color="transparent")
        self.quizFrame_subframe.grid(row=3, column=1, padx=10, pady=10)

        self.subject_dropdown = ctk.CTkOptionMenu(
            self.quizFrame_subframe,
            height=40,
            width=200,
            values=subject_list, 
            command=self.setSubject,
            variable=self.selectedQuizSubjectLevel,
            font=(ctk.CTkFont(size=15)))
        self.subject_dropdown.set("Choose a subject:")
        self.subject_dropdown.grid(row=0, column=0, padx=10, pady=10)

        self.gradeLevel_dropdown = ctk.CTkOptionMenu(
            self.quizFrame_subframe,
            height=40,
            width=200,
            values=gradeLevel_list, 
            command=self.setGrade,
            variable=self.selectedQuizGradeLevel,
            font=ctk.CTkFont(size=15))
        self.gradeLevel_dropdown.set("Choose a study level:")
        self.gradeLevel_dropdown.grid(row=0, column=1, padx=10, pady=10)

        self.quiz_topic_entry = ctk.CTkEntry(
            self.quizFrame,
            height=40,
            width=405,
            font=ctk.CTkFont(size=15),
            placeholder_text="Enter your topic here",
            fg_color="transparent")
        self.quiz_topic_entry.grid(row=4, column=1, padx=10, pady=10)

        self.createQuiz_btn = ctk.CTkButton(
            self.quizFrame,
            height=50,
            width=200,
            text="Create Quiz",
            font=ctk.CTkFont(size=20, weight="bold"),
            command=lambda: self.getAIQuiz())    
                                                
        self.createQuiz_btn.grid(row=5, column=1, padx=10, pady=60)

        self.wait_label = ctk.CTkLabel(
            self.quizFrame,
            font=ctk.CTkFont(size=15),
            wraplength=550,
            text="(It may take a moment to generate your quiz. Please be patient.)")
        self.wait_label.grid(row=2, column=1, padx=10, pady=10)

        #Initialize the default frame
        self.currentFrame = self.studentFrame
        self.currentTab = self.studentFrame
        
    def switchPanel(self, panel):
        panel.grid(row=0, column=1, sticky="nsew")

    def checkConnection(self, result):
        if isinstance(result, bool):
            while result == True:
                self.connectionStatus=('Status: Connection error!, Retrying...')
                self.askAI_btn.configure(state='disabled')
                self.createQuiz_btn.configure(state='disabled')
        else:
            self.connectionStatus=('Status: Connected')
            self.askAI_btn.configure(state='normal')
            self.createQuiz_btn.configure(state='disabled')

    def getAIQuiz(self, model = TutorGPT(mode='Quiz')):
        """
        Sends a prompt to AI and parses the response.
        If JSON code block is found, raises the quizContainer_frame and sends it the quiz data,
        if not, raises an error frame for the user
        """

        # Reset model settings
        model.setMode("Quiz")
        self.setMode("Quiz")
        msg = (self.quiz_topic_entry.get())
        self.modeManager(msg=msg)

        # Parsing AI response
        response_raw = ""
        parts = get_quiz()
        for part in parts:
            response_raw += part
        response_code = response_raw.strip().split("```")

        # Raise quiz frame if quiz was generated, sends quiz data list to quiz creation function and storage
        if len(response_code) == 3:
            response_data = response_code[1].replace("\n", "").replace("  ", "").replace("    ", "").replace("        ", "").replace("            ", "")
            response_data = response_data[1:len(response_data)-1]

            quiz_as_list = []
            while len(quiz_as_list) != 10:
                start = response_data.find("{")
                end = response_data.find("}")
                quiz_as_list.append(eval(response_data[start:end+1]))
                response_data = response_data[end+1:]

            quiz_data = quiz_as_list

            self.createQuiz(quiz_data)
            print("quiz sent to the creation function") # testing purposes
            stgsol.saveQuiz(self.subject_dropdown.get(), self.gradeLevel_dropdown.get(), quiz_data)
            print("quiz sent to storage") # testing purposes

        # Raises inner error frame if no quiz found
        else:
            self.raise_error(response_code[0])

    def raise_error(self, error):
        """
        Raises a small frame inside quizFrame and displays AI's error message.
        Destroys itself (but nothing else, don't worry) when closed
        """
        self.errorFrame = ctk.CTkFrame(
            self.quizFrame,
            border_width=1,
            fg_color="white")
        self.errorFrame.grid(row=1, column=1, rowspan=3)

        self.errorLabel = ctk.CTkLabel(
            self.errorFrame,
            font=ctk.CTkFont(size=15, weight="bold"),
            justify="left",
            text=f"Uh Oh! Something went wrong.")
        self.errorLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.error_subLabel = ctk.CTkLabel(
            self.errorFrame,
            font=ctk.CTkFont(size=15),
            wraplength=500,
            justify="left",
            text=f"The AI says:\n\n{error}\n\nPlease close this message and try again.")
        self.error_subLabel.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.error_x = ctk.CTkButton(
            self.errorFrame,
            width=5,
            fg_color="light grey",
            hover_color="light blue",
            text_color="grey50",
            text="x",
            command=self.errorFrame.destroy)
        self.error_x.grid(row=0, column=1, padx=1, pady=2, sticky="ne")

    def createQuiz(self, quiz_data):
        Quiz(quiz_data)
            
    # Get the response from the OpenAI API and display it in the AI response in the respective window
    def create_request(self, msg):
        self.newChat()
        self.process_request(msg)

    def newChat(self):
        if not self.chatWindows == []: #
            model.clear()
            return
        else:
            self.conversationFrame = scrollableFrame(self.chatWindow)
            self.chatWindows.append(self.conversationFrame)
            return

    # Get the response from the OpenAI API and display it in the AI response in the respective window
    def process_request(self, msg):
        # Create a scrollable frame to contain each the conversation between the user and the AI
        # Display the student's message and the AI's in the conversation
        print('PROCESSED')                
        self.modeManager(msg=msg)
        self.conversationFrame.addMsg(msg)
        self.switchPanel(self.conversationFrame)

# configure the textbox to update its height when the text changes

    def navbarEvent(self, name, tab):
        self.navbarLink = name
        root.title(f'{title} - {self.navbarLink} screen')
        self.chatBtn.configure(fg_color=("gray75", "gray75") if name == "Chat" else "transparent")
        self.quizBtn.configure(fg_color=("gray75", "gray75") if name == "Quiz" else "transparent")
        self.studentBtn.configure(fg_color=("gray75", "gray75") if name == "Student" else "transparent")
        # show selected Tab (Example: Chat, Quiz)
        if (self.currentTab != tab):
            self.currentTab.grid_forget()
            self.currentTab = tab
            print(self.currentTab, tab)
            tab.grid(row=0, column=1, sticky="nsew")
        else:
            pass

    '<><><><><><><><><><><> These functions set variables <><><><><><><><><><><> '
    
    def setSubject(self, subject): 
        print('SUBJECT:', subject) 
        model.setSubject(subject)

    def setGrade(self, grade):

        print('GRADE:', grade)
        model.setGradeLevel(grade)

        return
    def setMode(self, mode):
        self.mode = mode

        model.clear()
        model.setMode(mode)

        return    
    # This finds the current tutor mode and reroutes the AI behavior of the 'Ask AI button accordingly'
    def modeManager(self, msg):         
        if self.mode == 'Expand':
            model.excerptMode(msg)

        elif self.mode == 'Learn':
            model.learnMode(msg)

        elif self.mode == 'Quiz':
            model.quizMode(msg)

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

class Quiz(UI):
    def __init__(self, quiz_data):
        self.quizAnswers = []
        self.answer = ''
        self.quizFrame_subframe = None
        self.quiz_data = quiz_data
        self.quiz_length = len(self.quiz_data)
        self.current_question = ''
        self.quiz_choices = ''
        self.question_index = 0
        self.correct_answer = ''
        self.progress = 0
        self.max_score = 100

        # Create Quiz Panels. These are the screens that populate inside of the quizFrame
        
        self.quizContainerFrame = ctk.CTkFrame(self.quizFrame_subframe, corner_radius=0, fg_color="transparent")
        self.quizContainerFrame.grid_rowconfigure(8, weight=1)
        self.quizContainerFrame.grid_columnconfigure(4, weight=1)
        self.quizContainerFrame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        self.quizContainer = ctk.CTkFrame(self.quizContainerFrame, corner_radius=0, fg_color="transparent")
        self.quizContainer.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=20, pady=10)
        self.score_lbl = ctk.CTkLabel(self.quizContainer, text='')
        self.submit_button = ctk.CTkButton(self.quizContainerFrame, text='Submit', command=lambda: self.submitAnswer()) # type: ignore
        self.submit_button.grid(row=5, column=0, sticky="nsew", pady=10, padx=40)
        self.progress_bar = ctk.CTkProgressBar(self.quizContainerFrame)
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.grid(row=7, column=0, sticky="nsew", pady=10, padx=40)
        self.score_lbl.grid(row=8, column=0,)
        self.progress_bar.set(0)
        self.quizContainerFrame.grid_forget()

        self.display_question()

    def mapQuizData(self):
        self.current_question_data = self.quiz_data[self.question_index]
        vars = ['quiz_type', 'current_question', 'quiz_choices', 'correct_answer']
        params = ['type', 'question', 'options', 'answer']
        for var, param in zip(vars, params):
            value = self.current_question_data[param]
            setattr(self, var, value)
        self.quizAnswers.append({"Question": self.current_question, "Answer": self.correct_answer})

    def display_question(self):
        self.mapQuizData()
        self.create_widgets()

    def create_widgets(self):
        self.multipleChoiceFrame = createRadioButtons(self.quizContainer, title=self.current_question, values=self.quiz_choices)
        self.multipleChoiceFrame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        self.switchPanel(self.quizContainerFrame)

    def getStudentAnswers(self):
        self.answer = self.multipleChoiceFrame.get()

    def submitAnswer(self):
        # Send student response to AI
        self.checkAnswer()

    def checkAnswer(self):
        self.answer = self.multipleChoiceFrame.get()
            # Check if selected answers match correct answers
        if self.answer == self.correct_answer:
            Student.answers_correct += 1
            messagebox.showinfo("Result", "Correct!")
        else:
            messagebox.showinfo("Result", "Incorrect!")
        self.update_score()

    def nextQuestion(self):
        # This gets the student answer for the current question
        self.question_index += 1
        Student.answers.append(self.answer)
        if self.question_index == 10:
            messagebox.showinfo("Score", f"You scored {Student.score}% out of {self.max_score}%")
            # Show quiz results
            self.quizContainerFrame.grid_forget()
        self.display_question()

    def update_score(self):
        Student.score = ((Student.answers_correct / self.quiz_length) * 100)
        self.score_lbl.configure(text=f'Score: {Student.score}')
        self.progress += (1 / self.quiz_length)
        self.progress_bar.set(self.progress)
        self.nextQuestion()
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