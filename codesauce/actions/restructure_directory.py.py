#!/usr/bin/python3
# Imports
import os
import questionary

from codesauce.utils.config import Config
from codesauce.prompts.system_prompt_builder import build_system_prompt
from codesauce.prompts.user_prompt_builder import build_directory_init_prompt
from codesauce.prompts.restructure_dir import RD_TASK_NAME, RD_SYSTEM_PROMPT
from codesauce.utils.colors import Color
from codesauce.modules.general import GeneralInteraction
from codesauce.functions.function_interaction import FunctionInteraction
from codesauce.tools.loader import Loader


class RestructureDirectory(FunctionInteraction):
    def interact(self, arguments):
        self.arguments = arguments

        Color.print("{B}Launching Directory Restructuring")

        restructure_notes = self.arguments["instructions"]
        # Get the latest directory structure
        self.get_latest_directory_structure()

        # Create system and user prompts
        self.create_prompts(restructure_notes)

        # Ask the AI
        ai_response = self.ask_ai()

        # Save the generated code
        self.save_generated_code(ai_response)
        function_response = {
            "actions": "Generated new directory structure.",
            "completed": True,
        }
        return function_response

    def get_latest_directory_structure(self):
        new_directory = Loader()
        new_directory.load(os.getcwd())

    def create_prompts(self, instructions: str):
        with open("directory_structure.md", "r") as f:
            directory_structure = f.read()

        system_prompt = build_system_prompt(RD_TASK_NAME, RD_SYSTEM_PROMPT)

        user_prompt = build_directory_init_prompt(instructions, directory_structure)

        self.chat_history.append(system_prompt)
        self.chat_history.append(user_prompt)

    def ask_ai(self):
        ai_bot = GeneralInteraction(self.chat_history)
        ai_bot.interact(self.chat_history)
        last_ai_response = self.chat_history[-1]
        return last_ai_response

    def save_generated_code(self, ai_response):
        gen_code_dir = Config.generated_code_dir

        content = ai_response["content"]
        filename = "directory_structure.md"
        updated_file = content.split("```")[0]
        updated_file = updated_file.replace(
            "FILE_NAME", "Updated File Path: " + filename
        )
        summary = content.split("```")[2]

        code = content.split("```")[1]
        lines = code.split("\n")
        lines = lines[1:]
        code = "\n".join(lines)

        # Save the cleaned code to a new file
        basename, extension = os.path.splitext(filename)
        generated_file_path = basename + "_generated" + extension
        with open(generated_file_path, "w") as file:
            file.write(code)

        # Save the suggestions and summary to a new file
        summary_file_path = basename + "_generated_summary.txt"
        summary_file_path = os.path.join(gen_code_dir, summary_file_path)
        with open(summary_file_path, "w") as file:
            file.write(updated_file + "\n\n" + summary)
