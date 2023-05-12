import openai
import datetime
import os

import json

# openai.api_key = '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'


# response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = [
#     {"role": "system", "content": "you are a quiz creation app, your answers will be formatted in a json file"},
#     {"role": "user", "content": "make a 3 question quiz about elemetary level astronomy"},
#     ]
# )
# print(response)



class storagesolutions:

    '''
    Storage solutions,

    functions housekeeping, save quiz, save chat
    '''
    def __init__(self):
        pass

    def housekeep(self):
        #use this function at the start of the app to create and get folders ready, it will create the necessary folders for the stuff that needs to be saved, and will check for those same folders in the future
        if os.path.exists("quizSTG") and os.path.exists("chatSTG"):
            print("folder exist")


        else:
            pathList = ['quizSTG', 'chatSTG'] #names of folders on list to iterate through them
            for i in pathList:
                path = os.path.join(i)
                os.mkdir(path)

    def saveQuiz(self, subject, grade, response):
        #will save output from AI in a json file, parsing could be necesary, naming conventions for the files are up to change.
        file_name = str(subject) + "quiz" + str(grade) #file name, could add datetime module to name the files in a more personalized manner
        file_path = file_name + ".json"
        save_path = 'quizSTG'
        with open(file_path, 'w') as fp:
            json.dump(response,fp)
            os.path.join('quizSTG', file_path)
        fp.close
        
    def saveChat(self, chat, subject, grade):
        #
        file_name = 'chat' + str(subject) + str(grade) + str(datetime.date.today)
        file_path = file_name + ".txt"
        with open(file_path, "w") as fp:
            fixChat = chat.split() #neeed the necesary parameter to split and parse the chat
            fp.write(fixChat)
        fp.close
        os.path.join('chatSTG', file_path)
        
    def folderNav(self):
        '''
        this function prints all entries in a folder, and splits the names
        so its easily accesible, ,maily used to access old tests
        '''
        with os.scandir('') as entries: #scan directory, need to work on making it dinamic
            for entry in entries:
                name = str(entry)
                nameSplit = name.split('.')#split the files and creates the list
                name_list = [nameSplit]
                return entry
            print(name_list) #print just the file names.
                
    def getQuiz(self, userInput):
        '''
        this should get a json file and save it in a varible to be used by chloes function to create the quiz.
        '''
        path_file = userInput + ".json"
        with os.scandir('quizSTG') as entries: #scan directory
            for entry in entries:
                if entry == path_file: #checks for path file 
                    with open(path_file, 'r') as fp: #open and reads json 
                      quizFile =   json.load(fp)
                      fp.close()
                      return quizFile 
    
    
    def getChat(self, userInput):
        path_file = userInput + '' # Havent decide what kind of file will chat be 
        with os.scandir('chatSTG') as entries:
            for entry in entries:
                if entry == path_file:
                    with open(path_file, 'r') as fp:
                        quizfile = json.load(fp)
                        fp.close()
                        return quizfile         
        
    
