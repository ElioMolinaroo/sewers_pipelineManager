from pathlib import Path

# Recursive function that goes through a dict to find unique values to a given key
def findKeyValues(data, target_key, receiving_list):
    for key, value in data.items():
        if isinstance(value, dict):
            findKeyValues(value, target_key, receiving_list)
        elif key == target_key:
            if value in receiving_list:
                pass
            else:
                receiving_list.append(value)


# This function helps you get a list of shots if one of their parameter (ie: sequence) has a specific value
def findShotsWithValue(shots, parameter, value):
    matching_shots = []

    for shot_name, shot_params in shots.items():
        if parameter in shot_params and shot_params[parameter] == value:
            matching_shots.append(shot_name)

    return matching_shots


# Sort a string by its trailing number
def sortByTrailingNumber(s):
    # Extract the trailing number from the string
    number = float(s.split('Sequence ')[-1])
    return number


# Checks for files in directory
def directoryEmpty(path):
    is_empty = next(Path(path).iterdir(), None) is None
    return is_empty
