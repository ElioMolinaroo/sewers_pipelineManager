import os
import shutil
from pathlib import Path

from libs import loginLibs
from libs import projectLibs


# Formats shot number to the desired length with a trailing zero (except for decimal shot numbers)
def formatShotSequenceNumbers(number_input, format_size: int) -> str:
    if number_input.is_integer() is True:
        formatted_number = int(number_input)
        formatted_number = str(formatted_number).zfill(format_size)
        formatted_number = formatted_number + '0'
    else:
        number_input = int(number_input*10)
        formatted_number = str(number_input).zfill(format_size+1)

    return formatted_number


# Updates the Create Shot UI depending on the master layout radio button
def createShotUpdateUI(ui):
    if ui.masterLayoutRadioButton.isChecked() is True:
        ui.shotSpinBox.setEnabled(False)
    else:
        ui.shotSpinBox.setEnabled(True)


# Find folders matching the provided string
def matchingFolder(directory, target_string):
    # Use glob to retrieve all folder names in the specified directory
    folder_directory = Path(directory)
    folders = [subdir.name for subdir in folder_directory.iterdir() if subdir.is_dir()]

    # Check if any folder matches the provided string
    for folder in folders:
        if folder == target_string:
            return True

    return False


'''# Add the created shot to the project database
def addShotToDatabase(name: str, path, sequence: str, master: bool):
    # Get current database data
    current_project_cookies = loginLibs.loadJsonData(projectLibs.CURRENT_PROJECT_DATABASE)
    database_file = Path(current_project_cookies['path']) / 'project_data.json'
    data = loginLibs.loadJsonData(str(database_file))

    # Build the shot entry
    shot_entry = {name: {"path": str(path), "sequence": sequence, "master": master}}

    # Add the shot entry to the database
    if len(data['shots']) == 0:
        data['shots'] = shot_entry
    else:
        data['shots'].update(shot_entry)

    # Update the database
    loginLibs.registerCookies(data, str(database_file))


# Add the created asset to the project database
def addAssetToDatabase(name: str, path, category: str):
    # Get current database data
    current_project_cookies = loginLibs.loadJsonData(projectLibs.CURRENT_PROJECT_DATABASE)
    database_file = Path(current_project_cookies['path']) / 'project_data.json'
    data = loginLibs.loadJsonData(str(database_file))

    asset_entry = {name: {"path": str(path), "category": category}}

    # Add the shot entry to the database
    if len(data['assets']) == 0:
        data['assets'] = asset_entry
    else:
        data['assets'].update(asset_entry)

    # Update the database
    loginLibs.registerCookies(data, str(database_file))'''


# Build the sequence nice name from a shot
def buildSequenceNiceName(shot_name):
    if '_master_layout' in shot_name:
        shot_name = shot_name.replace('_master_layout', '')
    else:
        shot_name = shot_name.split('_sh')[0]

    # Format sequence name to: Sequence X
    shot_name = shot_name.replace('sq', '')
    shot_name = shot_name.lstrip('0')
    sequence_number = int(shot_name) / 10
    if sequence_number.is_integer() is True:
        sequence_number = int(sequence_number)
    sequence_format = f'Sequence {sequence_number}'

    return sequence_format


# Creates a Maya file at the specified directory with the specified name
def createMayaFile(name, path):
    source_file = Path(os.getenv('USERPROFILE')) / '.sewers' / 'databases' / 'maya2023TemplateFile.ma'
    destination_dir = Path(path)

    # Copy the file to the new directory
    shutil.copy(source_file, destination_dir)

    # Change the name of the new file
    old_file = Path(path) / 'maya2023TemplateFile.ma'
    new_file = Path(path) / f'{name}.ma'

    os.rename(old_file, new_file)

    # Add metadata
    #current_username = loginLibs.getCurrentUsername()
    #addUserMetadataToMayaFile(current_username, new_file, 13)


'''# Adds username metadata to the corresponding maya file at the given line index
def addUserMetadataToMayaFile(username: str, filepath, line_index: int):
    entry = f'fileInfo "savedBy" "{username}";\n'

    with open(filepath, 'r+') as fd:
        contents = fd.readlines()
        contents.insert(line_index, entry)
        fd.seek(0)
        fd.writelines(contents)
        fd.close()'''


# Uploads the asset or shot description in the given file, if file doesn't exist: creates it
def uploadAssetDescription(description: str, filepath: str):
    # Check if the file exists
    with open(filepath, 'w') as file:
        pass
        file.write(description)
        file.close()


# Checks if the nice name is part of the path and returns a boolean
def checkForNameInPath(asset_name: str, asset_path: str) -> bool:
    if asset_name in asset_path:
        name_in_path = True
    else:
        name_in_path = False

    return name_in_path
