import shutil, os

MOD_DIR = "C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\mods"

mod_dir_list = os.listdir(MOD_DIR)

for member in mod_dir_list:
    path = os.path.join(MOD_DIR, member)
    if os.path.isdir(path) and ".zip" not in path:
        info_path = os.path.join(path, 'modinfo.lua')
        if os.path.isfile(info_path):
            with open(os.path.normpath(info_path), encodi1ng='utf-8') as item:
                for line in item:
                    if "name=" in line or "name =" in line:
                        workshop_id = os.path.basename(member)
                        name = line.split("=")[1]
                        print(name, workshop_id, "\n")
                        break
                    

                    