import sys
import os
import subprocess
from inspect import cleandoc
import hashlib
import shutil

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
        mkdir .repo/snapshots
        touch .repo/logs
        mkdir .repo/cache""")
    bash_execute(command)


def commit():
    file_list = bash_execute('ls -a')
    if('.repo' not in file_list):
        raise Exception("Directory uninitialized.")
    elif(len(sys.argv) < 3):
        raise Exception("Please enter commit message.")

    #clear cache directory
    cache_dir_files = bash_execute("ls -a .repo/cache/").split("\n")[2:-1]
    for file in cache_dir_files:
        bash_execute(f"rm -r .repo/cache/{file}")
        
    
    
    #make new commit directory with temp as name
    user = bash_execute('whoami')
    date_time = bash_execute("date")
    commit_message = sys.argv[2]
    hash = hashlib.sha1( bytes(user + date_time + commit_message, 'utf-8') ).hexdigest()
    bash_execute(f"mkdir .repo/snapshots/temp")
    
    #copy working directory files into new temp directory
    bash_execute(f'rsync -a --exclude=.repo --exclude=vcs --exclude=scripts.py ./ .repo/snapshots/temp')

    #compress the directory into a file named with the hash and remove temp
    shutil.make_archive(f".repo/snapshots/{hash}", "zip", f".repo/snapshots/temp")
    bash_execute("rm -r .repo/snapshots/temp")

    
    #store commit info in logs file
    logs_file = open(f".repo/logs", "a")
    logs_file.write('\n\n' + hash + '\n' + user + date_time + commit_message + '\n')
    logs_file.close()
    


def log():
    log_output = ''
    
    file = open(f".repo/logs", "r")
    file_data = file.read()
    commits = file_data.split('\n\n')[1:]
    file.close()
    
    for commit in commits:
        #extracting commit info
        commit = commit.split('\n')
        commit = list( filter( lambda a: a != '', commit) )
        
        commit_hash = commit[0]
        user = commit[1]
        date_time = commit[2]
        message = commit[3]
        
        log_output += cleandoc(f"""
            Snapshot: {commit_hash}
            Author: {user}
            Date & time: {date_time}
            Message: {message}""") + '\n\n'
    
    print(log_output)



def checkout():
    if len(sys.argv) < 3:
        raise Exception("Please provide commit hash")

    hash = sys.argv[2]
    commit_file = f".repo/snapshots/{hash}"

    #checks if hash exists
    commit_list = bash_execute("ls .repo/snapshots/")
    commit_list = commit_list.split('\n')[:-1]
    if f"{hash}.zip" not in commit_list:
        raise Exception("Hash not found.")
    
    #save workding directory
    bash_execute(f'rsync -a --exclude=.repo --exclude=vcs --exclude=scripts.py ./ .repo/cache')
    
    file_list = bash_execute("ls -a")
    file_list = file_list.split('\n')[2:-1]
    for file in file_list:
        if file not in ['.repo', 'scripts.py', 'vcs']:
            bash_execute(f"rm -r {file}")

    #unzip hash file to working directory
    shutil.unpack_archive(f".repo/snapshots/{hash}.zip")
    
    

     