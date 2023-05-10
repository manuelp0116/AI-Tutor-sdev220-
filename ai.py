import openai # AI outputs
from openai.error import APIConnectionError # Connection Error Handling
# import whisper

from typing import Any, overload # function overloading
from textwrap import dedent # To make docstrings look nicer in the
import copy

openai.api_key = "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"

def retryConnection(max_retries):
    def decorator(function):
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    result = function(*args, **kwargs) # complete() function

                    for chunk in result:
                        yield chunk

                    break
                except APIConnectionError:
                    if i % 2 == 0:
                        print(f"Connection Failed, retrying... ({i}/{max_retries})\n")
                    
                    if i == max_retries:
                        print("Insure you are connected to the internet and try again\n")
                        return True # Return True to communicate the error with the GUI
        return wrapper
    return decorator

class ModelBase:
    def __init__(self, prompt, systemPrompt):
        self.prompt = prompt # What we're asking the AI to do (ex: "give me a quiz on the French Revolution")
        self.systemPrompt = systemPrompt # What the AI is (EX: you are an instructor)

        self.history = [] # This is the stored chat history.
        self.api = openai.ChatCompletion()

        self.chat = { #initialize the chat with a system prompt
            "messages": [
                {"role": "system", "content": systemPrompt},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": "Understood! How can I help you?"}
            ]
        }

    #----------------------------- Main Method -----------------------------#

    @retryConnection(max_retries=100)
    def complete(self, temperature=0.8, top_p=1, stream=True):
        '''
        Get's a response from the AI according to the question layed out in the prompt
        This function takes in two optional parameters:
            `temperature` - the randomness of the output - Set at 0.8 by default\n
            `top_p` - controls outputs via nucleus sampling. 0.5 means half of all likelyhood-weighed options are considered - set at 1 by default

        Returns:
            A generator object that contains all the chunks of AI output. This is necessary for streaming outputs.
        '''
        if self.history: #check if there are messages in the history
            self.store(self.history[-1])

        msg = {"role": "user", "content": self.prompt} # Parse the user prompt

        self.chat["messages"].append(msg) #append the dictionary to the inner list in chat

        # Get the AI response
        if stream: # if the user wants to stream their response
            completion = self.api.create(model="gpt-3.5-turbo", messages=self.chat["messages"], temperature=temperature, top_p=top_p, stream=True)

            collectedMessages = []
            for chunk in completion:
                collectedMessages.append(chunk["choices"][0]["delta"])
                if "content" in chunk["choices"][0]["delta"]:
                    yield chunk["choices"][0]["delta"]["content"]

            self.logCompletion(collectedMessages) #Add the AI's response to message history

        else:
            completion = self.api.create(model="gpt-3.5-turbo", messages=self.chat["messages"], temperature=temperature, top_p=top_p)
                    
            self.logCompletion(completion) #Add the AI's response to message history

            return completion["choices"][0]["content"]

    #----------------------------- Chat History Management -----------------------------#

    def logCompletion(self, messages):
        '''
        Builds a message dictionary from a list of messages. Message Dictionaries look like this:
        >>> messageDict = {"role": "assistant", "content": "How can I help you?"}

        This function takes in one parameter:
            `messages` - a list of messages to be evaluated

        `messages` contains chunks of messages from the AI, with the first chunk being the role of the output.
        This function takes in those chunks of outputs and recontructs a message dictionary to save in chat history.
        '''
        # Define the variables
        collectedResponse = []
        ResponseDict = {}
        resultDict = {}

        # Loop over the messages list and sort them into the resulting dictionary and a list
        for message in messages:
            if "role" in message: # If the "role" dictionary is found, place it in the result dictionary
                resultDict.update(message)
            else: # Every other dictionary (the "content" dictionaries) will be placed in a list
                collectedResponse.append(message)   

        ResponseDict.update(collectedResponse[0]) # Update the responseDict with the first dictionary in the collectedResponse list

        # loop over the dictionaries in the collectedResponse list
        for response in collectedResponse:
            if "content" in response: # if there is a "content" key contained within the response dictionary
                # Concatenate the strings from the two dictionaries into the responseDictionary
                # This allows all the string chunks to be in one place
                value = response["content"]
                ResponseDict["content"] += value

        resultDict.update(ResponseDict) # concatenate the response dictionary into the resulting dictionary to create the final product

        self.history.append(resultDict) # save the resulting message dictionary to history

        # print(self.history) # debug

    # Using overloads here because there should be multiple ways a developer can use this function
    @overload
    def store(self, message: dict[str, str]):
        '''
        Stores a message into chat history. Useful when injecting messages to add context.

        This function takes in one parameter:
            `message`: dictionary[keyType: string, valueType: string] - the message to be added.
        '''
        ...

    @overload
    def store(self, message: str, *, role="user"):
        '''
        Constructs a message string and stores it into chat history. Useful when injecting messages to add context.

        This function takes in one required parameter and one optional parameter:
            `message`: string - the message to be added.
            `role`: Optional[string] - The role of the message ("user", or "assistant")
        '''
        ...

    def store(self, message: dict[str, str] | str, *, role="user"):
        if isinstance(message, dict): # if the message is a dictionary
            self.chat["messages"].append(message) # store the message

        elif isinstance(message, str): # if the message is a string
            if role in ("user", "assistant"): # if the role is either "user" or "assistant"
                messageDict = {"role": role, "content": message} # construct the message dictionary
                self.chat["messages"].append(messageDict) # store the message
            else: # if the role is anything but "user" or "assistant"
                print(f"Role must be either \"user\" or \"assistant\". You entered {role}.") # print an error message

    # Using overloads here because there should be multiple ways a developer can use this function
    @overload
    def storeAt(self, index, message: dict[str, str]):
        '''
        Stores a message into chat history. Useful when injecting messages to add context.

        This function takes in one parameter:
            `message`: dictionary[keyType: string, valueType: string] - the message to be added.
            `index`: Optional[int] - where in the history the message should be added
        '''
        ...

    @overload
    def storeAt(self, index, message: str, role="user"):
        '''
        Constructs a message string and stores it into chat history. Useful when injecting messages to add context.

        This function takes in one required parameter and one optional parameter:
            `message`: string - the message to be added.
            `index`: Optional[int] - where in the history the message should be added
            `role`: Optional[string] - The role of the message ("user", or "assistant")
        '''
        ...

    def storeAt(self, index, message: dict[str, str] | str, role="user"):
        if isinstance(message, dict): # if the message is a dictionary
            self.chat["messages"].insert(index - 1, message) # insert the message at the position specified

        elif isinstance(message, str): # if the message is a string
            if role in ("user", "assistant"): # if the string is either "user" or "assistant"
                messageDict = {"role": role, "content": message} # construct the message dictionary
                self.chat["messages"].insert(index - 1, messageDict) # insert the message at the position specified
            else: # if the string is anything but "user" or "assistant"
                print(f"Role must be either \"user\" or \"assistant\". You entered {role}.") # print an error

    @overload
    def modify(self, index, newMessage: dict[str, str]):
        '''
        Modifies a message stored in the chat history by using its index to grab it

        This function takes in two required parameters:
            `index`: int - where in the history the message should be added
            `message`: dict[str, str] - the message to be added.
        '''
        ...
    
    @overload
    def modify(self, index, newMessage: str, role=""):
        '''
        Constructs a message dictionary and uses that and the index to modify a message stored in the chat history

        This function takes in two required parameters and one optional parameter:
            `index`: int - where in the history the message should be added
            `message`: dict[str, str] - the message to be added.
            `role`: Optional[string] - The role of the message ("user", or "assistant")
            
        '''
        ...
    
    def modify(self, index, newMessage: dict[str, str] | str, role=""):
        MAX_INDEX = len(self.chat["messages"]) # the amount of messages in the chat - a constant variable
        RESTRICTED_NUMS = [1, (MAX_INDEX * -1) - 1] # These are the indexes of the AI instructions that shouldn't be modified - a constant variable

        if isinstance(newMessage, dict):
            if index > MAX_INDEX: # if the index is more than the amount of messages in the chat
                print(f"The chat history is not more than {MAX_INDEX} messages long!")
            else:
                for i, dicts in enumerate(self.chat["messages"]): # enumerate through the dictionaries to get the dictionary and the index
                    if i == index: # if i equals the index input by the user
                        if i not in RESTRICTED_NUMS:
                            self.chat["messages"].remove(dicts) # remove the dictionary at that location
                            self.chat["messages"].insert(index, newMessage) # insert the new message
                        else:
                            print("The index you have chosen is the AI instructions. You cannot delete this index. Choose another index")

        elif isinstance(newMessage, str):
            if index > MAX_INDEX: # if the index is more than the amount of messages in the chat
                print(f"The chat history is not more than {MAX_INDEX} messages long!")
            else:
                for i, dicts in enumerate(self.chat["messages"]): # enumerate through the dictionaries to get the dictionary and the index
                    if i == index: # if i equals the index input by the user
                        if i not in RESTRICTED_NUMS: # if the index is not restricted
                            if role == "": # if the role string has not been set
                                temp = self.chat["messages"].pop(i) # remove the dictionary at that location and grab a temporary version of it
                                messageDict = {"role": temp["role"], "content": newMessage} # construct the message dictionary
                                self.chat["messages"].insert(index, messageDict) # insert the new message
                            else: # if the role string has been set
                                self.chat["messages"].remove(dicts) # remove the dictionary at that location and grab a temporary version of it
                                messageDict = {"role": role, "content": newMessage} # construct the message dictionary
                                self.chat["messages"].insert(index, messageDict) # insert the new message
                        else:
                            print("The index you have chosen is the AI instructions. You cannot delete this index. Choose another index")

    def clear(self):
        '''
        clears the chat history so the user can start from scratch conversing with the AI
        '''
        self.chat["messages"].clear() #Clear the list

        self.chat = { #Re-add the system prompt (this should never be deleted)
            "messages": [{"role": "system", "content": self.systemPrompt}]
        }

    def delete(self, index):
        '''
        Deletes a specific message from message history by finding it's index. 
        This function takes one parameter:
            `index` - the specific message to delete from chat history
        
        indexes 0, 1, and the respective negative indexes will be restricted for protection of the AI instructions

        In the case of -1, the index will work like normal in deleting the most recent response
        '''
        MAX_INDEX = len(self.chat["messages"]) # the amount of messages in the chat - a constant variable
        RESTRICTED_NUMS = [0, 1, (MAX_INDEX * -1) - 2, (MAX_INDEX * -1) - 1] # These are the indexes of the AI instructions that shouldn't be deleted - a constant variable

        if index > MAX_INDEX: # if the index is more than the amount of messages in the chat
            print(f"The chat history is not more than {MAX_INDEX} messages long!")
        else:
            for i, dicts in enumerate(self.chat["messages"]): # enumerate through the dictionaries to get the dictionary and the index
                if i == index: # if i equals the index input by the user plus the offset
                    if i not in RESTRICTED_NUMS:
                        self.chat["messages"].remove(dicts) # remove the dictionary at that location
                    else:
                        print("The index you have chosen is the AI instructions. You cannot delete this index. Choose another index")

    #----------------------------- Prompt Modifiers -----------------------------#

    def setSystem(self, systemPrompt):
        '''
        sets the system prompt
        '''
        self.systemPrompt = systemPrompt

    def setPrompt(self, prompt):
        '''
        sets the user prompt
        '''
        self.prompt = prompt

