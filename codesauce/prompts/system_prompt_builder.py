#!/usr/bin/python3

# Imports
from codesauce.prompts.philosophy import GENERAL_PHILOSOPHY

from codesauce.prompts.project_prompts import PROJ_TASK_NAME, PROJ_SYSTEM_PROMPT
from codesauce.prompts.code_clean_prompts import CC_TASK_NAME

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


def build_ai_assistant_prompt(message: str):
    return {
        "role": "assistant",
        "content": message,
    }


########################################################################
# Project Description Prompt
########################################################################


def build_project_description_prompt():
    return build_system_prompt(PROJ_TASK_NAME, PROJ_SYSTEM_PROMPT)


########################################################################
# Code Cleaning Prompts
########################################################################
def build_code_cleaning_sys_prompt(
    prompt: str,
):
    return build_system_prompt(CC_TASK_NAME, prompt)
