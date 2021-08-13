#!/usr/bin/env python3

import sys
import os

# Get the folder this script is in and add the source folder to the PATH.
scriptPath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(scriptPath, 'src'))

import main

if __name__ == "__main__":
    # Ensure we are in the root folder for resource access.
    os.chdir(scriptPath)
    main.start_game()
