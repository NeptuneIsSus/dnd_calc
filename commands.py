import sys

commands = []
player_data = {}



# BASE COMMAND CLASS



class cmd:

    # Specific cmd functions

    def description(self) -> str:
        return "No description was given..."

    def bio(self) -> str:
        return "This command is lacking in the explanation department...\n> Please remind the author of this program to give me instructions!!!"
    
    def execute(self, args:list) -> str:
        return ""
    
    def get_acceptable_args(self) -> list:
        return []

    # Universal cmd functions

    def check_validity(self, args:list) -> str:
        # return "" = success, otherwise it's considered an error
        
        # ARG TYPES:
        # int - whole number
        # float - decimal number
        # percent - 0.0 to 1.0
        # range - number between min and max values
        # rangei - whole number between min and max values
        # str - text
        # custom - custom list from the list key
        # setting optional to true makes it optional

        valids = self.get_acceptable_args()

        if len(args) - 1 < len(valids):
            return "<!!> Not enough arguments were given!"

        for i, a in enumerate(valids):
            # print(i, a, args[i + 1], a["type"])
            argument = args[i + 1]
            match a["type"]:
                case "int":
                    try:
                        num = int(argument)
                        continue
                    except ValueError:
                        return f"<!!> Argument {i + 1} ({argument}) must be a whole number!"
                case "float":
                    try:
                        num = float(argument)
                        continue
                    except ValueError:
                        return f"<!!> Argument {i + 1} ({argument}) must be a number!"
                case "percent":
                    try:
                        num = float(argument)
                        if num <= 1.0 and num >= 0.0:
                            continue
                        else:
                            return f"<!!> Argument {i + 1} ({argument}) must be a value between 0.0 and 1.0!"
                    except ValueError:
                        return f"<!!> Argument {i + 1} ({argument}) must be a number!"
                case "range":
                    try:
                        num = float(argument)
                        if num <= float(a["max"]) and num >= float(a["min"]):
                            continue
                        else:
                            return f"<!!> Argument {i + 1} ({argument}) must be a value between {a["min"]} and {a["max"]}!"
                    except ValueError:
                        return f"<!!> Argument {i + 1} ({argument}) must be a number!"
                case "rangei":
                    try:
                        num = int(argument)
                        if num <= int(a["max"]) and num >= int(a["min"]):
                            continue
                        else:
                            return f"<!!> Argument {i + 1} ({argument}) must be a value between {a["min"]} and {a["max"]}!"
                    except ValueError:
                        return f"<!!> Argument {i + 1} ({argument}) must be a number!"
                case "str":
                    continue
                case "custom":
                    options = a["list"]
                    matcher = next((option for option in options if option.lower().startswith(argument.lower())),None)
                    if matcher is None:
                        lister = ""
                        for item in options:
                            lister += f"{item}, "
                        return f"<!!> Argument {i + 1} ({argument}) must match one of these options!\n<!!> {lister}"
                    else:
                        continue

                case _:
                    return "<!!> Failed due to bug in the code"

        return ""

    def autocomplete(self,args,index) -> str:
        argument = args[index]
        options = self.get_acceptable_args()[index - 1]["list"]
        matcher = next((option for option in options if option.lower().startswith(argument.lower())),None)
        if matcher is None:
            print("<!!> ERROR IN AUTOCOMPLETE: Something was wrong with the code and allowed an illegal autocomplete to happen")
            input("<!!> Press enter to quit")
            sys.exit()
            matcher = ""
        return matcher



# SPECIFIC COMMANDS



class cmdAbilityScore(cmd):
    def description(self) -> str:
        return "Checks the +/- modifier of a given stat number"

    def bio(self) -> str:
        b = "Enter a number between 1 and 30, and I'll calculate the modifier that is added to your roll"
        b += "\n> Normally you should be using the /stat command, but I'm here incase you wanna learn about a stat number you don't have"
        return b

    def get_acceptable_args(self) -> list:
        return [{"name":"stat_number","prompt": "Please enter a stat number (between 1 to 30)","type":"rangei","min":1,"max":30}]

    def execute(self, args:list) -> str:
        result = self.get_score(args)
        return f"> You'd have a {result} modifier with that stat number."

    def get_score(self, args:list):
        num = int(args[1])
        num2 = (num - 10) // 2
        if num2 > 0:
            result = f"+{num2}"
        else:
            result = num2
        return result

class cmdStat(cmd):
    def description(self) -> str:
        return "Checks the +/- modifier of a given stat"

    def bio(self) -> str:
        b = "Gives your modifier of a current stat that gets added when you roll said stat"
        b += "\n> Such stats are Strength, Dexterity, Constitution, Intelligence, Wisdom, and Charisma" 
        return b

    def get_acceptable_args(self) -> list:
        return [{
            "name": "stat_name", "prompt": "Please enter one of the 6 stats", "type": "custom",
            "list": ["strength","dexterity","constitution","intelligence","wisdom","charisma"]
        }]

    def execute(self, args:list) -> str:
        stat_name = self.autocomplete(args,1)
        stat_score = player_data["stats"][stat_name]
        ability_score = cmdAbilityScore()
        score = ability_score.get_score(["",stat_score])
        return f"> You have a {score} modifier in {stat_name.title()} ({stat_score})"

class cmdHelp(cmd):
    def description(self) -> str:
        return "Provides helpful information about this program"

    def bio(self) -> str:
        b = "I tell you everything you need to know about this program!"
        b += "\n> Here's a list of all the different 'help' categories..."
        b += "\n> /help commands : Gives a list of all available commands"
        b += "\n> /help cmd <command> : Explains what a specific command does"
        return b

    def get_acceptable_args(self) -> list:
        return [{
            "name": "category", "prompt": "Please enter a type of help", "type": "custom",
            "list": ["commands", "cmd"]
        }]

    def help_commands(self) -> str:
        barrier = "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="
        lister = f"\n> Here's a list of all the available commands\n{barrier}"
        for c in commands:
            command = c["cmd"]()
            lister += f"\n> /{c["id"]} : {command.description()}"
        lister += f"\n{barrier}\n> Type '/help cmd <command>' to learn more!\n"
        return lister

    def help_cmd(self, id:str) -> str:
        for c in commands:
            if c["id"] == id:
                command = c["cmd"]()
                full_text = "\n> Arguments look like (argument) for number input and <argument> for text input"
                full_text += f"\n> /{id}"
                for a in command.get_acceptable_args():
                    if a["type"] == "str" or a["type"] == "custom":
                        pre = "<"
                        suf = ">"
                    else:
                        pre = "("
                        suf = ")"
                    full_text += f" {pre}{a["name"]}{suf}"
                full_text += f"\n> {command.bio()}\n"
                return full_text
        return f"<!!> Command '/{id}' does not exist, run '/help commands' to see all commands that DO exist"

    def execute(self, args:list) -> str:
        category = self.autocomplete(args,1)
        match category:
            case "commands":
                return self.help_commands()
            case "cmd":
                return self.help_cmd(args[2])

        return ""



# Adding all commands to a list

commands = [
    {"cmd": cmdAbilityScore, "id": "ability_score"},
    {"cmd": cmdStat, "id": "stat"},
    {"cmd": cmdHelp, "id": "help"}
]

# Command referencer

def execute_command(args:list):
    for c in commands:
        if c["id"] == args[0]:
            command = c["cmd"]()
            error = command.check_validity(args)

            if error == "":
                print(command.execute(args))
            else:
                print(error)

            return
    
    print(f"<!!> Command '/{args[0]}' does not exist, run '/help commands' to see all commands that DO exist")
