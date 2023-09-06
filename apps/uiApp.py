import os
import sys

from PyQt6 import QtCore
from PyQt6 import QtWidgets
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtGui import QFont

from apps import assetViewerApp
from apps import socketApp
from control import sewersController
from libs import browserLibs
from libs import loginLibs
from libs import projectLibs
from libs import uiLibs

UI_THEME_STATE = 'light'


# Preps the UI, adding the missing elements from the sewersUI.ui file
def prepUi(ui):
    # Create the default connections for the login/register combo box
    ui.loginButton.model().item(0).setEnabled(False)

    # Create and set a model for the tree view
    path = 'C:/'
    model = QFileSystemModel()
    model.setRootPath(QtCore.QDir.rootPath())  # Set the root path for the model
    ui.fileManagerColumnView.setModel(model)
    ui.fileManagerColumnView.setRootIndex(model.index(path))

    # Limits the number of characters for the asset and shots descriptions
    ui.assetDescriptionPlainText.textChanged.connect(lambda: uiLibs.limitCharacters(ui.assetDescriptionPlainText, 120))
    ui.shotDescriptionPlainText.textChanged.connect(lambda: uiLibs.limitCharacters(ui.shotDescriptionPlainText, 120))

    # Create the status bar logic
    socketApp.updateConnectionStatus(ui)

    # Create the change of creator type (shot or asset widgets)
    def handleIndexChanged():
        index = ui.createTypeComboBox.currentIndex()
        ui.creatorStackedWidget.setCurrentIndex(index)
    ui.createTypeComboBox.currentIndexChanged.connect(handleIndexChanged)

    # Update the assets
    browserUpdateAssets(ui)

    return model


# Initialise function of the login module, checking for cookies
def sewersInit():
    # Check for existing user cookies
    test_cookies = loginLibs.checkForCookies()

    # if no cookies were found
    if test_cookies == 0:
        print("You're not logged in, please login to use Sewers...")
        return 'noLog'

    # If cookies were found
    elif test_cookies == 2:
        current_username = loginLibs.getCurrentUsername()
        database_path = loginLibs.pathToDatabase('preLoginCookies.json')
        data = loginLibs.loadJsonData(database_path)
        user_permissions = data['permissions_level']
        print(f'Logged in as {current_username}')

        return ['loggedIn', current_username, user_permissions]

    # If there is an error with the cookies database
    else:
        print("ERROR: Unexpected issue in the cookies' database...")

        return 'Error'


# Checks whether a username is in the users database or not
def usernameInDatabase(username):
    # Load the JSON users file as a dictionary
    database_path = loginLibs.pathToDatabase('users.json')
    raw_data = loginLibs.loadJsonData(database_path)
    # Looks for the list of users
    users = loginLibs.extractData(raw_data, 'username')

    # Check if the username is in the database
    if username in users:
        return True
    else:
        return False


# Updates the UI when the login or register process is successful
def loginRegisterUpdateUI(ui):
    # Gets the username of the new user
    current_username = loginLibs.getCurrentUsername()
    ui.usernameLabel.setText(current_username)

    # Sets the permissions level of the user
    database_path = loginLibs.pathToDatabase('preLoginCookies.json')
    data = loginLibs.loadJsonData(database_path)
    current_permissions = data['permissions_level']
    ui.userRoleLabel.setText(current_permissions)

    # Sets the current project if found in cookies
    current_project_path = projectLibs.getCurrentProject(projectLibs.CURRENT_PROJECT_DATABASE)[1]
    if len(current_project_path) != 0:
        projectLibs.setCurrentProject(ui)
        uiLibs.enableButtons(ui)
    else:
        for i in ui.userUiInputs:
            i.setEnabled(False)
        ui.createProjectButton.setEnabled(True)
        ui.loadProjectButton.setEnabled(True)
        ui.setProjectButton.setEnabled(True)
        ui.logoutButton.setEnabled(True)


# Updates the sequences in the sequences list
def browserSequenceUpdate(ui):
    data = projectLibs.getProjectData()

    sequences = []

    if len(data) != 0:
        browserLibs.findKeyValues(data, 'sequence', sequences)

        def sortByTrailingNumber(s):
            # Extract the trailing number from the string
            number = float(s.split('Sequence ')[-1])
            return number
        sorted_sequences = sorted(sequences, key=sortByTrailingNumber)

        # Update the UI
        ui.shotComboBox.clear()
        for i in sorted_sequences:
            ui.shotComboBox.addItem(i)

        ui.shotComboBox.setCurrentIndex(0)


