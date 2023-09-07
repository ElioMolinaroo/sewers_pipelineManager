from pathlib import Path

from databases.projectData import projectStructures
from libs import loginLibs
from libs import projectLibs


# Create the main function for the project loader
# TODO add the project artists functionality
def prepareLoadProject(ui):
    # Locate the project
    project_path = projectLibs.fileDialogReturnFolder(ui, 'Load a Project')

    # Check if a folder was selected
    if len(project_path) != 0:
        # Get the name of the project
        project_name = projectLibs.getFolderName(project_path)

        # Replace cookies in the current project database
        current_cookies_path = projectLibs.CURRENT_PROJECT_DATABASE
        cookies_entry = projectLibs.formatProjectData(project_name, project_path, [], '', '', '')
        loginLibs.registerCookies(cookies_entry, current_cookies_path)

        # Enter cookies in the projects database
        projects_cookies_path = projectLibs.PROJECTS_DATABASE
        loginLibs.writeJsonData(cookies_entry, projects_cookies_path)

        return [project_path, project_name, [], '', '']
    else:
        return ['', '', '', '', '']


# Launches the UI for the project location browser
def createProjectBrowseDialog(ui):
    # Locate the project
    project_path = projectLibs.fileDialogReturnFolder(ui, 'Choose a directory for your project')

    # Set the line edit of the browse project to the chosen project
    if len(project_path) != 0:
        ui.browseProjectLineEdit.setText(project_path)


# Uses the provided information to create a project and update the Sewers UI
def createProject(project_name: str, project_path, project_template: str):
    # Get the dictionary corresponding to the project template
    if project_template == 'Asset ESMA':
        base_folder_structure = projectStructures.struct_assetESMA
        assets_path = ''
        shots_path = ''
        project_type = 'asset'
    elif project_template == 'Pipeline ESMA':
        base_folder_structure = projectStructures.struct_pipelineESMA
        assets_path = str(Path(project_path) / project_name / projectStructures.assets_pipelineESMA)
        shots_path = str(Path(project_path) / project_name / projectStructures.shots_pipelineESMA)
        project_type = 'pipeline'

    # Change the name of the project
    folder_structure = projectLibs.changeProjectName(project_name, base_folder_structure)

    # Create the folder structure
    formatted_path = Path(project_path)
    projectLibs.createFolderStructure(folder_structure, formatted_path)

    # Update project path to be INSIDE the directory and not just before it
    project_path = f'{project_path}/{project_name}'

    # Create the project database
    projectLibs.createProjectData(project_path)

    # Replace cookies in the database
    cookies_path = projectLibs.CURRENT_PROJECT_DATABASE
    cookies_entry = projectLibs.formatProjectData(project_name, project_path, [], assets_path, shots_path, project_type)
    loginLibs.registerCookies(cookies_entry, cookies_path)

    # Enter cookies in the projects database
    projects_cookies_path = projectLibs.PROJECTS_DATABASE
    loginLibs.writeJsonData(cookies_entry, projects_cookies_path)


# Loads the items into the set project list
def load_items(list_widget):
    # Clear the existing items in the list widget
    list_widget.clear()
    # Look for items in the projects database
    raw_data = loginLibs.loadJsonData(projectLibs.PROJECTS_DATABASE)
    projects_names = loginLibs.extractData(raw_data, 'name')
    # Add items to the list widget
    list_widget.addItems(projects_names)
