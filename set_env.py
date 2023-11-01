from os.path import abspath, dirname, join
from sys import path

# For VSCode compability
parent_folder = dirname(abspath(__file__))
path.insert(0, parent_folder)
path.insert(0, join(parent_folder, 'global_data'))
