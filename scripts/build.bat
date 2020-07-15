pyinstaller -n="shard_projector" -w --noconfirm ^
    --icon="./img/icon.ico" ^
    --add-data="./img/*;./img" ^
    --add-data="./ini/*;./ini" ^
.\source\model.py