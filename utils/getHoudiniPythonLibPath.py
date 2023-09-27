import os
from pathlib import Path


# Get a path to the python executable
def getHouPath():
    result = []
    search_path = Path('C:/Program Files/Side Effects Software')
    filename = 'hou.py'

    for root, dir, files in os.walk(search_path):
        if filename in files:
            result.append(os.path.join(root, filename))

    # Get the previous folder from the file path
    raw_path = Path(result[0])
    houdini_python_dir_path = str(raw_path).removesuffix(str(raw_path).split('\\')[-1])
    format_path = Path(houdini_python_dir_path)

    return str(format_path)

def writePathToDisk(hou_path: str, file_name):
    filepath = Path(os.getenv('USERPROFILE')) / '.sewers' / 'databases' / file_name
    text_file = open(filepath, 'w')
    text_file.write(hou_path)
    text_file.close()

try:
    path = getHouPath()
    writePathToDisk(path, 'houdiniPythonLibsPath.txt')
except:
    print('\nHoudini was not found, skipped path fetching...\n')
