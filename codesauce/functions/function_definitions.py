 #!/usr/bin/python3

# Imports

# Define the AI function for code review
code_review_func_definition = {
    "name": "perform_code_review",
    "description": "Perform crucial code cleaning operations, such as refactoring and optimizing code to make it more readable, maintainable, and efficient, adhering to the coding standards of the respective language.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to file to be reviewed"
            },
        },
        "required": ["file_path"]
    }
}

generate_code_func_definition = {
    "name": "generate_code",
    "description": "Performs dynamic code generation based on clearly defined coding tasks or goals.",
    "parameters": {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "The path to file where code will be generated for."
            },
            "coding_task": {
                "type": "string",
                "description": "A clear description of the coding task or goal."
            }
        },
        "required": ["filename", "coding_task"]
    }
}

restructure_directory_func_definition = {
    "name": "restructure_directory",
    "description": "Review the current directory structure and restructure and rename the current directory to be more efficient.",
    "parameters": {
        "type": "object",
        "properties": {
            "instructions": {
                "type": "string",
                "description": "A description of directory restructuring instructions to assist the AI."
            }
        },
        "required": ["instructions"]
    }
}


annotate_code_func_definition = {
    "name": "annotate_code",
    "description": "Add helpful comments to the code, explaining complex sections or detailing the purpose and functionality of specific blocks of code for a specific file.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to be annotated."
            },
        },
        "required": ["file_path"]
    }
}

create_new_file_func_definition = {
    "name": "create_new_file",
    "description": "Create a new file with the provided filename and content.",
    "parameters": {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "The name of the file to be created."
            },
            "content": {
                "type": "string",
                "description": "The content to be written into the file."
            }
        },
        "required": ["filename", "content"]
    }
}

# Additional Function Definitions

create_file_from_references_func_definition = {
    "name": "create_file_from_references",
    "description": "Create a file and generate code based on user instructions and a provided list of files to reference.",
    "parameters": {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "The name of the file to be created."
            },
            "instructions": {
                "type": "string",
                "description": "The user instructions for generating code."
            },
            "references": {
                "type": "array",
                "items": {
                    "type": "string",
                    "description": "The list of files to reference for generating code."
                }
            }
        },
        "required": ["filename", "instructions", "references"]
    }
}

update_code_from_references_func_definition = {
    "name": "update_code_from_references",
    "description": "Update an existing file by generating code based on user input and files referenced.",
    "parameters": {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "The name of the file to be updated."
            },
            "user_input": {
                "type": "string",
                "description": "The user input for generating code."
            },
            "references": {
                "type": "array",
                "items": {
                    "type": "string",
                    "description": "The list of files to reference for generating code."
                }
            }
        },
        "required": ["filename", "user_input", "references"]
    }
}

# Updated AI function definitions
ai_function_definitions = [
    code_review_func_definition,
    generate_code_func_definition,
    create_file_from_references_func_definition,
    restructure_directory_func_definition
]

#ai_function_definitions = [
#    code_review_func_definition,
#    generate_code_func_definition,
#    restructure_directory_func_definition,
#    annotate_code_func_definition,
#    create_new_file_func_definition,
#    create_file_from_references_func_definition,
#    update_code_from_references_func_definition
#]