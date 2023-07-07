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
