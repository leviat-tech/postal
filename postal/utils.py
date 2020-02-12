import os
import re
from subprocess import call


# call a shell command in subprocess
def shell(command, silent=False):
    if silent:
        with open(os.devnull, 'w') as DEVNULL:
            return call(command, shell=True, stdout=DEVNULL, stderr=DEVNULL) == 0
    else:
        return call(command, shell=True) == 0

def sanitized_working_directory():
    return re.sub('[^0-9a-zA-Z]+', '-', os.path.basename(os.getcwd())).strip('-')
