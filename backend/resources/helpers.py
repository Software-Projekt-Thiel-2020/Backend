from typing import List


def check_params_int(params: List):
    """
    Checks a List of params if they are really castable to int.

    :except: ValueError if one of the Parameters isn't an int
    :return: -
    """
    for param in params:
        if param:
            int(param)
