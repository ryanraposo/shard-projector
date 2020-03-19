pyinstaller -n="shard_projector" -w --noconfirm ^
--icon="./icon/icon.ico" ^
--add-data="./icon/*;./icon" ^
--add-data="./img/*;./img" ^
--add-data="./data/ini/cluster_configuration.json;./data/ini" ^
--add-data="./data/ini/shard_configuration.json;./data/ini" ^
model.py