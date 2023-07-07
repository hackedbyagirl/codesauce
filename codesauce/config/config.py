#!/usr/bin/python3

# Imports
import os
import json

from dotenv import load_dotenv

from codesauce.utils.colors import Color


class Config(object):
    """Stores configuration variables and functions for FileHunter"""

    initialized = False
    verbose = 0

    @classmethod
    def init(cls):
        """
        Sets up default initial configuration values.
        """

        if cls.initialized:
            return
        cls.initialized = True

        cls.verbose = 0

        # Environmental Variable
        cls.openai_key = None

        # Codesauce Workspace
        cls.workspace = None

        # Arguments
        cls.model = "gpt-3.5-turbo-16k"  # gpt-4 if you have the access
        cls.chunk_size = 1000
        cls.chunk_overlap = 0
        cls.embedded_size = 1536

        # Chatbot
        cls.chatbot_name = "CodeSauce"
        cls.log_dir = "logs"
        cls.chat_history_dir = "logs/chat_history"
        cls.improvement_notes_dir = "logs/improvement_notes"
        cls.generated_code_dir = "logs/generated_code"

        # Will overwrite provided variables above
        cls.load_env()
        cls.create_log_dirs()

    ############################################
    @classmethod
    def set_workspace_path(cls, workspace_path: str):
        """Sets workspace path"""
        cls.workspace = workspace_path

    @classmethod
    def save_chat_log(cls, chat_filename, chat_history):
        """Saves chat log to file"""
        chat_history_file = os.path.join(cls.chat_history_dir, chat_filename)

        with open(chat_history_file, "w") as f:
            json.dump(chat_history, f)

    @classmethod
    def load_env(cls):
        """Gets Environmental Variables"""

        cls.openai_key = os.getenv("OPENAI_API_KEY")

        if cls.openai_key is None:
            load_dotenv()
            cls.openai_key = os.getenv("OPENAI_API_KEY")

        if cls.openai_key is None:
            Color.print(
                "{R}OPENAI_API_KEY Not Found: {W} Please set OPENAI_API_KEY as an environmental variable or in in .env file"
            )
            cls.exit(1)

    @classmethod
    def create_log_dirs(cls):
        """Create Log Directories"""
        os.makedirs(cls.log_dir, exist_ok=True)

        cls.create_chat_history_dir()
        cls.create_improvement_notes_dir()
        cls.create_generated_code_dir()

    @classmethod
    def create_chat_history_dir(cls):
        """Creates chat log directory"""

        os.makedirs(cls.chat_history_dir, exist_ok=True)

    @classmethod
    def create_improvement_notes_dir(cls):
        """Creates chat log directory"""

        os.makedirs(cls.improvement_notes_dir, exist_ok=True)

    @classmethod
    def create_generated_code_dir(cls):
        """Creates chat log directory"""

        os.makedirs(cls.generated_code_dir, exist_ok=True)

    @classmethod
    def exit(cls, code=0):
        """Exit Program"""
        Color.print("\n{Y}Exiting program...")

        exit(code)


###############################################################

if __name__ == "__main__":
    Config.init()
