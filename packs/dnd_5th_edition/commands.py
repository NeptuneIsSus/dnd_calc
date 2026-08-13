import sys
import random

commands = []
player_data = {}



# UNIVERSAL VALUES



stat_list = ["strength","dexterity","constitution","intelligence","wisdom","charisma"]
skill_list = ["acrobatics", "animal_handling", "arcana", "athletics", "deception", "history", "insight", "intimidation", "investigation", "medicine", "nature", "perception", "performance", "persuasion", "religion", "sleight_of_hand", "stealth", "survival"]
skill_reference = {
        "acrobatics": "dexterity",
        "animal_handling": "wisdom",
        "arcana": "intelligence",
        "athletics": "strength",
        "deception": "charisma",
        "history": "intelligence",
        "insight": "wisdom",
        "intimidation": "charisma",
        "investigation": "intelligence",
        "medicine": "wisdom",
        "nature": "intelligence",
        "perception": "wisdom",
        "performance": "charisma",
        "persuasion": "charisma",
        "religion": "intelligence",
        "sleight_of_hand": "dexterity",
        "stealth": "dexterity",
        "survival": "wisdom"
        }



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

    def check_individual_validity(self, input:str, valid:dict, index:int = 0) -> str:
        multiple = f"{index} " if index else ""
        match valid["type"]:
            case "int":
                try:
                    num = int(input)
                    return ""
                except ValueError:
                    return f"<!!> Argument {multiple}({input}) must be a whole number!"
            case "float":
                try:
                    num = float(input)
                    return ""
                except ValueError:
                    return f"<!!> Argument {multiple}({input}) must be a number!"
            case "percent":
                try:
                    num = float(input)
                    if num <= 1.0 and num >= 0.0:
                        return ""
                    else:
                        return f"<!!> Argument {multiple}({input}) must be a value between 0.0 and 1.0!"
                except ValueError:
                    return f"<!!> Argument {multiple}({input}) must be a number!"
            case "range":
                try:
                    num = float(input)
                    if num <= float(valid["max"]) and num >= float(valid["min"]):
                        return ""
                    else:
                        return f"<!!> Argument {multiple}({input}) must be a value between {valid["min"]} and {valid["max"]}!"
                except ValueError:
                    return f"<!!> Argument {multiple}({input}) must be a number!"
            case "rangei":
                try:
                    num = int(input)
                    if num <= int(valid["max"]) and num >= int(valid["min"]):
                        return ""
                    else:
                        return f"<!!> Argument {multiple}({input}) must be a value between {valid["min"]} and {valid["max"]}!"
                except ValueError:
                    return f"<!!> Argument {multiple}({input}) must be a number!"
            case "str":
                return ""
            case "custom":
                options = valid["list"]
                matcher = next((option for option in options if option.lower().startswith(input.lower())),None)
                if matcher is None:
                    lister = ""
                    for item in options:
                        lister += f"{item}, "
                    return f"<!!> Argument {multiple}({input}) must match one of these options!\n<!!> {lister}"
                else:
                    return ""

            case _:
                return "<!!> Failed due to bug in the code"

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
        # setting "default" to something makes the argument optional

        valids = self.get_acceptable_args()

        i = 1
        while True:
            # print(f"Next (index:{i})")

            if i > len(valids):
                # print("finished adding to command")
                break

            if len(args) > i:
                # print(f"skipping argument {i}",args,len(args))
                is_valid = self.check_individual_validity(args[i],valids[i - 1],i)
                if is_valid:
                    return is_valid
                i += 1
                continue

            if "default" in valids[i - 1]:
                # print("default found and now setting")
                args.append(valids[i - 1]["default"])
                continue

            while True:
                # print(f"asking user for argument {i}")
                given = input(f"{valids[i - 1]["prompt"]}: ")
                if " " in given:
                    print("<!!> Individual arguments cannot contain spaces")
                    continue
                is_valid = self.check_individual_validity(given,valids[i - 1])
                if is_valid == "":
                    i += 1
                    args.append(given)
                    break
                else:
                    print(is_valid)
        
        
        return ""

    def autocomplete(self,args,index) -> str:
        argument = args[index]
        acceptable_argument = self.get_acceptable_args()[index - 1]
        strict = ("default" in acceptable_argument)
        options = acceptable_argument["list"]
        matcher = next((option for option in options if option.lower().startswith(argument.lower())),None)
        if matcher is None:
            if strict:
                print("<!!> ERROR IN AUTOCOMPLETE: Something was wrong with the code and allowed an illegal autocomplete to happen")
                input("<!!> Press enter to quit")
                sys.exit()
                matcher = ""
            else:
                matcher = acceptable_argument["default"]
        return matcher

    def custom_autocomplete(self,text:str,options:list[str]) -> str:
        if text == "":
            return ""
        matcher = next((option for option in options if option.lower().startswith(text.lower())),None)
        if matcher is None:
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
        num = self.get_score(args)
        if num > 0:
            result = f"+{num}"
        else:
            result = num
        return f"> You'd have a {result} modifier with that stat number."

    def get_score(self, args:list) -> int:
        num = int(args[1])
        num2 = (num - 10) // 2
        return num2

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
            "list": stat_list
        }]

    def get_modifier(self,stat_name:str) -> list:
        stat_score = player_data["stats"][stat_name]
        ability_score = cmdAbilityScore()
        score = ability_score.get_score(["",stat_score])
        return [score,stat_score]


    def execute(self, args:list) -> str:
        stat_name = self.autocomplete(args,1)
        result = self.get_modifier(stat_name)
        if result[0] > 0:
            num = f"+{result[0]}"
        else:
            num = result[0]
        return f"> You have a {num} modifier in {stat_name.title()} ({result[1]})"

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
        lister += f"\n{barrier}\n> Type '/help cmd <command>' to learn more!"
        return lister

    def help_cmd(self, id:str) -> str:
        for c in commands:
            if c["id"] == id:
                command = c["cmd"]()
                full_text = "\n> Arguments look like (argument) for number input and <argument> for text input. ? means that the argument is optional"
                full_text += f"\n> /{id}"
                for a in command.get_acceptable_args():
                    if a["type"] == "str" or a["type"] == "custom":
                        pre = "<"
                        suf = ">"
                    else:
                        pre = "("
                        suf = ")"
                    full_text += f" {pre}{a["name"]}{"?" if "default" in a else ""}{suf}"
                full_text += f"\n>\n> {command.bio()}"
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

