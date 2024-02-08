import os
import time
from pathlib import Path

from apps import fileApp
from libs import assetViewerLibs


# Queries the new information when executed and replaces the JSON file's contents
def getAssetInfo(filepath):
    # Get main info from path
    filepath = str(Path(filepath))
    filename = filepath.split('\\')[-1]

    # Get asset type
    if '05_shot' in filepath:
        asset_type = filename.split('_E_')[0].split('_')[-1]
        raw_asset_name = filename.split('_E_')[0].split('_')
        raw_asset_name = f'{raw_asset_name[0]}_{raw_asset_name[1]}'
        asset_name = raw_asset_name.upper()
    elif '04_asset' in filepath:
        asset_type = filepath.split('04_asset')[1].split('\\')[1]
        raw_asset_name = filename.split('_')[0]
        asset_name = raw_asset_name.upper()
    else:
        asset_type = ''
        raw_asset_name = filename.split('_')[0]
        asset_name = raw_asset_name.upper()

    # Get current version
    current_version = filename.split('.')[0].split('_')[-1]

    # Get last save user
    last_save_user = assetViewerLibs.getLastSaveUser(filepath)

    # Get time of last save
    unix_timestamp = Path(filepath).stat().st_mtime
    raw_time = time.localtime(unix_timestamp)
    time_last_save = time.strftime('%d/%m/%y %H:%M', raw_time)

    # Get the latest version
    directory = filepath.removesuffix(filename)
    directory = str(Path(directory))
    last_file = os.listdir(directory)[-1]
    latest_version = last_file.split('.')[0].split('_')[-1]

    description = assetViewerLibs.getDescription(filepath, raw_asset_name)

    '''# Get thumbnail path
    thumbnail_path = None
    dnt_path = filepath.split(raw_asset_name)[0]
    dnt_path = Path(dnt_path) / raw_asset_name / '_do_not_touch_'
    if dnt_path.exists() is True:
        for file in os.listdir(dnt_path):
            if 'thumbnail' in str(file):
                thumbnail_path = str(dnt_path / str(file))
            else:
                thumbnail_path = None
    else:
        thumbnail_path = None'''

    #'thumbnail_path': thumbnail_path
    return {
        'asset_name': asset_name,
        'asset_type': asset_type,
        'current_version': current_version,
        'last_save_user': last_save_user,
        'time_last_save': time_last_save,
        'latest_version': latest_version,
        'description': description
    }


# Checks if the user is located within an asset's or a shot's path
def isUserInAsset(explorer_widget):
    user_path, item = fileApp.getClickedFilePath(explorer_widget)

    # Check if the user has anything selected in the explorer, if not throw an error
    if user_path is None:
        asset_path = None
        asset_name = None
        print('\nERROR: You need to select an object in the explorer, failed to perform action...\n')
    else:
        user_path = str(Path(user_path))

        # Split the path to get the asset path
        if '04_asset' in user_path:
            asset_name = user_path.split('04_asset')[1].split('\\')[2]
            asset_path = Path(user_path.split(asset_name)[0]) / asset_name
        elif '05_shot' in user_path:
            asset_name = user_path.split('05_shot')[1].split('\\')[1]
            asset_path = Path(user_path.split(asset_name)[0]) / asset_name
        else:
            asset_path = None
            asset_name = None
            print('\nERROR: You are not located within an asset or shot, failed to perform action...\n')

    return [asset_path, asset_name]
