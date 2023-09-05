import os
import shutil
from pathlib import Path


def filterMayaFiles(current_working_directory):
    # Convert the directory into a list of the files it contains
    files = os.listdir(current_working_directory)

    # Remove the files which aren't Maya files
    for i in files:
        current_file = os.path.basename(i)
        if '.ma' not in current_file and '.mb' not in current_file:
            files.remove(i)

    return files


def getNewFileName(files_list):
    # Remove the file extensions for the entire list
    no_extension_files = []
    for i in files_list:
        raw_file = Path(i)
        processed_file = raw_file.with_suffix('')
        processed_file = processed_file.__str__()
        no_extension_files.append(processed_file)

    # Sort the files according to their trailing numbers
    no_extension_files.sort(key=lambda x: int(x.split('_E_')[-1]))

    # Get last element of the list
    current_last_version = no_extension_files[-1]

    # Replace trailing number
    lead, trail = current_last_version.split('_E_')
    trail = int(trail) + 1
    trail = f"{trail:03d}"

    # Create new last version name
    new_last_version = lead + '_E_' + str(trail)

    return new_last_version


def createNewVersion(current_working_directory, old_file, new_file):
    old_file_path = Path(current_working_directory) / old_file
    new_file_path = Path(current_working_directory) / new_file
    shutil.copyfile(old_file_path, new_file_path)
