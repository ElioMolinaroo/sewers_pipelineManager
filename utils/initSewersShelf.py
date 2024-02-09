import os
import shutil
from pathlib import Path

sewers_path = Path.cwd()
base_shelf_path = sewers_path / 'mayaSewers' / 'base_shelf.mel'
sewers_shelf_path = sewers_path / 'mayaSewers' / 'shelf_SEWERS.mel'
correct_path_line = f"path_to_sewers = '{sewers_path.as_posix()}'"
icons_path = sewers_path / 'icons'

# Temporarily copy the shelf to modify into the directory
shutil.copy(base_shelf_path, sewers_shelf_path)


'''# Updates the Sewers' path in the scripts inside the shelf
def updateSewersPath(search_string, replacement_line):
    with open(sewers_shelf_path, 'rt') as file:
        data = file.read()
        file.flush()
        file.close()

    with open(sewers_shelf_path, 'rt') as file:
        lines = file.readlines()
        for line in lines:
            if search_string in line:
                script_lines = line.split(r'\n')
                for script_line in script_lines:
                    if search_string in script_line:
                        source_string = script_line
        file.flush()
        file.close()

    with open(sewers_shelf_path, 'wt') as file:
        data = data.replace(source_string, replacement_line)
        file.write(data)
        file.close()'''


# Updates the icons' path in the scripts inside the shelf
def updateIconsPath(search_string, path_to_icons):
    with open(sewers_shelf_path, 'rt') as file:
        data = file.read()
        file.flush()
        file.close()

    with open(sewers_shelf_path, 'rt') as file:
        lines = file.readlines()
        for line in lines:
            if search_string in line:
                script_lines = line.split(r'\n')
                for script_line in script_lines:
                    if search_string in script_line:
                        source_string = script_line
                        icon_name = source_string.split('/')[-1]
                        icon_name = icon_name.replace('" \n', '')
                        new_path = path_to_icons / icon_name
                        replacement_line = f'        -image "{new_path.as_posix()}"\n'
                        data = data.replace(source_string, replacement_line)
        file.flush()
        file.close()

    with open(sewers_shelf_path, 'wt') as file:
        file.write(data)
        file.close()


def getMayaShelvesPath():
    mayaPath_path = Path(os.getenv('USERPROFILE')) / '.sewers' / 'databases/mayaPath.txt'
    with open(mayaPath_path, 'r') as file:
        maya_path = file.read()
        file.close()

    result = []
    search_path = Path(os.path.join(os.path.expanduser("~"), "Documents")) / 'maya'
    dir_name = 'shelves'

    for root, dirs, files in os.walk(search_path):
        if dir_name in dirs:
            result.append(os.path.join(root, dir_name))
    return result[0]


# Main Function
def initSewersShelf():
    # Modify the shelf inside of Maya
    #updateSewersPath('path_to_sewers = ', correct_path_line)
    updateIconsPath('-image ', icons_path)
    updateIconsPath('-image1 ', icons_path)

    maya_shelves_path = getMayaShelvesPath()

    shutil.copy(sewers_shelf_path, maya_shelves_path)


initSewersShelf()
