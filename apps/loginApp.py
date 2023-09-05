import libs.loginLibs as loginLibs

BASE_PERMISSIONS_LEVEL = 'artist'


# Registers a new user
def userRegister(username: str, password: str):
    # Get the path to the users database
    database_path = loginLibs.pathToDatabase('users.json')

    # Registers the user in the database
    formatted_entry = loginLibs.formatCredentialsEntry(username, password, BASE_PERMISSIONS_LEVEL)
    loginLibs.writeJsonData(formatted_entry, database_path)

    # Register the cookies
    cookies_entry = loginLibs.formatCredentialsEntry(username, password, BASE_PERMISSIONS_LEVEL)
    loginLibs.registerCookies(cookies_entry)

    print(f'User {username} added to the database')


# Checks for user's information and, if correct, logs the user in
def userLogin(username: str, password: str):
    # Load the JSON users file as a dictionary
    database_path = loginLibs.pathToDatabase('users.json')
    raw_data = loginLibs.loadJsonData(database_path)
    # Looks for the list of users
    users = loginLibs.extractData(raw_data, 'username')

    # Check if the username is in the database
    if username in users:
        # Get the position of the found username in the list
        username_position = loginLibs.getDataPosition(users, username)
        # Get the password at the matching position
        passwords = loginLibs.extractData(raw_data, 'password')
        password_at_pos = loginLibs.getDataAtPosition(passwords, username_position)
        # Get the permissions level at the matching position
        permissions_levels = loginLibs.extractData(raw_data, 'permissions_level')
        permissions_at_pos = loginLibs.getDataAtPosition(permissions_levels, username_position)

        # Check if the password matches the one given
        if password_at_pos == password:

            # Register the cookies
            cookies_entry = loginLibs.formatCredentialsEntry(username, password, permissions_at_pos)
            loginLibs.registerCookies(cookies_entry)

            print(f"You're logged in as {username}.")
            return ['success', permissions_at_pos]

        else:
            print("ERROR: The password provided doesn't match the username...")
            return ['failure', permissions_at_pos]

    else:
        print('ERROR: This username is not in the database...')
        return 'failure'


# Logs the current user out
def userLogout(ui):
    # Get the current user information from the cookies
    loginLibs.deleteCookies()
    # Change the username back to the default ____
    ui.usernameLabel.setText('_____')
    print("You're logged out.")
