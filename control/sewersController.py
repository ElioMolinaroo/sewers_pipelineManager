import shutil
import time
from pathlib import Path

from PyQt6.QtGui import QIcon

from apps import actionButtonsApp
from apps import assetViewerApp
from apps import creatorApp
from apps import fileApp
from apps import loginApp
from apps import projectApp
from apps import recentFilesApp
from apps import socketApp
from apps import uiApp
from apps import contextMenusApp
from libs import actionButtonsLibs
from libs import assetViewerLibs
from libs import browserLibs
from libs import creatorLibs
from libs import loginLibs
from libs import projectLibs
from libs import socketLibs
from libs import uiLibs
from libs import fileLibs
from ui import uiView


# Implement the logout process
def logoutProcess(ui):
    # Disable the interface except for the login button
    uiLibs.disableButtons(ui)
    # Call the logout delete cookies function
    loginApp.userLogout(ui)
    # Call the project reset function
    projectLibs.setProjectAsDefault(ui)


# Implement the login or registering process
def loginRegisterProcess(ui, login_dialog, register_dialog):
    # Check what the user chose
    login_or_register = uiLibs.comboBoxSelection(ui.loginButton)

    # Implement the login process
    if login_or_register == 'Login':
        instance_login = login_dialog()
        instance_login.login_signal.connect(lambda: uiApp.loginRegisterUpdateUI(ui))
        instance_login.exec()

    # Implement the register process
    elif login_or_register == 'Register':
        instance_register = register_dialog()
        instance_register.register_signal.connect(lambda: uiApp.loginRegisterUpdateUI(ui))
        instance_register.exec()


# Initialises the UI look according to the available cookies
def initUi(ui):
    # execute sewersInit
    return_cookies = uiApp.sewersInit()

    # Lock the UI if no projects are set
    current_project_path = projectLibs.getCurrentProject(projectLibs.CURRENT_PROJECT_DATABASE)[1]

    # Set the connections if a user is already logged in
    if 'loggedIn' in return_cookies:
        uiLibs.enableButtons(ui)
        # Look for a current project in the cookies if not, disables most of the UI
        if len(current_project_path) == 0:
            for i in ui.userUiInputs:
                i.setEnabled(False)
            ui.createProjectButton.setEnabled(True)
            ui.loadProjectButton.setEnabled(True)
            ui.setProjectButton.setEnabled(True)
            ui.logoutButton.setEnabled(True)
        # Update the current username and its permissions
        ui.usernameLabel.setText(return_cookies[1])

    # Set the connections if no user is logged in
    elif 'noLog' in return_cookies:
        uiLibs.disableButtons(ui)
        ui.loginButton.setEnabled(True)

    # Preps the UI, adding the missing elements from the sewersUI.ui file
    model = uiApp.prepUi(ui)

    return model


# Verifies whether the login credentials entered are correct or not
def loginVerification(ui):
    # Gather the content of the username and password slots
    input_username = uiLibs.returnLineEdit(ui.usernameLineEdit)
    input_password = uiLibs.returnLineEdit(ui.passwordLineEdit)
    # Execute the login function
    login_status = loginApp.userLogin(input_username, input_password)
    if login_status[0] == 'success':
        ui.login_signal.emit()


# Verifies whether the login credentials entered are already used and creates them if not
def registerVerification(ui):
    # Gather the content of the slots
    input_username = uiLibs.returnLineEdit(ui.usernameLineEdit)
    input_password = uiLibs.returnLineEdit(ui.passwordLineEdit)
    input_confirm_password = uiLibs.returnLineEdit(ui.confirmPasswordLineEdit)
    # Look for errors
    if uiApp.usernameInDatabase(input_username) is True:
        print('ERROR: This username already exists...')
    elif len(input_username) < 2:
        print('ERROR: Your username must be at least 2 characters long...')
    elif len(input_password) < 4:
        print('ERROR: Your password must be at least 4 characters long...')
    elif input_password != input_confirm_password:
        print('ERROR: The confirmation is different than the password...')
    else:
        loginApp.userRegister(input_username, input_password)
        ui.register_signal.emit()


# Function executed when the load project button is clicked
def loadProject(ui):
    # Updates the current project database and extracts project's path, name, and users
    project_data = projectApp.prepareLoadProject(ui)

    # Check if a project directory was chosen
    if project_data[0] == '':
        pass
    elif project_data[0] != 'C:/':
        project_path = project_data[0]
        project_name = project_data[1]
        project_artists = project_data[2]
        project_assets_path = project_data[3]
        project_shots_path = project_data[4]

        # Update the UI to fit the new project
        ui.projectNameLabel.setText(str.upper(project_name))
        model = ui.model
        ui.fileManagerColumnView.setRootIndex(model.index(project_path))

        # Update the UI
        uiLibs.enableButtons(ui)
        uiLibs.projectTypeChangeUI(ui)
    else:
        print("WARNING: Couldn't set this project, path must be invalid...")


