import json
import customtkinter as ctk
from tkinter import messagebox

# Define a class for the quiz GUI
class createCheckBoxes(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []
        self.title = title

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            checkbox = ctk.CTkCheckBox(self, text=value)
            checkbox.grid(row=i+1, column=0, padx=10, pady=10, sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes
    
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
    
class QuizGUI(ctk.CTk):
    def __init__(self, quiz_data):
        super().__init__()
        self.quiz_data = quiz_data
        self.quiz_length = len(self.quiz_data)
        self.quiz_type = ''
        self.current_question = ''
        self.correct_answer = ''
        self.student_answer = ''
        self.options = ''
        self.question_index = 0
        self.answers_correct = 0
        self.progress = 0
        self.max_score = 100
        self.score = 0
        self.grid_rowconfigure(8, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create GUI elements
        self.title('Quiz')
        self.geometry('400x400')
        self.question_label = ctk.CTkLabel(self, text='')
        self.question_label.grid(row=0, column=0)
        self.score_lbl = ctk.CTkLabel(self, text='')
        self.score_lbl.grid(row=8, column=0,)
        self.submit_button = ctk.CTkButton(self, text='Submit', command=self.submitAnswer)
        self.submit_button.grid(row=5, column=0, sticky="nsew", pady=10, padx=40)
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.grid(row=7, column=0, sticky="nsew", pady=10, padx=40)
        self.progress_bar.set(0)

        self.display_question()

    def setQuizData(self):
        self.current_question_data = self.quiz_data[self.question_index]
        vars = ['quiz_type', 'current_question', 'correct_answer']
        params = ['type', 'question', 'answer']
        for var, param in zip(vars, params):
            value = self.current_question_data[param]
            setattr(self, var, value)

    def create_widgets(self):
        self.setQuizData()
        if self.quiz_type == 'Fill in the Blank':
            self.question_label.configure(self, text=self.current_question, fg_color="gray30", corner_radius=6)
            self.question_label.grid(row=1, column=0, sticky="ew")
            self.answer_entry = ctk.CTkEntry(self)
            self.answer_entry.grid(row=4, column=0, sticky="ew", padx=30)
            
        elif self.quiz_type == 'Multiple Choice':
            self.quiz_options = self.quiz_data[self.question_index]['options']
            self.multipleChoiceFrame = createRadioButtons(self, self.current_question, values=self.quiz_options)
            self.multipleChoiceFrame.grid(row=0, column=0, padx=40, pady=10, sticky="nsew")
                               
        elif self.quiz_type == 'Multiple Answer':
            self.quiz_options = self.quiz_data[self.question_index]['options']
            self.multipleAnswerFrame = createCheckBoxes(self, self.current_question, values=self.quiz_options)
            self.multipleAnswerFrame.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")

    def display_question(self):
        self.create_widgets()

    def ignoreCaseSensitive(self, state):
        if state is True:
            self.student_answer = self.student_answer.lower()
            self.correct_answer = self.correct_answer.lower()
        else:
            return False
    

    def getStudentAnswers(self):
        # Get current question data
        if self.quiz_type == 'Fill in the Blank':
            # Get selected answers
            self.student_answer = self.answer_entry.get()
            self.ignoreCaseSensitive(True)
            print(self.student_answer, self.correct_answer)
        if self.quiz_type == 'Multiple Answer':
        # Get a set of selected answers
            self.student_answer = self.multipleAnswerFrame.get()
        if self.quiz_type == 'Multiple Choice':
            # Get multiple choice answer as a set of selected answers
            self.student_answer = self.multipleChoiceFrame.get()

    def submitAnswer(self):
        print('AI Response Here')
        # Send student response to AI
        # model.complete(self.student_answer)
        self.checkAnswer()

    def checkAnswer(self):
        self.getStudentAnswers()
            # Check if selected answers match correct answers
        if set(self.student_answer) == set(self.correct_answer):
            self.answers_correct += 1
            messagebox.showinfo("Result", "Correct!")
        else:
            messagebox.showinfo("Result", "Incorrect!")
        self.update_score()

    def nextQuestion(self):
        print('Go here?')
        self.question_index += 1
        if self.question_index == self.quiz_length:
            messagebox.showinfo("Score", f"You scored {self.score}% out of {self.max_score}%")
            self.destroy()
            return
        self.display_question()

    def update_score(self):
        self.score = ((self.answers_correct / self.quiz_length) * 100)
        self.score_lbl.configure(text=f'Score: {self.score}')
        self.progress += (1 / self.quiz_length)
        self.progress_bar.set(self.progress)
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

quiz_gui = QuizGUI(quiz_data)
quiz_gui.mainloop()
