class Quiz (ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.label = ctk.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)
        self.questions = questions
        self.quiz_length = len(self.questions)
        self.current_question = 0
        self.answers_correct = 0
        self.progress = 0
        self.max_score = 10
        self.score = 0
        
        # Create the GUI
        self.quiz_TopLevelWindow = ctk.CTk()
        self.quiz_TopLevelWindow.title("Quiz")
        self.question_label = ctk.CTkLabel(self.quiz_TopLevelWindow, text="Question")
        self.question_label.pack()
        self.answer_options = []
        self.selected_option = ctk.IntVar()
        for i in range(4):
            answer_option = ctk.CTkRadioButton(self.quiz_TopLevelWindow, text="Option", variable=self.selected_option, value=i)
            self.answer_options.append(answer_option)
            answer_option.pack()
        self.submit_button = ctk.CTkButton(self.quiz_TopLevelWindow, text="Submit", command=self.submit_answer)
        self.submit_button.pack()
        self.next_button = ctk.CTkButton(self.quiz_TopLevelWindow, text="Next", command=self.next_question)
        self.next_button.configure(state="disabled")
        self.next_button.pack()
        self.score_lbl = ctk.CTkLabel(self.quiz_TopLevelWindow, text='')
        self.score_lbl.pack()
        self.progress_bar = ctk.CTkProgressBar(self.quiz_TopLevelWindow)
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.pack(padx=20, pady=10)
        self.progress_bar.set(0)

        self.display_question()
        
        # Start the GUI
        self.quiz_TopLevelWindow.mainloop()
    
    def display_question(self):
        question = self.questions[self.current_question]
        self.question_label.configure(text=question["question"])
        for i, option in enumerate(question["choices"]):
            self.answer_options[i].configure(text=option)
    
    def submit_answer(self):
        question = self.questions[self.current_question]
        selected_option = self.selected_option.get()
        
        if selected_option == question["answer"]:
            self.answers_correct += 1
            messagebox.showinfo("Result", "Correct!")
        else:
            messagebox.showinfo("Result", "Incorrect!")
        
        self.update_score(self.answers_correct)
        self.submit_button.configure(state="disabled")
        self.next_button.configure(state="normal")

    def update_score(self, var_in):
        self.score = (var_in / len(self.questions) * 100)
        self.score_lbl.configure(text=f'Score: {self.score}')
        self.progress += (1 / self.quiz_length)
        self.progress_bar.set(self.progress)
        return self.score, self.progress
    
    def next_question(self):
        self.current_question += 1
        if self.current_question == len(self.questions):
            messagebox.showinfo("Score", f"You scored {self.score}% out of {self.max_score}%")
            self.quiz_TopLevelWindow.destroy()
            return
        self.display_question()
        self.submit_button.configure(state="normal")
        self.next_button.configure(state="disabled")

# Sample json input
questions = [
      {
        "question": "What is the capital city of France?",
        "choices": ["London", "Paris", "Berlin", "Madrid"],
        "answer": 1
      },
      {
        "question": "Who is the founder of Microsoft?",
        "choices": ["Steve Jobs", "Bill Gates", "Mark Zuckerberg", "Jeff Bezos"],
        "answer": 1
      },
      {
        "question": "What is the largest country in the world?",
        "choices": ["Russia", "Canada", "China", "Brazil"],
        "answer": 0
      },
      {
        "question": "What is the name of the currency used in Japan?",
        "choices": ["Yuan", "Euro", "Dollar", "Yen"],
        "answer": 3
      },
      {
        "question": "What is the smallest country in the world?",
        "choices": ["Vatican City", "Monaco", "Nauru", "San Marino"],
        "answer": 0
      }
    ]