#!/usr/bin/python3

# Imports
import os
import questionary

from codesauce.config.config import Config
from codesauce.utils.colors import Color
from codesauce.modules.general_interaction import GeneralInteraction
from codesauce.modules.function_interaction import FunctionInteraction
from codesauce.tools.chunk_code import chunk_code, create_chunked_prompts, create_chunked_reference_prompts
from codesauce.prompts.user_prompt_builder import (
    build_code_generator_prompt,
    build_multi_code_generator_prompt,
    build_multi_code_generator_final_prompt,
    build_code_reference_user_prompt,
    build_multi_code_reference_final_prompt,
    build_new_code_generator_prompt
)
from codesauce.prompts.system_prompt_builder import (
    build_ai_assistant_prompt,
    build_system_prompt
)


AI_FIRST_MESSAGE = "First Message received, continue."
AI_MESSAGE = "Message received, continue."
AI_FIRST_CODE_REF = "First Code Reference received, continue."
AI_CODE_REF_MESSAGE = "Code Reference received, continue."
CODE_GEN_TASK = 'cg_task'

UPDATE_CODE_GEN_PROMPT = 'ucg_prompt'
UPDATE_CODE_MULTI_PROMPT = 'ucgm_prompt'
UPDATE_CODE_WR_PROMPT = 'ucgwr_prompt'
NEW_CODE_GEN_PROMPT = 'ncg_prompt'
NEW_CODE_WR_PROMPT = 'ncgwr_prompt'


class GenerateCode(FunctionInteraction):
    def interact(self, arguments):
        self.arguments = arguments
        self.path = Config.workspace

        # Check to see if instructions key exists
        if "instructions" in self.arguments:
            return_value = self.launch_new_code_function()

        else:
            return_value = self.launch_update_code_function()

        return return_value

    ########################################################################
    # Function Specific Logic
    ########################################################################
    def launch_new_code_function(self):
        """ Generates new code file """
        instructions = self.arguments["instructions"]
        new_file_name = self.arguments.get("filename")
        references = self.arguments.get("references")

        if not self.process_references(references, NEW_CODE_WR_PROMPT):
            system_prompt = build_system_prompt(CODE_GEN_TASK, NEW_CODE_GEN_PROMPT)
            self.chat_history.append(system_prompt)

        user_prompt = build_new_code_generator_prompt(instructions)
        self.chat_history.append(user_prompt)

        ai_response = self.ask_ai()

        self.save_new_code(ai_response, new_file_name)

        function_response = {
            "actions": "Recieved code generation instructions and saved response to file.",
            "completed": True,
        }
        return function_response

    def launch_update_code_function(self):
        """ Updates existing code file """
        Color.print("{B}Generating Code for Existing file ...\n")

        update_file = self.arguments["filename"]
        instructions = self.arguments["coding_task"]
        references = self.arguments.get("references")
        prompt_functions = {
            'initial': build_code_generator_prompt,
            'final': build_multi_code_generator_final_prompt,
            'intermediate': build_multi_code_generator_prompt,
        }

        ai_messages = {
            'initial': "AI_FIRST_MESSAGE",
            'intermediate': "AI_INTERMEDIATE_MESSAGE",
        }
        update_file_path = self.load_file(update_file)

        # Call the refactored function here and check the return value
        if not self.process_references(references, UPDATE_CODE_WR_PROMPT):
            system_prompt = build_system_prompt(CODE_GEN_TASK, UPDATE_CODE_GEN_PROMPT)
            self.chat_history.append(system_prompt)

        update_file_code_blocks = chunk_code(update_file_path)

        if len(update_file_code_blocks) > 1:
            updated_chat_history = create_chunked_prompts(self.chat_history, update_file_code_blocks, instructions, prompt_functions, ai_messages)
            self.chat_history.extend(updated_chat_history)

        else:
            user_prompt = build_code_generator_prompt(update_file_code_blocks[0], coding_task)
            self.chat_history.append(user_prompt)

        function_response = {
            "actions": "Loaded file, recieved generated code, and saved response to file.",
            "completed": True,
        }
        return function_response

    ########################################################################
    # Code Generation Functions
    ########################################################################
    def load_file(self, file_name: str) -> str:
        """
        Load the code from the specified file in the current directory.
        """
        # Get all files in the current directory and its subdirectories
        matches = []
        for root, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                if filename == file_name:
                    matches.append(os.path.join(root, filename))

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

    def ask_ai(self):
        ai_bot = GeneralInteraction(self.chat_history)
        ai_bot.interact(self.chat_history)

        last_ai_response = self.chat_history[-1]
        return last_ai_response

    ########################################################################
    # Helper Functions
    ########################################################################
    def process_references(self, references, prompt_type):
        """ Process the references """

        if references:
            system_prompt = build_system_prompt(CODE_GEN_TASK, prompt_type)
            self.chat_history.append(system_prompt)

            for ref in references:
                ref_file_path = self.load_file(ref)
                self.update_chat_history_with_reference(ref_file_path)

            return True

        else:
            return False

    def update_chat_history_with_reference(self, file_path: str):
        ref_prompts = {
            'initial': build_code_reference_user_prompt,
            'final': build_multi_code_reference_final_prompt,
            'intermediate': build_code_reference_user_prompt,
        }
        
        ai_ref_messages = {
            'initial': AI_FIRST_CODE_REF,
            'final': AI_CODE_REF_MESSAGE,
            'intermediate': AI_CODE_REF_MESSAGE,
        }
    
        ref_code_blocks = chunk_code(file_path)

        if len(ref_code_blocks) > 1:            
            updated_chat_history = create_chunked_reference_prompts(self.chat_history, ref_code_blocks, ref_prompts, ai_ref_messages)
            self.chat_history.extend(updated_chat_history)

        else:
            user_prompt = build_code_reference_user_prompt(ref_code_blocks[0])
            ai_prompt_message = build_ai_assistant_prompt("AI_CODE_REF_MESSAGE")

            self.chat_history.append(user_prompt)
            self.chat_history.append(ai_prompt_message)

    def save_updated_response(self, ai_response: dict, filename: str, file_path: str):
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

        generated_code_dir = Config.updated_code_dir
        generated_code_notes_dir = Config.improvement_notes_dir

        generated_file_name = basename + "_updated" + extension
        summary_file_name = basename + "_updated_summary.txt"

        generated_file = os.path.join(generated_code_dir, generated_file_name)
        summary_file = os.path.join(generated_code_notes_dir, summary_file_name)

        with open(generated_file, "w") as file:
            file.write(code)

        with open(summary_file, "w") as file:
            file.write(updated_file + "\n\n" + summary)

    def save_new_code(self, ai_response: dict, filename: str = None):
        content = ai_response["content"]
    
        code = content.split("```")[1]
        lines = code.split("\n")
        lines = lines[1:]
        code = "\n".join(lines)

        # File Saving operations
        if filename:
            basename, extension = os.path.splitext(filename)

        else:
            user_filename = questionary.text("Please enter a filename for the generated code. Please include the file extension.\n Example: test.py").ask()

            basename, extension = os.path.splitext(user_filename)

        generated_code_dir = Config.generated_code_dir
        generated_file_name = basename + "_generated" + extension
        generated_file = os.path.join(generated_code_dir, generated_file_name)

        with open(generated_file, "w") as file:
            file.write(code)