# Execute to launch the Create Project dialog UI
def createProjectUI(ui, create_project_dialog):
    instance_create_project = create_project_dialog()
    instance_create_project.create_project_signal.connect(lambda: projectLibs.setCurrentProject(ui))
    # Launch the project path browser
    instance_create_project.exec()


# Global function for creating a project, encapsulating all the logic
def createProjectProcess(ui):
    # Query information from the project folder browser
    project_name = uiLibs.returnLineEdit(ui.projectNameLineEdit)
    project_template = uiLibs.comboBoxSelection(ui.pipelineTemplateComboBox)
    project_path = ui.browseProjectLineEdit.text()

    # Check for white spaces in the project name
    if ' ' in project_name:
        project_name = project_name.replace(' ', '_')

    # Checks if the path exists
    if len(project_path) == 0:
        path_exists = False
    else:
        path_exists = Path.exists(Path(project_path))

    if path_exists is True and len(project_name) != 0:
        complete_path = Path(project_path) / project_name
        if complete_path.exists() is False:
            # Create the project
            projectApp.createProject(project_name, project_path, project_template)
            ui.create_project_signal.emit()
        else:
            print("ERROR: The project you're trying to create already exists in this directory, try another name or another location...")
    else:
        print('ERROR: Missing critical project information to create it...')


# Execute to launch the Create Project dialog UI
def setProjectUI(ui, set_project_dialog):
    instance_set_project = set_project_dialog()
    # Connects the ok button of the set project dialog to the set project function
    instance_set_project.set_project_signal.connect(lambda: projectLibs.setCurrentProject(ui))
    # Loads the projects into the set project dialog
    projectApp.load_items(instance_set_project.setProjectList)
    # Launches the set project dialog
    instance_set_project.exec()


# Sets the selected project in the set project dialog
def setProject(ui):
    # Queries project data
    item_selection = ui.setProjectList.currentItem()
    if item_selection is not None:
        selected_project = item_selection.text()

        if len(selected_project) != 0:
            # Look for items in the projects database
            raw_data = loginLibs.loadJsonData(projectLibs.PROJECTS_DATABASE)
            projects_names = loginLibs.extractData(raw_data, 'name')
            # Get the position of the selected name
            target_name_position = loginLibs.getDataPosition(projects_names, selected_project)
            # Get the full entry at the given position
            entry = raw_data[target_name_position]
            # Change the cookies to the current project
            loginLibs.registerCookies(entry, projectLibs.CURRENT_PROJECT_DATABASE)
            ui.set_project_signal.emit()

    else:
        print('No project were selected...')


# Logic of the asset or shot button
def createTemplate(ui):
    # Check if asset or shot is selected
    template_type = ui.createTypeComboBox.currentText()

    if template_type == 'ASSET':
        # Create the asset
        creatorApp.createAsset(ui)
        # Reset the fields to their default value
        ui.assetTypeComboBox.setCurrentIndex(0)
        ui.assetNameLineEdit.setText('')
        ui.assetDescriptionPlainText.clear()
        # Update the browser UI
        uiApp.browserUpdateAssets(ui)

    elif template_type == 'SHOT':
        # Prep the shot
        shot_name = creatorApp.prepShot(ui)

        # Check if there is already a shot with this name
        current_project_cookies = loginLibs.loadJsonData('databases/projectData/currentProject.json')
        raw_path = current_project_cookies['shots_path']
        folder_match = creatorLibs.matchingFolder(raw_path, shot_name)

        if folder_match is True:
            print(f'ERROR: Shot {shot_name} has already been created...')
        else:
            creatorApp.createShot(ui, shot_name)
            # Update the browser UI
            uiApp.browserUpdateShots(ui)

        # Reset the fields to their default value
        ui.sequenceSpinBox.setValue(1)
        ui.shotSpinBox.setValue(1)
        ui.masterLayoutRadioButton.setChecked(False)
        ui.shotDescriptionPlainText.clear()


# Logic for the UI switch of the browser tab
def browserUpdateUI(ui):
    # Check the name of the button and display the list view accordingly
    if ui.browserButton.text() == 'ASSET BROWSER':
        # Update the list of sequences
        uiApp.browserSequenceUpdate(ui)

        # Update UI
        ui.browserButton.setText('SHOT BROWSER')
        ui.browserStackedWidget.setCurrentIndex(1)

    elif ui.browserButton.text() == 'SHOT BROWSER':
        ui.browserButton.setText('ASSET BROWSER')
        ui.browserStackedWidget.setCurrentIndex(0)


