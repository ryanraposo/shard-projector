pyinstaller -n="Shard Projector" -w --noconfirm --icon="./img/dstctl.ico" --add-data="./img/*;./img" --add-data="./data/ini/cluster_configuration.json;./data/ini" --add-data="./data/ini/shard_configuration.json;./data/ini" dstctl.py