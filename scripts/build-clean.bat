echo "Cleaning up build folders, artifacts, and output..."
del shard_projector.spec
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q __pycache__
