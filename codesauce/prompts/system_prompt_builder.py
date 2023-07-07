#!/usr/bin/python3

# Imports
from codesauce.prompts.philosophy import GENERAL_PHILOSOPHY

from codesauce.prompts.project_prompts import PROJ_TASK_NAME, PROJ_SYSTEM_PROMPT
from codesauce.prompts.code_clean_prompts import CC_TASK_NAME
from codesauce.prompts.code_generation_prompts import CG_TASK_NAME

TASK_NAMES = {
    'cc_task': CC_TASK_NAME,
    'cg_task': CG_TASK_NAME,
    'project_task': PROJ_TASK_NAME,
}

SYSTEM_PROMPTS = {
    'cc_prompt': CC_SYSTEM_PROMPT,
    'ccm_prompt': CCM_SYSTEM_PROMPT,

    'ucg_prompt': UCG_SYSTEM_PROMPT,
    'ucgm_prompt': UCG_M_SYSTEM_PROMPT,
    'ucgwr_prompt': UCGWR_SYSTEM_PROMPT,

    'ncg_prompt': NCG_SYSTEM_PROMPT,
    'ncgwr_prompt': NCGWR_SYSTEM_PROMPT,
    "proj_prompt": PROJ_SYSTEM_PROMPT,

}


########################################################################
# Main User Prompt Builders
########################################################################


def generate_system_prompt(task_name, task_prompt):
    gen_philosophy = GENERAL_PHILOSOPHY.replace("[TASK_NAME]", task_name)
    system_prompt = gen_philosophy.replace("[TASK_PROMPT]", task_prompt)

    return {
        "role": "system",
        "content": system_prompt,
    }

def build_system_prompt(task_key: str, prompt: str):
    task_name = TASK_NAMES[task_key]
    task_prompt = SYSTEM_PROMPTS[prompt]

    return build_system_prompt(task_name, task_prompt)


def build_ai_assistant_prompt(message: str):
    return {
        "role": "assistant",
        "content": message,
    }
