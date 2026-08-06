# The Command Prompt esque program that can run commands such as rolling or attacking etc. with characters

from commands import execute_command

while True:
    command = input("/")
    args = command.split()
    # print(args)
    execute_command(args)
    

    