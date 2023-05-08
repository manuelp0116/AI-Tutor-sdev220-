"""
Function to display quiz and gather input from the student. Also grades the quiz.
"""


def take_quiz(quiz: dict):
    """
    Presents questions one at a time and gets input for student answer. Grades quiz at the end.
    """

    """PART 1: TAKE THE QUIZ AND GET STUDENT_ANSWER"""

    # gets question and choices text
    for question in quiz.values():
        print(question.text)

        for letter, choice in question.choices.items():
            print(f"{letter}) {choice}")

        print("\n")

        # gets input for student's answer, updates the question class with student_answer
        question.student_answer = input("Enter your answer as a letter: ").upper()
        while question.student_answer not in question.choices.keys():
            question.student_answer = input(
                "Invalid entry. Enter your answer as a letter: "
            ).upper()
            continue
        print("\n")

    """PART 2: DISPLAY RESULTS AND CALCULATE THE QUIZ SCORE"""

    # initiate values for calculations
    correct = 0
    total = 0

    # gets question, choices, and student answer text
    for question in quiz.values():
        print(question.text)

        for letter, choice in question.choices.items():
            print(f"{letter}) {choice}")

        if question.answer == question.student_answer:
            print(f"Your answer: {question.student_answer}. That's correct!")
            correct += 1
            total += 1
        else:
            print(
                f"Your answer: {question.student_answer}. That wasn't right. The correct answer was {question.answer}"
            )
            total += 1
        print("\n")

    percentage = correct / total
    print(f"Your score for this quiz: {correct}/{total} or {percentage}%")


take_quiz()
