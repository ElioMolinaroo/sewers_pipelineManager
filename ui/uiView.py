import sys

import qdarktheme
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, QEvent, QObject, QThread, Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QShortcut, QKeySequence

from apps import actionButtonsApp
from apps import contextMenusApp
from time import sleep
from apps import recentFilesApp
from apps import uiApp
from control import sewersController
from libs import creatorLibs
from libs import projectLibs


# Worker thread class for maya connection checking and updating
class CheckConnectionWorker(QObject):
    maya_connected_signal = pyqtSignal()
    maya_disconnected_signal = pyqtSignal()

    def checkMayaConnection(self):
        from libs import socketLibs
        while True:
            sleep(5)
            connection_test = socketLibs.isConnectedToMaya(sewers_window)
            if connection_test is True:
                self.maya_connected_signal.emit()
            elif connection_test is False:
                self.maya_disconnected_signal.emit()


# Class for the main UI window
class SewersUI(QMainWindow):
    def __init__(self):
        super(SewersUI, self).__init__()

        # Load the UI file
        uic.loadUi('ui/sewersUI.ui', self)

        # Change the theme to have an auto dark theme
        qdarktheme.setup_theme('light', custom_colors={"primary": "#191919",
                                                       "foreground": "#191919",
                                                       "background": "f2f2f2"})

        # Create a variable with all the user-driven inputs
        self.userUiInputs = [self.loginButton, self.logoutButton, self.recentFilesListWidget,
                             self.playblastButton, self.publishButton, self.saveVersionButton,
                             self.fileManagerColumnView, self.createProjectButton, self.loadProjectButton,
                             self.setProjectButton, self.rightHandTabs]

        # Declare the last_selected_index global variable
        global last_selected_index
        last_selected_index = None

        # Create the status bar QLabel
        self.statusBarLabel = QLabel()

        # Call initUI function
        self.model = sewersController.initUi(self)

        # Open Maya connection check worker thread
        self.OpenMayaCheckThread()
        # Update UI when signal arrives
        from libs import socketLibs
        self.worker.maya_connected_signal.connect(lambda: socketLibs.statusBarConnectionStatus(self, 'Connected', '#3ec922'))
        self.worker.maya_disconnected_signal.connect(lambda: socketLibs.statusBarConnectionStatus(self, 'Not Connected', '#e32910'))

        # Login module events
        self.loginButton.activated.connect(lambda: sewersController.loginRegisterProcess(self, LoginUI, RegisterUI))
        self.logoutButton.clicked.connect(lambda: sewersController.logoutProcess(self))
        self.userIcon.pressed.connect(lambda: uiApp.themeToggle(self, self.fileManagerColumnView))

        # Project module events
        self.loadProjectButton.clicked.connect(lambda: sewersController.loadProject(self))
        if self.loginButton.isEnabled() is False:
            projectLibs.setCurrentProject(self)
        self.createProjectButton.clicked.connect(lambda: sewersController.createProjectUI(self, CreateProjectUI))
        self.setProjectButton.clicked.connect(lambda: sewersController.setProjectUI(self, SetProjectUI))

        # Creating tabs shortcuts
        slot_1_shortcut = QShortcut(QKeySequence('Alt+1'), self)
        slot_1_shortcut.activated.connect(lambda: self.rightHandTabs.setCurrentIndex(0))
        slot_2_shortcut = QShortcut(QKeySequence('Alt+2'), self)
        slot_2_shortcut.activated.connect(lambda: self.rightHandTabs.setCurrentIndex(1))
        slot_3_shortcut = QShortcut(QKeySequence('Alt+3'), self)
        slot_3_shortcut.activated.connect(lambda: self.rightHandTabs.setCurrentIndex(2))

        # Creator module events
        self.createTemplateButton.clicked.connect(lambda: sewersController.createTemplate(self))
        self.masterLayoutRadioButton.toggled.connect(lambda: creatorLibs.createShotUpdateUI(self))

        # Browser module events
        self.browserButton.clicked.connect(lambda: sewersController.browserUpdateUI(self))
        self.shotComboBox.currentIndexChanged.connect(lambda: uiApp.browserUpdateShots(self))
        self.assetComboBox.currentIndexChanged.connect(lambda: uiApp.browserUpdateAssets(self))

        def goToShotSelectionPlusSaveIndex():
            global last_selected_index
            item_address = sewersController.browserGoToSelection(self, self.shotListWidget, 'shots')
            last_selected_index = item_address
        self.shotListWidget.itemDoubleClicked.connect(lambda: goToShotSelectionPlusSaveIndex())

        def goToAssetSelectionPlusSaveIndex():
            global last_selected_index
            item_address = sewersController.browserGoToSelection(self, self.assetListWidget, 'assets')
            last_selected_index = item_address
        self.assetListWidget.itemDoubleClicked.connect(lambda: goToAssetSelectionPlusSaveIndex())
        # Installing event filter for context menu
        self.shotListWidget.installEventFilter(self)
        self.assetListWidget.installEventFilter(self)

        # File Explorer module events
        self.fileManagerColumnView.activated.connect(lambda: sewersController.openFileFromExplorer(self, self.fileManagerColumnView))
        self.fileManagerColumnView.clicked.connect(lambda: sewersController.updateViewerInfo(self, self.fileManagerColumnView))

        # Keeps track of last selected item
        def setLastSelectedIndex(explorer):
            global last_selected_index
            from apps import fileApp
            path, item_address = fileApp.getClickedFilePath(explorer)
            last_selected_index = item_address
        self.fileManagerColumnView.selectionModel().selectionChanged.connect(lambda: setLastSelectedIndex(self.fileManagerColumnView))
        # Installing event filter for context menu
        self.fileManagerColumnView.installEventFilter(self)

        # Action Buttons module events
        self.saveVersionButton.clicked.connect(lambda: actionButtonsApp.saveVersionConfirmationUI(self, SaveVersionConfirmationUI))
        self.publishButton.clicked.connect(lambda: actionButtonsApp.publishConfirmationUI(self, PublishConfirmationUI))
        self.playblastButton.clicked.connect(lambda: sewersController.playblastPreProcess(PlayblastUI, self.fileManagerColumnView))

        # Recent Files module events
        self.recentFilesListWidget.itemDoubleClicked.connect(lambda: recentFilesApp.goToSelectedFile(self))

        # Viewer module events
        self.assetIconButton.clicked.connect(lambda: sewersController.thumbnailUpdateProcess(self, self.fileManagerColumnView))
        self.addCommentButton.clicked.connect(lambda: sewersController.addCommentUI(AddCommentUI))
        self.reviewCommentsButton.clicked.connect(lambda: sewersController.reviewCommentsUI(ReviewCommentsUI))
        self.rightHandTabs.currentChanged.connect(lambda: uiApp.updateCommentButtonCount(self, self.fileManagerColumnView))

    # Create the event filter for context menus
    def eventFilter(self, source, event):
        source_browser = True if source == self.shotListWidget or source == self.assetListWidget else False

        # Create the explorer context menu
        if source == self.fileManagerColumnView and event.type() == QEvent.Type.ContextMenu:
            index = source.indexAt(event.pos())
            if index.data() is None:
                index = last_selected_index

            # New file sub menu
            self.new_file_menu = QMenu('New File')
            add_maya_file = self.new_file_menu.addAction('Maya File (*.ma)')
            add_nuke_file = self.new_file_menu.addAction('Nuke File (*.nk)')
            add_nuke_file.setEnabled(False)
            add_houdini_file = self.new_file_menu.addAction('Houdini File (*.hip)')
            add_houdini_file.setEnabled(False)
            add_zbrush_file = self.new_file_menu.addAction('ZBrush File (*.zpr)')

            # Maya actions sub menu
            self.maya_actions_menu = QMenu('Maya Actions')
            import_maya_scene = self.maya_actions_menu.addAction('Import')
            reference_maya_scene = self.maya_actions_menu.addAction('Reference')

            # Main menu
            self.explorer_menu = QMenu(self)
            copy_full_path = self.explorer_menu.addAction('Copy Full Path')
            open_folder = self.explorer_menu.addAction('Open Containing Folder')
            self.explorer_menu.addSeparator()
            new_folder = self.explorer_menu.addAction('New Folder')
            self.explorer_menu.addMenu(self.new_file_menu)
            self.explorer_menu.addSeparator()
            rename_object = self.explorer_menu.addAction('Rename')
            delete_object = self.explorer_menu.addAction('Delete')
            self.explorer_menu.addSeparator()
            self.explorer_menu.addMenu(self.maya_actions_menu)
            # Executes the menu for it to be visible where the screen is right-clicked
            execution = self.explorer_menu.exec(event.globalPos())

            # Call the functions according to the clicked action
            if execution == copy_full_path:
                contextMenusApp.copyFullPath(index)
            elif execution == open_folder:
                contextMenusApp.openFolder(index)
            elif execution == delete_object:
                sewersController.deleteAssetUI(index, DeleteFileUI)
            elif execution == rename_object:
                sewersController.renameFileUI(index, RenameFileUI)
            elif execution == new_folder:
                sewersController.renameFileUI(index, CreateFolderUI)
            elif execution == add_maya_file:
                sewersController.createFileUI(index, CreateFileUI, 'maya')
            elif execution == add_zbrush_file:
                sewersController.createFileUI(index, CreateFileUI, 'zbrush')
            elif execution == import_maya_scene:
                sewersController.sewersReferenceImportMaya(self, index, 'import')
            elif execution == reference_maya_scene:
                sewersController.sewersReferenceImportMaya(self, index, 'reference')

            return True

        # Create the browser context menu
        elif source_browser is True and event.type() == QEvent.Type.ContextMenu:
            index = source.indexAt(event.pos())

            browser_menu = QMenu(self)
            delete_asset = browser_menu.addAction('Delete')
            rename_asset = browser_menu.addAction('Rename')
            update_users = browser_menu.addAction('Update Users')
            update_users.setEnabled(False)

            # Executes the menu for it to be visible where the screen is right-clicked
            execution = browser_menu.exec(event.globalPos())

            # Call the functions according to the clicked action
            if execution == rename_asset:
                sewersController.renameAssetProcess(index, RenameAssetUI)
            elif execution == delete_asset:
                sewersController.deleteAssetUI(index, DeleteAssetUI)

            return True

        return super().eventFilter(source, event)

    # Class for Maya connection checks on worker thread
    def OpenMayaCheckThread(self):
        self.thread = QThread()
        self.worker = CheckConnectionWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.checkMayaConnection)

        self.thread.start()


