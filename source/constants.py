import os
import pathlib

DIR_ROOT = pathlib.Path(__file__).parents[1]  # If source...
if os.path.exists(os.path.abspath('./shard_projector.exe')): # If binary bundle...
    DIR_ROOT = os.path.dirname(pathlib.Path(__file__)) 
DIR_INI = os.path.join(DIR_ROOT, "ini")
DIR_TEMP = os.path.join(DIR_ROOT, "temp")
DIR_EXT = os.path.join(DIR_ROOT, "ext")
DIR_IMG = os.path.join(DIR_ROOT, "img")


if __name__ == "__main__":
    for each in [DIR_ROOT, DIR_INI, DIR_IMG, DIR_EXT]:
        print(each)