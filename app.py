"""
Cover Letter Generator Application
License: MIT
Author: Brendan Smiley

"""

from App import Application

# Required for eel to work with PyInstaller
import sys, io

buffer = io.StringIO()
sys.stdout = sys.stderr = buffer


def main():
    App = Application()


main()
