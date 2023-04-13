"""
Best prompt to get consistently structured response:
In JSON format, with keys for question, choices, answer: create a multiple choice quiz for a {LEARNING LEVEL} student about {TOPIC}. Make the quiz {# OF QUESTIONS} questions long with 4 choices each. Make the choices key in a single dictionary format and the JSON object a list of dictionaries
"""


import json

quiz = {}

# for testing, just copied and pasted a response I got
response_from_AI = [
    'Sure! Here is a JSON document with 5 questions about horses and the answer key:\n\n```\n[\n    {\n      "question": "What is the average lifespan of a horse?",\n      "choices": {\n        "A": "10-15 years",\n        "B": "20-25 years",\n        "C": "30-35 years",\n        "D": "40-45 years"\n      },\n      "answer": "B"\n    },\n    {\n      "question": "What is a baby horse called?",\n      "choices": {\n        "A": "Foal",\n        "B": "Colt",\n        "C": "Stallion",\n        "D": "Mare"\n      },\n      "answer": "A"\n    },\n    {\n      "question": "What is the fastest horse breed?",\n      "choices": {\n        "A": "Thoroughbred",\n        "B": "Quarter Horse",\n        "C": "Arabian",\n        "D": "Standardbred"\n      },\n      "answer": "A"\n    },\n    {\n      "question": "What is the term for a male horse that has been castrated?",\n      "choices": {\n        "A": "Stallion",\n        "B": "Gelding",\n        "C": "Colt",\n        "D": "Mare"\n      },\n      "answer": "B"\n    },\n    {\n      "question": "What is the name of the famous horse that won the Triple Crown in 2018?",\n      "choices": {\n        "A": "Secretariat",\n        "B": "Seattle Slew",\n        "C": "American Pharoah",\n        "D": "Justify"\n      },\n      "answer": "D"\n    }\n  ]\n```\n\nI hope this helps! Let me know if you have any other questions.'
]

resp_str = response_from_AI[0]  # gets the string version of the response (since it returns a list with one entry by default)
resp_split = resp_str.split("```")  # splits string to isolate the code block as the second item in a list (new list is [fluff text, JSON CODE BLOCK WE WANT, more fluff])

resp_list = json.loads(resp_split[1].strip())  # converts JSON code block into python list

# putting the quiz info into a dictionary
for i in range(len(resp_list)):
    quiz[f"q{i+1}"] = resp_list[i]

# print/display quiz
for j in range(len(quiz)):
    print(
        f"""
        {quiz[f"q{j+1}"]["question"]})
        A) {quiz[f"q{j+1}"]["choices"]["A"]}
        B) {quiz[f"q{j+1}"]["choices"]["B"]}
        C) {quiz[f"q{j+1}"]["choices"]["C"]}
        D) {quiz[f"q{j+1}"]["choices"]["D"]}
        """
    )
