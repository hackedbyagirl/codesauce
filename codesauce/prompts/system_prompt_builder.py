#!/usr/bin/python3

# Imports
from codesauce.prompts.philosophy import GENERAL_PHILOSOPHY

from codesauce.prompts.project_prompts import PROJ_TASK_NAME, PROJ_SYSTEM_PROMPT

########################################################################
# Main User Prompt Builders
########################################################################

def build_system_prompt(task_name, task_prompt):
    gen_philosophy = GENERAL_PHILOSOPHY.replace("[TASK_NAME]", task_name)
    system_prompt = gen_philosophy.replace("[TASK_PROMPT]", task_prompt)
    
    return {
        "role": "system",
        "content": system_prompt,
    }

########################################################################
# Project Description Prompt
########################################################################

def build_project_description_prompt():
    system_prompt = build_system_prompt(PROJ_TASK_NAME, PROJ_SYSTEM_PROMPT)
    return system_prompt