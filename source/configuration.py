import sys
import configparser
import pathlib, shutil
import os
import requests
import zipfile
import subprocess

from constants import PLATFORMS
import wh

class Environment:
    """Has methods for bootstrapping dependencies & initializing environment variables.
    """

    def __init__(self):
        self.platform = self._get_platform()
        self.programs = self._get_installed_programs()

    def _get_platform(self) -> PLATFORMS:
        if sys.platform == "win32":
            return PLATFORMS.WINDOWS
        elif sys.platform == "linux" or sys.platform == "linux2":
            return PLATFORMS.LINUX
        elif sys.platform == "darwin":
            return PLATFORMS.MACOSX
    
    def _get_installed_programs(self):
        if self.platform == PLATFORMS.WINDOWS:
            return wh.get_all()

    def program_is_installed(self, patterns):
        for each in self.programs:
            name = each['name'].lower()
            if all(elem in name for elem in patterns):
                return True
        return False

    def debug_search_installed_programs(self, patterns):
        matches = []
        for each in self.programs:
            name = each['name'].lower()
            if all(elem in name for elem in patterns):
                matches.append(name)
        print('[debug search installed programs] matches:', matches)

    def install_steamcmd(self, update_config=False):
        """Installs SteamCMD as an add-in (shard-projector/add-ins/steamcmd).

        Raises:
            Exception: If SteamCMD add-in is already installed, a FileExistsError will be raised.
        """

        temp_path = os.path.join(pathlib.Path(__file__).parents[1], "temp")
        install_path = os.path.join(pathlib.Path(__file__).parents[1], "add-ins", "steamcmd")
        exec_path = os.path.join(install_path, "steamcmd.exe")

        if os.path.exists(exec_path):
            raise FileExistsError("SteamCMD add-in already installed.")
        
        # Download latest steamcmd installer zip to temp directory
        zurl = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
        response = requests.get(zurl)
        zpath = os.path.join(temp_path, "steamcmd.zip")
        zfile_io = open(zpath, 'wb')
        zfile_io.write(response.content)
        zfile_io.close()

        # Extract zip contents to add-ins/steamcmd and delete zip from temp
        zfile = zipfile.ZipFile(zpath, 'r')
        zfile.extractall(install_path)
        zfile.close()
        os.remove(zpath)

        # Run installer in add-ins/steamcmd
        exec_path = os.path.join(install_path, "steamcmd.exe")
        subprocess.Popen(exec_path)


class Configuration:
    """A reader/writer for a specific (.ini) configuration file.
    """

    def __init__(
        self,
        path=None,
        defaults_path=None
        ):
        self.path = path
        self._parser = configparser.ConfigParser(strict=False)
        if defaults_path:
            self.set_defaults(defaults_path)
        
    def _read(self):
        """Reads the INI configuration into internal memory.
        """
        return self.path in self._parser.read(self.path)

    def as_dict(self):
        """Gets INI configuration as a dictionary.
           
        Returns:
            configuration_dict (dict): Sections mapped to a dictionary of key-value pairs.
        """
        self._read()
        configuration_dict = {}
        for section in self._parser.sections():
            configuration_dict[section] = {}
            for key, val in self._parser.items(section):
                val = val.strip('"')
                val = val.strip("'")
                configuration_dict[section][key] = val
        return configuration_dict

    def get(self, section, option):
        """Gets value text as it appears in the configuration file.

        Args:
            section (str): The section to be retrieved.
            option (str): The option to be retrieved.

        Returns:
            value (str): The corresponding value.
        """
        self._read()
        return self._parser.get(section, option)

    def get_typed(self, section, option):
        """Gets value from configuration file as expected type.

        Args:
          section (str): The section to be retrieved.
          option (str): The option to be retrieved.

        Returns:
            value : Boolean for 'true' and 'false' values, int for numeric, and str for others.
        """
        self._read()
        value = self._parser.get(section, option)
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        if value.isnumeric():
            return int(value)

    def get_sections(self):
        """Gets sections from the INI configuration file.
        
        Returns:
            sections (list): A list of section names.
        """        
        self._read()
        return self._parser.sections()

    def update_from_dict(self, dictionary):
        """Updates INI configuration file from a dictionary. 
        
        Args:
            dictionary (dict): Sections mapped to key-value pairs.
        """        
        self._read()
        for section in dictionary:
            for k, v in dictionary[section].items():
                self._parser.set(section, k, v)
        with open(self.path, 'w') as configfile:
            self._parser.write(configfile)

    def set_defaults(self, path):
        self._parser.read(path)
        self.defaults = self.as_dict()

