import json
import hashlib
from pathlib import Path
import os

# Variable describing the path to the cookies' database on each machine
LOGIN_COOKIES_DATABASE = Path(os.getenv('USERPROFILE')) / '.sewers' / 'databases' / 'preLoginCookies.json'

"""Create the functions of the login module"""


'''# Creates the formatting of the username/password pair into a dictionary entry
def formatCredentialsEntry(username: str, password: str, permissions_level: str):
    return {"username": username, "password": password, "permissions_level": permissions_level}
'''

# Loads data from a JSON file as a dictionary
def loadJsonData(database_path):
    with open(database_path, 'r') as file:
        data = json.load(file)
        file.close()

    return data


# Adds a dictionary entry to an existing JSON file
def writeJsonData(dict_entry, database_path):
    with open(database_path, 'r+') as file:
        file_data = json.load(file)
        file_data.append(dict_entry)
        file.seek(0)
        json.dump(file_data, file, indent=3)
        file.close()


# Returns the path to the given database
def pathToDatabase(database_name: str):
    path = Path(os.getenv('USERPROFILE')) / '.sewers' / 'databases' / database_name
    return path


# Extracts a piece of data from the database
def extractData(database_dict: dict, data_name: str):
    target_data = []
    for i in database_dict:
        target_data.append(i[data_name])

    return target_data


# Extracts the position of a string in a given list
def getDataPosition(data_list: list, target_string: str):
    position = 0
    for i in data_list:
        if i == target_string:
            break
        position += 1

    return position


# Checks for password at given position in dict
def getDataAtPosition(database_list: list, data_position: int):
    return database_list[data_position]


'''# Get the current username from the cookies
def getCurrentUsername():
    # Get the path to the users database
    database_path = pathToDatabase('preLoginCookies.json')

    # Load the cookies database
    data = loadJsonData(database_path)

    # Extract the name of the user
    cookies_username = data['username']

    return cookies_username


# Checks in the cookies' database is a user is already present
def checkForCookies(cookies_path=LOGIN_COOKIES_DATABASE):
    # Checks if the given cookie file has already one registered user inside
    with open(cookies_path) as file:
        user_cookies = json.load(file)
        file.close()

    if len(user_cookies) == 0:
        return 0
    elif len(user_cookies) == 1:
        return 1
    else:
        return 2'''


# Registers a username in the cookies' database
def registerCookies(cookies_entry, cookies_path=LOGIN_COOKIES_DATABASE):
    # Replace the contents of the cookies JSON file by the updated cookies
    with open(cookies_path, 'w') as file:
        json.dump(cookies_entry, file, indent=3)
        file.close()


# Delete cookies from the given cookies' database
def deleteCookies(cookies_path=LOGIN_COOKIES_DATABASE):
    # Replace the contents of the cookies JSON file by the updated cookies
    with open(cookies_path, 'w') as file:
        file.close()
    with open(cookies_path, 'r+') as file:
        json.dump([], file)
        file.close()


# Hashes a password into a sha256 object and returns a string of it
def passwordHasher(password: str):
    # Hashes the password into a sha256 object
    test_hash = hashlib.sha256()
    test_hash.update(password.encode())
    # Output the hashed password as a string
    hash_password = test_hash.hexdigest()
    return hash_password
