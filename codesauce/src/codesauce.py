#!/usr/bin/python3

# Imports
from codesauce.utils.cli import CLI
from codesauce.config.config import Config
from codesauce.utils.display import Display

class CodeSauce(object):
    def __init__(self):
        Display.display_banner()
        Display.display_main_description()

        # Initialize Config
        Config.init()

    def launch(self):
        app = CLI()
        app.launc_main_cli()
