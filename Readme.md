# BrainSpark AI-Tutor

## to run it run ptyhon gui.py

## Description 
This app powered by openAI Api was made with the intend to help students with their learning, this app has two main modes, chat, and quiz or test me; chat will allow 
the user to chat with an AI made and trained specifically to help answering and expanding on school related topic, the user will be able to get a more personaliazed chat
selecting the grade, and subject from the dropdowns, this will make the AI an expert on the topic. The quiz function will let the user get a quiz made in the spot from the selection of grade, subject
and the topic t hat the student wants to study for.


   # AI
   we are using openAI API for our project, this way we can se the capabilities of chatgpt3.5 turbo to answer all the questions the user has, and  thanks to this we are able to create a json file output to create personalized AI generated quizzes.

   ## `retryConnection` Decorator

   The `retryConnection` decorator is used to handle retries for functions that may encounter API connection errors. It ensures that the decorated function is called again if there's a connection error, up to a specified maximum number of retries. This decorator is especially useful when working with external APIs that may experience occasional connection issues.

   - `max_retries`: The maximum number of retries allowed before giving up and raising an error.

   Example usage:

   ```python
   @retryConnection(max_retries=5)
   def some_api_call():
      ...
   ```

   When used, the `retryConnection` decorator wraps the function and catches any API connection errors. If an error is encountered, it will retry the function call up to `max_retries` times. If the maximum number of retries is reached, the decorator will raise an error.

   # `ModelBase` Class

   The `ModelBase` class is the base class for creating different AI models within Brain Spark. It provides a set of common methods and attributes for managing chat history, storing messages, and interacting with the AI.

   ## Methods

   ### `__init__(self, prompt, systemPrompt)`

   The constructor for the `ModelBase` class initializes the object with a given prompt and system prompt.

   - `prompt`: The initial prompt for the AI to start with. This sets the context for the AI's responses.
   - `systemPrompt`: The system prompt that sets the behavior of the AI. This can be used to guide the AI in generating specific types of responses.

   The `__init__` method initializes the `ModelBase` object with the provided `prompt` and `systemPrompt`. These values are used to set the context and behavior of the AI when generating responses.

   ### `complete(self, temperature=0.8, top_p=1, stream=True)`

   This method sends a request to the AI to generate a response based on the given `prompt` and `systemPrompt`. It takes three optional parameters:

   - `temperature`: Controls the randomness of the AI's output (default is 0.8). Higher values result in more random responses, while lower values make the output more focused and deterministic.
   - `top_p`: Controls the AI's output via nucleus sampling (default is 1). This parameter helps in filtering out low-probability responses.
   - `stream`: A boolean value indicating whether the output should be streamed as a generator (default is True). If set to True, the method returns a generator object that yields chunks of the AI's output as they become available.

   The `complete` method sends a request to the AI with the current `prompt` and `systemPrompt` and returns a generator object containing the AI's response. The optional parameters `temperature`, `top_p`, and `stream` can be used to fine-tune the AI's output.

   ### `logCompletion(self, messages)`

   This method takes a list of messages, constructs a message dictionary, and stores it into the chat history. It takes one parameter:

   - `messages`: A list of messages (strings) to be evaluated and stored.

   The `logCompletion` method processes the list of `messages` and constructs a message dictionary for each message. The role of the message (either "user" or "assistant") is determined by the first chunk in the list. The message dictionary is then stored in the chat history.

   ### `store(self, message: dict[str, str])`

   This method stores a message dictionary into the chat history. It takes one parameter:

   - `message`: A dictionary containing the message to be added. The dictionary should have a "role" key (either "user" or "assistant") and a "content" key (the actual message text).

   The `store` method takes a `message` in the form of a dictionary and adds it to the chat history. The `message` dictionary should contain the role and content of the message.

   ### `store(self, message: str, *, role="user")`

   This method constructs a message dictionary and stores it into the chat history. It takes one required parameter and one optional parameter:

   - `message`: The message to be added (a string).
   - `role`: The role of the message ("user" or "assistant", default is "user").

   The `store` method creates a message dictionary with the given `message` and `role` and adds it to the chat history.

   ### `storeAt(self, index, message: dict[str, str])`

   This method stores a message dictionary into the chat history at a specific index. It takes two parameters:

   - `index`: The index at which the message should be added.
   - `message`: A dictionary containing the message to be added. The dictionary should have a "role" key (either "user" or "assistant") and a "content" key (the actual message text).

   The `storeAt` method inserts a `message` dictionary at the specified `index` in the chat history.

   ### `storeAt(self, index, message: str, role="user")`

   This method constructs a message dictionary and stores it into the chat history at a specific index. It takes two required parameters and one optional parameter:

   - `index`: The index at which the message should be added.
   - `message`: The message to be added (a string).
   - `role`: The role of the message ("user" or "assistant", default is "user").

   The `storeAt` method creates a message dictionary with the given `message` and `role` and inserts it at the specified `index` in the chat history.

   ### `modify(self, index, newMessage: dict[str, str])`

   Modifies a message stored in the chat history by using its index to grab it.

   - `index`: int - The index of the message in the chat history.
   - `newMessage`: dict[str, str] - The new message dictionary to replace the old message.

   ### `modify(self, index, newMessage: str, role="")`

   Constructs a message dictionary and uses that and the index to modify a message stored in the chat history.

   - `index`: int - The index of the message in the chat history.
   - `newMessage`: str - The new message content to replace the old message content.
   - `role`: Optional[string] - The role of the message ("user", or "assistant"). If not provided, the role of the original message will be used.

   ### `delete(self, index)`

   This method deletes a specific message from the chat history by finding its index. It takes one parameter:

   - `index`: The index of the message to delete from the chat history.

   The `delete` method removes a message from the chat history at the specified `index`. Note that some indexes (0, 1, and their respective negative values) are restricted to protect the AI instructions.

   ### `setSystem(self, systemPrompt)`

   This method sets the system prompt for the AI. It takes one parameter:

   - `systemPrompt`: The new system prompt. This can be used to guide the AI in generating specific types of responses.

   The `setSystem` method updates the AI's `systemPrompt`, which influences the AI's behavior when generating responses.

   ### `setPrompt(self, prompt)`

   This method sets the prompt for the AI. It takes one parameter:

   - `prompt`: The new prompt. This sets the context for the AI's responses.

   The `setPrompt` method updates the AI's `prompt`, which provides context for the AI's responses.

   # `TutorGPT` Class

   The `TutorGPT` class is a subclass of `ModelBase` and provides additional methods for managing subjects, grade levels, and modes for the AI tutor.

   ## Methods

   ### `__init__(self, subject, gradeLevel, mode="learn")`

   The constructor for the `TutorGPT` class initializes the object with a given subject, grade level, and mode.

   - `subject`: The subject for the AI tutor to focus on (e.g., "math", "history").
   - `gradeLevel`: The grade level for the AI tutor to target (e.g., "3rd grade", "high school").
   - `mode`: The mode of operation for the AI tutor (default is "learn"). Other modes include "quiz" and "expand".

   The `__init__` method initializes the `TutorGPT` object with the provided `subject`, `gradeLevel`, and `mode`. These values are used to customize the AI tutor's behavior and focus.

   ### `addTopic(self, topic)`

   This method sets the topic for the AI tutor in learn and quiz modes. It takes one parameter:

   - `topic`: The topic of discussion (e.g., "fractions", "World War I").

   The `addTopic` method sets the AI tutor's topic, which helps direct the AI's focus when generating responses in learn and quiz modes.

   ### `addExcerpt(self, excerpt)`

   This method sets an excerpt of text for the AI tutor to expand on, providing more context. It takes one parameter:

   - `excerpt`: The excerpt of text for the AI to expand upon (e.g., a paragraph from a textbook or an article).

   The `addExcerpt` method sets the AI tutor's excerpt, which is used when the AI is tasked with expanding on a piece of text to provide more context. This can help users understand parts of a textbook or article that may be cryptic or use too much technical jargon.

   ### `setMode(self, mode)`

   This method sets the mode of operation for the AI tutor. It takes one parameter:

   - `mode`: The new mode of operation (e.g., "learn", "quiz", "expand").

   The `setMode` method updates the AI tutor's mode of operation. This influences the type of responses generated by the AI (e.g., learning material, quizzes, or expanded explanations).

   ### `setSubject(self, subject)`

   This method sets the subject for the AI tutor. It takes one parameter:

   - `subject`: The new subject (e.g., "math", "history").

   The `setSubject` method updates the AI tutor's subject, which helps direct the AI's focus when generating responses.

   ### `setGradeLevel(self, gradeLevel)`

   This method sets the grade level for the AI tutor. It takes one parameter:

   - `gradeLevel`: The new grade level (e.g., "3rd grade", "high school").

   The `setGradeLevel` method updates the AI tutor's targeted grade level. This helps the AI generate content that is appropriate for the specified grade level, ensuring that the material is neither too simple nor too advanced for the user.

   ### `setQuizConfiguration(self, configuration)`

   This method sets the quiz configuration settings for the AI tutor. It takes one parameter:

   - `configuration`: The new quiz configuration settings (e.g., number of questions, difficulty level, question format).

   The `setQuizConfiguration` method updates the AI tutor's quiz configuration settings, allowing you to customize the quizzes generated by the AI. This is particularly useful when you want to create practice quizzes with specific requirements, such as a certain number of questions or a particular difficulty level.

   # InstructionsManager

   A class for managing and changing the AI base instructions (not specific prompts).

   ## Methods

   ### `__init__(self, subject, gradeLevel)`

   Initializes the InstructionsManager class with a subject and gradeLevel.

   - `subject`: str - The subject for the AI instructions.
   - `gradeLevel`: str - The grade level for the AI instructions.

   ### `addRule(self, rule, *subrules)`

   Adds a single rule and a variable number of subrules to the rules list.

   - `rule`: str - The main rule to be added.
   - `*subrules`: str - A list of subrules to be added under the main rule.

   ### `removeRule(self, index)`

   Removes a rule and all of its subrules.

   - `index`: int - The index of the rule to be removed.

   ### `modifyInitial(self, subject, gradeLevel)`

   Modifies the initial instruction set with a new subject and gradeLevel.

   - `subject`: str - The new subject for the AI instructions.
   - `gradeLevel`: str - The new grade level for the AI instructions.

   ### `getRulesContext(self)`

   Gets the rules as an injection-ready formatted context string.

   ### `getRules(self)`

   Formats the rules as a string and returns them.

   # Storage solutions
   this class deal with storage for our different files, chat and quiz, quizzes are stored in json file, and chat would be stored in a txt file. Tiem cosntrains made us not being able to use this class, and storage solutions is not in use at the moment. thefuntions on this class are:
   
   * ### housekeep: 
      * functionn checks for directory name with os and creates directory path to save chat and 

   * ### saveQuiz:
      * this function will save a json file with the quiz information for

   

## Contributing

 ### github repo: 
    https://github.com/manuelp0116/AI-Tutor-sdev220-

 ### contributors: 
    Manuel Paredes
    Braden Shrum
    Chloe Moore
    Charles Philips
 

## prerequisites

   ### install 
   * customTkinter
   * PIL
   *tkinter