class cmdSkill(cmd):
    def description(self) -> str:
        return "Checks the +/- modifier of a given skill"

    def bio(self) -> str:
            b = "Gives your modifier of a current skill that gets added when you roll said skill"
            b += "\n> Such skills are Acrobatics, Animal Handling, Arcana, Athletics, Deception, History, Insight, Intimidation, Investigation,\n> Medicine, Nature, Perception, Performance, Persuasion, Religion, Sleight of Hand, Stealth, and Survival" 
            return b

    def get_acceptable_args(self) -> list:
        return [{
            "name": "skill_name", "prompt": "Please enter one of the 18 skills", "type": "custom",
            "list": skill_list
        }]

    def get_modifier(self,skill_name:str) -> list:
        stat_name = skill_reference[skill_name]
        result = cmdStat().get_modifier(stat_name)
        score = result[0]
        if skill_name in player_data["proficiency_abilities"]:
            proficient = True
            score += player_data["proficiency_bonus"]
        else:
            proficient = False
        return [score,stat_name,proficient]

    def execute(self, args: list) -> str:
        skill_name = self.autocomplete(args,1)
        result = self.get_modifier(skill_name)
        if result[0] > 0:
            num = f"+{result[0]}"
        else:
            num = result[0]
        msg = f"> You have a {num} modifier in {skill_name.title()} ({result[1].title()})"
        if result[2]:
            msg += " (Proficient)"
        return msg

