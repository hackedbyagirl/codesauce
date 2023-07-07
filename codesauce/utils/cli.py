#!/usr/bin/python3

# Imports
import questionary
import os

from questionary import Style

from codesauce.config.config import Config
from codesauce.utils.colors import Color

## CLI Styler
custom_style = Style(
    [
        ("separator", "fg:#6C6C6C"),
        ("qmark", "fg:#FF9D00 bold"),
        ("question", "bold"),
        ("selected", "fg:#5F819D"),
        ("pointer", "fg:#FF9D00 bold"),
        ("choice", "fg:#FF9D00 bold"),
        ("answer", "fg:#5F819D bold"),
    ]
)


class CLI(object):
    """
    Initial CLI
    """

    def __init__(self):
        """Init Class"""
        self.mode = ""

    def launc_main_cli(self):
        """Launch main CLI"""

        while True:
            method = questionary.select(
                "Please select a method for how you would like to provide your code:",
                choices=["Current Directory", "Directory Path", "Exit"],
                style=custom_style,
            ).ask()
            if method == "Exit":
                Config.exit(1)

            if method == "Current Directory":
                self.handle_cwd()

            if method == "Directory Path":
                self.handle_path()

    def handle_path(self):
        """
        Gets Code Directory Path and sends to loader
        """
        from codesauce.modules.chatbot import ChatBot
        from codesauce.tools.loader import Loader

        dir_path = questionary.path(
            "Please provide the path to the code directory",
            only_directories=True,
            style=custom_style,
        ).ask()

        Color.print("{G}Action: {W}Retrieving Code from Local Code Repository")
        Config.set_workspace_path(dir_path)

        loader = Loader()
        loader.load()

        chatbot = ChatBot()
        chatbot.interact()

    def handle_cwd(self):
        """
        Launches loader that handles current directory
        """

        from codesauce.modules.chatbot import ChatBot
        from codesauce.tools.loader import Loader

        Color.print("{G}Action: {W}Retrieving Code from Current Directory")
        cwd = os.getcwd()
        Config.set_workspace_path(cwd)

        loader = Loader()
        loader.load()

        chatbot = ChatBot()
        chatbot.interact()
