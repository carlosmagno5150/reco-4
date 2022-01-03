import settings
import os
from os.path import isfile, isdir
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory


def ask_open_file():
    Tk().withdraw()
    return askopenfilename()


def ask_open_directory():
    Tk().withdraw()
    return askdirectory()


def create_default_dir():
    known_dir = settings.get_known_dir()
    unknown_dir = settings.get_unknown_dir()
    # Check whether the specified path exists or not
    exist1 = os.path.exists(known_dir)
    exist2 = os.path.exists(unknown_dir)
    if not exist1:
        os.makedirs(known_dir)
    if not exist2:
        res = f'{unknown_dir}/resized'
        os.makedirs(f'{unknown_dir}')
        os.makedirs(res)


def check_name_in_known_dir(name):
    name = name.lower()
    cwd = f"{os.getcwd()}\{settings.get_known_dir()}"
    count = 0
    filenames = os.listdir(cwd)
    for file in filenames:
        if isfile(f'{cwd}\{file}'):
            str = file.split('_')
            if (str[0] == name):
                count += 1
    return f'{name}_{count + 1}'


def get_name(name_img):
    names = name_img.split('/')
    names = names[len(names)-1].split('_')
    return names[0]


def get_files(path):
    files = []
    filenames = os.listdir(path)
    for file in filenames:
        if isfile(f'{path}/{file}'):
            if '.jpg' in file.lower() or '.png' in file.lower() or '.jpeg' in file.lower():
                files.append(f'{path}/{file}')
    return files


def get_sub_directories(path):
    dirs = []
    filenames = os.listdir(path)
    for file in filenames:
        if isdir(f'{path}/{file}'):
            dirs.append(f'{path}/{file}')
    return dirs
