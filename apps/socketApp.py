from libs import socketLibs


# Checks if Maya is open if yes it tries to execute the command, if not updates the status bar
def sendMayaCommandProcess(ui, command: str):
    maya_open = socketLibs.isProgramOpen('maya.exe')

    if maya_open is True:
        # Opens a socket and connects to it
        socketLibs.connectToMaya(socketLibs.PORT)
        # Send a command to Maya
        socketLibs.sendMayaCommand(command)
        # Get the output data sent from Maya
        data = socketLibs.getMayaOutput()
        # Disconnects from the socket
        socketLibs.disconnectFromMaya()

        #socketLibs.statusBarConnectionStatus(ui, 'Connected', '#3ec922')
        return data

    else:
        #socketLibs.statusBarConnectionStatus(ui, 'Not Connected', '#e32910')
        return False


# Updates the Connection status automatically
def updateConnectionStatus(ui):
    connection_test = socketLibs.isConnectedToMaya(ui)
    if connection_test is True:
        socketLibs.statusBarConnectionStatus(ui, 'Connected', '#3ec922')
    elif connection_test is False:
        socketLibs.statusBarConnectionStatus(ui, 'Not Connected', '#e32910')


# Connects Safely to Maya and throws an error to SEWERS otherwise
def safeMayaConnect(ui, port):
    if socketLibs.isConnectedToMaya(ui) is True:
        return True
    else:
        print('TRYING TO CONNECT...')
        socketLibs.connectToMaya(port)
