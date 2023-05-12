import customtkinter as ctk # Import customtkinter module using a shortened version 'ctk'
from tkinter import messagebox # This is used to show a messagebox
import json, os, time
from PIL import Image # Import python image library for the button images
from ai import TutorGPT # The AI class
from dataclasses import dataclass
from textwrap import dedent
from storageSolutions import * # File that runs storage logic

# Class Quiz:
    #def__init(self, master, quiz_data)
#       super.()__init__(master)
#       self.subject (Ex. 'History')
#       self.grade ('secondary')
#       

# This allows the AI to generate
def get_generator():
    response=model.complete()
    for chunk in response:
        yield chunk

model = TutorGPT(subject=currentSubject, gradeLevel=currentGradeLevel)
root = ctk.CTk() # Create the app's customtkinter window
title = ('AI Tutor') # Title of the app
subject_list = ["History", "Math", "Science", "Literature", "Business/Law"]
gradeLevel_list = ["Elementary school", "Middle school", "Secondary school", "College/University"]

# This class is used to create a new scrollable frame. Once instantiated, the program can add mesages from both
# User and Assistant.
class scrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, msg):
        self.grid_columnconfigure(0, weight=1)
        self.msgboxes = []
        self.req_height = 10

    
    # This function gets the student message and creates new message boxes inside of the conversationFrame
    def addMsg(self, msg):
        senders=['User', 'Assistant'] #User is the Student and Assisistant is the AI
        for sender in senders:
            msgbox = ctk.CTkTextbox(self, height=10, wrap="word")
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
                        msgbox.insert('end', f"{char}\n")6
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
    answer = ''
    answers = []
    chatInput = ''
    answers_correct = 0
    name = ''
    score = 0.0

