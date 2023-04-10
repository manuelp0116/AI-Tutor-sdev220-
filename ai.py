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

    def complete(self, temperature=0.8, top_p=1):
        '''
        Get's a response from the AI according to the question layed out in the prompt
        This function takes in two optional parameters:
            temperature: the randomness of the output - Set at 0.8 by default
            top_p: controls outputs via nucleus sampling. 0.5 means half of all likelyhood-weighed options are considered - set at 1 by default
        '''
        if self.history: #check if there are messages in the history
            self.store(self.history[-1])

        msg = {"role": "user", "content": self.prompt} # Parse the user prompt

        self.chat["messages"].append(msg) #append the dictionary to the inner list in chat

        # Get the AI response
        completion = self.api.create(model="gpt-4", messages=self.chat["messages"], temperature=temperature, top_p=top_p)

        # print(completion.choices[0].message)
        self.history.append(completion.choices[0].message) #Add the AI's response to message history
        # print("\n", self.history)

        # print("\n", completion.choices[0].message.content)
        return completion.choices[0].message.content

    def clear(self):
        '''
        clears the chat history so the user can start from scratch conversing with the AI
        '''
        self.chat["messages"].clear() #Clear the list

        self.chat = { #Re-add the system prompt (this should never be deleted)
            "messages": [{"role": "system", "content": self.systemPrompt}]
        }

    def store(self, messageDict):
        '''
        Stores a message into chat history. Useful when injecting messages to add context.
        '''
        self.chat["messages"].append(messageDict)

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
    def __init__(self, systemPrompt, mode, subject, gradeLevel):
        self.prompt = f"Hello, I am a student coming to you for help. I am in {gradeLevel} and I'm studying {subject} today"
        super().__init__(self.prompt, systemPrompt)

        self.mode = mode
        self.subject = subject
        self.gradeLevel = gradeLevel

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
            self.prompt = f"Can you create a practice quiz about {topic}?" # Change the prompt to fit the user's requirements
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

    def setMode(self, mode):
        self.mode = mode

    def setSubject(self, subject):
        self.subject = subject

    def setGradeLevel(self, gradeLevel):
        self.gradeLevel = gradeLevel
