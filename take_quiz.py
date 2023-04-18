from create_quiz import *



def take_quiz():
    for question in quiz.values():
        print(question.text)
        for letter, choice in question.choices.items():
            print(f"{letter}) {choice}")
        print("\n")

        question.student_answer = input("Enter your answer as a letter: ").upper()
        while question.student_answer not in question.choices.keys():
            question.student_answer = input("Invalid entry. Enter your answer as a letter: ").upper()
            continue
        print("\n")


    correct = 0
    total = 0

    for question in quiz.values():
        print(question.text)
        for letter, choice in question.choices.items():
            print(f"{letter}) {choice}")

        if question.answer == question.student_answer:
            print(f"Your answer: {question.student_answer}. That's correct!")
            correct += 1
            total += 1
        else:
            print(f"Your answer: {question.student_answer}. That not it. The correct answer was {question.answer}")
            total += 1
        print("\n")

    print(f"Your score for this quiz: {correct}/{total} or {correct/total*100:.2f}%")

take_quiz()
