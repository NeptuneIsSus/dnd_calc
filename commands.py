import sys

commands = {}
player_data = {}



# BASE COMMAND CLASS



class cmd:

    # Specific cmd functions

    def description(self) -> str:
        return "Description"
    
    def execute(self, args:list):
        pass
    
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

    def get_acceptable_args(self) -> list:
        return [{"name":"stat_number","prompt": "Please enter a stat number (between 1 to 30)","type":"rangei","min":1,"max":30}]

    def execute(self, args:list):
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

    def get_acceptable_args(self) -> list:
        return [{
            "name": "stat_name", "prompt": "Please enter one of the 6 stats", "type": "custom",
            "list": ["strength","dexterity","constitution","intelligence","wisdom","charisma"]
        }]

    def execute(self, args: list):
        stat_name = self.autocomplete(args,1)
        stat_score = player_data["stats"][stat_name]
        ability_score = cmdAbilityScore()
        score = ability_score.get_score(["",stat_score])
        return f"> You have a {score} modifier in {stat_name}"



# Adding all commands to a list

commands = {
    "ability_score": cmdAbilityScore,
    "stat": cmdStat
}

# Command referencer

def execute_command(args:list):
    if args[0] in commands:
        c = commands[args[0]]()
        error = c.check_validity(args)
        if error == "":
            print(c.execute(args))
        else:
            print(error)
    else:
        print(f"<!!> Command '/{args[0]}' does not exist, run '/help commands' to see all commands that DO exist")
