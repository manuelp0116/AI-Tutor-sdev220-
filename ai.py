import openai # AI outputs
from openai.error import APIConnectionError # Connection Error Handling
# import whisper

from typing import overload # function overloading
from textwrap import dedent # To make docstrings look nicer in the editor

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
                        return None
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
    def complete(self, temperature=0.8, top_p=1):
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
        completion = self.api.create(model="gpt-4", messages=self.chat["messages"], temperature=temperature, top_p=top_p, stream=True)

        # print(completion.choices[0].message)
        # print("\n", self.history)
        # print("\n", completion.choices[0].message.content)

        collectedMessages = []
        for chunk in completion:
            collectedMessages.append(chunk["choices"][0]["delta"])
            if "content" in chunk["choices"][0]["delta"]:
                yield chunk["choices"][0]["delta"]["content"]
                
        self.logCompletion(collectedMessages) #Add the AI's response to message history

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
                print(f"Role must be either \"user\" or \"assistant\". You entered {role}.") # print an error message

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
                        print("The index you have chosen is the AI isntructions. You cannot delete this index. Choose another index")

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

class TutorGPT(ModelBase):
    def __init__(self, subject, gradeLevel, mode="learn"):
        prompt = f"Hello, I am a student coming to you for help. I am in {gradeLevel} and I'm studying {subject} today"
        systemPrompt = f"You are a professional {gradeLevel} instructor who specializes in teaching in the {subject} area of study"
        self.instructions = dedent(f"""\
            Subject: {subject}
            Grade Level: {gradeLevel}
            Rules: {{
                1. Don't generate content that isn't based on the subject
                2. Don't generate content that's not at the grade level
                3. Don't generate any content that isn't relevant 
                    a. For example, Alien Planets have nothing to do with Health. Pulleys and Levers have nothing to do with Programming
                4. Tell the user what rule an invalid prompt violates 
                    a. for example if the user violates rule one, say: "I'm sorry, but I am not allowed to generate any content that isn't based on your selected subject. Please change the topic or change your subject"
            }}
            ENFORCE THESE RULES
            Example prompt: generate a multiple choice quiz about math at the college level about how speakers use ultrasonic wavelengths to transmit sound throughout the air.
            Example output: Here's a multiple choice quiz about how speakers use ultrasonic wavelengths to transmit sound throughout the air as it relates to math.

            Do you understand these rules?""")

        rulesStart = self.instructions.find("Rules:")
        rulesEnd = self.instructions.find("}")

        self.rules = self.instructions[rulesStart:rulesEnd]

        self.mode = mode
        self.subject = subject
        self.gradeLevel = gradeLevel
        self.quizConfiguration = ["", "out", "out"]

        super().__init__(prompt, systemPrompt)

        self.storeAt(2, {"role": "user", "content": self.instructions})
        self.storeAt(3, "I understand. I will make sure that I enforce all four rules in the way you described.", "assistant")
        print(self.chat["messages"])
    #----------------------------- TutorGPT Setup -----------------------------#

    def addTopic(self, topic):
        '''
        Sets the topic for modes learn and quiz. 
        
        For learn, the AI is asked if it can help the user learn about a topic.
        
        For quiz, the AI is asked to create a practice quiz based on the topic.

        This function takes in one parameter:
            topic - the topic of discussion
        '''
        # Make sure we are in the right mode
        if self.mode == "learn":
            self.prompt = f"Remember the rules:\n{self.rules}\n\nQuestion: Can you help me learn about {topic}?" # Change the prompt to fit the user's requirements
        elif self.mode == "quiz":
            self.prompt = f"Remember the rules:\n{self.rules}\n\nQuestion: Can you create a practice quiz about {topic} with{self.quizConfiguration[0]} Multiple Choice questions, with{self.quizConfiguration[1]} Multiple Answer questions, and with{self.quizConfiguration[2]} Short Answer questions?" # Change the prompt to fit the user's requirements
        else:
            if self.mode == "expand":
                print("Add topic reqiures a topic name, not a topic description. Use addExcerpt()")
            else:
                print(f"Mode {self.mode} not compatible with addTopic()")

    def addExcerpt(self, excerpt):
        '''
        Sets the excerpt of text for expansion modes where the AI is tasked with expanding on a piece of text to provide more context.

        This is designed to help the user understand a part of the textbook that may either by cryptic, or uses too much technical jargon.

        This function takes in one parameter:
            excerpt - the excerpt of text the user will provide to the AI
        '''
        if self.mode == "expand":
            self.prompt = f"Remember the rules:\n{self.rules}\n\nQuestion: Can you help me understand what this means: \"{excerpt}\"?"
        elif self.mode == "learn":
            print("Excerpt mode is for excerpts taken from textbooks or other source material that the student needs help understanding, not for learning about a topic. Use addTopic()")
        elif self.mode == "quiz":
            print("creating a quiz based on an excerpt of text taken from a textbook is not helpful to the student, use addTopic()")

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