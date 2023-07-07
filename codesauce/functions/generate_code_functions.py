#!/usr/bin/python3

# Imports
import os
import questionary

from codesauce.utils.config import Config
from codesauce.prompts.system_prompt_builder import build_system_prompt
from codesauce.prompts.user_prompt_builder import build_code_generator_prompt, build_multi_code_generator_prompt, build_multi_code_generator_initial_prompt, build_multi_code_generator_final_prompt
from codesauce.prompts.code_gen_prompt import CG_TASK_NAME, CG_SYSTEM_PROMPT, CG_MULTI_SYSTEM_PROMPT
from codesauce.utils.colors import Color
from codesauce.modules.general import GeneralInteraction

from codesauce.functions.function_interaction import FunctionInteraction

class GenerateCode(FunctionInteraction):
    def interact(self, arguments):
        self.arguments = arguments
        
        filename = self.arguments['filename']
        coding_task = self.arguments['coding_task']

        Color.print("{B}Launching Code Generation Function")

         # Load the file
        file_path = self.load_file(filename)

        # Create prompts
        self.create_prompts(file_path, coding_task)
        
        # Ask the AI
        ai_response = self.ask_ai()

        self.save_response(ai_response, filename, file_path)

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
        for root, dirnames, filenames in os.walk('.'):
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
                choices=matches
            ).ask()
            return file_path
        else:
            return matches[0]
    
    def create_prompts(self, loaded_file: str, coding_task: str) -> None:
        # Load the file and return its contents
        with open(loaded_file, 'r') as file:
            loaded_file = file.readlines()
        
        # Remove blank lines
        lines = [line for line in loaded_file if line.strip() != ""]
        total_lines = len(lines)
       
        # Join the lines back into a single string
        loaded_file = "".join(lines)
        
        # Divide the content into blocks of 100 lines
        code_blocks = [lines[i:i + 100] for i in range(0, total_lines, 100)]

        # Define the system prompt
        if len(code_blocks) > 1:
            system_prompt = build_system_prompt(CG_TASK_NAME, CG_MULTI_SYSTEM_PROMPT)
            self.chat_history.append(system_prompt)

            # Create a user prompt for each code block
            for i, block in enumerate(code_blocks):
                if i == 0:
                    user_prompt = build_multi_code_generator_initial_prompt(coding_task, block)
                    ai_prompt_message = {"role": "assistant", "content": "First Message received, continue."}

                    self.chat_history.append(user_prompt)
                    self.chat_history.append(ai_prompt_message)
                
                elif i == len(code_blocks) - 1:
                    user_prompt = build_multi_code_generator_final_prompt(coding_task, block)
                    self.chat_history.append(user_prompt)
                
                else:
                    user_prompt = build_multi_code_generator_prompt(block)
                    ai_prompt_message = {"role": "assistant", "content": "Message received, continue."}

                    self.chat_history.append(user_prompt)
                    self.chat_history.append(ai_prompt_message)

        else:
            system_prompt = build_system_prompt(CG_TASK_NAME, CG_SYSTEM_PROMPT)
            user_prompt = build_code_generator_prompt(coding_task, loaded_file)
            
            self.chat_history.append(system_prompt)
            self.chat_history.append(user_prompt)
            #return system_prompt, user_prompt


    def ask_ai(self):
        ai_bot = GeneralInteraction(self.chat_history)
        ai_response = ai_bot.interact(self.chat_history)

        last_ai_response = self.chat_history[-1]
        return last_ai_response

    def save_response(self, ai_response: dict, filename: str, file_path: str):
        gen_code_dir = Config.generated_code_dir
        
        content = ai_response["content"]

        updated_file = content.split("```")[0]
        updated_file = updated_file.replace("FILE_NAME", "Updated File Path: " + file_path)
        summary = content.split("```")[2]

        code = content.split("```")[1]
        lines = code.split("\n")
        lines = lines[1:]
        code = "\n".join(lines)
        
        # Save the cleaned code to a new file
        basename, extension = os.path.splitext(filename)
        generated_file_path = basename + "_generated" + extension
        generated_file_path = os.path.join(gen_code_dir, generated_file_path)
        with open(generated_file_path, 'w') as file:
            file.write(code)

        # Save the suggestions and summary to a new file
        summary_file_path = basename + "_generated_summary.txt"
        summary_file_path = os.path.join(gen_code_dir, summary_file_path)
        with open(summary_file_path, 'w') as file:
            file.write(updated_file + "\n\n" + summary)