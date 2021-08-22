import sys
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
    elif(len(sys.argv) < 3):
        raise Exception("Please enter commit message.")
    
    #makes new commit directory with commit number as name
    file_list = bash_execute('ls .repo/snapshots/').split()
    num_of_files = len(file_list)
    new_file_number = num_of_files + 1
    bash_execute(f"mkdir .repo/snapshots/{new_file_number}")
    
    #copies working directory files into new commit directory
    bash_execute(f'rsync -a --exclude=.repo --exclude=vcs --exclude=scripts.py ./ .repo/snapshots/{new_file_number}')
    
    #creates .commit file inside snapshot and stores info inside
    user = bash_execute('whoami')
    date_time = bash_execute("date")
    commit_message = sys.argv[2]
    commit_file = open(f".repo/snapshots/{new_file_number}/.commit", "w")
    commit_file.write(user + date_time + commit_message + '\n')
    commit_file.close()