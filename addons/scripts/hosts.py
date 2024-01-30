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


def hosts_file_add(domain, IP):
    return os.system(f"echo '{IP} {domain} www.{domain}' >> /etc/hosts")


def show_hosts_file():
    return os.system(f"tail -5 /etc/hosts")
  

def hosts_file_remove(domain):
    return os.system(f'echo "$(grep -v "{domain}" /etc/hosts)" > /etc/hosts')
    

def ping_check(domain):
    return os.system(f"ping -c3 {domain}")


domain = input(f"{bg.cyan}Please add domain: {colors.reset}")
IP = input("Please add IP for the domain: ")

print("Initialising hosts file script... ")

hosts_file_add(domain, IP)

print("Hosts file contents: ")

show_hosts_file()

user_input_0 = input("Would you like to perform a ping test? Yes/No \n")

if user_input_0 == "Yes" or user_input_0 == "y" or user_input_0 == "yes":
    ping_check(domain)

user_input = input("Would you like to delete the domain from the hosts file? Yes/No \n")

if user_input == "Yes" or user_input == "y" or user_input == "yes":
    hosts_file_remove(domain)
    print("Entry removed from the hosts file. ")
    
    show_hosts_file()

print("Closing script. ")