class InstructionsManager:
    '''
    A class for managing and changing the AI base instructions (not specific prompts)
    '''
    def __init__(self, subject, gradeLevel):
        self.rules = [
            {"Rule": "Don't generate content that isn't based on the subject", "Sub Rules": []}, 
            {"Rule": "Don't generate content that's not at the grade level", "Sub Rules": []}, 
            {"Rule": "Don't generate any content that isn't relevant", "Sub Rules": ["a. For example, Alien Planets have nothing to do with Health. Pulleys and Levers have nothing to do with Programming"]}, 
            {"Rule": "Tell the user what rule an invalid prompt violates", "Sub Rules": ["a. for example if the user violates rule one, say: \"I'm sorry, but I am not allowed to generate any content that isn't based on your selected subject. Please change the topic or change your subject\""]}
        ]

        self.instructions = dedent(f"""\
            Subject: {subject}
            Grade Level: {gradeLevel}
            Rules: {{
                1. {self.rules[0]["Rule"]}
                2. {self.rules[1]["Rule"]}
                3. {self.rules[2]["Rule"]}
                    a. {self.rules[2]["Sub Rules"][0]}
                4. {self.rules[3]["Rule"]}
                    a. {self.rules[3]["Sub Rules"][0]}
            }}
            ENFORCE THESE RULES
            Example prompt: generate a multiple choice quiz about math at the college level about how speakers use ultrasonic wavelengths to transmit sound throughout the air.
            Example output: Here's a multiple choice quiz about how speakers use ultrasonic wavelengths to transmit sound throughout the air as it relates to math.
            
            Do you understand these rules?""")
        
    def addRule(self, rule, *subrules):
        '''
        Adds a single rule and a variable number of subrules to the rules list.
        '''
        self.rules.append({"Rule": rule, "Sub Rules": list(subrules)})

    def removeRule(self, index):
        '''
        Removes a rule and all of its subrules

        Supports counting numbers if the number is not negative. If you want to delete rule 1, simply call
        >>> removeRule(1)
        
        However, if you want to remove rule 8 in a 1-10 ruleset using negative numbers, you'd still have to do it like this:
        >>> removeRule(-3)
        '''
        if index < 0: # check for a negative number
            self.rules.reverse() # reverse the list to represent negative indexing

            for i, rule in enumerate(self.rules):
                if -i - 1 == index: # if the negative of the index matches the negative index from the parameter
                    self.rules.remove(rule) # remove the rule at that index
                    self.rules.reverse() # reverse the list again to bring it back to its normal state

        else: # if the index is positive
            for i, rule in enumerate(self.rules): 
                if i == index - 1: # if the index matches the natural number 
                    self.rules.remove(rule) # remove the rule

    def modifyInitial(self, subject, gradeLevel):
        '''
        Modifies the initial instruction set with a new subject and gradeLevel. It's very limited, but it can still be useful.

        Use this function in conjunction with the `modify()` method in the `ModelBase` class to force change an initial state
        '''
        self.instructions = dedent(f"""\
            Subject: {subject}
            Grade Level: {gradeLevel}
            Rules: {{
                1. {self.rules[0]["Rule"]}
                2. {self.rules[1]["Rule"]}
                3. {self.rules[2]["Rule"]}
                    a. {self.rules[2]["Sub Rules"][0]}
                4. {self.rules[3]["Rule"]}
                    a. {self.rules[3]["Sub Rules"][0]}
            }}
            ENFORCE THESE RULES
            Example prompt: generate a multiple choice quiz about math at the college level about how speakers use ultrasonic wavelengths to transmit sound throughout the air.
            Example output: Here's a multiple choice quiz about how speakers use ultrasonic wavelengths to transmit sound throughout the air as it relates to math.
            
            Do you understand these rules?""")

    def getRulesContext(self):
        '''
        Gets the rules as an injection-ready formatted context string
        '''
        return f"Remember the rules:\n{self.getRules()}\n\n"
    
    def getRules(self):
        '''
        Formats the rules as a string and returns them
        '''
        ruleListStr = ""
        
        for dict in self.rules: # get the rule dictionaries
            # save the values
            rule = dict["Rule"]
            subRules = dict["Sub Rules"]
            
            if not subRules: # if there are no subrules for the current rule
                ruleListStr += f"1. {rule}\n"
            else: # if the current rule has one or more sub rules
                ruleListStr += f"1. {rule}\n"

                for subRule in subRules: 
                    ruleListStr += "\t" # add a tab to denote a sub-rule
                    ruleListStr += f"{subRule}\n" # add the subrule and a newline

        # compile the formatted string
        resultStr = dedent(f"""\
            Rules: {{
                {ruleListStr}
            }}
        """)
        
        return resultStr

