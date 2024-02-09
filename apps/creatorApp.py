from pathlib import Path

from apps import uiApp
from databases import structures
from libs import creatorLibs
from libs import loginLibs
from libs import projectLibs


# Logic for creating assets depending on their options
def createAsset(ui):
    # Define the user variables
    nice_asset_name = ui.assetNameLineEdit.text()
    asset_type = ui.assetTypeComboBox.currentText()
    description = ui.assetDescriptionPlainText.toPlainText()

    if len(nice_asset_name) == 0:
        print('\nERROR: No name was provided for the asset...\n')

    else:
        '''# Queries the path to the asset directory corresponding to the chosen category
        current_project_cookies = loginLibs.loadJsonData(projectLibs.CURRENT_PROJECT_DATABASE)
        current_project_path = current_project_cookies['assets_path']'''
        asset_path = Path(ui.model.rootPath()) / "04_asset" / asset_type

        # Check if the asset name is somewhere in the path, if yes create a safe name
        if creatorLibs.checkForNameInPath(nice_asset_name, str(asset_path)) is True:
            safe_asset_name = f'{nice_asset_name}_safe'
        else:
            safe_asset_name = nice_asset_name

        # Create the folder structure
        base_folder_structure = structures.asset_template
        folder_structure = projectLibs.changeProjectName(safe_asset_name, base_folder_structure)

        projectLibs.createFolderStructure(folder_structure, asset_path)

        '''# Create the comments database
        with open(str(asset_path / safe_asset_name / '_do_not_touch_' / 'comments_database.json'), 'w') as file:
            file.write('[]')
            file.close()

        # Writes the asset description in file at the given filepath
        current_asset_database = asset_path / safe_asset_name / '_do_not_touch_' / 'description.txt'
        creatorLibs.uploadAssetDescription(description, current_asset_database)

        # Add the asset to the database
        path = str(Path(asset_path) / safe_asset_name)
        creatorLibs.addAssetToDatabase(safe_asset_name, path, asset_type)'''

        # Update shot and asset UI
        #uiApp.browserUpdateShots(ui)
        uiApp.browserUpdateAssets(ui)

        print(f'\nThe {nice_asset_name.upper()} asset was created successfully.\n')


# Logic for preparing shot names
def prepShot(ui):
    # Define the user variables
    raw_sequence_number = ui.sequenceSpinBox.value()
    raw_shot_number = ui.shotSpinBox.value()
    master_layout = ui.masterLayoutRadioButton.isChecked()

    sequence_number = creatorLibs.formatShotSequenceNumbers(raw_sequence_number, 3)
    shot_number = creatorLibs.formatShotSequenceNumbers(raw_shot_number, 3)

    # Create the sequence name
    if master_layout is True:
        shot_name = f'sq{sequence_number}_master_layout'
    else:
        shot_name = f'sq{sequence_number}_sh{shot_number}'

    return shot_name


# Creates the folders structure for the shot
def createShot(ui, nice_shot_name):
    # Query the description
    description = ui.shotDescriptionPlainText.toPlainText()

    '''# Queries the path to the asset directory corresponding to the chosen category
    current_project_cookies = loginLibs.loadJsonData(projectLibs.CURRENT_PROJECT_DATABASE)
    raw_path = current_project_cookies['shots_path']'''
    shots_path = Path(ui.model.rootPath()) / "05_shot"

    # Check if the shot name is somewhere in the path, if yes create a safe name
    if creatorLibs.checkForNameInPath(nice_shot_name, str(shots_path)) is True:
        safe_asset_name = f'{nice_shot_name}_safe'
    else:
        safe_asset_name = nice_shot_name

    # Create the folder structure:
    base_folder_structure = structures.shot_template
    folder_structure = projectLibs.changeProjectName(safe_asset_name, base_folder_structure)

    # Create the shot folders
    projectLibs.createFolderStructure(folder_structure, shots_path)

    '''# Create the comments database
    with open(str(shots_path / safe_asset_name / '_do_not_touch_' / 'comments_database.json'), 'w') as file:
        file.write('[]')
        file.close()

    # Writes the shot description in file at the given filepath
    current_shot_database = shots_path / safe_asset_name / '_do_not_touch_' / 'description.txt'
    creatorLibs.uploadAssetDescription(description, current_shot_database)

    # Add the shot to the database
    shots_path = Path(shots_path) / safe_asset_name
    # Query sequence and master
    master = True if '_master_layout' in safe_asset_name else False
    sequence = creatorLibs.buildSequenceNiceName(safe_asset_name)

    #creatorLibs.addShotToDatabase(safe_asset_name, shots_path, sequence, master)'''

    # Update shot and asset UI
    uiApp.browserUpdateShots(ui)
    uiApp.browserUpdateAssets(ui)

    print(f'\n{nice_shot_name} was created successfully.\n')
