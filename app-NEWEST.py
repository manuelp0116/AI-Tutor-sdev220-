# Program name:       AI Tutor
# Author:             Braden Shrum, Manuel Padre Charles Phillips Chloe Moore, 
# Version:            version 1.0
# Last revision date: 04/29/2023
# The objective of this program is to help a student study more effectively 
# This enable the student to narrow and tailor study help to their own needs such as subject, study level and specific learning parameters. 

# Example AI Request: 'I am a {study level} student, studying {subject}, teach me about photosynthesis'
# Wherein study level='high school' and subject='Biology'


# Standard libraries we might use later on
import random
import math
import time

# User Created Classes
from ai import TutorGPT # The AI class
# from gui import UI # The CustomTkinter class

#------------------------------------------------------------
# OpenAI API functions go here



#------------------------------------------------------------
# Whisper speech transcription functions go here



#------------------------------------------------------------
# Tkinter Functions go here

mode.setMode(mode) # 
model.setQuizConfiguration(setup)
model.addExcerpt(excerpt)

tuple = {mode}, {setMode}

def eventHandler(self, mode, event)

modes = {"mode1": mode_1, "mode2": mode_2}

def handle_mode(mode):
    function = modes.get(mode)
    if function is not None:
        function()
    else:
        print("Invalid mode")

for mode in modes:
    handle_mode(mode)

   
    



#------------------------------------------------------------
# Basic functions go here

def testAI(model: TutorGPT):
    '''
    This is a function that serves as a proof-of-concept for the AI tutor. It provides an interface for the AI to discuss about a topic with the user.

    right now, the user cannot input anything, but this will come later as we integrate the GUI into the program
    '''
    mode = input("""

    
        
        Choose a study mode: 
            Learn: Learn about any topic
            Expand: Get help understanding a certain concept
            Quiz: Generate quiz from a topic
            Stop: Close the application

        Study Mode > """) # Primer input
    
    mode = mode.lower() # convert all the test to lowercase

    while mode != "stop": # loop until the user types "stop"
        model.setMode(mode) # set the mode

        if mode == "quiz": # if the mode is quiz
            topic = input("Please enter a topic of study > ") # get the topic of discussion
            
            # get the setup of the quiz and split it by ", "
            setup = input("""
                Enter the types of questions you want asked in your quiz:
                    Multiple Choice: Choose one of 4 possible answers
                    Multiple Answer: At least two answers are correct, and up to four are correct
                    Short Answer: An input requiring you to put in your own answer

                Queston Types (y/N separated by ', ' if more than one) > """).lower().split(", ")
            
            # format the y and n inputs to work with the prompting technique
            for i, value in enumerate(setup):
                if value == "y":
                    setup[i] = ""
                elif value == "n":
                    setup[i] = "out"
            
            model.setQuizConfiguration(setup) #set the quiz configuration

            model.addTopic(topic) # add the quiz topic and settings

        elif mode == "learn": # if the mode is learn
            # get the topic and add it
            topic = input("Please enter a topic of study > ")
            model.addTopic(topic)

        elif mode == "expand": # if the mode is expand
            # get the text excerpt and add it
            excerpt = input("Paste in your excerpt of text here > ")
            model.addExcerpt(excerpt)

        else: # input validation
            print("Please choose a valid option \n")

            mode = input("""
        
                Choose a study mode: 
                    Learn: Learn about any topic
                    Expand: Get help understanding a certain concept
                    Quiz: Generate quiz from a topic
                    Stop: Close the application

                Study Mode > """) # ask the user again for input
            mode = mode.lower()
            continue # skip over the rest of the code and restart the loop

        response = model.complete() # get the response stream

        print('\n\n')

        # Print the response generation in real-time
        for chunk in response:
            # end has to equal an empty string to stop the print statement from printing every chunk on a new line
            # flush has to equal True so that the print statement can print the characters in real time
            print(chunk, end='', flush=True)

        # take input again and make it lowercase
        mode = input("""
        
        Choose a study mode: 
            Learn: Learn about any topic
            Expand: Get help understanding a certain concept
            Quiz: Generate quiz from a topic
            Stop: Close the application

        Study Mode > """)
        mode = mode.lower()

def main():
    pass

def testMain():
    pass

if __name__ == "__main__":
    # testMain()
    # testAI()
    main()