# Class for the login dialog window
class LoginUI(QDialog):
    login_signal = pyqtSignal()

    def __init__(self):
        super(LoginUI, self).__init__()
        # Load the UI file
        uic.loadUi('ui/loginDialog.ui', self)

        # Define the behaviours of the OK button
        self.loginButtonBox.accepted.connect(lambda: sewersController.loginVerification(self))


# Class for the register dialog window
class RegisterUI(QDialog):
    register_signal = pyqtSignal()

    def __init__(self):
        super(RegisterUI, self).__init__()

        # Load the UI file
        uic.loadUi('ui/registerDialog.ui', self)

        # Define the behaviours of the OK button
        self.registerButtonBox.accepted.connect(lambda: sewersController.registerVerification(self))


# Class for the create project dialog window
class CreateProjectUI(QDialog):
    create_project_signal = pyqtSignal()

    def __init__(self):
        super(CreateProjectUI, self).__init__()
        # Load the UI file
        uic.loadUi('ui/createProjectDialog.ui', self)

        # Define the behaviour of the BROWSE button
        from apps.projectApp import createProjectBrowseDialog
        self.browseProjectButton.clicked.connect(lambda: createProjectBrowseDialog(self))

        # Define the behaviours of the OK button
        self.createProjectButtonBox.accepted.connect(lambda: sewersController.createProjectProcess(self))


