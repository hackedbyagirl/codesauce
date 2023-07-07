#!/usr/bin/python3


########################################################################
# Main User Prompt Builders
########################################################################
def build_user_prompt(content: str):
    return {
        "role": "user",
        "content": content,
    }


########################################################################
# Project Related User Prompts
########################################################################
def build_project_user_prompt(description: str):
    proj_description = f"Project Description:\n{description}"

    return build_user_prompt(proj_description)