class TutorGPT(ModelBase):
    def __init__(self, subject, gradeLevel, mode="learn"):
        prompt = f"Hello, I am a student coming to you for help. I am in {gradeLevel} and I'm studying {subject} today"
        systemPrompt = f"You are a professional {gradeLevel} instructor who specializes in teaching in the {subject} area of study"
        self.instructionsMgr = InstructionsManager(subject, gradeLevel)

        self.mode = mode
        self.subject = subject
        self.gradeLevel = gradeLevel
        self.quizConfiguration = ["", "out", "out"]

        super().__init__(prompt, systemPrompt)

        self.storeAt(2, {"role": "user", "content": self.instructionsMgr.instructions})
        self.storeAt(3, "I understand. I will make sure that I enforce all four rules in the way you described.", "assistant")
    #----------------------------- TutorGPT Setup -----------------------------#

    def learnMode(self, topic):
        '''
        Sets the topic for modes learn and quiz. 
        
        For learn, the AI is asked if it can help the user learn about a topic.
        
        For quiz, the AI is asked to create a practice quiz based on the topic.

        This function takes in one parameter:
            topic - the topic of discussion
        '''
        # Make sure we are in the right mode
        if self.mode == "learn":
            self.prompt = f"{self.instructionsMgr.getRulesContext()}Question: Can you help me learn about {topic}?" # Change the prompt to fit the user's requirements
        elif self.mode == "quiz":
            print("Creating a quiz based on a topic meant for learning is not helpful to the student, use quizMode()")
        else:
            if self.mode == "expand":
                print("Add topic reqiures a topic name, not a topic description. Use excerptMode()")
            else:
                print(f"Mode {self.mode} not compatible with learnMode()")

    def quizMode(self, topic):
        '''
        Compiles the quiz prompt for the AI
        '''

        if self.mode == "expand":
            print("Add topic reqiures a topic name, not a topic description. Use excerptMode()")
        elif self.mode == "learn":
            print("Excerpt mode is for excerpts taken from textbooks or other source material that the student needs help understanding, not for learning about a topic. Use learnMode()")
        elif self.mode == "quiz":
            self.prompt = f"{self.instructionsMgr.getRulesContext()}Question: Can you create a practice quiz about {topic} with{self.quizConfiguration[0]} Multiple Choice questions, with{self.quizConfiguration[1]} Multiple Answer questions, and with{self.quizConfiguration[2]} Short Answer questions? Give the response in JSON format as a list of dictionaries, with keys for question, choices, answer. Put the choices key in the following format: {{A: <text for choice A>, B: <text for choice B>, C: <text for choice C>, D: <text for choice D>}}, create the quiz for a {self.gradeLevel} student about {self.subject}. In particular, focus on {topic}. Make the quiz 10 questions long with 4 choices each." # Change the prompt to fit the user's requirements

    def excerptMode(self, excerpt):
        '''
        Sets the excerpt of text for expansion modes where the AI is tasked with expanding on a piece of text to provide more context.

        This is designed to help the user understand a part of the textbook that may either by cryptic, or uses too much technical jargon.

        This function takes in one parameter:
            excerpt - the excerpt of text the user will provide to the AI
        '''
        if self.mode == "expand":
            self.prompt = f"{self.instructionsMgr.getRulesContext()}Question: Can you help me understand what this means: \"{excerpt}\"?"
        elif self.mode == "learn":
            print("Excerpt mode is for excerpts taken from textbooks or other source material that the student needs help understanding, not for learning about a topic. Use learnMode()")
        elif self.mode == "quiz":
            print("creating a quiz based on an excerpt of text taken from a textbook is not helpful to the student, use quizMode()")

    #----------------------------- Attribute Modifiers -----------------------------#

    def setMode(self, mode):
        self.mode = mode

    def setSubject(self, subject):
        self.subject = subject

    def setGradeLevel(self, gradeLevel):
        self.gradeLevel = gradeLevel

    def setQuizConfiguration(self, configuration):
        self.quizConfiguration = configuration

# This part of the code is used solely for testing purposes.
# It won't run when app.py is executed because __name__ will only equal "__main__" if this python file is the main execution file
if __name__ == "__main__":
    instructions = """\
    Subject:
    Grade Level:
    Rules: {
        1. Don't generate a quiz that isn't based on the subject
        2. Don't generate a quiz that's not at the grade level
        3. Don't generate any content that isn't relevant 
            a. For example, Alien Planets have nothing to do with Health. Pulleys and Levers have nothing to do with Programming
        4. Tell the user what rule an invalid prompt violates 
            a. for example if the user violates rule one, say: "I'm sorry, but I am not allowed to generate any content that isn't based on your selected subject. Please change the topic or change your subject"
    }
    ENFORCE THESE RULES
    Example prompt: generate a multiple choice quiz about math at the college level about how speakers use ultrasonic wavelengths to transmit sound throughout the air.
    Example output: Here's a multiple choice quiz about how speakers use ultrasonic wavelengths to transmit sound throughout the air as it relates to math.

    Do you understand these rules?"""
    modifiedInstructions = dedent(instructions)
    print(modifiedInstructions)