# Gets the currently selected item and navigates to it in the folder view
def browserGoToSelection(ui, clicked_widget, shots_or_assets: str):
    # Get current database data
    current_project_cookies = loginLibs.loadJsonData('databases/projectData/currentProject.json')
    database_file = Path(current_project_cookies['path']) / 'project_data.json'
    raw_data = loginLibs.loadJsonData(str(database_file))
    database = raw_data[shots_or_assets]

    # Get the selected name
    item = clicked_widget.currentItem()
    name = item.text()

    # Query the category of asset/shot
    if shots_or_assets == 'shots':
        category = ui.shotCategoryComboBox.currentText()
    elif shots_or_assets == 'assets':
        category = ui.assetCategoryComboBox.currentText()

    # Build the path to the desired directory
    selection_path = database[name]['path']
    if shots_or_assets == 'shots':
        selection_path = str(Path(selection_path) / 'maya/scenes' / category)
    elif shots_or_assets == 'assets':
        selection_path = str(Path(selection_path) / 'maya/scenes/edit' / category)

    # Update the UI to the selected path
    model = ui.model
    ui.fileManagerColumnView.setCurrentIndex(model.index(selection_path))

    # Check if the directory is empty
    is_empty = browserLibs.directoryEmpty(selection_path)

    # If the directory is empty open a popup to create maya file
    if is_empty is True:
        uiApp.mayaFileUI(uiView.MayaFileUI, name, selection_path, category)

    return model.index(selection_path)


# Creates and initialises maya files for empty directories
def initMayaFile(raw_name, file_path, step):
    formatted_name = f'{raw_name}_{step}_E_001'

    # Create the Maya file
    creatorLibs.createMayaFile(formatted_name, file_path)

    print(f'{formatted_name.upper()} was created successfully.')


# Process to open a file when an item from the file explorer gets double-clicked
def openFileFromExplorer(ui, explorer_widget):
    # Get the full path to the double-clicked item
    full_path, item = fileApp.getClickedFilePath(explorer_widget)

    try:
        # Check if it is a Maya file
        if str(full_path).endswith('.ma') is True or str(full_path).endswith('.mb') is True:
            # Launches the process to open the file
            openMayaFileProcess(ui, str(full_path))
            # Adds the file to the recent files list
            item_name = item.data()
            recentFilesApp.addToRecentFiles(ui, item_name, full_path)
        # If it's not a maya file, open it with its default application
        else:
            fileLibs.openFile(str(full_path))

    except:
        print("WARNING: Sewers can't open this file type...")


# Opens A file in a running instance of maya or creates one, it also creates a connection with SEWERS
def openMayaFileProcess(ui, file_path: str):
    file_path = Path(file_path)

    if file_path.exists() is False:
        print("ERROR: This file couldn't be open because of an issue with the path...")

    else:
        cmds_open_command = f'import maya.cmds as cmds; cmds.file(force=1, save=1); cmds.file(r"{file_path}", force=1, open=1); cmds.commandPort(name=":5050", sourceType="python");'

        if socketLibs.isProgramOpen('maya.exe') is True:
            # Check if Maya is open and connected
            is_connected = socketLibs.isConnectedToMaya(ui)
            if is_connected is True:
                # Check if the current file is untitled
                is_untitled = actionButtonsLibs.isCurrentUntitled(ui)

                if is_untitled is True:
                    buffer_file = Path.cwd() / 'temp/buffer_file.ma'
                    buffer_file = buffer_file.as_posix()
                    # Open the buffer file
                    socketApp.sendMayaCommandProcess(ui, f'cmds.file(rename="{str(buffer_file)}")')
                    socketApp.sendMayaCommandProcess(ui, f'cmds.file(save=True, type="mayaAscii")')

                # Open the requested file
                socketApp.sendMayaCommandProcess(ui, cmds_open_command)
            else:
                print('ERROR: Maya is open but not connected, connect and try again...')

        else:
            fileApp.openMayaFile(str(file_path))


