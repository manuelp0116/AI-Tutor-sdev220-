import json
from dataclasses import dataclass


# create class for questions
@dataclass
class Question:
    text: str
    choices: dict
    answer: str
    student_answer: str
    quiz_type: str


def create_quiz(response: str):
    """
    Takes Ai response as a string and returns quiz as a dictionary of dictionaries, with each subsequent dictionary being a question of the quiz (as a class)

    Returned quiz dictionary is in following format:
        {quizname: {
                question1: Question(), ###questions are an object of our Question class
                question2: Question(),
                ...
                question10: Question()
                }
        }

    Question class is in the following format:
        question#.text = "Text of question#" (eg. "What is the capital of Germany?")
        question#.choices = {
                                "A": "Text of choice A" (eg. "Vancouver")
                                "B": "Text of choice B" (eg. "Madrid")
                                "C": "Text of choice C" (eg. "Zurich")
                                "D": "Text of choice D" (eg. "Berlin")
                            }
        question#.answer = "Letter of the correct answer" (eg. "D")
        question#.student_answer = "Letter of student answer" (eg. "C") ### Default value is a blank string
    """

    # checks if a JSON code block exists in the response, exits function if not
    try:
        split_respose = response.strip().split("```")
        json_list = json.loads(split_respose[1].strip())

    except:
        print(
            "Uh oh! Something went wrong and we couldn't generate your quiz. Please try again."
        )
        exit()

    # initiate quiz dicitonary object
    quiz = {}

    # enter info from parsed JSON list into the quiz dictionary
    for i in range(len(json_list)):
        quiz[f"question{i+1}"] = Question(
            text=json_list[i]["question"],
            choices=json_list[i]["choices"],
            answer=json_list[i]["answer"],
            student_answer="",
            quiz_type="Multiple Choice",
        )

    return quiz


### TESTING STUFF BELOW

# for testing, I just copied and pasted a response I got

# good string
# response_from_AI = 'Here is an example JSON object that contains a multiple choice quiz about horses:\n\n```\n[\n  {\n    "question": "What is the gestation period of a horse?",\n    "choices": {\n      "A": "4 months",\n      "B": "6 months",\n      "C": "9 months",\n      "D": "12 months"\n    },\n    "answer": "C"\n  },\n  {\n    "question": "Which of the following is not a horse breed?",\n    "choices": {\n      "A": "Thoroughbred",\n      "B": "Quarter Horse",\n      "C": "Arabian",\n      "D": "Bengal"\n    },\n    "answer": "D"\n  },\n  {\n    "question": "What is the name of the fastest horse on record?",\n    "choices": {\n      "A": "Secretariat",\n      "B": "Man o\' War",\n      "C": "Winning Colors",\n      "D": "Black Caviar"\n    },\n    "answer": "A"\n  }\n]\n```\n\nIn this example, there are three questions about horses, each with four possible choices. The correct answer for each question is indicated by the value of the "answer" key, which corresponds to the key of the correct choice in the "choices" dictionary.\n\nFeel free to modify the questions, choices, and answers to suit the needs of your intermediate students.'

# bad string
response_from_AI = "string of text"

quiz = create_quiz(response_from_AI)


# print quiz to check input values
for question in quiz.values():
    print(question.text)
    for letter, choice in question.choices.items():
        print(f"{letter}) {choice}")
    print("\n")
