import os
import shutil
import subprocess
from pathlib import Path

import pyperclip

from apps import socketApp
from apps import uiApp
from libs import contextMenusLibs
from libs import creatorLibs
from libs import fileLibs
from libs import loginLibs
from libs import projectLibs


# Copes the full path of a right-clicked item to the clipboard
def copyFullPath(index):
    try:
        # Get path to item
        full_path = fileLibs.getItemPath(index)
        # Copies the path to the clipboard
        pyperclip.copy(str(full_path))

    except:
        print('\nERROR: could not query item path as not item is selected...\n')


# Opens in the file explorer the folder containing the file you selected
def openFolder(index):
    try:
        # Get path to item
        full_path = str(contextMenusLibs.getPathToItem(index))

        # Format the path to the correct directory
        if Path(full_path).is_dir() is True:
            folder_path = Path(full_path)
        else:
            item_name = full_path.split('\\')[-1]
            folder_path = Path(full_path.removesuffix(item_name))

        # Open file explorer at the given path if the path exists
        if folder_path.exists() is True:
            subprocess.Popen(f'explorer {folder_path}')

    except:
        print('\nERROR: could not query item path as not item is selected...\n')


# In the browser tab, renames everything in the asset to the given string
def renameAsset(ui, index, new_nice_name):
    if new_nice_name == '' or index.data() is None:
        print("\nERROR: No new name was provided or you didn't choose an object to rename, skipped the renaming of the object...\n")
        return

    old_asset_path, old_asset_name, raw_database, object_type = contextMenusLibs.processAssetData(index)

    if old_asset_path is None:
        print('\nERROR: This object might not be in the assets/shots database...\n')
    elif object_type == 'shots' and 'sq' not in new_nice_name:
        print('\nERROR: The formatting of this shot name is wrong...\n')
    else:
        new_path_to_asset = Path(old_asset_path.removesuffix(old_asset_name))

        if new_nice_name in str(new_path_to_asset):
            new_safe_name = f'{new_nice_name}_safe'
        else:
            new_safe_name = new_nice_name

        new_asset_path = Path(old_asset_path.removesuffix(old_asset_name)) / new_safe_name

        # Iterates over every asset and file in the new directory
        for root, dirs, files in os.walk(new_asset_path):
            for file in files:
                if old_asset_name in file:
                    # Create the new file name
                    new_file_name = file.replace(old_asset_name, new_safe_name)
                    # Get the needed paths
                    old_file_path = os.path.join(root, file)
                    new_file_path = os.path.join(root, new_file_name)
                    # Rename the file
                    os.rename(old_file_path, new_file_path)

            for folder in dirs:
                if old_asset_name in folder:
                    # Create the new folder name
                    new_folder_name = folder.replace(old_asset_name, new_safe_name)
                    # Get the needed paths
                    old_folder_path = os.path.join(root, folder)
                    new_folder_path = os.path.join(root, new_folder_name)
                    # Rename the folder
                    os.rename(old_folder_path, new_folder_path)

        # Rename the root folder of the asset
        try:
            Path(old_asset_path).rename(new_asset_path)

            # Rename instances in the database
            old_asset_data = raw_database[object_type][old_asset_name]
            raw_database[object_type].pop(old_asset_name)
            old_asset_data['path'] = str(new_asset_path)
            raw_database[object_type][new_safe_name] = old_asset_data

            # Update the project cookies
            current_project_cookies = loginLibs.loadJsonData(projectLibs.CURRENT_PROJECT_DATABASE)
            database_file = Path(current_project_cookies['path']) / 'project_data.json'
            loginLibs.registerCookies(raw_database, str(database_file))

            # Refresh browser tab
            uiApp.browserUpdateAssets(ui)
            uiApp.browserUpdateShots(ui)

            print(f'\nSuccessfully renamed {old_asset_name.upper()} to {new_safe_name.upper()}.\n')

        except Exception as e:
            print(e)


# In the browser tab, allows you to move an asset to the trash folder of the SEWERS
def deleteAsset(ui, index):
    object_name = index.data()
    if object_name is None:
        print('\nERROR: No element was provided, aborted the deletion process...\n')
        return

    # Get necessary data
    asset_path, asset_name, raw_database, object_type = contextMenusLibs.processAssetData(index)
    trash_folder = Path.cwd() / 'trash'

    # Move the folder to the trash
    if Path(trash_folder / asset_name).exists() is True:
        path_asset_in_trash = Path(trash_folder / asset_name)
        shutil.rmtree(path_asset_in_trash)
        shutil.move(asset_path, trash_folder)
    else:
        shutil.move(asset_path, trash_folder)

    # Recreate database without entry
    raw_database[object_type].pop(asset_name)
    # Update the project cookies
    current_project_cookies = loginLibs.loadJsonData(projectLibs.CURRENT_PROJECT_DATABASE)
    database_file = Path(current_project_cookies['path']) / 'project_data.json'
    loginLibs.registerCookies(raw_database, str(database_file))

    # Refresh browser tab
    uiApp.browserUpdateAssets(ui)
    uiApp.browserUpdateShots(ui)

    print(f'\nSuccessfully moved {asset_name.upper()} to the trash folder.\n')


