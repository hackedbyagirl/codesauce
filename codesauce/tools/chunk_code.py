from codesauce.prompts.system_prompt_builder import build_ai_assistant_prompt

def chunk_code(file_path: str) -> list:
    # Load the file and return its contents
    with open(file_path, "r") as file:
        file_path = file.readlines()

    # Remove blank lines
    lines = [line for line in file_path if line.strip() != ""]
    total_lines = len(lines)

    # Join the lines back into a single string
    file_path = "".join(lines)

    # Divide the content into blocks of 100 lines
    code_blocks = [lines[i : i + 100] for i in range(0, total_lines, 100)]

    return code_blocks

def create_chunked_prompts(chat_history: list, code_blocks: list, coding_task: str, prompt_functions: dict, ai_messages: dict) -> None:
    # Create a user prompt for each code block
    for i, block in enumerate(code_blocks):
        if i == 0:
            user_prompt = prompt_functions['initial'](block, coding_task)
            ai_prompt_message = build_ai_assistant_prompt(ai_messages['initial'])

            chat_history.append(user_prompt)
            chat_history.append(ai_prompt_message)

        elif i == len(code_blocks) - 1:
            user_prompt = prompt_functions['final'](block, coding_task)
            chat_history.append(user_prompt)

        else:
            user_prompt = prompt_functions['intermediate'](block)
            ai_prompt_message = build_ai_assistant_prompt(ai_messages['intermediate'])

            chat_history.append(user_prompt)
            chat_history.append(ai_prompt_message)

    return chat_history
    