#!/usr/bin/python3

# Imports
import os

from codesauce.utils.colors import Color


class Display(object):
    @staticmethod
    def display_banner():
        design = (
            "\n"
            "\n"
            "       ___      ___      ___   /  ___      ___      ___               ___      ___    \n"
            "     //   ) ) //   ) ) //   ) / //___) ) ((   ) ) //   ) ) //   / / //   ) ) //___) ) \n"
            "    //       //   / / //   / / //         \ \    //   / / //   / / //       //        \n"
            "   ((____   ((___/ / ((___/ / ((____   //   ) ) ((___( ( ((___( ( ((____   ((____     \n"
            "\n"
        )

        Color.print("{B}" + design)
        header = "{R}                          @hackedbyagirl {W}| {P} Hack the World\n"
        Color.print(header)

    @staticmethod
    def display_main_description():
        """
        Display main screen at launch
        """
        # Welcome Message
        Color.print("\n\n\t\t\t\t{B} *** Welcome to Codesauce ***\n\n")

    @staticmethod
    def display_interactive_chat_banner():
        """
        Display welcome banner for interactive chat session
        """
        Display.clear_screen()
        Color.print("\n{B}Welcome to the Interactive Codesauce Session\n")
        Color.print(
            "\n{W}You are now in an interactive session with Codesauce. Codesauce AI will assist you provide with a broad spectrum of coding and development tasks while providing insightful responses based on its analysis.\n"
        )

    ########################################################################
    # Helper Functions
    ########################################################################
    @staticmethod
    def clear_screen():
        """Clear Screen"""
        os.system("cls" if os.name == "nt" else "clear")
