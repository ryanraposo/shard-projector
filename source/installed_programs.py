"""
Derivative of code originally authored by Orsiris de Jong
"""
import winreg

def get_reg_entries(hive, flag):
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                          0, winreg.KEY_READ | flag)

    count_subkey = winreg.QueryInfoKey(aKey)[0]

    installation_entries = []

    for i in range(count_subkey):
        software = {}
        try:
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]
            try:
                software['version'] = winreg.QueryValueEx(asubkey, "DisplayVersion")[0]
            except EnvironmentError:
                software['version'] = 'undefined'
            try:
                software['publisher'] = winreg.QueryValueEx(asubkey, "Publisher")[0]
            except EnvironmentError:
                software['publisher'] = 'undefined'
            installation_entries.append(software)
        except EnvironmentError:
            continue

    return installation_entries

def get_all():
    local_32 = get_reg_entries(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY)
    local_64 = get_reg_entries(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY)
    current_user = get_reg_entries(winreg.HKEY_CURRENT_USER, 0)

    installed_program_list = local_32 + local_64 + current_user
    return installed_program_list
