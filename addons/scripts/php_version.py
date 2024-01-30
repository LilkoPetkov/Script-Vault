from pathlib import Path
import os


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

        
current_path = os.getcwd()
bin_path = "/usr/local/bin"
bash_profile = None
idx = 1
lst = []
php_versions = {
    1: "TestteSt1",
}
    
# functions

def print_hr():
    print(f"{colors.reset}-------------------------")


# Code

for path in Path(current_path).rglob('.bash_profile'):
    bash_profile = str(path)

for php in Path(bin_path).rglob("php*"):
    lst.append(str(php))

lst.sort()

for php in lst:
    php_v = str(php).split("/")[4]

    if any([el for el in php_v if el.isdigit()]):
        php_versions[idx] = str(php)
        idx += 1

php_versions = dict(sorted(php_versions.items(), key=lambda x:x[1]))
php_versions = dict(sorted(php_versions.items(), key=lambda x:x[0]))

print_hr()

print(f"{fg.lightcyan}{colors.bold}Initiating script...{colors.reset}")

print_hr()

for k, v in php_versions.items():
    value = v.split("/")[4]
    print(f"{k} - {value}")

print_hr()
u_input = int(input(f"{fg.lightcyan}{colors.bold}Please choose PHP version:\n{colors.reset}"))
print_hr()

if u_input in php_versions:
    with open(bash_profile, "a") as f:
        f.write(f"alias php='{php_versions[u_input]}'\nalias composer='{php_versions[u_input]} -d memory_limit=4096M /usr/local/bin/composer.phar'")
        print(f"{fg.lightcyan}{colors.bold}PHP version changed{colors.reset}")
        print_hr()
        os.system("rm -f php_version.py")
        print(f"{fg.green}{colors.bold}Script deleted{colors.reset}")
        print_hr()
        print(f"{fg.lightcyan}{colors.bold}Please make sure to -> source .bash_profile{colors.reset}")
else:
    print(f"{bg.red}{colors.bold}Invalid input.{colors.reset}")

