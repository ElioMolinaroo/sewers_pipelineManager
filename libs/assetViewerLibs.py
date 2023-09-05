import textwrap
from pathlib import Path

from PyQt6.QtWidgets import QFileDialog


# Gets the last user who saved a given file
def getLastSaveUser(filepath: str):
    # Initialise raw_info
    raw_info = ''
    with open(filepath, 'r') as file:
        try:
            for line in file:
                if 'fileInfo "savedBy"' in line:
                    raw_info = str(line,)
                    break
        except Exception:
            print('WARNING: Could not get last save user because of file format...')
        file.close()

    file.close()

    if len(raw_info) != 0:
        # Extract the username from the raw information
        username = raw_info.split('"')[3]
        return username

    else:
        return


# Gets the description from the given asset filepath and formats it
def getDescription(filepath: str, asset_name: str):
    # Gets the path to the description txt file
    path_to_description = Path(filepath.split(asset_name)[0]) / asset_name / '_do_not_touch_' / 'description.txt'

    if path_to_description.exists() is False:
        return ''
    else:
        with open(path_to_description, 'r') as file:
            description = file.read()
            file.close()

        # Format the description to have a new line character every 35 character
        wrapper = textwrap.TextWrapper(width=35)
        lines = wrapper.wrap(description)
        formatted_description = '\n'.join(lines)

        return formatted_description


# Opens a file dialog and returns the user selected file
def fileDialogReturnFile(ui, dialog_title):
    file = QFileDialog.getOpenFileName(ui, dialog_title, 'C:/', "Images (*.png *.xpm *.jpg *.tif)")
    return file
