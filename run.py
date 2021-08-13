#!/usr/bin/env python3

import sys
import os

print(os.path.dirname(os.path.realpath(__file__)))

# Get the folder this script is in
scriptPath = os.path.dirname(os.path.realpath(__file__))
# Our source files
sys.path.insert(1, os.path.join(scriptPath, 'src'))

import main

if __name__ == "__main__":
    os.chdir(scriptPath) # Ensure we are in the root folder for resource acess
    main.start_game()
