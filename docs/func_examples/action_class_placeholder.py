#!/usr/bin/python3

# Imports
from codesauce.modules.function_interaction import FunctionInteraction

## If prompts are needed 
from codesauce.prompts.system_prompt_builder import (
    build_ai_assistant_prompt,
    build_system_prompt
)

class ActionClass(FunctionInteraction):
    def interact(self, arguments):
        self.arguments = arguments

        # Check to see if instructions key exists
        if "example_arugment" in self.arguments:
            return_value = self.launch_class_action1()

        else:
            return_value = self.launch_class_action2()

        return return_value

    ########################################################################
    # Class Action Function Logic
    ########################################################################

  def launch_class_action1(self):
        """ Specific Action Logic """

  def launch_class_action2(self):
        """ Specific Action Logic """
