from enum import Enum
import os, pathlib


APP_DIR = os.path.join(pathlib.Path(__file__).parents[1])

ADDINS = {    
    "STEAMCMD" : {
        "DOWNLOAD" : "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip", # Download from
        "UNPACK" : "steamcmd", # Unzip to
        "INSTALL" : "", # Install with
        "PATH" : "steamcmd", # Find at
        "USE" : "steamcmd/steamcmd.exe", # Run with
        "UPDATE" : "steamcmd/steamcmd.exe" # Update with
    },
    "NULLRENDERER" : {
        "DOWNLOAD" : None,
        "UNPACK" : None,
        "INSTALL" : "steamcmd/steamcmd.exe +login anonymous +app_update 343050 validate +quit",
        "PATH" : "steamcmd/steamapps/common/Don't Starve Together Dedicated Server",
        "USE" : "steamcmd/steamapps/common/Don't Starve Together Dedicated Server/bin/dontstarve_dedicated_server_nullrenderer.exe",
        "UPDATE" : "steamcmd/steamcmd.exe +login anonymous +app_update 343050 validate +quit"
    }
}
