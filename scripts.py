import subprocess
from inspect import cleandoc

def bash_execute(commands):
    commands = commands.split('\n')
    last_output = ''
    for command in commands:
        last_output = subprocess.run(command.split(' '), stdout=subprocess.PIPE, text=True).stdout

def init():
    file_list = subprocess.run(['ls', '-a'], stdout=subprocess.PIPE, text=True).stdout
    
    if ".repo" in file_list:
        raise Exception("Directory already initialized.")
    
    command = cleandoc("""
        mkdir .repo
        mkdir .repo/refs
        touch .repo/refs/tags
        touch .repo/snapshots""")
    bash_execute(command)