#!/usr/bin/python3

# Imports
import os
import questionary


from codesauce.utils.colors import Color
from codesauce.modules.general_interaction import GeneralInteraction
from codesauce.modules.function_interaction import FunctionInteraction
from codesauce.config.config import Config
from codesauce.tools.chunk_code import chunk_code
from codesauce.prompts.system_prompt_builder import (
    build_ai_assistant_prompt,
    build_code_cleaning_sys_prompt,
)
from codesauce.prompts.user_prompt_builder import (
    build_code_cleaning_user_prompt,
    build_multi_code_cleaning_final_prompt,
)
from codesauce.tools.chunk_code import chunk_code
from codesauce.prompts.code_clean_prompts import (
    CC_SYSTEM_PROMPT,
    CC_MULTI_SYSTEM_PROMPT,
)


AI_FIRST_MESSAGE = "First Message received, continue."
AI_MESSAGE = "Message received, continue."


class OptimizeCode(FunctionInteraction):
    def interact(self, arguments):
        self.arguments = arguments

        Color.print("{B}Launching Code Cleaning and Optimization...\n")
        filenames = self.arguments["files"]
        context = self.arguments["context"]

        if context == "":
            context = None

        for file in filenames:
            full_file_path = self.load_file(file)

            self.create_prompts(full_file_path, context)

            ai_response = self.ask_ai()

            self.save_response(ai_response, file, full_file_path)

        function_response = {
            "actions": "Loaded file, asked AI for code review, received response, and saved response to file.",
            "completed": True,
        }
        return function_response

    ########################################################################
    # Code Review Functions
    ########################################################################
    def load_file(self, file_name: str) -> str:
        """
        Load the code from the specified file in the current directory.
        """
        # Get all files in the current directory and its subdirectories
        matches = []
        for root, dirnames, filenames in os.walk("."):
            for filename in filenames:
                if filename == file_name:
                    matches.append(os.path.join(root, filename))

        # If no matches were found, return an empty string
        if not matches:
            Color.print(
                "{Y} Warning: {W}No file with the specified name was found. Please select a different file."
            )

            file_path = questionary.path(
                "Please select intended file for cleaning and optimization",
            ).ask()

            return file_path

        # If multiple matches were found, ask the user to select one
        elif len(matches) > 1:
            file_path = questionary.select(
                "Multiple files with the specified name were found. Please select one:",
                choices=matches,
            ).ask()
            return file_path
        else:
            return matches[0]

    def create_prompts(self, loaded_file: str, context: str = None):
        # Load the file and return its contents
        code_blocks = chunk_code(loaded_file)

        # Define the system prompt
        if len(code_blocks) > 1:
            system_prompt = build_code_cleaning_sys_prompt(CC_MULTI_SYSTEM_PROMPT)
            self.chat_history.append(system_prompt)

            # Create a user prompt for each code block
            for i, block in enumerate(code_blocks):
                if i == 0:
                    user_prompt = build_code_cleaning_user_prompt(block, context)
                    ai_prompt_message = build_ai_assistant_prompt(AI_FIRST_MESSAGE)

                    self.chat_history.append(user_prompt)
                    self.chat_history.append(ai_prompt_message)

                elif i == len(code_blocks) - 1:
                    user_prompt = build_multi_code_cleaning_final_prompt(block)
                    self.chat_history.append(user_prompt)

                else:
                    user_prompt = build_code_cleaning_user_prompt(block)
                    ai_prompt_message = build_ai_assistant_prompt("AI_MESSAGE")

                    self.chat_history.append(user_prompt)
                    self.chat_history.append(ai_prompt_message)

        else:
            system_prompt = build_code_cleaning_sys_prompt(CC_SYSTEM_PROMPT)
            user_prompt = build_code_cleaning_user_prompt(code_blocks[0], context)

            self.chat_history.append(system_prompt)
            self.chat_history.append(user_prompt)

    def ask_ai(self):
        ai_bot = GeneralInteraction(self.chat_history)
        ai_bot.interact(self.chat_history)

        last_ai_response = self.chat_history[-1]
        return last_ai_response

    def save_response(self, ai_response: dict, filename: str, file_path: str):
        content = ai_response["content"]

        suggestions = content.split("```")[0]
        suggestions = suggestions.replace(
            "FILE_NAME", "Cleaned File Path: " + file_path
        )

        summary = content.split("```")[2]

        code = content.split("```")[1]
        lines = code.split("\n")
        lines = lines[1:]
        code = "\n".join(lines)

        # File Saving operations
        basename, extension = os.path.splitext(filename)

        cleaned_code_dir = Config.generated_code_dir
        cleaned_code_notes_dir = Config.improvement_notes_dir

        cleaned_file_name = basename + "_cleaned" + extension
        summary_file_name = basename + "_cleaned_summary.txt"

        cleaned_file = os.path.join(cleaned_code_dir, cleaned_file_name)
        summary_file = os.path.join(cleaned_code_notes_dir, summary_file_name)

        with open(cleaned_file, "w") as file:
            file.write(code)

        with open(summary_file, "w") as file:
            file.write(suggestions + "\n\n" + summary)
