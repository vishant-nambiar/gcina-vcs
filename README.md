# gcina
-----------------------------------------------
gcina is a version control system CLI, similar to git or mercurial. gcina initializes your desired directory as a repository and stores your work efficiently both speed and memory wise, helping you recover or revert to a previous work state anytime. The name gcina comes from the Zulu word 'gcina' which means to save or keep.

## How it works
You can run gcina on any directory that you would like to use as a repository to store your work. To do so, you have to tell gcina to commit it, which is explained further below. A commit can be thought of as a snapshot of your work in time, something you would like to save in case you need to come back to it later. Every commit generates a unique SHA1 hash which is used to identify the commit. All commits and their info can be viewed. Every commit is stored in a compressed format to use only minimal space, and is uncompressed when you wish to revert to it. When you revert to a commit, your work state is saved, and you can return to it later if you wish to. 

## How to use it
gcina has been developed for *nix systems with bash. It should work in Windows with WSL too.
To use gcina, download the gcina script from the repo and paste it in your `bin` directory. It's location may differ based upon your OS. You can also paste it in the directory that you want to convert to a repo and use the script directly from there.
After this, `cd` to the directory you want to use as a repo to run gcina. You can run different gcina commands from the terminal in the form `gcina <command> <options>`.
The main functionalities available with gcina are:
- `init`: Initialize a directory to be a gcina repo. Will give an error if directory is already initialized. Example command: `gcina init`
- `commit <commit message>`: Store your current working directory as a commit. Mandatory message argument describing your commit. Examlple command: `gcina commit 'initial commit'`
- `log`: Displays a list of all commits and addtional information about them, i.e hash, author, datetime created. Example command: `gcina log`
- `checkout <commit hash>`: restores your working directory to the state it was when you made the commit with the hash provided. The mandatory hash of the desired commit to revert to can be found and copied from `log`. Example command `gcina checkout 4c90aa70f10a28ccd75988f2e61355fb987e490e`.
- Additionally, when reverting to a previous commit, the state of the working directory before the `checkout` command was used is cached. This cached work state can be recovered using `gcina checkout workdir`. If a commit was made after checkout, then the cached work state is deleted.

## Dependencies
gcina uses only Python standard libraries, specifically sys, subprocess, inspect, hashlib and shutil.

## License
This project is covered under the [GNU General Public License V3](https://www.gnu.org/licenses/gpl-3.0.en.html).
