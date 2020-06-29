"""For f5 building in vscode. 
"""

import subprocess, os

batch_path = os.path.abspath("scripts/build.bat")

subprocess.call(
    batch_path
)