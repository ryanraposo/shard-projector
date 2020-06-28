<p align="center">
  <a href="" rel="noopener">
 <img width=400px height=400px src="img\sp-icon-header.png" alt="Shard Projector"></a>
</p>

<p align="center" style="font-size: 300%"> Shard Projector
</p>
<p align="center" style="font-size: 140%"> Desktop dedicated servers for Don't Starve Together. 
</p>
<br>

NOTE: Shard Projector takes technical knowledge to play around with at the moment. In simple terms, it runs like a dream if you have a very predictable setup. That (called localization) is a top priority and well underway, as its the main roadblock for our non-windows friends. Tech knowledge an asset, at least for the alpha phase.

Users looking forward to the ease-of-use aspects don't have long to wait. In fact the development branch build just above this readme will take custom paths and even install steamcmd as an addin all on its own for you, but the release version (v0.1) is a tricky mistress. Thanks for waiting ❤

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Features](#features)
    - [Modern Interface](#modern-interface)
    - [Cross-platform](#cross-platform)
- [Getting Started](#getting-started)
  - [Usage](#usage)
    - [(Alpha) Windows](#alpha-windows)
    - [(Unstable) Linux & MACOSX](#unstable-linux--macosx)
- [What's working right now?](#whats-working-right-now)
- [What's being worked on?](#whats-being-worked-on)
    - [For developers](#for-developers)
    - [For users](#for-users)
- [Notice](#notice)
  
# Introduction

Shard Projector is a user-friendly, 64bit, multi-threaded desktop app for running Don't Starve Together servers on Windows & Linux. 

It was designed to bridge the gap for non-technical players who want to host worlds of their own, and provide an option other than a monthly server-subscription. Use it to run worlds of all kinds easily for you & your friends on dedicated servers that are simple to setup, manage, moderate and access- even when you're not online!

Whether you're running a LAN server at the house, hosting a 24-player online for your region, or debugging mods, Shard Projector has features you'll appreciate.

# Features

### Modern Interface

Simple yet powerful controls for running, monitoring, and configuring your server.

![Shard Projector](img/sp-running-preview.png)

### Cross-platform

Developed with Tkinter, a framework for creating user-interfaces that works wherever Python can run.

Shard Projector currently supports Windows, with Linux and MAC OS X support in mind since the beginning. 

*Note: get in touch with me at raposo.ryan@gmail.com if you'd like to assist with MACOSX optimization/testing. Early-access to new versions a guarantee!*

# Getting Started


## Usage

### (Alpha) Windows 

NOTE: Shard Projector takes technical knowledge to play around with at the moment. Thats going to be characteristic for the alpha phase. Users looking forward to the ease-of-use aspects don't have long to wait, the development build will take custom paths and even install steamcmd as an addin all on its own for you, but the release version (v0.1) is a tricky mistress. Thanks for waiting ❤

moRequires a steamcmd installation of Don't Starve Together Dedicated Server! Localization & pathing are extremely basic in v0.1a, as they are being overhauled to account for Linux and MacOSX. Essentially you must have a steamcmd installation with the server installed at "C:/steamcmd". 

- Easy: Users can download Shard Projector from releases. No installation necessary. Unzip to a convenient location and run as expected. 
- Other: Building isn't necessary. Clone the repo and run with model.py as an entry point. Might need to install a few packages using pip.

*Known issue (v0.1a): if targeted server configuration folder is not located in (..Documents\Klei\DoNotStarveTogether) the server may fail to start.*

### (Unstable) Linux & MACOSX

- Clone the repo and run with model.py as an entry point. Unstable and not optimized, but not far off :) 

# What's working right now?

*Note: many of these are present but still in early stages of development. Please report any issues you experience. Be a hero!* 

- Windows support
- Easy-to-use targeting of server configuration folders. ex 'MyDediServer'
- Shard input/output
- In-app configuration of servers (cluster.ini, server.ini(s))
- In-app configuration of application (environment, paths, etc) 
- Web interface & remote commands (highly experimental)

# What's being worked on?

### For developers
- MVC architecture
- Class architecture
- Custom ttk widgets
- Config-to-widget strategies
- 'Mover' ui tool for development (& making Tkinter your b...*est friend*.)
- Cluster token tasks in-app

### For users
- 2-way implementation of the web interface
- Better scrolling
- Better resizing (sorry!)
- Viewing & configuration of mods
- Generation of new servers

# Notice

Klei Entertainment is not associated with this project in any way. 
