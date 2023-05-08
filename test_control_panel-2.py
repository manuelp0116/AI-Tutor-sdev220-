import customtkinter as ctk

class createWidgets(ctk.CTkFrame):
    def __init__(self, master, title, values, widget):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.values = values
        self.widget = widget
        self.radiobuttons, self.checkboxes, self.switches, self.textboxes=[], [], [], []
        self.variable = ctk.StringVar(value="")

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, pady=(10, 0), sticky="ew")

        widget_dict = {'radiobutton': ctk.CTkRadioButton,'checkbox': ctk.CTkCheckBox,
        'switch': ctk.CTkSwitch,'textbox': ctk.CTkTextbox}
        for widget_name, widget_class in widget_dict.items():
            setattr(self, widget_name, widget_class(self))

        for i, choice in enumerate(self.choices):
            widget = widget_class(self, text=choice)
            widget.grid(row=len(widget_list), column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

            values = ['Multiple Choice','Multiple Answer','Fill in the Blank'] 
            self.quizSettings = controlPanel(self, '', values=values, widget='radiobutton')

            values = ['Student Response','AI Response','Student Response']

    def msgBox(self):
        title='Quiz creation screen'
        values=inputBox.get()
        self.quizSettings = createWidgets(self, title=title, values=values, widget='radiobutton')


    def type_msg(self):
        # Add each character of the message one-by-one with a delay
        # chunks = get_generator()
        for chunk in response:
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




       
    