class UI:
    def __init__(self, window):
        # set grid layout 1x2
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)
        self.currentPanel = ''
        self.currentTab = ''
        self.connectionStatus = 'Connection Status:'
        self.chatWindows = []
        self.navbarLink = ''
        self.placeholder=''

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

        self.connectionStatusHeader_lbl = ctk.CTkLabel(self.navbarFrame, text=f"{self.connectionStatus}")
        self.connectionStatusHeader_lbl.grid(row=8, column=0, padx=20, pady=10, sticky="s")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navbarFrame, values=["Light", "Dark", "System"],)
        self.appearance_mode_menu.grid(row=9, column=0, padx=20, pady=15, sticky="s")

        #####################################################################################################
        "<><><><><><><><><><><><><><>  Handler to creat a new Chat Frame  <><><><><><><><><><><><><><><><><>"
        #####################################################################################################
        self.chatFrame = ctk.CTkFrame(window, corner_radius=0, fg_color="transparent")
        self.chatFrame.grid_rowconfigure(0, weight=1)
        self.chatFrame.grid_columnconfigure(1, weight=1)
        self.chatFrame.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)

        # Create question input field and add widgets into the chatFrame
        self.chat_input = ctk.CTkEntry(self.chatFrame, placeholder_text=f"{self.placeholder}", fg_color="transparent")
        self.chat_input.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        self.askAI_btn = ctk.CTkButton(self.chatFrame, text="Ask AI", font=ctk.CTkFont(size=15, weight="bold"), command=lambda: self.create_request())
        self.askAI_btn.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

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
            variable=ctk.StringVar(),
            font=(ctk.CTkFont(size=15)))
        self.subject_dropdown.set("Choose a subject:")
        self.subject_dropdown.grid(row=0, column=0, padx=10, pady=10)

        self.gradeLevel_dropdown = ctk.CTkOptionMenu(
            self.quizFrame_subframe,
            height=40,
            width=200,
            values=gradeLevel_list,
            variable=ctk.StringVar(),
            font=ctk.CTkFont(size=15))
        self.gradeLevel_dropdown.set("Choose a study level:")
        self.gradeLevel_dropdown.grid(row=0, column=1, padx=10, pady=10)

        self.topic_entry = ctk.CTkEntry(
            self.quizFrame,
            height=40,
            width=405,
            font=ctk.CTkFont(size=15),
            placeholder_text="Enter your topic here",
            fg_color="transparent")
        self.topic_entry.grid(row=4, column=1, padx=10, pady=10)

        self.createQuiz_btn = ctk.CTkButton(
            self.quizFrame,
            height=50,
            width=200,
            text="Create Quiz",
            font=ctk.CTkFont(size=20, weight="bold"),
            command=lambda: self.getAIQuiz(model))
        self.createQuiz_btn.grid(row=5, column=1, padx=10, pady=60)

        self.wait_label = ctk.CTkLabel(
            self.quizFrame,
            font=ctk.CTkFont(size=15),
            wraplength=550,
            text="(It may take a moment to generate your quiz. Please be patient.)")
        self.wait_label.grid(row=2, column=1, padx=10, pady=10)

        #Initialize the default frame
        self.currentFrame = self.studentFrame
        self.studentFrame.tkraise()

    def setPanel(self, panel):
        self.currentPanel = panel
        
    def switchPanel(self, panel):
        self.currentPanel.grid_forget()
        self.setPanel(panel)
        print(self.currentPanel, panel)
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

    def getAIQuiz(self, model: TutorGPT):
        """
        Sends a prompt to AI and parses the response.
        If JSON code block is found, raises the quizContainer_frame and sends it the quiz data,
        if not, raises an error frame for the user
        """
        # Reset model settings
        model.setMode("quiz")
        model.setSubject(self.subject_dropdown.get())
        model.setGradeLevel(self.gradeLevel_dropdown.get())
        model.quizMode(topic=self.topic_entry.get())

        # Call the AI
        response = model.complete(stream=True)

        # Parsing AI response
        response_raw = ""
        for chunk in response:
            response_raw += chunk
        response_code = response_raw.strip().split("```")

        # Raise quiz frame if quiz was generated, sends quiz data list to quiz creation function and storage
        if len(response_code) == 3:
            response_data = response_code[1].replace("\n", "").replace("  ", "").replace("    ", "").replace("        ", "").replace("            ", "")
            response_data = response_data[1:len(response_data)-1]

            quiz_as_list = []
            while len(quiz_as_list) != 10:
                start = response_data.find("{")
                end = response_data.find("}")
                quiz_as_list.append(response_data[start:end+1])
                response_data = response_data[end+1:]

            self.quiz_data = quiz_as_list
            self.createQuiz(self.quiz_data)
            print("quiz sent to the creation function") # testing purposes
            storagesolutions.saveQuiz(self, subject=self.subject_dropdown.get(), grade=self.gradeLevel_dropdown.get(), response=self.quiz_data)
            print("quiz sent to storage") # testing purposes

        # Raises inner error frame if no quiz
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
        Quiz(quiz_data=quiz_data)
        self.switchPanel(self.QuizContainerFrame)

    def checkFields(self):
        if self.currentTab == 'Chat':
            while self.chat_input.get() != '':
                self.askAI_btn.configure(state='normal')
            self.askAI_btn.configure(state='disabled')
        elif self.currentTab == 'Quiz':
            while self.quiz_input.get() != '':
                self.createQuiz_btn.configure(state='normal')
            self.createQuiz_btn.configure(state='disabled')

    # Get the response from the OpenAI API and display it in the AI response in the respective window
    def create_request(self):
        if self.checkFields() and self.checkConnection(result=model.complete()):
            # Create a scrollable frame to contain each the conversation between the user and the AI
                self.chatHistoryFrame = scrollableFrame(self.chatFrame)
                # Display the student's message and the AI's in the conversation
                Student.chatInput = self.chat_input.get()
                self.chatHistoryFrame.addChat(message=Student.chatInput, senders=['User', 'Assistant'])
                self.chatWindows.append(self.chatHistoryFrame)
        else:
            return

