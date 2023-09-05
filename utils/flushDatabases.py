from pathlib import Path
import json


def flushTextFile(file_path):
    with open(file_path, 'w') as file:
        file.close()


def flushJsonFile(file_path):
    data = []
    with open(file_path, 'w') as file:
        json.dump(data, file)
        file.close()


def flushDatabases():
    databases_path = Path.cwd() / 'databases'

    # Get texts path into a list
    houdini_path_file = databases_path / 'houdiniPythonLibsPath.txt'
    maya_path_file = databases_path / 'mayaPath.txt'
    python_path_file = databases_path / 'pythonPath.txt'
    text_paths = [houdini_path_file, maya_path_file, python_path_file]

    # Get JSON paths
    pre_login_cookies_file = databases_path / 'preLoginCookies.json'
    users_file = databases_path / 'users.json'
    current_project_file = databases_path / 'projectData' / 'currentProject.json'
    projects_file = databases_path / 'projectData' / 'projects.json'
    json_paths = [pre_login_cookies_file, users_file, current_project_file, projects_file]

    # Flush the databases
    for text_file in text_paths:
        flushTextFile(text_file)
    for json_file in json_paths:
        flushJsonFile(json_file)


flushDatabases()
