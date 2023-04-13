"""
Best prompt to get consistently structured response:
In JSON format, with keys for question, choices, answer: create a multiple choice quiz for a {LEARNING LEVEL} student about {TOPIC}. Make the quiz {# OF QUESTIONS} questions long with 4 choices each. Make the choices key in a single dictionary format with the keys capitalized and the JSON object a list of dictionaries
"""


import json

quiz = {}

# for testing, just copied and pasted a response I got
response_from_AI = [
    'Here is an example JSON object that contains a multiple choice quiz about horses:\n\n```\n[\n  {\n    "question": "What is the gestation period of a horse?",\n    "choices": {\n      "A": "4 months",\n      "B": "6 months",\n      "C": "9 months",\n      "D": "12 months"\n    },\n    "answer": "C"\n  },\n  {\n    "question": "Which of the following is not a horse breed?",\n    "choices": {\n      "A": "Thoroughbred",\n      "B": "Quarter Horse",\n      "C": "Arabian",\n      "D": "Bengal"\n    },\n    "answer": "D"\n  },\n  {\n    "question": "What is the name of the fastest horse on record?",\n    "choices": {\n      "A": "Secretariat",\n      "B": "Man o\' War",\n      "C": "Winning Colors",\n      "D": "Black Caviar"\n    },\n    "answer": "A"\n  }\n]\n```\n\nIn this example, there are three questions about horses, each with four possible choices. The correct answer for each question is indicated by the value of the "answer" key, which corresponds to the key of the correct choice in the "choices" dictionary.\n\nFeel free to modify the questions, choices, and answers to suit the needs of your intermediate students.'
]

resp_str = response_from_AI[
    0
]  # gets the string version of the response (since it returns a list with one entry by default)
resp_split = resp_str.split(
    "```"
)  # splits string to isolate the code block as the second item in a list (new list is [fluff text, JSON CODE BLOCK WE WANT, more fluff])

resp_list = json.loads(
    resp_split[1].strip()
)  # converts JSON code block into python list


# putting the quiz info into a dictionary
for i in range(len(resp_list)):
    quiz[f"q{i+1}"] = resp_list[i]


# print/display quiz
for j in range(len(quiz)):
    print(
        f"""
        {quiz[f"q{j+1}"]["question"]}
        A) {quiz[f"q{j+1}"]["choices"]["A"]}
        B) {quiz[f"q{j+1}"]["choices"]["B"]}
        C) {quiz[f"q{j+1}"]["choices"]["C"]}
        D) {quiz[f"q{j+1}"]["choices"]["D"]}
        """
    )
