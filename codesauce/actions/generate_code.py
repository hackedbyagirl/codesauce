#!/usr/bin/python3

# Imports
import os
import questionary

from codesauce.utils.config import Config
from codesauce.prompts.system_prompt_builder import build_system_prompt
from codesauce.prompts.user_prompt_builder import (
    build_code_generator_prompt,
    build_multi_code_generator_prompt,
    build_multi_code_generator_final_prompt,
)
from codesauce.prompts.code_gen_prompt import (
    CG_TASK_NAME,
    CG_SYSTEM_PROMPT,
    CG_MULTI_SYSTEM_PROMPT,
    CG_REF_SYSTEM_PROMPT,
)
from codesauce.utils.colors import Color
from codesauce.modules.general_interaction import GeneralInteraction

from codesauce.modules.function_interaction import FunctionInteraction

from codesauce.prompts.system_prompt_builder import (
    build_ai_assistant_prompt,
    build_code_cg_ref_sys_prompt,
)
from codesauce.prompts.user_prompt_builder import (
    build_code_reference_user_prompt,
    build_multi_code_reference_final_prompt,
)


from codesauce.tools.chunk_code import chunk_code


AI_FIRST_MESSAGE = "First Message received, continue."
AI_MESSAGE = "Message received, continue."
AI_FIRST_CODE_REF = "First Code Reference received, continue."
AI_CODE_REF_MESSAGE = "Code Reference received, continue."


class GenerateCode(FunctionInteraction):
    def interact(self, arguments):
        self.arguments = arguments

        Color.print("{B}Launching Code Generation ...\n")
        file = self.arguments["filename"]
        coding_task = self.arguments["coding_task"]
        references = self.arguments["references"]

        code_file = self.load_file(file)

        if references:
            system_prompt = build_system_prompt(CG_TASK_NAME, CG_REF_SYSTEM_PROMPT)
            self.chat_history.append(system_prompt)

            for ref in references:
                ref_file_path = self.load_file(ref)
                self.update_chat_history_with_reference(ref_file_path)

                self.create_prompts(code_file, coding_task)

                ai_response = self.ask_ai()

        function_response = {
            "actions": "Loaded file, recieved generated code, and saved response to file.",
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
            print("No file with the specified name was found.")
            return ""

        # If multiple matches were found, ask the user to select one
        elif len(matches) > 1:
            file_path = questionary.select(
                "Multiple files with the specified name were found. Please select one:",
                choices=matches,
            ).ask()
            return file_path
        else:
            return matches[0]

    def update_chat_history_with_reference(self, file_path: str):
        code_blocks = chunk_code(file_path)

        if len(code_blocks) > 1:
            # Create a user prompt for each code block
            for i, block in enumerate(code_blocks):
                if i == 0:
                    user_prompt = build_code_reference_user_prompt(block)
                    ai_prompt_message = build_ai_assistant_prompt(AI_FIRST_CODE_REF)

                    self.chat_history.append(user_prompt)
                    self.chat_history.append(ai_prompt_message)

                elif i == len(code_blocks) - 1:
                    user_prompt = build_multi_code_reference_final_prompt(block)
                    ai_prompt_message = build_ai_assistant_prompt("AI_CODE_REF_MESSAGE")

                    self.chat_history.append(user_prompt)
                    self.chat_history.append(ai_prompt_message)

                else:
                    user_prompt = build_code_reference_user_prompt(block)
                    ai_prompt_message = build_ai_assistant_prompt("AI_CODE_REF_MESSAGE")

                    self.chat_history.append(user_prompt)
                    self.chat_history.append(ai_prompt_message)

        else:
            user_prompt = build_code_reference_user_prompt(code_blocks[0])
            ai_prompt_message = build_ai_assistant_prompt("AI_CODE_REF_MESSAGE")

            self.chat_history.append(user_prompt)
            self.chat_history.append(ai_prompt_message)

    def create_prompts(self, loaded_file: str, coding_task: str) -> None:
        # Load the file and return its contents
        code_blocks = chunk_code(loaded_file)

        # Define the system prompt
        if len(code_blocks) > 1:
            # Create a user prompt for each code block
            for i, block in enumerate(code_blocks):
                if i == 0:
                    user_prompt = build_code_generator_prompt(block, coding_task)
                    ai_prompt_message = build_ai_assistant_prompt(AI_FIRST_MESSAGE)

                    self.chat_history.append(user_prompt)
                    self.chat_history.append(ai_prompt_message)

                elif i == len(code_blocks) - 1:
                    user_prompt = build_multi_code_generator_final_prompt(
                        block, coding_task
                    )
                    self.chat_history.append(user_prompt)

                else:
                    user_prompt = build_multi_code_generator_prompt(block)
                    ai_prompt_message = build_ai_assistant_prompt("AI_MESSAGE")

                    self.chat_history.append(user_prompt)
                    self.chat_history.append(ai_prompt_message)

        else:
            user_prompt = build_code_generator_prompt(code_blocks[0], coding_task)
            self.chat_history.append(user_prompt)

    def ask_ai(self):
        ai_bot = GeneralInteraction(self.chat_history)
        ai_bot.interact(self.chat_history)

        last_ai_response = self.chat_history[-1]
        return last_ai_response

    def save_response(self, ai_response: dict, filename: str, file_path: str):
        content = ai_response["content"]

        updated_file = content.split("```")[0]
        updated_file = updated_file.replace(
            "FILE_NAME", "Updated File Path: " + file_path
        )
        summary = content.split("```")[2]

        code = content.split("```")[1]
        lines = code.split("\n")
        lines = lines[1:]
        code = "\n".join(lines)

        # File Saving operations
        basename, extension = os.path.splitext(filename)

        generated_code_dir = Config.generated_code_dir
        generated_code_notes_dir = Config.improvement_notes_dir

        generated_file_name = basename + "_generated" + extension
        summary_file_name = basename + "_generated_summary.txt"

        generated_file = os.path.join(generated_code_dir, generated_file_name)
        summary_file = os.path.join(generated_code_notes_dir, summary_file_name)

        with open(generated_file, "w") as file:
            file.write(code)

        with open(summary_file, "w") as file:
            file.write(updated_file + "\n\n" + summary)