class cmdRoll(cmd):
    def description(self) -> str:
        return "Automatically rolls dice for you"

    def bio(self) -> str:
        b = "Randomly generates a number to simulate a die roll, ya hear? It's unbiased John! No the program does not have a grudge against YOU SPECIFICALLY"
        b += "\n> Die rolls are usually types as '(die_count)d(die_sides)+/-(modifier). Some examples being 1d20, 2d10, 1d8+2, 10d6-2"
        b += "\n> That's only for custom rolls though, you can also just type a Stat, Skill, Weapon, Spell, Bonus Action you name it! /roll p for an easy Perception check"
        b += "\n> You can also add either advantage or disadvantage after the roll type, you roll an extra time and choose the higher/lower roll respectively"
        b += "\n> Adding a number after the dis/advantage (1d20 adv 3) chooses how many sets it chooses from, in this case it'd roll 3 extra sets and choose between the three results"
        b += "\n> Knock yourself out! This is what the calculator was made for! Go /roll 100d100+100 adv 100 if you want, it's your choice."
        return b

    def get_acceptable_args(self) -> list:
        return [
            {"name": "roll_type", "prompt": "Please enter a roll type like a skill or weapon, or custom roll (2d12+3)","type":"str"},
            {
                "name": "advantage", "prompt": "Add either an advantage or disadvantage, or leave blank for neither","type":"custom","default":"",
                "list": ["advantage","disadvantage"]
            },
            {"name": "adv_count", "prompt": "How many times should we count your dis/advantage (default is 1)","type":"int","default":1}
        ]

    def get_adv(self,adv_type:str,adv_count:int) -> list:
        sets = 1
        choose_highest = True
        adv = self.custom_autocomplete(adv_type,["advantage","disadvantage"])
        # print(adv)
        if adv:
            sets += adv_count
            if adv == "disadvantage":
                choose_highest = False
        return [choose_highest, sets]

    def roll(self,die:int,sides:int,modifier:int = 0,sets:int=1,choose_highest:bool=True) -> list:
        results:list[int] = []
        result_info:list[str] = []
        # print(sets,range(sets))
        # print(die,range(die))
        for s in range(sets):
            roll = 0
            roll_info:list[str] = []
            for d in range(die):
                r = random.randint(1,sides)
                roll += r
                roll_info.append(str(r))
            results.append(roll + modifier)
            mod = (f"+{modifier}" if modifier>0 else str(modifier)) if modifier else ""
            result_info.append(f"({", ".join(roll_info)}) --> {roll}{mod}" + (f" --> {roll + modifier}" if modifier else ""))

        if choose_highest:
            chosen = max(results)
        else:
            chosen = min(results)

        return [chosen,result_info]

    def custom_roll(self,code:str,adv_type:str="",adv_count:int=1) -> list:
        # die, sides, modifier
        error = ""

        if not "d" in code:
            return [False, "<!!> An improper dice roll was given (You forgot the d), type /help cmd roll to see what a proper roll looks like"]

        try:
            if "+" in code:
                splitter = code.split("+")
                code2 = splitter[0]
                error = "The number after the + must be a positive whole number" # for TypeError info
                modifier = int(splitter[1])
            elif "-" in code:
                splitter = code.split("-")
                code2 = splitter[0]
                error = "The number after the - must be a positive whole number" # for TypeError info
                modifier = -int(splitter[1])
            else:
                code2 = code
                modifier = 0

            splitter = code2.split("d")

            error = "Illegal die count, must be a whole number" # for TypeError info
            die = int(splitter[0])

            error = "Illegal side count, must be a whole number" # for TypeError info
            sides = int(splitter[1])

            error = "Unidentified" # for TypeError info
            adv = self.get_adv(adv_type,adv_count)
            # print("ADV:",adv)
            
            roll = self.roll(die,sides,modifier,adv[1],adv[0])

            return [True, roll[0], roll[1]]
        except ValueError:
            return [False, f"<!!> An improper dice roll was given ({error}), type /help cmd roll to see what a proper roll looks like"]

    def stat_roll(self,stat_name:str,adv_type:str="",adv_count:int=1) -> list:
        # print("ADV COUNT:",adv_count)
        roll = []
        modifier = cmdStat().get_modifier(stat_name)[0]
        if modifier:
            modifier = f"+{modifier}" if modifier>0 else str(modifier)
            code = f"1d20{modifier}"
        else:
            code = "1d20"

        roll = self.custom_roll(code,adv_type,adv_count)
        roll[0] = code
        return roll

    def execute(self, args: list) -> str:
        # print(args)
        a_t = args[2]
        a_c = int(args[3])

        stat_name = self.custom_autocomplete(args[1],stat_list)
        if stat_name != "":
            result = self.stat_roll(stat_name,a_t,a_c)
            msg:list[str] = []
            msg.append(f"Rolling for {stat_name.title()} ({result[0]})")
            msg.extend(result[2])
            msg.append(f"Result: {result[1]}")
            return f"> {"\n> ".join(msg)}"

        try:
            check = int(args[1][0]) # Checks if the first character is a number
            result = self.custom_roll(args[1],a_t,a_c)
            if result[0]:
                msg:list[str] = result[2]
                msg.append(f"Result: {result[1]}")
                return f"> {"\n> ".join(msg)}"
            else:
                return result[1]
        except ValueError:
            return f"<!!> Either your roll type wasn't found, or you typed the code wrong. type /help cmd roll to see what a proper roll looks like"

    

# Adding all commands to a list

commands = [
    {"cmd": cmdAbilityScore, "id": "ability_score"},
    {"cmd": cmdStat, "id": "stat"},
    {"cmd": cmdHelp, "id": "help"},
    {"cmd": cmdSkill, "id": "skill"},
    {"cmd": cmdRoll, "id": "roll"}
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
