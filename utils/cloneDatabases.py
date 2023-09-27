from pathlib import Path
from os import getenv
import shutil

def cloneDatabases():
    databases_path = Path.cwd() / 'databases'
    target_folder = Path(getenv('USERPROFILE')) / '.sewers'
    target_path = target_folder / 'databases'
    # Make the sewers directory
    target_folder.mkdir(exist_ok=True)
    # Copy databases into it
    shutil.copytree(databases_path, target_path, dirs_exist_ok=True)

    # Remove __pycache__ folder
    shutil.rmtree(target_path / '__pycache__')
    shutil.rmtree(target_path / 'projectData' / '__pycache__')

cloneDatabases()
