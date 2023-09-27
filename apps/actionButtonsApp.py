import os
import re
import shutil
from pathlib import Path

from apps import socketApp
from libs import socketLibs
from libs import actionButtonsLibs
from libs import fileLibs
from libs import projectLibs
from ui import uiView


# Updates the info for the new version file
def getNewVersionInfo(old_name: str, old_path: str):
    try:
        path_to_file = Path(old_path.removesuffix(old_name))

        # Extracting the variables
        temp_name, extension = old_name.split('.')
        raw_numbers = re.split(r'(\d+)', temp_name)[-2]
        raw_name = temp_name.removesuffix(raw_numbers)

        # Creating the updated variables
        new_numbers = int(raw_numbers) + 1
        new_numbers = str(new_numbers).zfill(3)
        extension.replace(' ', '')
        # Merging the modified variables to get the output
        new_name = f'{raw_name}{new_numbers}.{extension}'
        new_path = path_to_file / new_name
        new_path = str(new_path.as_posix())

        return [new_name, new_path]

    except:
        return ''


# Updates the info for the publish file
def getPublishInfo(old_path: str):
    try:
        root_path, path_to_file = old_path.split('edit')
        root_path = Path(root_path) / 'publish'

        path_to_file = path_to_file.split('_E_')[0]
        path_to_file = str(path_to_file) + '_P.ma'
        path_to_file = str(root_path) + path_to_file

        # Convert the result to a readable output
        file_path = Path(path_to_file)

        file_name = str(file_path).split('\\')[-1]
        publish_path = Path(str(file_path).removesuffix(file_name))

        publish_exists = file_path.is_file()

        return [file_path, publish_exists]
    except:
        return ''


# Saves a version
def saveVersion(ui, new_path, new_name, old_name):
    # Send commands to create the new file
    socketApp.sendMayaCommandProcess(ui, f'cmds.file(rename="{new_path}")')
    socketApp.sendMayaCommandProcess(ui, f'cmds.file(save=True, type="mayaAscii")')

    print(f'{old_name.upper()} versioned up successfully to {new_name.upper()}.')


# Saves a publish
def savePublish(publish_exists, new_name, new_path, old_path):
    # Start the Publish process
    if publish_exists is True:
        os.remove(new_path)
        shutil.copy2(old_path, new_path)
    elif publish_exists is False:
        shutil.copy2(old_path, new_path)

    print(f'{new_name.upper()} was published successfully.')


# Execute to launch the Publish dialog UI
def publishConfirmationUI(ui, publish_confirmation_dialog):
    instance_publish_confirmation = publish_confirmation_dialog()
    # Launches the set project dialog
    instance_publish_confirmation.exec()


# Execute to launch the Save Version dialog UI
def saveVersionConfirmationUI(ui, save_version_confirmation_dialog):
    instance_save_version_confirmation = save_version_confirmation_dialog()
    # Launches the set project dialog
    instance_save_version_confirmation.exec()


# Opens Maya in standalone to get a list of cameras
def getCamerasList(ui, maya_file_path: str):
    """The standalone commands and importing cmds are already embedded, don't do them twice"""
    maya_safe_path = Path(maya_file_path).as_posix()

    script = f'''
cmds.file("{maya_safe_path}", open=1, force=1)
available_cameras = cmds.listCameras()
print(available_cameras)
    '''

    # Connect to Maya
    socketLibs.connectToMaya(socketLibs.PORT)

    # Get the raw string output and convert it back to a list of cameras
    if socketLibs.isConnectedToMaya(ui) is True and socketApp.sendMayaCommandProcess(ui, 'cmds.file(q=1, sn=1)').split('/')[-1] == uiView.last_selected_index.data():
        raw_output = socketApp.sendMayaCommandProcess(ui, 'cmds.listCameras()')
    else:
        raw_output = fileLibs.runCodeMayaStandalone(script)

    converted_output = eval(raw_output)

    return converted_output


# Gets the playblast required settings from the playblast UI
def getPlayblastInfo(ui):
    # Get the raw inputs from the UI
    camera = ui.cameraComboBox.currentText()
    _format = ui.encodingComboBox.currentText()
    format_width = ui.formatWidthLineEdit.text()
    format_height = ui.formatHeightLineEdit.text()
    filename = ui.filenameLineEdit.text()
    # Get the playblast path
    playblast_path = ui.pathPushButton.property('playblast_path')

    # Check if the image format is valid
    if format_width.isdigit() is True and int(format_width) >= 1 and format_height.isdigit() is True and int(format_height) >= 1:
        format_width = int(format_width)
        format_height = int(format_height)
    else:
        format_width = 1920
        format_height = 1080
        print('\nWARNING: Your format is invalid, the playblast will use 1920x1080...\n')

    # Check if filename exists, if yes, checks if it's valid
    if len(filename) == 0:
        filename = None
    else:
        forbidden_characters = r'/\\$#@!%^&*|?<>,.=+ '
        for char in forbidden_characters:
            if char in filename:
                print('\nWARNING: The filename you provided was incorrect, the playblast will have the default naming...\n')
                filename = None
                break

    # Format the user options in a dictionary
    user_options = {
        "camera": camera,
        "format": _format,
        "image_format": (format_width, format_height),
        "filename": filename,
        "playblast_path": playblast_path
    }

    return user_options


# Tries to execute a playblast, prints an error message otherwise
def tryPlayblast(ui, maya_file: str):
    # Get the playblast information from the UI
    user_options = getPlayblastInfo(ui)

    # Try to playblast
    try:
        state = actionButtonsLibs.playblast(str(Path(maya_file).as_posix()), user_options["camera"], user_options["format"], image_format=user_options["image_format"], playblast_path=user_options["playblast_path"], filename=user_options["filename"])
        if state == 1:
            print(f'ERROR: Something went wrong, check the provided path...')
    except:
        print(f'ERROR: Something went wrong with the playblast...')


# Opens a dialog to choose a folder
def getPlayblastFolder(ui):
    # Locate the folder
    project_path = projectLibs.fileDialogReturnFolder(ui, 'Choose your playblast directory...')
    project_path = str(Path(project_path).as_posix())

    # Check if a folder was selected
    if len(project_path) != 0:
        ui.pathPushButton.setProperty('playblast_path', project_path)
        ui.pathPushButton.setText('Path selected!')