# Updates the shot list according to the selected sequence
def browserUpdateShots(ui):
    raw_data = projectLibs.getProjectData()

    if len(raw_data) != 0:
        shots_database = raw_data['shots']

        # Get the current sequence tab
        current_browsed_sequence = ui.shotComboBox.currentText()

        current_sequence_shots = browserLibs.findShotsWithValue(shots_database, 'sequence', current_browsed_sequence)

        ui.shotListWidget.clear()

        for shot in current_sequence_shots:
            ui.shotListWidget.addItem(shot)


# Updates the asset list according to the selected type
def browserUpdateAssets(ui):
    raw_data = projectLibs.getProjectData()

    if len(raw_data) != 0:
        assets_database = raw_data['assets']

        current_browsed_type = ui.assetComboBox.currentText()
        current_browsed_type = current_browsed_type.lower()

        ui.assetListWidget.clear()

        # Show the assets according to their type
        if current_browsed_type == 'all':
            for asset in assets_database:
                ui.assetListWidget.addItem(asset)
        else:
            # Get the assets matching the selected type
            assets_list = browserLibs.findShotsWithValue(assets_database, 'category', current_browsed_type)
            for asset in assets_list:
                ui.assetListWidget.addItem(asset)


# Execute to launch the Create Project dialog UI
def mayaFileUI(maya_file_dialog, name, path, step):
    instance_maya_file = maya_file_dialog(name, path, step)
    # Launch the project path browser
    instance_maya_file.exec()


# Updates the number of comments displayed on the view comments button
def updateCommentButtonCount(ui, explorer_widget):
    # Suppress the print statements
    original_stdout = sys.stdout
    dummy_stdout = open('temp/dummy_std', 'w')
    sys.stdout = dummy_stdout
    # Call the function and store its return value inside variables
    try:
        asset_path, asset_name = assetViewerApp.isUserInAsset(explorer_widget)
    except:
        asset_path = None
    # Restore the original stdout
    dummy_stdout.close()
    sys.stdout = original_stdout
    os.remove('temp/dummy_std')

    if asset_path is not None:
        # Query the path to the comments' database in the selected asset
        comments_database_path = asset_path / '_do_not_touch_' / 'comments_database.json'

        data = loginLibs.loadJsonData(comments_database_path)
        number_of_comments = len(data)

        # Update the button
        ui.reviewCommentsButton.setText(f'  Review Comments ({number_of_comments})')
    else:
        ui.reviewCommentsButton.setText('  Review Comments (0)')


# Creates the UI elements needed for the See Comments UI and places them accordingly
def createCommentWidgets(ui, username: str, date: str, comment: str, comment_number: int):
    # Create the widgets' names
    frame_name = f'frame00{comment_number}Frame'
    username_name = f'username00{comment_number}Label'
    date_name = f'date00{comment_number}Label'
    comment_name = f'comment00{comment_number}Label'

    # Create the widgets
    frame_widget = QtWidgets.QFrame()
    frame_widget.setObjectName(frame_name)

    username_label = QtWidgets.QLabel(username, parent=frame_widget)
    username_label.setObjectName(username_name)
    username_label.setFont(QFont('Segoe UI', 10))

    date_label = QtWidgets.QLabel(date, parent=frame_widget)
    date_label.setObjectName(date_name)
    date_label.setFont(QFont('Segoe UI', 10))

    comment_label = QtWidgets.QLabel(comment, parent=frame_widget)
    comment_label.setObjectName(comment_name)
    comment_label.setWordWrap(True)

    # Add the widgets to the layout
    grid_layout = QtWidgets.QGridLayout(frame_widget)
    grid_layout.addWidget(username_label, 0, 0)
    grid_layout.addWidget(date_label, 0, 1)
    grid_layout.addWidget(comment_label, 1, 0, 1, 2)

    # Add the frame to the main layout
    ui.scrollAreaLayout.addWidget(frame_widget, 0)


# Toggles between the two themes
def themeToggle(ui, explorer_widget):
    global UI_THEME_STATE

    if UI_THEME_STATE == 'light':
        uiLibs.setToDarkTheme(ui)
        UI_THEME_STATE = 'dark'

    elif UI_THEME_STATE == 'dark':
        uiLibs.setToLightTheme(ui)
        UI_THEME_STATE = 'light'

    # Update Viewer UI only if project is set
    current_project_cookies = loginLibs.loadJsonData('databases/projectData/currentProject.json')
    if len(current_project_cookies) != 0:
        sewersController.updateViewerInfo(ui, explorer_widget)
