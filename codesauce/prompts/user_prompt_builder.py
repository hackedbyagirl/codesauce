#!/usr/bin/python3


########################################################################
# Main User Prompt Builders
########################################################################
def build_user_prompt(content: str):
    return {
        "role": "user",
        "content": content,
    }

def build_user_question_prompt(user_question: str):
    question = f"Question:\n{user_question}"
    
    return build_user_prompt(question)

########################################################################
# Project Related User Prompts
########################################################################
def build_project_user_prompt(description: str):
    proj_description = f"Project Description:\n{description}"

    return build_user_prompt(proj_description)

########################################################################
# Code Cleaning Prompt Builders
########################################################################
def build_code_cleaning_user_prompt(code, context = None):
    if context:
        code_cleaning_prompt = f"""Code to Clean and Optimize:\n{code}\nContext:\n{context}"""
    else:
        code_cleaning_prompt = f"""Code to Clean and Optimize:\n{code}"""
    
    return build_user_prompt(code_cleaning_prompt)

def build_multi_code_cleaning_final_prompt(code):
    last_code_review_prompt = f"""Code to Clean and Optimize:\n{code}\n\nThis is the last code block."""

    return build_user_prompt(last_code_review_prompt)