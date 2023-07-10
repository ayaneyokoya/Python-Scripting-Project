import os
import json # to work w/ json files
import shutil # will allow copying & overriding operations
from subprocess import PIPE, run # will allow running almost any terminal command
import sys # access to command line arguments  

GAME_DIR_PATTERN = "game"
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE_COMMAND = ["go", "build"]

def find_all_game_paths(source):
    game_paths = []
    
    # will walk recursively through source directory
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)
        
        break
    
    return game_paths

def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, '')
        new_names.append(new_dir_name)
    
    return new_names

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

# recursive copy method
def copy_and_overwrite(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)

def make_json_metadata_file(path, game_dirs):
    data = {
        "gameNames": game_dirs,
        "numberOfGames": len(game_dirs)
    }
    # using "with" will automatically close the file
    with open(path, "w") as f:
        json.dump(data, f)
        
# method to compile the code inside directory
def compile_game_code(path):
    code_file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            # checks if file is a .go file
            if file.endswith(GAME_CODE_EXTENSION):
                code_file_name = file
                break
        break
    
    if code_file_name is None:
        return
    
    command = GAME_COMPILE_COMMAND + [code_file_name]
    
def run_command(command, path):
    cwd = os.getcwd()
    os.chdir(path)
    
    # stdout & stdin: location where command is accepting input & dumping output
    # PIPE makes a bridge between python code and process used to run command
    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)

def main(source, target):
    cwd = os.getcwd()
    # will join the path based on operating system
    source_path = os.path.join(cwd, source) 
    target_path = os.path.join(cwd, target) 
    
    # finds game paths (directories) from source directory
    game_paths = find_all_game_paths(source_path)
    # will give just the directory name but removes "game"
    new_game_dirs = get_name_from_paths(game_paths, "_game")
    
    create_dir(target_path)
    
    # zip takes matching elements from two arrays and combine them into a tuple
    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
        compile_game_code(dest_path)
    
    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata_file(json_path, new_game_dirs)

# checks that file was ran directly 
# won't execute anything if a function or class were imported from this file
if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and target directory only.")
    
    # strip off name of python file & get two arguments to be stored into separate variables
    source, target = args[1:]
    main(source, target)