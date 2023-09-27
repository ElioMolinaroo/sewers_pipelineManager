import json
import shutil
from pathlib import Path
import os

from PyQt6.QtWidgets import QFileDialog

from libs import loginLibs
from libs import uiLibs

CURRENT_PROJECT_DATABASE = Path(os.getenv('USERPROFILE')) / '.sewers' / 'databases' / 'projectData' / 'currentProject.json'
PROJECTS_DATABASE = Path(os.getenv('USERPROFILE')) / '.sewers' / 'databases' / 'projectData' / 'projects.json'


# Changes the project name
def changeProjectName(project_name, dictionary):
    dictionary['name'] = project_name
    return dictionary


# Recursive algorithm going into nested dictionaries to create folders
def createFolderStructure(dictionary, root_dir):
    if 'name' in dictionary:
        directory_path = root_dir / dictionary['name']
        directory_path.mkdir(exist_ok=True)
        root_dir = directory_path

    if 'children' in dictionary:
        for child in dictionary['children']:
            createFolderStructure(child, root_dir)

        # Creates a maya workspace inside folders named 'maya'
        if dictionary['name'] == 'maya':
            createMayaWorkspace(root_dir)


# Copies the maya workspace file from the databases folder and pastes it at the given path
def createMayaWorkspace(path):
    workspace_path = Path(os.getenv('USERPROFILE')) / '.sewers' / 'databases' / 'projectData' / 'workspace.mel'
    destination_path = Path(path)

    shutil.copy2(workspace_path, destination_path)


# Opens a file dialog and returns the user selected folder
def fileDialogReturnFolder(ui, dialog_title):
    folder = QFileDialog.getExistingDirectory(ui, dialog_title, 'C:/')
    return folder


# Gets the name of the end folder in a path
def getFolderName(path=str):
    elements = path.split('/')
    folder_name = elements[-1]
    return folder_name


# Creates the formatting of the project data into a dictionary entry
def formatProjectData(project_name: str, project_path: str, project_artists: list, assets_path: str, shots_path: str, project_type: str):
    return {"name": project_name,
            "path": project_path,
            "artists": project_artists,
            "assets_path": assets_path,
            "shots_path": shots_path, 
            "project_type": project_type}


# Sets the project UI widgets to their default
def setProjectAsDefault(ui):
    ui.projectNameLabel.setText('NO PROJECT')
    model = ui.model
    ui.fileManagerColumnView.setRootIndex(model.index('C:/'))


# Queries the data of the current project and returns them as a tuple
def getCurrentProject(database_path):
    data = loginLibs.loadJsonData(database_path)

    # Check if there is a project currently opened
    if len(data) != 0:
        return [data['name'], data['path'], data['artists']]
    else:
        return ['', '', '']


# Sets the current project according to the provided cookies list
def setCurrentProject(ui, current_project_database=CURRENT_PROJECT_DATABASE):
    dict_project_cookies = loginLibs.loadJsonData(current_project_database)
    current_project_path = getCurrentProject(CURRENT_PROJECT_DATABASE)[1]

    if len(dict_project_cookies) != 0 and len(current_project_path) != 0:
        project_cookies = list(dict_project_cookies.values())
        # Sets the project name
        ui.projectNameLabel.setText(str.upper(project_cookies[0]))
        # Sets the project path
        model = ui.model
        ui.fileManagerColumnView.setRootIndex(model.index(project_cookies[1]))
        # Update the UI
        uiLibs.enableButtons(ui)
        uiLibs.projectTypeChangeUI(ui)

        print(f'\nProject {str.upper(project_cookies[0])} has been set successfully.\n')
    else:
        print('\nNo project cookies were found...\n')


# Filters item in a given list according to the letters being typed
def filter_items(search_bar, search_list):
    # Sets the search text to the content of the search bar
    search_text = search_bar.text()

    # Iterates through the items in the list to fins the potential matches
    for i in range(search_list.count()):
        item = search_list.item(i)
        # Hides elements that don't match the string
        if search_text.lower() in item.text().lower():
            item.setHidden(False)
        else:
            item.setHidden(True)


# Create the project json file
def createProjectData(project_path):
    # Create the data
    project_data = {"shots": {}, "assets": {}}

    # Write the data to the project_data file
    filename = 'project_data.json'
    filepath = Path(project_path) / filename
    with open(filepath, 'w') as file:
        json.dump(project_data, file)
        file.close()


# Queries the current project data if it exists, returns an empty string otherwise
def getProjectData():
    # Get current database data
    current_project_cookies = loginLibs.loadJsonData(CURRENT_PROJECT_DATABASE)
    database_file = Path(current_project_cookies['path']) / 'project_data.json' if len(current_project_cookies) != 0 else ''

    if len(str(database_file)) != 0 and database_file.exists() is True:
        raw_data = loginLibs.loadJsonData(str(database_file))
        return raw_data
    else:
        return ''