# Class for the set project dialog window
class SetProjectUI(QDialog):
    set_project_signal = pyqtSignal()

    def __init__(self):
        super(SetProjectUI, self).__init__()
        # Load the UI file
        uic.loadUi('ui/setProjectDialog.ui', self)

        # Define a custom slot for the filter function of the search bar
        self.searchBarLineEdit.textChanged.connect(lambda: projectLibs.filter_items(self.searchBarLineEdit, self.setProjectList))

        # Define the behaviours of the OK button
        self.setProjectButtonBox.accepted.connect(lambda: sewersController.setProject(self))


# Class for the create maya file dialog window
class MayaFileUI(QDialog):
    def __init__(self, name, path, step):
        self.name = name
        self.path = path
        self.step = step

        super(MayaFileUI, self).__init__()
        # Load the UI file
        uic.loadUi('ui/createMayaFileDialog.ui', self)

        # Define the behaviours of the OK button
        self.mayaFileButtonBox.accepted.connect(lambda: sewersController.initMayaFile(self.name, self.path, self.step))


# Class for the save version dialog window
class SaveVersionConfirmationUI(QDialog):
    def __init__(self):
        save_version_signal = pyqtSignal

        super(SaveVersionConfirmationUI, self).__init__()
        # Load the UI file
        uic.loadUi('ui/sewersConfirmationDialog.ui', self)

        # Customise the dialog
        self.sewersConfirmationTextLabel.setText('Saving a version is undoable, are you sure you want to continue?')

        # Define the behaviour of the YES button
        self.sewersConfirmationButtonBox.accepted.connect(lambda: sewersController.saveVersionProcess(self))


