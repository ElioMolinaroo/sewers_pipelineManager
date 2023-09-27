from pathlib import Path
import os

from libs import fileLibs
from libs import loginLibs
from libs import socketLibs


# Opens a maya file in a new instance of maya through a mel launcher it creates
def openMayaFile(file_path: str):
    # Python code for MEL launcher
    python_launcher_code = f'import maya.cmds as cmds; cmds.file(r"{file_path}", force=1, open=1); cmds.commandPort(name=":{socketLibs.PORT}", sourceType="python");'
    # Create the MEL file
    mel_launcher_file = open('temp/temp_mel_launcher.mel', 'w')
    mel_launcher_file.flush()
    mel_launcher_file.close()

    # Write the MEL launcher code encoded python to the MEL file
    fileLibs.pythonToMel(python_launcher_code, 'temp/temp_mel_launcher.mel')

    launcher_full_path = Path.cwd() / 'temp/temp_mel_launcher.mel'

    # get the maya path
    with open(Path(Path(os.getenv('USERPROFILE')) / '.sewers' / 'databases/mayaPath.txt'), 'r') as file:
        maya_path = file.read()
        file.close()

    # Open the mel launcher which opens the file
    if len(maya_path) != 0:
        maya_path = Path(maya_path)
        fileLibs.openFileWithApp(launcher_full_path, maya_path)
    else:
        print("\nERROR: Couldn't find maya path, try to run getAppsData...\n")


# Get the path to the clicked item in the file explorer
def getClickedFilePath(explorer_widget):
    '''# Get the root path
    current_project_cookies = loginLibs.loadJsonData('databases/projectData/currentProject.json')
    root_path = current_project_cookies['path']'''

    # Get the selected item name
    item = explorer_widget.currentIndex()

    selected_item_path = fileLibs.getItemPath(item)

    '''# Reconstruct the correct path
    path_string = '//'.join(selected_item_path)
    project_name = root_path.split('/')[-1]
    path_within_project = path_string.split(project_name)[-1]
    path_within_project = path_within_project[2:]

    full_path = Path(root_path) / path_within_project'''

    return [selected_item_path, item]
