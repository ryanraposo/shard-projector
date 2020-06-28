
pyinstaller -n="shard_projector" -w --noconfirm ^
--icon="./img/icon.ico" ^
--add-data="./img/*;./icon" ^
--add-data="./img/*;./img" ^
--add-data="./data/*;./data" ^
--add-data="./source/cluster_defaults.ini;./" ^
--add-data="./source/settings.ini;./" ^
--add-data="./source/settings_defaults.ini;./" ^
--add-data="./source/shard_defaults.ini;./" ^
.\source\model.py

echo "Cleaning up build artifacts..."
del shard_projector.spec
rmdir /s /q build
rmdir /s /q __pycache__