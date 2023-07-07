#!/usr/bin/python3

# Imports
import time
import questionary

from datetime import datetime


from codesauce.utils.colors import Color
from codesauce.config.config import Config
from codesauce.utils.display import Display
from codesauce.modules.function_call import FunctionCall
from codesauce.actions.input import get_user_question
from codesauce.prompts.user_prompt_builder import build_user_question_prompt
from codesauce.actions.input import get_project_description
from codesauce.prompts.user_prompt_builder import build_project_user_prompt
from codesauce.prompts.system_prompt_builder import (
    build_ai_assistant_prompt,
    build_system_prompt
)

PROJ_TASK = 'project_task'
PROJ_PROMPT = 'proj_prompt'


class ChatBot(object):
    def __init__(self):
        self.chat_history = []
        self.call_functions = FunctionCall(self.chat_history)
        timestamp = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d_%H-%M-%S")
        self.chat_file = f"chat_log_{timestamp}.json"

    def launch(self):
        # Display banner
        Display.display_interactive_chat_banner()

        proj_desc = self.request_project_description()

        if proj_desc != False:
            proj_system_prompt = build_system_prompt(PROJ_TASK, PROJ_PROMPT)
            proj_user_prompt = build_project_user_prompt(proj_desc)

            self.chat_history.append(proj_system_prompt)
            self.chat_history.append(proj_user_prompt)
            self.chat_history.append(
                build_ai_assistant_prompt(
                    "Thank you for providing a project description as context"
                )
            )

    def interact(self):
        """
        Begins interaction with chabot
        """

        # Launch initial ai interaction
        # self.launch()

        # Engage in Interactive chat loop
        # Get project Description
        Color.print(
            "\n{B}Instructions: {W}\n\tFeel free to provide as much detail as possible when asking questions. You are able to enter multiple lines using the 'ENTER' button."
        )
        while True:
            question = get_user_question()
            if question == False:
                Config.save_chat_log(self.chat_file, self.chat_history)
                Config.exit(1)

            # Add question to chat history
            user_prompt = build_user_question_prompt(question)
            self.chat_history.append(user_prompt)

            # Launch ai interaction
            self.chat_history = self.call_functions.interact(self.chat_history)

    ########################################################################
    # Helper Functions
    ########################################################################

    def request_project_description(self):
        """Requests project description"""
        Color.print(
            "\n{Y}Question: \n{W}Would you like to provide a general description for your project? This can help the AI system better understand what you are reviewing. If you want to provide a description, enter 'yes'. Otherwise, enter 'no'.\n"
        )
        response = questionary.select(
            "Select Mode:",
            choices=["Yes", "No"],
        ).ask()

        if response == "Yes":
            proj_description = get_project_description()
            return proj_description
        else:
            return False
