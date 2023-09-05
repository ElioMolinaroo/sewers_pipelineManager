from pathlib import Path

import qdarktheme
from PyQt6.QtGui import QIcon

from control import sewersController


# Returns the name of the action required by the user in a combo box
def comboBoxSelection(combo_box):
    user_selection = combo_box.currentText()
    return user_selection


# Disables all the user interface except for the login button
def disableButtons(ui):
    for i in ui.userUiInputs:
        i.setEnabled(False)
    ui.loginButton.setEnabled(True)


# Enables all the user interface except for the login button
def enableButtons(ui):
    for i in ui.userUiInputs:
        i.setEnabled(True)
    ui.loginButton.setEnabled(False)


# Shows a dialog window
def showDialogUI(dialog):
    instance_dialog = dialog()

    instance_dialog.exec()


# Returns the content of a QLineEdit
def returnLineEdit(line_edit):
    # Retrieve the text from the QLineEdit and print it
    text = line_edit.text()
    return text


# Limits the number of characters of a plain text widget
def limitCharacters(widget, max_chars: int):
    current_text = widget.toPlainText()

    if len(current_text) > max_chars:
        # Sets the text to the same one without the last character
        widget.setPlainText(current_text[:max_chars])
        # Places the cursor back at the end of the text
        cursor = widget.textCursor()
        cursor.setPosition(max_chars)
        widget.setTextCursor(cursor)


# Sets the UI to the dark theme
def setToDarkTheme(ui):
    qdarktheme.setup_theme('dark', custom_colors={"primary": "#d9d9d9",
                                                  "foreground": "#d9d9d9",
                                                  "background": "#242424"})

    # Set icons to their dark version
    ui.addCommentButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'addCommentAlt.png')))
    ui.createProjectButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'createProjectAlt.png')))
    ui.loadProjectButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'loadProjectAlt.png')))
    ui.logoutButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'logOutAlt.png')))
    ui.playblastButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'playblastAlt.png')))
    ui.publishButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'publishAlt.png')))
    ui.reviewCommentsButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'reviewCommentsAlt.png')))
    ui.saveVersionButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'saveVersionAlt.png')))
    ui.setProjectButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'setProjectAlt.png')))
    ui.assetIconButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'takeSnapshotButtonAlt.png')))
    ui.userIcon.setIcon(QIcon(str(Path.cwd() / 'icons' / 'userLogoAlt.png')))


# Sets the UI to the light theme
def setToLightTheme(ui):
    qdarktheme.setup_theme('light', custom_colors={"primary": "#191919",
                                                   "foreground": "#191919",
                                                   "background": "f2f2f2"})

    # Set icons to their light version
    ui.addCommentButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'addComment.png')))
    ui.createProjectButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'createProject.png')))
    ui.loadProjectButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'loadProject.png')))
    ui.logoutButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'logOut.png')))
    ui.playblastButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'playblast.png')))
    ui.publishButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'publish.png')))
    ui.reviewCommentsButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'reviewComments.png')))
    ui.saveVersionButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'saveVersion.png')))
    ui.setProjectButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'setProject.png')))
    ui.assetIconButton.setIcon(QIcon(str(Path.cwd() / 'icons' / 'takeSnapshotButton.png')))
    ui.userIcon.setIcon(QIcon(str(Path.cwd() / 'icons' / 'userLogo.png')))
