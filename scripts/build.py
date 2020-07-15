import subprocess, os.path
from os.path import abspath, basename, dirname, exists, join


print("""
[1] Normal
[2] No Artifacts
[3] Debug
""")

batch = ""

user_input = input("Select a build option [1-3]: ")
if user_input == '1':
    batch = abspath("scripts/build.bat")
elif user_input == '2':
    batch = abspath("scripts/build-noartifacts.bat")
elif user_input == '3':
    batch = abspath("scripts/build-debug.bat")
else:
    quit()

print(batch)
subprocess.call(batch)