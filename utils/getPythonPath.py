import os
from pathlib import Path


# Get a path to the python executable
def getPythonPath():
    result = []
    search_path = Path(os.getenv('LOCALAPPDATA')) / 'Programs' / 'Python'
    filename = 'python.exe'

    for root, dir, files in os.walk(search_path):
        if filename in files:
            result.append(os.path.join(root, filename))

    if len(result) == 0 and "Elio" in str(os.getenv('USERPROFILE')):
        result = ["C:/Users/Elio/anaconda3/envs/sewers/python.exe"]

    return result[0]


def writePathToDisk(python_path: str, file_name):
    filepath = Path(os.getenv('USERPROFILE')) / '.sewers' / 'databases' / file_name
    text_file = open(filepath, 'w')
    text_file.write(python_path)
    text_file.close()


try:
    path = getPythonPath()
    writePathToDisk(path, 'pythonPath.txt')
except:
    print('\nERROR: Could not find a python distribution...\n')
