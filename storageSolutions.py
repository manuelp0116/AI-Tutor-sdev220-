import openai
import datetime
import os

import json

openai.api_key = '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'


response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = [
    {"role": "system", "content": "you are a quiz creation app, your answers will be formatted in a json file"},
    {"role": "user", "content": "make a 3 question quiz about elemetary level astronomy"},
    ]
)
print(response)



def saveQuiz(response):
    
  
    if os.path.exists("quizSTG"): #checks fro folder to store the quizzes

        filename = "quiz" + str(1) #creates file name, need to find a way to create diff names every time 
        file_path = filename + ".json"
        file_dir = os.path.dirname("QuizSTG")
        with open(file_path, 'w') as fp:
            json.dump(response, fp)
    else:    
        directory = "QuizSTG"
        # Path
        path = os.path.join(directory)
  
        # Create the directory
        os.mkdir(path)

def saveChat(response):
    if os.path.exists("ChatSTG"):
    
        count = 1
        file_path = "Chat" + str(count)
        count += 1
        file_dir = os.path.dirname("ChatSTG")
        with open(file_path, 'w') as fp:
            json.dump(response, fp)
    else:    
        directory = "ChatSTG"
        # Path
        path = os.path.join(directory)
  
        # Create the directory
        os.mkdir(path)
        
def readQuiz():
    
