import os
import pathlib

DIR_ROOT = pathlib.Path(__file__).parents[1]  # If source...
if os.path.exists(os.path.abspath('./shard_projector.exe')): # If binary bundle...
    DIR_ROOT = os.path.dirname(pathlib.Path(__file__)) 
DIR_INI = os.path.join(DIR_ROOT, "ini")
DIR_TEMP = os.path.join(DIR_ROOT, "temp")
DIR_EXT = os.path.join(DIR_ROOT, "ext")
DIR_IMG = os.path.join(DIR_ROOT, "img")
    
# STEAMCMD = {
#     "REQUIRES" : None, # Check for...
#     "DOWNLOAD" : "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip", # Download from...
#     "UNPACK" : "steamcmd", # Unzip to...
#     "INSTALL" : "steamcmd/steamcmd.exe", # Install with...
#     "PATH" : "steamcmd", # Find at...
#     "EXECUTE" : "steamcmd/steamcmd.exe", # Run with...
#     "UPDATE" : None # Update with...
# }
# NULLRENDERER = {
#     "REQUIRES" : STEAMCMD,
#     "DOWNLOAD" : None,
#     "UNPACK" : None,
#     "INSTALL" : "steamcmd/steamcmd.exe +login anonymous +app_update 343050 validate +quit",
#     "PATH" : "steamcmd/steamapps/common/Don't Starve Together Dedicated Server",
#     "EXECUTE" : "steamcmd/steamapps/common/Don't Starve Together Dedicated Server/bin/dontstarve_dedicated_server_nullrenderer.exe",
#     "UPDATE" : "steamcmd/steamcmd.exe +login anonymous +app_update 343050 validate +quit"
# }


if __name__ == "__main__":
    for each in [DIR_ROOT, DIR_INI, DIR_IMG, DIR_EXT]:
        print(each)