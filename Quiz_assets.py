class Quiz:
    def __init__(self):
        self.quiz_length = len(self.quizData)
        self.current_question = 0
        self.answers_correct = 0
        self.progress = 0
        self.max_score = 100
        self.score = 0
        self.selected_option = ctk.IntVar()
        self.answer_options = []
        for i in range(4):
            answer_option = ctk.CTkRadioButton(UI.quizContainer, text="Option", variable=self.selected_option, value=i)
            self.answer_options.append(answer_option)
            answer_option.pack()
        self.submit_button = ctk.CTkButton(UI.quizContainer, text="Submit", command=self.submit_answer)
        self.submit_button.pack()
        self.next_button = ctk.CTkButton(UI.quizContainer, text="Next", command=self.next_question)
        self.next_button.configure(state="disabled")
        self.next_button.pack()
        self.score_lbl = ctk.CTkLabel(UI.quizContainer, text='')
        self.score_lbl.pack()
        self.progress_bar = ctk.CTkProgressBar(UI.quizContainer)
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.pack(padx=20, pady=10)
        self.progress_bar.set(0)

        self.display_question()

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
            self.window.destroy()
            return
        self.display_question()
        self.submit_button.configure(state="normal")
        self.next_button.configure(state="disabled")

    def loadQuiz(self, filename):
        with open(filename, "r") as file:
            self.quizData = json.load(file)
