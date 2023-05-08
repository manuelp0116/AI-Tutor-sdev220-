import customtkinter as ctk

class controlPanel(ctk.CTkFrame):
    def __init__(self, master, title, values, command):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.radiobuttons, self.checkboxes, self.switches=[]
        self.command = command
        self.variable = ctk.StringVar(value="")

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, pady=(10, 0), sticky="ew")

    def createWidgets(self, widget):
        for i, value in enumerate(self.values):
            widget = (self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i+1, column=0, padx=10, pady=10, sticky="w")
            self.radiobuttons.append(radiobutton)

            checkbox,checkboxes

    def getRbValues(self):
        return self.variable.get()
    
    def setQuizData(self):
        self.current_question_data = self.quiz_data[self.question_index]
        vars = ['checkbox', 'radiobutton', 'switch']
        params = ['checkboxes', 'radiobuttons', 'switches']
        for var, param in zip(vars, params):
            value = self.current_question_data[]
            setattr(self, var, value)

    widget
    
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