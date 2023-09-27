import os
import shutil
from pathlib import Path

from libs import fileLibs
from apps import socketApp
from libs import socketLibs
from libs import projectLibs


# Get path to the item (excluding the item itself)
def getPathToItem(index):
    selected_item_path = fileLibs.getItemPath(index)
    item_name = str(Path(selected_item_path).as_posix()).split('/')[-1]
    full_path = str(Path(selected_item_path.removesuffix(item_name)))

    return full_path


# Processes asset data to feed the renameAsset function
def processAssetData(index):
    # Get asset name
    old_asset_name = index.data()
    object_type = 'shots' if '_master_layout' in old_asset_name or '_sh' in old_asset_name else 'assets'

    # Get the corresponding asset entry in the database
    raw_data = projectLibs.getProjectData()
    assets_database = raw_data[object_type]

    asset_data = None
    for entry in assets_database:
        if entry == str(old_asset_name):
            asset_data = assets_database[str(old_asset_name)]
            break

    if asset_data is not None:
        old_asset_path = asset_data['path']
    else:
        old_asset_path = None

    return [old_asset_path, old_asset_name, raw_data, object_type]


# Gets the path to inside a folder or to the folder a file is contained in depending on what's selected
def getRelativePathToFileOrFolder(path):
    if Path(path).is_dir() is True:
        path_to_folder = path
        path_to_folder = Path(path_to_folder)
    elif Path(path).is_file() is True:
        path_to_folder = path.removesuffix(path.split('/')[-1])
        path_to_folder = Path(path_to_folder)
    else:
        path_to_folder = None

    return path_to_folder


# Creates a zbrush file at the specified directory with the specified name
def createZbrushFile(name, path):
    source_file = Path('databases/zbrush2023TemplateFile.zpr')
    destination_dir = Path(path)

    # Copy the file to the new directory
    shutil.copy(source_file, destination_dir)

    # Change the name of the new file
    old_file = Path(path) / 'zbrush2023TemplateFile.zpr'
    new_file = Path(path) / f'{name}.zpr'

    os.rename(old_file, new_file)

    print(f'\nSuccessfully created file {name.upper()}.zpr.\n')


# Check if the file provided is currently open in Maya
def isMayaFileOpen(ui, file_path):
    # Check if Maya is open and connected
    maya_connection = socketLibs.isConnectedToMaya(ui)

    if maya_connection is False:
        return False
    else:
        # Get maya path
        maya_open_file = socketApp.sendMayaCommandProcess(ui, 'cmds.file(q=1, sn=1)')
        
        # Compare both paths
        is_open = True if str(Path(file_path).as_posix) == str(Path(maya_open_file).as_posix) else False

        return is_open
    