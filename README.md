<h1 align="center">
  <br>
  <a href="" rel="noopener">
  <img src="img\sp-icon-header.png"></a>
  <br>
  Shard Projector
  <br>
</h1>

<h4 align="center">Desktop dedicated servers for Steam-based games.</h4>
<p align="center">
  <a href="#about">About</a> |
  <a href="#features">Features</a> | 
  <a href="#usage">Usage</a> |
  <a href="#known-issues">Known Issues</a> |
  <a href="#contributing">Contributing</a> |
  <a href="#notice">Notice</a>
</p>

# About

Shard Projector is in active development. While efforts will be made to keep documentation informative and accurate, it too is subject to drastic changes. Some lapses in reliability may arise during this phase. 

Current features target **Don't Starve Together** servers and development will keep that heading as a priority until Shard Projector could be considered a substantial benefit to the game's community. To that end several major updates are planned.

# Features

Shard Projector is a 64bit, multi-threaded desktop app for running Don't Starve Together servers on Windows with support for Linux & MACOSX coming soon. 

![Shard Projector](img/sp-running-preview.png)

# Usage

## Release
Users can download Shard Projector from [releases](https://github.com/ryanraposo/shard-projector/releases). No installation necessary. Unzip to a convenient location and run as expected. 

## Source
 
Use model.py to run Shard Projector with the interpreter.

## Build

Alternatively, you can build a binary bundle. You'll need pyinstaller:

```
pip install pyinstaller
```

Then run the build script:
```
python scripts/build.py
```

# Known Issues

Windows (v0.1a)
- if targeted server configuration folder is not located in (..Documents\Klei\DoNotStarveTogether) the server may fail to start.
- a gameserver based at C:/steamcmd is expected by Shard Projector even when the UI suggests otherwise

# Contributing

UNDER CONSTRUCTION

# Notice

Valve is not associated with this project in any way. 

Klei Entertainment is not associated with this project in any way. 


