import time
from pathlib import Path

from apps import fileApp
from apps import socketApp
from libs import fileLibs
from libs import loginLibs
from libs import projectLibs


def isCurrentUntitled(ui):
    test_untitled = socketApp.sendMayaCommandProcess(ui, 'cmds.file(query=1, l=1)')
    test_untitled = test_untitled.removeprefix("['")
    test_untitled = test_untitled.removesuffix("']")
    test_untitled = test_untitled.split('/')[-1]
    if test_untitled == 'untitled':
        return True
    else:
        return False


# Checks if the file selected in the file explorer (if there is) is a Maya file
def isClickedMayaFile(explorer_widget):
    # Check if filepath is provided
    filepath, item = fileApp.getClickedFilePath(explorer_widget)

    if len(filepath) != 0:
        # Get the root path
        current_project_cookies = loginLibs.loadJsonData(projectLibs.CURRENT_PROJECT_DATABASE)
        root_path = current_project_cookies['path']

        # Look for a Maya extension
        is_maya_extension = True if '.ma' in str(filepath) or '.mb' in str(filepath) else False

        if Path(filepath) == Path(root_path) or is_maya_extension is False:
            return None
        else:
            return filepath
    else:
        return None


# Does a playblast on the input maya file with the user settings
def playblast(maya_file_path: str, camera: str, encoding: str,
              image_format, playblast_path, filename):
    # Check for image format
    if image_format is None:
        image_format = (1920, 1080)
    else:
        image_format = image_format

    # Check for encoding
    if encoding == 'avi':
        compression = 'none'
    else:
        compression = 'H.264'

    # Check for filename and apply correct extension
    if filename is not None:
        final_filename = filename
    else:
        # Create filename from time
        current_time = time.time()
        raw_time = time.localtime(current_time)
        time_last_save = time.strftime('%d-%m-%y_%H-%M-%S', raw_time)
        final_filename = time_last_save

    # Check for custom path
    if playblast_path is not None:
        dir_path = Path(playblast_path)
        playblast_path = dir_path / final_filename
        playblast_path = str(playblast_path.as_posix())
    else:
        dir_path = Path(maya_file_path.split('maya')[0]) / 'maya' / 'movies'
        playblast_path = dir_path / final_filename
        playblast_path = str(playblast_path.as_posix())

    if dir_path.exists() is False:
        return 1

    # Get the posix path to the playblast background
    raw_path = Path('temp/playblast_grey_bg.jpg').absolute()
    playblast_bg_path = str(raw_path.as_posix())

    playblast_script = f'''
cmds.file('{maya_file_path}', open=1, force=1)

cams = cmds.ls(type='camera')
for cam in cams:
    cmds.setAttr(cam + '.rnd', 0)
cmds.setAttr('{camera}.rnd', 1)

cam_shape = cmds.listRelatives('{camera}', s=1)[0]
img_plane = cmds.createNode('imagePlane')
cmds.connectAttr(img_plane+'.message', cam_shape + '.imagePlane[0]')
cmds.setAttr(img_plane + '.imageName', '{playblast_bg_path}', type='string')
cmds.setAttr(img_plane + '.depth', 10000)
cmds.setAttr(img_plane + '.fit', 0)
cmds.setAttr(img_plane + '.sizeX', 10)
cmds.setAttr(img_plane + '.sizeY', 10)
cmds.setAttr(img_plane + '.colorSpace', 'Raw', type='string')
cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", 1)

cmds.playblast(f='{playblast_path}', fmt='{encoding}', compression='{compression}', fo=1, s=0, cf=1, v=0, orn=0, os=1, fp=4, p=100, wh={image_format}, qlt=100)
'''

    # Runs the playblast script in standalone
    fileLibs.runCodeMayaStandalone(playblast_script)

    final_dir = playblast_path.removesuffix(f'/{final_filename}')
    print(f'\nPlayblast success! Your file was saved at the location:\n{final_dir}')
    