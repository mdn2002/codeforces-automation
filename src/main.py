#!/usr/bin/env python3
"""
Codeforces Problem Automation Tool
Main entry point for the application
"""

from src.utils.config_parser import ConfigParser
from src.problem_creator import ProblemCreator

def main():
    config = ConfigParser()
    problem_creator = ProblemCreator(config)
    print("This tool is now intended to be used with the browser extension and server workflow.")
    print("Start the server with: python3 cf_receiver.py")
    print("Then use the browser extension to send problems.")

if __name__ == "__main__":
    main() 