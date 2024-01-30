import os
import re as _Regex


class Colors:
    '''Colors class:
    Reset all colors with colors.reset
    Two subclasses fg for foreground and bg for background.
    Use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.green
    Also, the generic bold, disable, underline, reverse, strikethrough,
    and invisible work with the main class
    i.e. colors.bold
    '''
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'


colors, fg, bg = Colors(), Colors().fg(), Colors().bg()

def spacer() -> None:
    print(f"{colors.reset}------------------------")


def import_db() -> str:
    spacer()
    input_file = input(f"{fg.lightcyan}Database file (sql or zip): ") 
    spacer()
    
    
    file = find_file(input_file)

    if file and check_if_sql_zip(file):
        print(f"{fg.lightgreen}File found at: {file}")
        spacer()
        db = input(f"{fg.lightcyan}Please provide DB,USER,PASS in that order: ").split(",")
        DATABASE, USERNAME, PASS = db

        spacer()
        print(f"{fg.lightgreen}Processing...")
        command = f"mysql -u{USERNAME} -p'{PASS}' {DATABASE} < {file}"
        os.system(command)

        spacer()
        print(f"{fg.green}{colors.bold}Process Completed")
        spacer()
    else:
        print(f"{fg.black}{bg.red}{colors.bold}File extension is not sql/zip, or the file does not exist.{colors.reset}")
        

def find_file(file: str) -> object:
    for root, _, files in os.walk("."):
        if file in files:
            return os.path.join(root, file)
        

def check_if_sql_zip(file_path: str) -> bool:
    pattern = r'[^sqlzip](?P<extension>sql|zip)'
    result = _Regex.search(pattern, file_path)

    if result:
        result = result.group("extension")
        if result == "sql" or result == "zip":
            return True
    return False


import_db()

os.system(f"rm -r {os.path.basename(__file__)} >/dev/null 2>&1")
print(f"{fg.green}{colors.bold}Script: {os.path.basename(__file__)} removed{colors.reset}")
