if __name__ != '__main__':
    # For VSCode compability
    from os.path import abspath, dirname
    from sys import path
    parent_folder = dirname(abspath(__file__))
    path.insert(0, parent_folder)

from CONFIGURATION import *
from LoadedDbData import LoadedDbData
from BotEntities import BotEntities


class GlobalData(BotEntities, LoadedDbData):
    def __init__(self):
        super().__init__()
        pass


global_data = GlobalData()

if __name__ == '__main__':
    from pprint import pprint
    print(GlobalData.__mro__)
    pprint(global_data.listen_channels)
    pprint(global_data.real_account_bot)
    if global_data.listen_channels[-1001669922752]['reply_id']:
        print('True')
    else:
        print('False')
