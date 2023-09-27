import base64
import os
import subprocess
from pathlib import Path


with open('databases/mayaPath.txt', 'r') as file:
    data = file.read().removesuffix('maya.exe')
    file.close()
PATH_TO_MAYAPY = Path(data) / 'mayapy.exe'


# Opens any file with the provided application
def openFileWithApp(file_path, application_path):
    subprocess.Popen(f'{application_path} "-script" {file_path}')


# Opens any file with its default application
def openFile(file_path):
    os.startfile(file_path, 'open')


# Recursive function to retrieve the path of a pyqt object
def getItemPath(index):
    # Base case: If the index is invalid or has no parent, return an empty path
    if not index.isValid() or not index.parent().isValid():
        return []

    from ui import uiView
    path = uiView.sewers_window.model.filePath(index)

    return path


# Encodes a python file into a MEL launcher
def pythonToMel(python_code, melfile):
    python_code = bytes(python_code, encoding='utf-8')
    encoded = base64.urlsafe_b64encode(python_code)
    py_to_mel = f"import base64; _py_code = base64.urlsafe_b64decode({encoded}); _py_code = _py_code.decode('utf-8'); exec(_py_code)"
    with open(melfile, 'wt') as writer:
        writer.write('python("%s");' % py_to_mel)
        writer.flush()
        writer.close()


# Deletes the content of the temp MEL launcher
def flushMelLauncher():
    with open('temp/temp_mel_launcher.mel', 'w') as file:
        file.close()


# Runs a custom script in maya standalone using the mayapy interpreter
def runCodeMayaStandalone(script: str, path_to_mayapy=PATH_TO_MAYAPY):
    final_script = f'''
import maya.standalone
maya.standalone.initialize()
import maya.cmds as cmds
{script}
maya.standalone.uninitialize()
    '''

    # Run the code and get the last line of the output
    bytes_output = subprocess.run([path_to_mayapy, '-c', final_script], stdout=subprocess.PIPE, check=True)

    # Try to get an output
    try:
        str_raw_output = bytes_output.stdout.decode()
        str_output = str_raw_output.splitlines()[-1]
        return str_output
    
    except:
        return None
