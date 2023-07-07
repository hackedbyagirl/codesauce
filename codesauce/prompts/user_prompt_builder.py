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
# Code Reference Prompt Builders
########################################################################
def build_code_reference_user_prompt(code):
    code_ref_prompt = f"""Code Reference:\n{code}"""

    return build_user_prompt(code_ref_prompt)


def build_multi_code_reference_final_prompt(code):
    code_ref_prompt = f"""Code Reference:\n{code}\n\nThis is the last code block."""

    return build_user_prompt(code_ref_prompt)


########################################################################
# Code Cleaning Prompt Builders
########################################################################
def build_code_cleaning_user_prompt(code, context=None):
    if context:
        code_cleaning_prompt = (
            f"""Code to Clean and Optimize:\n{code}\nContext:\n{context}"""
        )
    else:
        code_cleaning_prompt = f"""Code to Clean and Optimize:\n{code}"""

    return build_user_prompt(code_cleaning_prompt)


def build_multi_code_cleaning_final_prompt(code):
    last_code_review_prompt = (
        f"""Code to Clean and Optimize:\n{code}\n\nThis is the last code block."""
    )

    return build_user_prompt(last_code_review_prompt)


########################################################################
# Code Generation Prompt Builders
########################################################################
def build_code_generator_prompt(code, context):
    code_gen_prompt = f"""Code Generator Task:\n{context}\nCode:\n{code}"""

    return build_user_prompt(code_gen_prompt)


def build_multi_code_generator_prompt(code):
    code_gen_prompt = f"""Code Continued:\n{code}"""

    return build_user_prompt(code_gen_prompt)


def build_multi_code_generator_final_prompt(code, context):
    code_gen_prompt = f"""Last Code Block:\n{code}\n\nCode Generator Task:\n{context}\n\nThis is the last code block."""

    return build_user_prompt(code_gen_prompt)
