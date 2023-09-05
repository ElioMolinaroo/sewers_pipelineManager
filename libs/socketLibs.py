import socket
import subprocess

from apps import socketApp

PORT = 5051


# Tries to connect to Maya
def connectToMaya(port):
    global maya_socket

    try:
        maya_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to Maya's command port
        maya_host = 'localhost'  # Maya's hostname or IP address
        maya_port = port  # The command port number used in Maya
        maya_socket.connect((maya_host, maya_port))
        return True

    except:
        #print("ERROR: The connection with Maya couldn't be made...")
        return False


# Disconnects from the running maya socket
def disconnectFromMaya():
    maya_socket.close()


# Sends commands to Maya
def sendMayaCommand(command: str):
    try:
        test_bytes = command.encode('utf-8')
        maya_socket.sendall(test_bytes)
    except:
        pass


def getMayaOutput():
    data = maya_socket.recv(1024)
    data = data.replace(b'\n\x00', b'').decode('utf-8')
    return data


# Creates the status bar connection status
def statusBarConnectionStatus(ui, connection_status: str, status_colour: str):
    # Add a permanent message to the status bar
    maya_connection_status = connection_status
    ui.statusBarLabel.setText(f'Maya Connection Status: {maya_connection_status}')
    ui.statusBar.addPermanentWidget(ui.statusBarLabel)

    # Change the style of the Status Bar message
    status_bar_colour = status_colour
    ui.statusBarLabel.setStyleSheet(f'color: {status_bar_colour}; font-weight: bold;')


# Checks if a given process is running
def isProgramOpen(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use built-in check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())


# Check if SEWERS are connected to Maya
def isConnectedToMaya(ui):
    try:
        connection_test = socketApp.sendMayaCommandProcess(ui, '1')
    except Exception as e:
        connection_test = False

    if connection_test is False:
        return False
    else:
        return True


# Check if the socket is open on the client side (SEWERS)
def isSocketOpen(sock):
    try:
        sock.fileno()
        return True
    except sock.error:
        return False
