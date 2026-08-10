# The Command Prompt esque program that can run commands such as rolling or attacking etc. with characters

from pathlib import Path
import commands
import sys
import json



player_name = ""
while True:
    player_name = input("Please enter a character ID: ")
    file_location = Path(f"players/{player_name}.json")
    if file_location.exists():
        print("Found character! Loading now...")
        with open(file_location, "r") as file:
            data = json.load(file)
            commands.player_data = data
        break
    else:
        print(f"Could not find character under ID '{player_name}'")

print("Welcome user! Type '/help commands' for a list of available commands \n")
while True:
    command = input("/")
    args = command.split()
    # print(args)
    commands.execute_command(args)
