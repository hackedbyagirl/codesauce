#!/usr/bin/python3

# Imports
import json

from time import sleep

# from codesauce.utils.colors import Color
from codesauce.modules.interaction import Interaction
from codesauce.functions.function_definitions import function_definitions
from codesauce.actions.optimize_code import OptimizeCode
from codesauce.actions.generate_code import GenerateCode
#from codesauce.actions.restructure_directory import RestructureDirectory
#from codesauce.actions.annotate_code import AnnotateCode

from codesauce.modules.general_interaction import GeneralInteraction


class FunctionCall(Interaction):
    def interact(self, messages):
        max_retry = 7
        retry = 0
        while True:
            try:
                response = self.openai_api.create(
                    model=self.model,
                    messages=messages,
                    functions=function_definitions,
                    function_call="auto",
                    temperature=self.temperature,
                )

                response_message = response.choices[0].message
                self.chat_history.append(response_message)

                # Check if 'function_call' is in the reply_content
                if "function_call" in response_message.to_dict():
                    function_call = response_message.to_dict()["function_call"]
                    function_name = function_call["name"]
                    function_arguments = function_call["arguments"]

                    available_functions = {
                        "optimize_code": OptimizeCode,
                        "generate_and_update_code": GenerateCode,
                        #"create_and_generate_code": CreateFileFromReferences,
                        #"restructure_directory": RestructureDirectory,
                        #"annotate_code": AnnotateCode,
                    }

                    # Test1
                    function_to_call = available_functions[function_name](
                        self.chat_history
                    )
                    f_arguments = json.loads(function_arguments)
                    function_response = function_to_call.interact(f_arguments)

                    self.chat_history.append(
                        {
                            "role": "function",
                            "name": function_name,
                            "content": str(function_response),
                        }
                    )

                else:
                    ai_chat = GeneralInteraction(self.chat_history)
                    ai_chat.interact(self.chat_history)
                break

            except Exception as oops:
                print(f'\n\nError communicating with OpenAI: "{oops}"')
                if "maximum context length" in str(oops):
                    self.chat_history.pop(0)
                    print("\n\n DEBUG: Trimming oldest message")
                    continue

                retry += 1
                if retry >= max_retry:
                    print(f"\n\nExiting due to excessive errors in API: {oops}")
                    exit(1)

                print(f"\n\nRetrying in {2 ** (retry - 1) * 5} seconds...")
                sleep(2 ** (retry - 1) * 5)

        return self.chat_history
