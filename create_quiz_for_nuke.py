import json


def create_quiz(response: str):
    """
    Takes Ai response as a string and returns quiz as a list of dictionaries, with each  dictionary being a question of the quiz

    question dictionaries are in the following format:
        {
            'type': 'Multiple Choice',
            'question': 'text of the question goes here', (eg. 'What is the capital of Germany?')
            'answer': 'text of the correct answer goes here' (eg. 'Berlin')
            'options': [
                'text of choice A', (eg. "Vancouver")
                'text of choice B', (eg. "Madrid")
                'text of choice C', (eg. "Zurich")
                'text of choice D' (eg. "Berlin")
            ]
    """

    # checks if a JSON code block exists in the response, exits function if not
    split_respose = response.strip().split("```")

    if len(split_respose) == 3:
        json_list = json.loads(split_respose[1].strip())
        return json_list
    else:
        return "Uh oh! Something went wrong and we couldn't generate your quiz. Please try again."





### TESTING STUFF BELOW

# for testing, I just copied and pasted a response I got

# good string
# response_from_AI = """Sure, I can help with that! Here's the quiz you requested:

# ```
# [
#     {
#         "type": "Multiple Choice",
#         "question": "What is the period in human history known as the Stone Age?",
#         "answer": "A time when early humans used stone tools and weapons.",
#         "options": ["A time when humans discovered fire.", "A time when humans invented the wheel.", "A time when humans built the pyramids.", "A time when early humans used stone tools and weapons."]
#     },
#     {
#         "type": "Multiple Choice",
#         "question": "What is the term for the period of the Stone Age when humans first started using stone tools?",
#         "answer": "The Paleolithic period",
#         "options": ["The Mesolithic period", "The Neolithic period", "The Bronze Age", "The Paleolithic period"]
#     },
#     {
#         "type": "Multiple Choice",
#         "question": "What is the term for the period of the Stone Age when humans started to settle in one place and engage in agriculture?",
#         "answer": "The Neolithic period",
#         "options": ["The Paleolithic period", "The Mesolithic period", "The Bronze Age", "The Neolithic period"]
#     },
#     {
#         "type": "Multiple Choice",
#         "question": "What is the term for the period of the Stone Age when humans started to use more advanced stone tools and weapons?",
#         "answer": "The Mesolithic period",
#         "options": ["The Paleolithic period", "The Neolithic period", "The Bronze Age", "The Mesolithic period"]
#     },
#     {
#         "type": "Multiple Choice",
#         "question": "What is the earliest known human species?",
#         "answer": "Homo habilis",
#         "options": ["Homo erectus", "Homo sapiens", "Homo neanderthalensis", "Homo habilis"]
#     },
#     {
#         "type": "Multiple Choice",
#         "question": "What is the term for the process by which humans domesticated plants and animals for human use?",
#         "answer": "Domestication",
#         "options": ["Agriculture", "Industrialization", "Domestication", "Urbanization"]
#     },
#     {
#         "type": "Multiple Choice",
#         "question": "What is the term for the study of ancient human remains?",
#         "answer": "Paleoanthropology",
#         "options": ["Archaeology", "Anthropology", "Paleontology", "Paleoanthropology"]
#     },
#     {
#         "type": "Multiple Choice",
#         "question": "What is the term for the process by which rocks or minerals are heated and then rapidly cooled to make them easier to shape?",
#         "answer": "Flintknapping",
#         "options": ["Smelting", "Forging", "Weaving", "Flintknapping"]
#     },
#     {
#         "type": "Multiple Choice",
#         "question": "What is the term for the diet of early humans, which consisted primarily of meat?",
#         "answer": "The hunter-gatherer diet",
#         "options": ["The vegan diet", "The paleo diet", "The Mediterranean diet", "The hunter-gatherer diet"]
#     },
#     {
#         "type": "Multiple Choice",
#         "question": "What is the term for the process by which humans first migrated out of Africa?",
#         "answer": "Out-of-Africa theory",
#         "options": ["Intra-Africa migration", "Eurasian expansion theory", "Multiregional hypothesis", "Out-of-Africa theory"]
#     }
# ]
# ```

# I hope this helps! Let me know if you need anything else."""
# bad string
# response_from_AI = "string of text"

# quiz = create_quiz(response_from_AI)
# print(quiz)
# print(len(quiz))


# print quiz to check input values
# for question in quiz.values():
#     print(question.text)
#     for letter, choice in question.choices.items():
#         print(f"{letter}) {choice}")
#     print("\n")
