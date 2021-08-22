from os import mkdir
import subprocess
from inspect import cleandoc

#Executes any number of bash commands, one on each line
def bash_execute(commands):
    commands = commands.split('\n')
    last_output = ''
    for command in commands:
        last_output = subprocess.run(command.split(' '), stdout=subprocess.PIPE, text=True).stdout
    return last_output

def init():
    file_list = bash_execute("ls -a")
    if ".repo" in file_list:
        raise Exception("Directory already initialized. If you think this is a mistake, please delete '.repo' before continuing.")
    
    command = cleandoc("""
        mkdir .repo
        mkdir .repo/refs
        touch .repo/refs/tags
        mkdir .repo/snapshots""")
    bash_execute(command)

def commit():
    file_list = bash_execute('ls -a')
    if('.repo' not in file_list):
        raise Exception("Directory uninitialized.")
    
    file_list = bash_execute('ls .repo/snapshots/').split()
    num_of_files = len(file_list)
    bash_execute(f"mkdir .repo/snapshots/{num_of_files + 1}")