# configure the textbox to update its height when the text changes

    def startLearning(self):
        self.studentFrame.grid_forget()  # remove startupScreen frame
        self.chatFrame.grid(row=0, column=0, sticky="nsew")  # show main frame

    def back_event(self):
        self.chatFrame.grid_forget()  # remove main frame
        self.studentFrame.grid(row=0, column=1, sticky="nsew")  # show login frame

    

    def navbarEvent(self, name, frame):
        navbarLink = self.navbarLink
        self.currentTab = name
        root.title(f'{title} - {self.currentTab} screen')
        self.chatBtn.configure(fg_color=("gray75", "gray75") if name == "Home" else "transparent")
        self.quizBtn.configure(fg_color=("gray75", "gray75") if name == "Chat" else "transparent")
        self.studentBtn.configure(fg_color=("gray75", "gray75") if name == "Student" else "transparent")
        # show selected Tab (Example: Chat, Quiz)
        if (self.currentTab != tab):
            self.currentTab.grid_forget()
            print(self.currentTab, tab)
            self.currentTab = tab
            tab.grid(row=0, column=1, sticky="nsew")
        else:
            pass


    '<><><><><><><><><><><> These functions set variables <><><><><><><><><><><> '
    def getCurrentDropdowns(self, dropdown):
        currentSubjectDropdown = dropdown
        currentGradeLevelDropdown = dropdown

    def setMode(self, mode):
        model.setMode(mode)

    def setExcerpt(self, excerpt):
        model.excerptMode(excerpt)

    #def getMode(self):
        #mode = self.mode.get()

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

class Quiz(UI):
    def __init__(self, quiz_data):
        super().__init__(self)
        self.quiz_data = quiz_data
        self.quiz_length = len(self.quiz_data)
        self.current_question = ''
        self.quiz_choices = ''
        self.answer = ''
        self.correct_answer = ''
        self.progress = 0
        self.max_score = 100

        self.display_question()

    def mapQuizData(self):
        self.current_question_data = self.quiz_data[len(Student.answers)]
        vars = ['current_question', 'quiz_choices' 'correct_answer']
        params = ['question', 'options' ,'answer']
        for var, param in zip(vars, params):
            value = self.current_question_data[param]
            setattr(self, var, value)
        self.quizAnswers.append({"Question": self.current_question, "Answer": self.correct_answer})

    def display_question(self):
        self.mapQuizData()
        self.create_widgets()

    def create_widgets(self):
        self.multipleChoiceFrame = createRadioButtons(self.quizContainer, title=self.current_question, values=self.quiz_choices)
        self.multipleChoiceFrame.grid(row=0, column=3, padx=40, pady=10, sticky="nsew")

    # function call: sanitizeInputField()

    # Function for checking if all the input fields are both filled and contain valid
    # entries before passing the input variables into the program.
    def sanitizeInputField(self, str_in):
        if str_in.isalnum() != 0:
            messagebox.showerror('Invalid request!', 'Please enter a valid request')
        else:
            str_out = str_in
            return str_out

    def check_fields(self, command):
        if not self.empty_fields() and self.validated_fields():
            command()

    def getStudentAnswers(self):
        Student.answer = self.multipleChoiceFrame.get()

    def submitAnswer(self):
        # Send student response to AI
        self.create_request(self.answer)
        self.checkAnswer()

    def checkAnswer(self):
        Student.answer = self.multipleChoiceFrame.get()
            # Check if selected answers match correct answers
        if Student.answer == self.correct_answer:
            Student.num_correct_answers +=1
            messagebox.showinfo("Result", "Correct!")
        else:
            messagebox.showinfo("Result", "Incorrect!")
            Student.answers.append(self.answer)
        self.update_score()

    def nextQuestion(self):
        # This gets the student answer for the current question
        self.answer.append(Student.answer)
        if len(Student.answers) == self.quiz_length:
            messagebox.showinfo("Score", f"You scored {Student.score}% out of {self.max_score}%")
            # Show quiz results
            self.quizResultsFrame = scrollableFrame(self.postQuizFrame)
            #self.quizResultsFrame.showQuizResults(results)
            self.switchPanel(self.quizResultsFrame)
        self.display_question()

    def update_score(self):
        Student.score = ((len(Student.correct_answers) / self.quiz_length) * 100)
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
