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
    return result[0]


def writePathToDisk(python_path: str, file_name):
    filepath = Path.cwd() / 'databases' / file_name
    text_file = open(filepath, 'w')
    text_file.write(python_path)
    text_file.close()


path = getPythonPath()
writePathToDisk(path, 'pythonPath.txt')
