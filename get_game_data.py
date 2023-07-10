import os
import json # to work w/ json files
import shutil # will allow copying & overriding operations
from subprocess import PIPE, run # will allow running almost any terminal command
import sys # access to command line arguments  

def main(source, target):
    cwd = os.getcwd()
    # will join the path based on operating system
    source_path = os.path.join(cwd, source) 
    target_path = os.path.join(cwd, target) 
    
    

# checks that file was ran directly 
# won't execute anything if a function or class were imported from this file
if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and target directory only.")
    
    # strip off name of python file & get two arguments to be stored into separate variables
    source, target = args[1:]
    main(source, target)