<h1 align="center">
  <br>
  <a href="" rel="noopener">
  <img src="img\sp-icon-header.png"></a>
  <br>
  Shard Projector
  <br>
</h1>

<h3 align="center">Desktop dedicated servers for Don't Starve Together</h3>
<p align="center">
  <a href="#features">Features</a> | 
  <a href="#usage">Usage</a> |
  <a href="#contributing">Contributing</a> |
  <a href="#notice">Notice</a>
</p>


<a align="center">

![built-with-love](https://gist.githubusercontent.com/ryanraposo/4aad8e64cd9c91db72b1b641cce4c90b/raw/5cbddb10fed1f0bb02a8632ea83a06a325b2d9a8/built-with-love.svg) ![might-just-ship-it](img/might-just-ship-it.png)

</a>


# Notes

Shard Projector is in active development. While efforts will be made to keep documentation informatve and accurate, it too is subject to drastic changes. Some lapses in reliability may arise during this phase.

Thank you for your patience, and remember to report issues where able!


**06/28/20**

- Shard Projector v0.1a may require technical knowledge to work on your system. 

- Incoming (1-3 days) release v0.2a introduces a feature (Add-ins) that enables reliable circumvention of the related issues. There are no releases planned before then.

# Features

Shard Projector is a 64bit, multi-threaded desktop app for running Don't Starve Together servers on Windows with support for Linux & MACOSX coming soon. 

![Shard Projector](img/sp-running-preview.png)

# Usage

## Release
Users can download Shard Projector from releases. No installation necessary. Unzip to a convenient location and run as expected. 

## Source
 
Use model.py to run Shard Projector with the interpreter.

## Build

Alternatively, you can build a binary bundle. You'll need pyinstaller:

```
pip install pyinstaller
```

Then run the build script:
```
python scripts\build.py
```

# Known Issues

Windows (v0.1a)
- if targeted server configuration folder is not located in (..Documents\Klei\DoNotStarveTogether) the server may fail to start.
- a nullrenderer based at C:/steamcmd is expected by Shard Projector even when the UI suggests otherwise

# Contributing 

# Notice

Valve is not associated with this project in any way. 

Klei Entertainment is not associated with this project in any way. 