# Moves a file/folder in the explorer to the trash folder of the SEWERS
def deleteFile(ui, index):
    object_name = index.data()
    if object_name is None:
        print('\nERROR: No element was provided, aborted the deletion process...\n')
        return

    # Get necessary data
    file_path = fileLibs.getItemPath(index)
    file_name = str(Path(file_path).as_posix()).split('/')[-1]
    path_to_file = str(Path(str(file_path).removesuffix(file_name)))
    trash_folder = str(Path.cwd() / 'trash')

    # Check if file to be renamed is open in Maya
    is_file_open = contextMenusLibs.isMayaFileOpen(ui, file_path)

    if is_file_open is True:
        print("\nERROR: The file you're trying to delete is currently open in Maya, open another file and try again...\n")
    else:
        # Move the folder to the trash
        test_path = Path(trash_folder) / file_name
        if test_path.exists() is True:
            path_file_in_trash = test_path
            path_file_in_trash.unlink()
            shutil.move(file_path, trash_folder)
        else:
            shutil.move(file_path, trash_folder)

        # Refresh explorer
        ui.fileManagerColumnView.update()
        # Update the UI to the selected path
        model = ui.model
        # Navigates to the file in the file explorer
        ui.fileManagerColumnView.setCurrentIndex(model.index(path_to_file))

        print(f'\nSuccessfully moved {file_name.upper()} to the trash folder.\n')


# In the explorer, renames the selected file to the given string
def renameFile(ui, index, new_file_name):
    if new_file_name == '' or index.data() is None:
        print("\nERROR: No new name was provided or you didn't choose an object to rename, skipped the renaming of the object...\n")
        return

    # Get/Create necessary data
    old_file_path = fileLibs.getItemPath(index)
    old_file_name = str(Path(old_file_path).as_posix()).split('/')[-1]
    extension = Path(old_file_name).suffix
    new_file_name = f'{new_file_name}{extension}'
    new_file_path = str(Path(str(old_file_path).replace(old_file_name, new_file_name)))

    # Check if file to be renamed is open in Maya
    is_file_open = contextMenusLibs.isMayaFileOpen(ui, old_file_path)

    if is_file_open is True:
        print("\nERROR: The file you're trying to rename is currently open in Maya, open another file and try again...\n")
    else:
        # Rename the file
        os.rename(old_file_path, new_file_path)

        # Refresh explorer
        ui.fileManagerColumnView.update()
        # Update the UI to the selected path
        model = ui.model
        # Navigates to the file in the file explorer
        ui.fileManagerColumnView.setCurrentIndex(model.index(new_file_path))

        print(f'\nSuccessfully renamed {old_file_name.upper()} to {new_file_name.upper()}.\n')


# Crates a folder in the specified directory in the explorer
def createFolder(path, folder_name):
    if path is None or folder_name == '':
        print('\nWARNING: No name or directory was provided for the folder creation...\n')
        return

    # Get the correct Path object where the folder needs to be created
    path_to_folder = contextMenusLibs.getRelativePathToFileOrFolder(path)
    folder_path = path_to_folder / folder_name
    Path.mkdir(folder_path)


# Execute this function to create a maya file inside the selected directory
def mayaFileProcess(path, file_name):
    if path is None or file_name == '':
        print('\nWARNING: No name or directory was provided for the file creation...\n')
        return

    # Get the correct Path object where the file needs to be created
    path_to_folder = contextMenusLibs.getRelativePathToFileOrFolder(path)

    creatorLibs.createMayaFile(file_name, path_to_folder)

    print(f'\nSuccessfully created file {file_name.upper()}.ma.\n')


# Execute this function to create a zbrush file inside the selected directory
def zbrushFileProcess(path, file_name):
    if path is None or file_name == '':
        print('\nWARNING: No name or directory was provided for the file creation...\n')
        return

    # Get the correct Path object where the file needs to be created
    path_to_folder = contextMenusLibs.getRelativePathToFileOrFolder(path)

    contextMenusLibs.createZbrushFile(file_name, path_to_folder)


# References the clicked Maya file inside the currently opened one
def referenceMayaFile(ui, index, file_name):
    # Get the full path
    path = fileLibs.getItemPath(index)
    path = str(Path(path).as_posix())
    # Create the command
    reference_command = f'import maya.cmds as cmds; cmds.file("{path}", reference=1, namespace="{file_name}")'
    # Execute the command
    test = socketApp.sendMayaCommandProcess(ui, reference_command)

    # Print the result of the command's success
    if test is None:
        print(f'\nSuccessfully referenced the file {file_name.upper()}.\n')
    else:
        print('\nERROR: Your file could not be referenced...\n')


# Imports the clicked Maya file inside the currently opened one
def importMayaFile(ui, index, file_name):
    # Get the full path
    path = fileLibs.getItemPath(index)
    path = str(Path(path).as_posix())
    # Create the command
    import_command = f'import maya.cmds as cmds; cmds.file("{path}", i=1, namespace="{file_name}")'
    # Execute the command
    test = socketApp.sendMayaCommandProcess(ui, import_command)

    # Print the result of the command's success
    if test is None or test == 'None':
        print(f'\nSuccessfully imported the file {file_name.upper()}.\n')
    else:
        print('\nERROR: Your file could not be imported...\n')

