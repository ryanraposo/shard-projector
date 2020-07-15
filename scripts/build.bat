pyinstaller -n="shard_projector" -w --noconfirm ^
    --icon="./img/icon.ico" ^
    --add-data="./img/*;./img" ^
    --add-data="./ini/*;./ini" ^
.\source\model.py

echo "Creating empty directories..."
cd dist/shard_projector
mkdir add-ins
mkdir temp