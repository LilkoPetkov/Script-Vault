from pathlib import Path
import os


current_path = os.getcwd()
apps = {

}

id = 1

for path in Path(current_path).rglob('wp-config.php'):
    app_name = str(path).split("/")[4]
    full_path = str(path).replace("/wp-config.php", "")
    apps[id] = [app_name, full_path]

    id += 1

print("-----------------------------------\n")

print("WordPress Apps Found:")

print("-----------------------------------\n")

for k, v in apps.items():
    print(f"{k}: {v[0]}")


print("-----------------------------------\n")

user_input = int(input("Please select app ID: \nApp ID: "))

print("-----------------------------------\n")

if user_input in apps:
    os.system(f"cd {apps[user_input][1]}; wget -q https://sportcentre.info/sandr.py; python3 sandr.py")

    print("-----------------------------------\n")
else:
    print(f"ID {user_input} does not exist")

    print("-----------------------------------\n")

os.system("rm -f script.py")
os.system(f"rm -f {apps[user_input][1]}/sandr.py")

