import configparser
import os
from os.path import abspath, basename, dirname, exists, join
import requests
import sys
import shutil
import subprocess
import zipfile

from constants import *


class Ini:
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
        """Reads the Ini configuration into internal memory.
        """
        return self.path in self._parser.read(self.path)

    def as_dict(self):
        """Gets Ini configuration as a dictionary.
           
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
        """Gets sections from the Ini configuration file.
        
        Returns:
            sections (list): A list of section names.
        """        
        self._read()
        return self._parser.sections()

    def update_from_dict(self, dictionary):
        """Updates Ini configuration file from a dictionary. 
        
        Args:
            dictionary (dict): Sections mapped to key-value pairs.
        """        
        self._read()
        for section in dictionary:
            for k, v in dictionary[section].items():
                self._parser.set(section, k, v)
        with open(self.path, 'w') as configfile:
            self._parser.write(configfile)
    
    def set(self, section, option, value):
        self._read()
        if value is None:
            value = ""
        self._parser.set(section, option, value)
        with open(self.path, 'w') as configfile:
            self._parser.write(configfile)
            
    def set_defaults(self, path):
        self._parser.read(path)
        self.defaults = self.as_dict()


class ResourceManager:
    """Responsible for: downloading, unpacking, installing, updating and tracking of application Add-Ins
    according to defined specifications and sequences.
    """
    def __init__(self):
        self.installed_dir = DIR_ADDINS
        self.downloaded_dir = DIR_TEMP

        config_path = join(DIR_INI, 'resource_manifest.ini')
        self.manifest = Ini(config_path)
        
        self._update_manifest()

    def _update_manifest(self):
        """Updates manifest records for downloaded Add-In packages and installations.
        """        
        for name, item in ADDINS.items():
            # Check for Add-In installation, update record.
            installation_path = join(self.installed_dir, item["PATH"])
            if exists(installation_path):
                self.manifest.set(name, "installed", installation_path)
            else:
                self.manifest.set(name, "installed", None)
            # Check for Add-In downloaded, update record.
            if item["DOWNLOAD"]:
                payload = basename(item["DOWNLOAD"])
                downloaded_path = join(self.downloaded_dir, payload)
            if exists(downloaded_path):
                self.manifest.set(name, "downloaded", downloaded_path)
            else:
                self.manifest.set(name, "downloaded", None)
        
    def _download(self, addin):
        """Downloads Add-In zip from its defined web source. Replaces any existing
        web download for Add-In.
        """
        if addin["DOWNLOAD"]:
            response = requests.get(addin["DOWNLOAD"])
            z_path = join(self.downloaded_dir, basename(addin["DOWNLOAD"]))
            shutil.rmtree(z_path, True)
            z_file_io = open(z_path, 'wb') #TODO: debug
            z_file_io.write(response.content)
            z_file_io.close()

    def _unpack(self, addin):
        """Extracts Add-In zip to its defined unpack location.
        """
        if addin["UNPACK"]:
            zip_path = join(self.downloaded_dir, basename(addin["DOWNLOAD"]))
            zfile = zipfile.ZipFile(zip_path, 'r')
            zfile.extractall(join(self.installed_dir, addin["UNPACK"]))
            zfile.close()
            os.remove(zip_path)

    def _install(self, addin):
        """Install Add-In  using its defined installation executable and returns
        the subprocess.
        """
        self._update_manifest()
        exec_install = addin["INSTALL"]
        if exec_install:
            return subprocess.Popen(self.path_to(exec_install))

    def _update(self, addin):
        """Update Add-In using its defined update executable and returns
        the subprocess.
        """
        self._update_manifest()
        exec_update = addin["UPDATE"]
        if exec_update:
            return subprocess.Popen(self.path_to(exec_update))

    def _uninstall(self, addin): 
        """Uninstall Add-In by deleting its installation folder.
        """
        self._update_manifest()
        installation = join(self.installed_dir, addin["PATH"])
        shutil.rmtree(installation, True)

    def verified_install(self, addin, shouldReaquire=False):
        """Performs Add-In component checks where applicable in descending
        order of necessity: Dependencies, base directory, and executable. If all
        pass, returns True. If any fail, returns False. [DEBUG WITH CAUTION]

        Args:
            addin (const Dict):  Dictionary of sequence and component information
            for a compatible Add-In.
            shouldReaquire (bool): If true, any failed checks will also result in an attempted
            reaquisition.
        """
        check = {}
        if addin["REQUIRES"]: # If expected and missing, verified_install it then continue
            dependency = addin["REQUIRES"]
            check["Dependency"] = self.verified_install(ADDINS[dependency], shouldReaquire)             
        if addin["EXECUTE"]: # Note presence if expected 
            check["Executable"] = exists(self.path_to(addin["EXECUTE"]))
        if addin["PATH"]: # Note presence if expected
            check["Directory"] = exists(self.path_to(addin["PATH"]))

        if all(case == True for case in check.values()): 
            return True

        if any(not case for case in [check["Executable"], check["Directory"]]):
            if shouldReaquire:
                self.reaquire(addin)
            return False

    def reaquire(self, addin):
        self._uninstall(addin)
        if addin["DOWNLOAD"]: self._download(addin)            
        if addin["UNPACK"]: self._unpack(addin)
        if addin["INSTALL"]: self._install(addin)
        if addin["UPDATE"]: self._update(addin)

    def path_to(self, segment):
        if 'zip' in segment:
            return join(self.downloaded_dir, segment)
        return join(self.installed_dir, segment)




