from enum import Enum
import os, pathlib


APP_DIR = os.path.join(pathlib.Path(__file__).parents[1])

ADDINS = {    
    "STEAMCMD" : {
        "REQUIRES" : None,
        "DOWNLOAD" : "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip", # Download from
        "UNPACK" : "steamcmd", # Unzip to
        "INSTALL" : "steamcmd/steamcmd.exe", # Install with
        "PATH" : "steamcmd", # Find at
        "EXECUTE" : "steamcmd/steamcmd.exe", # Run with
        "UPDATE" : None# Update with
    },
    "NULLRENDERER" : {
        "REQUIRES" : "STEAMCMD",
        "DOWNLOAD" : None,
        "UNPACK" : None,
        "INSTALL" : "steamcmd/steamcmd.exe +login anonymous +app_update 343050 validate +quit",
        "PATH" : "steamcmd/steamapps/common/Don't Starve Together Dedicated Server",
        "EXECUTE" : "steamcmd/steamapps/common/Don't Starve Together Dedicated Server/bin/dontstarve_dedicated_server_nullrenderer.exe",
        "UPDATE" : "steamcmd/steamcmd.exe +login anonymous +app_update 343050 validate +quit"
    }
}