# Saves a version of the file currently opened in Maya
def saveVersionProcess(ui):
    # Check if Maya is open and connected
    is_connected = socketLibs.isConnectedToMaya(ui)

    if socketLibs.isProgramOpen('maya.exe') and is_connected is True:
        # Get the path and name of the current file opened in Maya
        path = socketApp.sendMayaCommandProcess(ui, 'cmds.file(query=1, sceneName=1)')
        name = socketApp.sendMayaCommandProcess(ui, 'cmds.file(query=1, sceneName=1, shortName=1)')

        # Get the new name and path to save the file
        test_save_version_info = actionButtonsApp.getNewVersionInfo(name, path)
        if len(test_save_version_info) == 0:
            print("ERROR: the file couldn't be versioned up, probably due to an incorrect naming...")
        else:
            new_name, new_path = test_save_version_info
            # Saves a version of the file
            actionButtonsApp.saveVersion(ui, new_path, new_name, name)

            # Embed the saved by data into the file
            current_username = loginLibs.getCurrentUsername()
            socketApp.sendMayaCommandProcess(ui, f'cmds.fileInfo("savedBy", "{current_username}")')

    else:
        print('ERROR: Maya is not open or not connected...')


# Publishes the file currently open in Maya
def savePublishProcess(ui):
    # Check if Maya is open and connected
    is_connected = socketLibs.isConnectedToMaya(ui)

    if socketLibs.isProgramOpen('maya.exe') and is_connected is True:
        # Get the path and name of the current file opened in Maya
        path = socketApp.sendMayaCommandProcess(ui, 'cmds.file(query=1, sceneName=1)')
        name = socketApp.sendMayaCommandProcess(ui, 'cmds.file(query=1, sceneName=1, shortName=1)')
        # Save the current file
        socketApp.sendMayaCommandProcess(ui, 'cmds.file(save=1, type="mayaAscii")')
        # Check if there is already a publish file
        test_publish_info = actionButtonsApp.getPublishInfo(path)
        if len(test_publish_info) == 0:
            print("ERROR: the file couldn't be published as there is no publish folder in the project...")
        else:
            file_path, publish_exists = test_publish_info
            # Publish the file
            actionButtonsApp.savePublish(publish_exists, name, file_path, path)

            # Embed the saved by data into the file
            current_username = loginLibs.getCurrentUsername()
            socketApp.sendMayaCommandProcess(ui, f'cmds.fileInfo("savedBy", "{current_username}")')
    else:
        print('ERROR: Maya is not open or not connected...')


# Opens a pop-up with playblast options, treats them and return a dictionary
def playblastPreProcess(playblast_dialog, explorer_widget):
    # Check if filepath is a Maya file, if not error message
    maya_file = actionButtonsLibs.isClickedMayaFile(explorer_widget)

    if maya_file is None:
        print('ERROR: You need to select a maya file to playblast (.ma or .mb)...')
    else:
        # Get list of all cameras
        cameras = actionButtonsApp.getCamerasList(maya_file)
        # Pop-up with user options
        playblast_ui = playblast_dialog(cameras, maya_file)
        playblast_ui.exec()


# Updates the UI viewer info when executed
def updateViewerInfo(ui, explorer_widget):
    try:
        # Get the full path to the clicked item
        filepath, item = fileApp.getClickedFilePath(explorer_widget)

        if Path(filepath).is_dir() is False:
            asset_info = assetViewerApp.getAssetInfo(filepath)
        else:
            asset_info = None

        # Update the UI
        if asset_info is not None:
            ui.assetNameLabel.setText(asset_info['asset_name'])
            ui.typeAnswerLabel.setText(asset_info['asset_type'])
            ui.currentVersionAnswerLabel.setText(asset_info['current_version'])
            ui.savedByAnswerLabel.setText(asset_info['last_save_user'])
            ui.timeAnswerLabel.setText(asset_info['time_last_save'])
            ui.latestVersionAnswerLabel.setText(asset_info['latest_version'])
            ui.descriptionAnswerLabel.setText(asset_info['description'])
            if asset_info['thumbnail_path'] is not None:
                ui.assetIconButton.setIcon(QIcon(asset_info['thumbnail_path']))

    except:
        print('ERROR: could not update the viewer info...')

# Execute to launch the Add Comment dialog UI
def addCommentUI(add_comment_dialog):
    add_comment_project = add_comment_dialog()
    # Launch the add comment dialog
    add_comment_project.exec()


