"""
Best prompt to get consistently structured response:
In JSON format, with keys for question, choices, answer: create a multiple choice quiz for a {LEARNING LEVEL} student about {TOPIC}. Make the quiz {# OF QUESTIONS} questions long with 4 choices each. Make the choices key in a single dictionary format with the keys capitalized and the JSON object a list of dictionaries
"""

import json
from dataclasses import dataclass

# create class for questions
@dataclass
class Question:
    text: str
    choices: dict
    answer: str
    student_answer: str


def create_quiz(response: list):
    """Takes Ai response and returns a list of dictionaries, with each dictionary being a question of the quiz"""

    # parse AI response
    resp_string = response[0]
    resp_split = resp_string.split("```")
    resp_list = json.loads(resp_split[1].strip())

    # initiate quiz dicitonary object
    quiz = {}

    # enter info from parsed json list into the quiz dictionary
    for i in range(len(resp_list)):
        quiz[f"question{i}"] = Question(
            text=resp_list[i]["question"],
            choices=resp_list[i]["choices"],
            answer=resp_list[i]["answer"],
            student_answer="",
            )

    return quiz


### TESTING STUFF BELOW

# for testing, I just copied and pasted a response I got
response_from_AI = [
    'Here is an example JSON object that contains a multiple choice quiz about horses:\n\n```\n[\n  {\n    "question": "What is the gestation period of a horse?",\n    "choices": {\n      "A": "4 months",\n      "B": "6 months",\n      "C": "9 months",\n      "D": "12 months"\n    },\n    "answer": "C"\n  },\n  {\n    "question": "Which of the following is not a horse breed?",\n    "choices": {\n      "A": "Thoroughbred",\n      "B": "Quarter Horse",\n      "C": "Arabian",\n      "D": "Bengal"\n    },\n    "answer": "D"\n  },\n  {\n    "question": "What is the name of the fastest horse on record?",\n    "choices": {\n      "A": "Secretariat",\n      "B": "Man o\' War",\n      "C": "Winning Colors",\n      "D": "Black Caviar"\n    },\n    "answer": "A"\n  }\n]\n```\n\nIn this example, there are three questions about horses, each with four possible choices. The correct answer for each question is indicated by the value of the "answer" key, which corresponds to the key of the correct choice in the "choices" dictionary.\n\nFeel free to modify the questions, choices, and answers to suit the needs of your intermediate students.'
]


quiz = create_quiz(response_from_AI)


# print quiz to check input
for question in quiz.values():
    print(question.text)
    for letter, choice in question.choices.items():
        print(f"{letter}) {choice}")
    print("\n")
