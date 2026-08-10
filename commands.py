commands = {}

class cmd:
    def description(self) -> str:
        return "Description"
    
    def execute(self, args:list):
        pass
    
    def get_acceptable_args(self) -> list:
        return []



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
            match a["type"]:
                case "int":
                    try:
                        num = int(args[i + 1])
                        continue
                    except ValueError:
                        return f"<!!> Argument {i + 1} ({args[i + 1]}) must be a whole number!"
                case "float":
                    try:
                        num = float(args[i + 1])
                        continue
                    except ValueError:
                        return f"<!!> Argument {i + 1} ({args[i + 1]}) must be a number!"
                case "percent":
                    try:
                        num = float(args[i + 1])
                        if num <= 1.0 and num >= 0.0:
                            continue
                        else:
                            return f"<!!> Argument {i + 1} ({args[i + 1]}) must be a value between 0.0 and 1.0!"
                    except ValueError:
                        return f"<!!> Argument {i + 1} ({args[i + 1]}) must be a number!"
                case "range":
                    try:
                        num = float(args[i + 1])
                        if num <= float(a["max"]) and num >= float(a["min"]):
                            continue
                        else:
                            return f"<!!> Argument {i + 1} ({args[i + 1]}) must be a value between {a["min"]} and {a["max"]}!"
                    except ValueError:
                        return f"<!!> Argument {i + 1} ({args[i + 1]}) must be a number!"
                case "rangei":
                    try:
                        num = int(args[i + 1])
                        if num <= int(a["max"]) and num >= int(a["min"]):
                            continue
                        else:
                            return f"<!!> Argument {i + 1} ({args[i + 1]}) must be a value between {a["min"]} and {a["max"]}!"
                    except ValueError:
                        return f"<!!> Argument {i + 1} ({args[i + 1]}) must be a number!"
                case "str":
                    continue
                case _:
                    return "<!!> Failed due to bug in the code"

        return ""

class cmdAbilityScore(cmd):
    def description(self) -> str:
        return "Checks the +/- modifier of a given stat number"

    def get_acceptable_args(self) -> list:
        return [{"name":"stat_number","type":"rangei","min":1,"max":30}]

    def execute(self, args:list):
        num = int(args[1])
        result = 0

        if num > 30:
            result = "NAN"
        elif num == 30:
            result = 10
        elif num >= 28:
            result = 9
        elif num >= 26:
            result = 8
        elif num >= 24:
            result = 7
        elif num >= 22:
            result = 6
        elif num >= 20:
            result = 5
        elif num >= 18:
            result = 4
        elif num >= 16:
            result = 3
        elif num >= 14:
            result = 2
        elif num >= 12:
            result = 1
        elif num >= 10:
            result = 0
        elif num >= 8:
            result = -1
        elif num >= 6:
            result = -2
        elif num >= 4:
            result = -3
        elif num >= 2:
            result = -4
        elif num == 1:
            result = -5
        else:
            result = "NAN"

        if result == "NAN":
            return "<!!> Given stat number exceeds the stat caps (1-30)"
        else:
            if result > 0:
                result = f"+{result}"
            return f"> You'd have a {result} modifier with that stat number."

# AAAA

commands = {
    "ability_score": cmdAbilityScore
}

# AAAAA pt 2

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