# Logic to add a comment to the database
def addCommentProcess(ui, explorer_widget, sewers_ui):
    # Query the comment
    comment = ui.addCommentPlainTextEdit.toPlainText()

    # Check if the user is located somewhere in an asset/shot path
    asset_path, asset_name = assetViewerApp.isUserInAsset(explorer_widget)

    # Check if the comment is smaller than 1, if yes throws an error
    if len(comment) < 1:
        print('ERROR: Comments need to be at least 1 character...')
    elif asset_path is None:
        pass
    else:
        # Get the current active username
        username = loginLibs.getCurrentUsername()
        # Get the current date and time and formats it
        current_time = time.time()
        raw_time = time.localtime(current_time)
        comment_time = time.strftime('%d/%m/%y %H:%M', raw_time)
        # Get path to asset comments' database
        comments_database_path = asset_path / '_do_not_touch_' / 'comments_database.json'

        # Format the entry
        final_entry = {'comment': comment, 'comment_time': comment_time, 'user': username}

        # Add the entry to the database
        loginLibs.writeJsonData(final_entry, comments_database_path)

        # Update the View Comments button
        uiApp.updateCommentButtonCount(sewers_ui, explorer_widget)

        print(f'Comment for {asset_name.upper()} was successfully posted.')


# Execute to launch the Review Comments dialog UI
def reviewCommentsUI(review_comments_dialog):
    review_comments_project = review_comments_dialog()
    # Launch the review comments dialog
    review_comments_project.exec()


# Queries the comments' info from the database, passes them to the createWidgets function
def reviewCommentsProcess(ui, sewers_ui):
    # Check if the user is in a valid directory
    asset_path, asset_name = assetViewerApp.isUserInAsset(sewers_ui.fileManagerColumnView)

    if asset_path is None:
        print('ERROR: You are not located within an asset or a shot, failed to load comments...')
    else:
        # Get the path to the comments database
        comments_database_path = asset_path / '_do_not_touch_' / 'comments_database.json'

        # Query the data
        raw_data = loginLibs.loadJsonData(comments_database_path)
        number_of_comments = len(raw_data)
        comments = loginLibs.extractData(raw_data, 'comment')
        usernames = loginLibs.extractData(raw_data, 'user')
        comment_time_stamps = loginLibs.extractData(raw_data, 'comment_time')

        # Create the widgets for the UI and populate it
        for i in reversed(range(number_of_comments)):
            uiApp.createCommentWidgets(ui, usernames[i], comment_time_stamps[i], comments[i], i+1)


# Updates the thumbnail of the viewer
def thumbnailUpdateProcess(ui, explorer_widget):
    # Get the path to the image selected by the user
    raw_output = assetViewerLibs.fileDialogReturnFile(ui, 'Choose a thumbnail for the asset/shot...')
    source_path = raw_output[0]

    # Get the path to the current asset
    asset_path, asset_name = assetViewerApp.isUserInAsset(explorer_widget)

    if source_path == '' or asset_path is None:
        pass
    else:
        source_path = raw_output[0]
        source_extension = source_path.split('.')[-1]
        thumbnail_path = asset_path / '_do_not_touch_' / f'thumbnail.{source_extension}'

        # Upload the selected file to the asset database
        shutil.copy(source_path, thumbnail_path)

        updateViewerInfo(ui, explorer_widget)


# Process for updating asset name in the browser
def renameAssetProcess(index, asset_rename_dialog):
    old_name = index.data()
    asset_rename_project = asset_rename_dialog(index=index, old_name=old_name)
    asset_rename_project.exec()


# Process for deleting an asset in the browser
def deleteAssetUI(index, asset_delete_dialog):
    asset_delete_project = asset_delete_dialog(index)
    asset_delete_project.exec()


# Process for renaming files in the explorer
def renameFileUI(index, file_rename_dialog):
    file_rename_project = file_rename_dialog(index)
    file_rename_project.exec()


# Process for creating files in the explorer
def createFileUI(index, file_create_dialog, file_type):
    file_create_project = file_create_dialog(index, file_type)
    file_create_project.exec()


# Process to determine which function to execute depending on the type of file required
def createFileProcess(file_path, file_name, file_type):
    match file_type:
        case 'maya':
            contextMenusApp.mayaFileProcess(file_path, file_name)
        case 'zbrush':
            contextMenusApp.zbrushFileProcess(file_path, file_name)


# main command for references and imports to current Maya scene
def sewersReferenceImportMaya(ui, index, operation_type):
    # Error catching
    try:
        file_name = index.data()
        clean_file_name = file_name.removesuffix(Path(file_name).suffix)
    except:
        print('WARNING: This command needs a selected file to process...')
        return
    if file_name is None:
        print('WARNING: This command needs a selected file to process...')
        return
    if Path(file_name).suffix != '.ma' and Path(file_name).suffix != '.mb':
        print('WARNING: This command can only be performed on Maya files...')
        return

    # Links the corresponding function depending on the operation type
    match operation_type:
        case 'import':
            contextMenusApp.importMayaFile(ui, index, clean_file_name)
        case 'reference':
            contextMenusApp.referenceMayaFile(ui, index, clean_file_name)
        case _:
            print('ERROR: Unsupported operation type...')
