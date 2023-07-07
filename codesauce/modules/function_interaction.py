#!/usr/bin/python3

# Imports

class FunctionInteraction:
    def __init__(self, chat_history):
        self.chat_history = chat_history

    def interact(self, arguments):
        raise NotImplementedError