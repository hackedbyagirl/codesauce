#!/usr/bin/python3

# Imports
from codesauce.utils.colors import Color

def get_project_description():
    # Get project Description
    Color.print(
        "\n{B}Instructions: {W}Please provide a description of the current code base your working with. \n\tFeel free to provide as much detail as possible about your project. You are able to enter multiple lines using the 'ENTER' button."
    )
    Color.print("{Y}NOTE: {W}Use Ctrl-D (or Ctrl-Z on Windows) when finished.")
    Color.print("\n{P}Project Description:\n")

    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    results = "\n".join(lines)
    return results


def get_user_question():
    Color.print("{Y}NOTE: {W}Use Ctrl-D (or Ctrl-Z on Windows) to submit question when finished.")
    Color.print("\n{G}Question: ")
    question = []
    try:
        while True:
            user_input = input()
            question.append(user_input)
    except EOFError:
        pass

    results = "\n".join(question)

    if results.lower() == "exit":
        return False
    else:
        return results

