from os import listdir, mkdir
from os.path import abspath, dirname, isdir


def make_local_dir(folder: str = "log"):
    """Creates a log file folder if it does not yet exist"""

    work_dir = dirname(abspath(__file__))
    folder_path = work_dir + "\\" + folder

    if not isdir(folder_path):
        try:
            mkdir(folder_path)
            print(f"OK: created {folder_path}")
        except OSError as error:
            print(f"ERROR: (undetected) folder exists already, so: \n    {error}.")
            return False
    else:
        print(f"Ok: {folder} folder exists already.")

    return folder_path


def make_file_path(folder_path: str, file_str: str = "dqn"):
    """Creates new file path that does not yet exist"""

    dir_list = listdir(folder_path)
    print(f"Info: I found {len(dir_list)} files in folder_path.")

    for i in range(1000):
        name = file_str + str(i)
        if name not in dir_list:
            logfile_path = folder_path + "/" + name
            break
    print(f"Ok: made file_path for file {name}")
    return logfile_path, name


class DotDict(dict):
    """Enables dot.notation access to dictionary attributes"""

    def __getattr__(*args):
        val = dict.get(*args)
        return DotDict(val) if type(val) is dict else val

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
