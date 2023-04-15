import openai
# import whisper

openai.api_key = "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"

class ModelBase():
    def __init__(self, prompt, systemPrompt):
        self.api = openai.ChatCompletion()
        self.prompt = prompt
        self.systemPrompt = systemPrompt
        self.history = []

        self.chat = { #initialize the chat with a system prompt
            "messages": [
                {"role": "system", "content": systemPrompt},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": "Understood! How can I help you?"}
            ]
        }

    #----------------------------- Main Method -----------------------------#

    def complete(self, temperature=0.8, top_p=1):
        '''
        Get's a response from the AI according to the question layed out in the prompt
        This function takes in two optional parameters:
            temperature: the randomness of the output - Set at 0.8 by default
            top_p: controls outputs via nucleus sampling. 0.5 means half of all likelyhood-weighed options are considered - set at 1 by default

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

        The list input contains chunks of messages from the AI, with the first chunk being the role of the output.
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

    def store(self, messageDict):
        '''
        Stores a message into chat history. Useful when injecting messages to add context.
        '''
        self.chat["messages"].append(messageDict)

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
        Deletes a specific message from message history by finding it's index
        '''
        MAX_INDEX = len(self.chat["messages"])

        if index > MAX_INDEX:
            print(f"The chat history is not more than {MAX_INDEX} messages long!")
        elif index < 0:
            print(f"There cannot be negative messages! Use a positive number.")
        else:
            for i, dicts in enumerate(self.chat["messages"]):
                if i == index:
                    self.chat["messages"].remove(dicts)

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

        self.mode = mode
        self.subject = subject
        self.gradeLevel = gradeLevel
        self.quizConfiguration = ["", "out", "out"]

        super().__init__(prompt, systemPrompt)

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
            self.prompt = f"Can you help me learn about {topic}?" # Change the prompt to fit the user's requirements
        elif self.mode == "quiz":
            self.prompt = f"Can you create a practice quiz about {topic} with{self.quizConfiguration[0]} Multiple Choice questions, with{self.quizConfiguration[1]} Multiple Answer questions, and with{self.quizConfiguration[2]} Short Answer questions?" # Change the prompt to fit the user's requirements
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
            self.prompt = f"Can you help me understand what this means: \"{excerpt}\"?"
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
