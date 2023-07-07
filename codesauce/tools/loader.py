#!/usr/bin/python3

# Imports
import os
import fnmatch

from codesauce.utils.colors import Color
from codesauce.config.config import Config
from codesauce.utils.file_extensions import extensions_ignore, dirs_ignore

EXT_IGNORE = extensions_ignore
DIRS_IGNORE = dirs_ignore
DIR_STRUCTURE = "directory_structure.md"


class Loader(object):
    """Loader Class"""

    def __init__(self):
        """Init Class"""
        self.root_dir = Config.workspace
        self.code_files = []
        self.files = []
        self.chunks = []

    def load(self):
        """
        Begin performing code operations from root directory
        """
        try:
            Color.print("{G}Action: {W}Generating File Directory Path")
            self.generate_file_structure()

        except Exception as e:
            raise Exception(f"Error loading code: {e}")

    def generate_file_structure(self):
        """
        Generate file structure
        """
        dir_structure_path = os.path.join(Config.log_dir, DIR_STRUCTURE)

        with open(dir_structure_path, "w") as f:
            f.write("## Directory Structure\n```\n")
            for root, dirs, files in os.walk(self.root_dir):
                # Modifying dirnames list will update os.walk behavior
                dirs[:] = [d for d in dirs if d not in DIRS_IGNORE]

                level = root.replace(self.root_dir, "").count(os.sep)
                indent = " " * 4 * (level - 1) + "├── " if level > 0 else ""
                f.write("{}{}/\n".format(indent, os.path.basename(root)))
                subindent = " " * 4 * level + "├── "

                for filename in files:
                    # Ignore files with extensions in extensions_ignore
                    if filename.split(".")[-1] not in EXT_IGNORE:
                        f.write("{}{}\n".format(subindent, filename))
            f.write("```\n")