# Class for the publish dialog window
class PublishConfirmationUI(QDialog):
    def __init__(self):
        super(PublishConfirmationUI, self).__init__()
        # Load the UI file
        uic.loadUi('ui/sewersConfirmationDialog.ui', self)

        # Customise the dialog
        self.sewersConfirmationTextLabel.setText('Publishing is HIGHLY undoable, are you sure you want to continue?')

        # Define the behaviour of the YES button
        self.sewersConfirmationButtonBox.accepted.connect(lambda: sewersController.savePublishProcess(self))


# Class for the playblast dialog window
class PlayblastUI(QDialog):
    def __init__(self, cameras_list, maya_file):
        self.cameras_list = cameras_list
        self.maya_file = maya_file

        super(PlayblastUI, self).__init__()
        # Load the UI file
        uic.loadUi('ui/playblastDialog.ui', self)

        # Set the default path User Role to ''
        self.pathPushButton.setProperty('playblast_path', None)

        # Updates the cameras
        self.cameraComboBox.addItems(self.cameras_list)

        # Define the behaviour of the path button
        self.pathPushButton.clicked.connect(lambda: actionButtonsApp.getPlayblastFolder(self))

        # Define the behaviour of the OK button
        self.playblastButtonBox.accepted.connect(lambda: actionButtonsApp.tryPlayblast(self, self.maya_file))


# Class for the create project dialog window
class AddCommentUI(QDialog):
    def __init__(self):
        super(AddCommentUI, self).__init__()
        # Load the UI file
        uic.loadUi('ui/addCommentDialog.ui', self)

        # Limit the number of characters in the dialog
        from libs.uiLibs import limitCharacters
        self.addCommentPlainTextEdit.textChanged.connect(lambda: limitCharacters(self.addCommentPlainTextEdit, 250))

        # Define the behaviours of the OK button
        self.addCommentButtonBox.accepted.connect(lambda: sewersController.addCommentProcess(self, sewers_window.fileManagerColumnView, sewers_window))


# Class for the create project dialog window
class ReviewCommentsUI(QDialog):
    def __init__(self):
        super(ReviewCommentsUI, self).__init__()
        # Load the UI file
        uic.loadUi('ui/seeCommentsDialog.ui', self)

        # Create necessary widgets and populate the UI
        sewersController.reviewCommentsProcess(self, sewers_window)


