
pyinstaller -n="shard_projector" -w --noconfirm ^
--icon="./img/icon.ico" ^
--add-data="./img/*;./icon" ^
--add-data="./img/*;./img" ^
--add-data="./data/ini/cluster_configuration.json;./data/ini" ^
--add-data="./data/ini/shard_configuration.json;./data/ini" ^
.\source\model.py