import os
from pathlib import Path


# Get a path to the python executable
def getMayaPath():
    result = []
    search_path = Path('C:/Program Files/Autodesk')
    filename = 'maya.exe'

    for root, dir, files in os.walk(search_path):
        if filename in files:
            result.append(os.path.join(root, filename))
    return result[0]


def writePathToDisk(maya_path: str, file_name):
    filepath = Path.cwd() / 'databases' / file_name
    text_file = open(filepath, 'w')
    text_file.write(maya_path)
    text_file.close()


path = getMayaPath()
writePathToDisk(path, 'mayaPath.txt')
