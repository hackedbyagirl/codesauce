#!/usr/bin/python3

# Imports
import os
import questionary


from codesauce.utils.colors import Color
from codesauce.modules.general_interaction import GeneralInteraction
from codesauce.modules.function_interaction import FunctionInteraction
from codesauce.config.config import Config
from codesauce.tools.chunk_code import chunk_code, create_chunked_prompts
from codesauce.prompts.system_prompt_builder import build_system_prompt
from codesauce.prompts.user_prompt_builder import (
    build_code_cleaning_user_prompt,
    build_multi_code_cleaning_final_prompt,
)


AI_FIRST_MESSAGE = "First Message received, continue."
AI_MESSAGE = "Message received, continue."
CODE_CLEAN_TASK = 'cc_task'
CLEAN_CODE_GEN_PROMPT = 'cc_prompt'
CLEAN_CODE_MULTI_PROMPT = 'ccm_prompt'


class OptimizeCode(FunctionInteraction):
    def interact(self, arguments):
        self.arguments = arguments

        Color.print("{B}Launching Code Cleaning and Optimization...\n")
        filenames = self.arguments["files"]
        instructions = self.arguments.get("context")

        for file in filenames:
            full_file_path = self.load_file(file)

            self.create_prompts(full_file_path, instructions)

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

            return str(file_path)

        # If multiple matches were found, ask the user to select one
        elif len(matches) > 1:
            file_path = questionary.select(
                "Multiple files with the specified name were found. Please select one:",
                choices=matches,
            ).ask()
            return file_path
        else:
            return matches[0]

    def create_prompts(self, loaded_file: str, instructions: str = None):
        prompt_functions = {
            'initial': build_code_cleaning_user_prompt,
            'final': build_multi_code_cleaning_final_prompt,
            'intermediate': build_code_cleaning_user_prompt,
        }

        ai_messages = {
            'initial': "AI_FIRST_MESSAGE",
            'intermediate': "AI_INTERMEDIATE_MESSAGE",
        }

        update_file_code_blocks = chunk_code(loaded_file)
    
        if len(update_file_code_blocks) > 1:
            system_prompt = build_system_prompt(CODE_CLEAN_TASK, CLEAN_CODE_MULTI_PROMPT)
            self.chat_history.append(system_prompt)

            updated_chat_history = create_chunked_prompts(self.chat_history, update_file_code_blocks, instructions, prompt_functions, ai_messages)
            
            self.chat_history.extend(updated_chat_history)

        else:
            system_prompt = build_system_prompt(CODE_CLEAN_TASK, CLEAN_CODE_GEN_PROMPT)
            user_prompt = build_code_cleaning_user_prompt(update_file_code_blocks[0], instructions)

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
