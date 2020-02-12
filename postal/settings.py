import os
import re

config = {
    'stack': re.sub('[^0-9a-zA-Z]+', '-', os.path.basename(os.getcwd())).strip('-'),
    'mode': 'development',
    'compose': f'stack/development.yml'
}
