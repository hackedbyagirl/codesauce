 #!/usr/bin/python3

# Define the AI function for code review
optimize_code_func_definition = {
    "name": "optimize_code",
    "description": "Perform crucial code cleaning operations, such as refactoring and optimizing code to make it more readable, maintainable, and efficient, adhering to the coding standards of the respective language.",
    "parameters": {
        "type": "object",
        "properties": {
            "files": {
                "type": "array",
                "items": {
                    "type": "string",
                    "description": "The list of files that need to be cleaning and optimized."
                }
            },
            "context": {                  
                "type": "string",
                "description": "Context for code cleaning and optimization.",
                "default": ""
            },
        },
        "required": ["files"]
    }
}

generate_and_update_code_func_definition = {
    "name": "generate_and_update_code",
    "description": "Performs dynamic code generation based on clearly defined coding tasks or goals and integrates it into an exisiting file. Also uses reference files as context if any are provided.",
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
            },
            "references": {
                "type": "array",
                "items": {
                    "type": "string",
                    "description": "The list of files to reference for generating code."
                },
                "default": [],
                "description": "Optional: List of files to reference while updating code."
            }
        },
        "required": ["filename", "coding_task"]
    }
}

create_new_code_func_definition = {
    "name": "create_and_generate_code",
    "description": "Performs dynamic code generation based on clearly defined coding tasks or goals. Additionally, the user may include a filename for the generated code and/or reference files that can provide valuable context, if available.",
    "parameters": {
        "type": "object",
        "properties": {
            "instructions": {
                "type": "string",
                "description": "A clear description of the content or code that should be generated for the file."
            },
            "filename": {
                "type": "string",
                "description": "Optional: The name of the file to be created.",
                "default": "generated_code_file"
            },
            "references": {
                "type": "array",
                "items": {
                    "type": "string",
                    "description": "Optional: The list of files to reference for generating additional code."
                },
                "default": [],
                "description": "Optional: List of files to reference while generating code."
            }
        },
        "required": ["instructions"]
    }
}

restructure_directory_func_definition = {
    "name": "restructure_directory",
    "description": "Restructure the current directory to be more efficient.",
    "parameters": {
        "type": "object",
        "properties": {
            "instructions": {
                "type": "string",
                "description": "A description of directory restructuring instructions to assist the AI."
            }
        },
    }
}

annotate_code_func_definition = {
    "name": "annotate_code",
    "description": "Add helpful comments to the code, explaining complex sections or detailing the purpose and functionality of specific blocks of code for a specific file.",
    "parameters": {
        "type": "object",
        "properties": {
            "files": {
                "type": "array",
                "items": {
                    "type": "string",
                    "description": "The list of files that need to be annotated."
                }
            },
            "context": {                  
                "type": "string",
                "description": "Context for code annotation.",
                "default": ""
            },
        },
        "required": ["files"]
    }
}

# Updated AI function definitions
ai_function_definitions = [
    optimize_code_func_definition,
    generate_and_update_code_func_definition,
    annotate_code_func_definition,
    restructure_directory_func_definition,
    create_new_code_func_definition
]
