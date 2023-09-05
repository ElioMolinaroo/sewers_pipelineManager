from libs import recentFilesLibs


# Adds a specific file name to the recent files widget
def addToRecentFiles(ui, filename: str, filepath):
    # Get a list of the recent files
    item_names = recentFilesLibs.getRecentFiles(ui)

    if filename in item_names:
        # Get the current position of the item
        file_position = item_names.index(filename)
        # Move the element at the file position to the top
        ui.recentFilesListWidget.takeItem(file_position)
        ui.recentFilesListWidget.insertItem(0, filename)
        # Sets the user data of the item to the path
        recentFilesLibs.setPathData(ui, filepath)

    elif filename not in item_names:
        # Adds the item to the recent files
        ui.recentFilesListWidget.insertItem(0, filename)
        # Sets the user data of the item to the path
        recentFilesLibs.setPathData(ui, filepath)


# In the file explorer, navigates to the path of the selected item in the recent files
def goToSelectedFile(ui):
    # Get the address of the current item
    item_address = ui.recentFilesListWidget.currentItem()
    # Get the path through the User Role
    file_path = recentFilesLibs.getPathData(item_address)

    # Update the UI to the selected path
    model = ui.model
    # Navigates to the file in the file explorer
    ui.fileManagerColumnView.setCurrentIndex(model.index(file_path))
