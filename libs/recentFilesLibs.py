from PyQt6.QtCore import Qt


# Gets a list of all the files in recent names
def getRecentFiles(ui):
    number_of_items = ui.recentFilesListWidget.count()
    items_list = []

    for item in range(number_of_items):
        current_item = ui.recentFilesListWidget.item(item)
        item_name = current_item.text()
        items_list.append(item_name)

    return items_list


# Sets the data of the top-most item to the given file path
def setPathData(ui, filepath: str):
    item_address = ui.recentFilesListWidget.item(0)
    item_address.setData(Qt.ItemDataRole.UserRole, filepath)


# Reads the data of a given address
def getPathData(item_address):
    filepath = item_address.data(Qt.ItemDataRole.UserRole)
    filepath = str(filepath)

    return filepath
