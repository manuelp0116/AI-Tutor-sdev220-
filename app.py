'''
APP DESCRIPTION HERE
'''

# Standard libraries we might use later on
import random
import math
import time

# User Created Classes
from ai import TutorGPT # The AI class
# from gui import UI # The CustomTkinter class

#------------------------------------------------------------
# OpenAI API functions go here

def discuss(model: TutorGPT):
    '''
    This is a function that serves as a proof-of-concept for the AI tutor. It provides an interface for the AI to discuss about a topic with the user.

    right now, the user cannot input anything, but this will come later as we integrate the GUI into the program
    '''
    count = 0

    while True:
        if count >= 3:
            break

        if count == 0:
            model.addTopic("Astrophysics") #ideally we will have the user input here but since this isn't connected to a GUI just yet, we have to wait
        elif count == 1:
            model.setPrompt("Thanks for telling me about Astrophysics! Can you expand on #1?")
        elif count == 2:
            model.setMode("quiz")
            model.addTopic("Astrophysics") # Yes, I know this is very redundant, I will work on it in the next update

        print(model.prompt, "\n")
        response = model.complete()

        print(response, "\n") #This will later be turned into printing to the GUI

        count += 1

    print(model.history)

systemPrompt = "You are an instructor that specializes in all subjects. You can teach and coach about anything, as you have unlimited knowlege."

tutor = TutorGPT(systemPrompt, "learn", "Astrophysics", "college")

discuss(tutor)

#------------------------------------------------------------
# Whisper speech transcription functions go here



#------------------------------------------------------------
# Tkinter Functions go here



#------------------------------------------------------------
# Basic functions go here

def main():
    pass

if __name__ == "__main__":
    main