# Class for the renameAsset dialog window
class RenameAssetUI(QDialog):
    def __init__(self, index, old_name):
        self.index = index
        self.old_name = old_name

        super(RenameAssetUI, self).__init__()
        # Load the UI file
        uic.loadUi('ui/sewersRenameDialog.ui', self)

        # Set the lineEdit to have the old name in it by default
        self.newNameLineEdit.setText(old_name)

        # Define the behaviours of the OK button
        self.sewersRenameButtonBox.accepted.connect(lambda: contextMenusApp.renameAsset(sewers_window, self.index, self.newNameLineEdit.text()))


# Class for the deleteAsset dialog window
class DeleteAssetUI(QDialog):
    def __init__(self, index):
        self.index = index

        super(DeleteAssetUI, self).__init__()
        # Load the UI file
        uic.loadUi('ui/sewersDeleteDialog.ui', self)

        # Set the lineEdit to have the old name in it by default
        self.sewersDeleteTextLabel.setText('Are you sure you want to delete this object? It will be moved to the trash folder of the SEWERS...')

        # Define the behaviours of the OK button
        self.sewersDeleteButtonBox.accepted.connect(lambda: contextMenusApp.deleteAsset(sewers_window, self.index))


# Class for deleting files from the explorer window
class DeleteFileUI(QDialog):
    def __init__(self, index):
        self.index = index

        super(DeleteFileUI, self).__init__()
        # Load the UI file
        uic.loadUi('ui/sewersDeleteDialog.ui', self)

        # Set the lineEdit to have the old name in it by default
        self.sewersDeleteTextLabel.setText('Are you sure you want to delete this object? It will be moved to the trash folder of the SEWERS...')

        # Define the behaviours of the OK button
        self.sewersDeleteButtonBox.accepted.connect(lambda: contextMenusApp.deleteFile(sewers_window, self.index))


# Class for renaming files from the explorer window
class RenameFileUI(QDialog):
    def __init__(self, index):
        self.index = index

        super(RenameFileUI, self).__init__()
        # Load the UI file
        uic.loadUi('ui/sewersRenameDialog.ui', self)

        # Define the behaviours of the OK button
        self.sewersRenameButtonBox.accepted.connect(lambda: contextMenusApp.renameFile(sewers_window, self.index, self.newNameLineEdit.text()))


# Class for creating folders from the explorer window
class CreateFolderUI(QDialog):
    def __init__(self, index):
        self.index = index

        super(CreateFolderUI, self).__init__()
        # Load the UI file
        uic.loadUi('ui/sewersRenameDialog.ui', self)

        # Modify the UI elements to make a create folder dialog
        self.sewersRenameTitleLabel.setText('CREATE FOLDER')
        self.newNameLabel.setText('Folder name:')
        self.sewersRenameTextLabel.setText('This action is undoable but you can easily delete it afterwards. Otherwise, click no...')

        # Define the behaviours of the OK button
        self.sewersRenameButtonBox.accepted.connect(lambda: contextMenusApp.createFolder(sewers_window.model.filePath(self.index), self.newNameLineEdit.text()))


# Class for creating files from the explorer window
class CreateFileUI(QDialog):
    def __init__(self, index, file_type):
        self.index = index
        self.file_type = file_type

        super(CreateFileUI, self).__init__()
        # Load the UI file
        uic.loadUi('ui/sewersRenameDialog.ui', self)

        # Modify the UI elements to make a create folder dialog
        self.sewersRenameTitleLabel.setText('CREATE FILE')
        self.newNameLabel.setText('File name:')
        self.sewersRenameTextLabel.setText('This action is undoable but you can easily delete it afterwards. Otherwise, click no...')

        # Define the behaviours of the OK button
        self.sewersRenameButtonBox.accepted.connect(lambda: sewersController.createFileProcess(sewers_window.model.filePath(self.index), self.newNameLineEdit.text(), self.file_type))


# Top function launching the SEWERS
def startUI():
    global sewers_window

    # Initialise the app
    app = QApplication([])
    print('Sewers loaded successfully.')
    sewers_window = SewersUI()
    sewers_window.show()
    sys.exit(app.exec())
