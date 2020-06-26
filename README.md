<p align="center">
  <a href="" rel="noopener">
 <img width=400px height=400px src="img\sp-icon-header.png" alt="Shard Projector"></a>
</p>

<p align="center" style="font-size: 300%"> Shard Projector
</p>
<p align="center" style="font-size: 140%"> Desktop dedicated servers for Don't Starve Together. 
</p>
<br>

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Dev Journal](#dev-journal)
  - [Simple Setup](#simple-setup)
  - [In-app World Configuration](#in-app-world-configuration)
- [Features](#features)
    - [Modern Interface & Architecture](#modern-interface--architecture)
    - [Webview & Remote commands (experimental)](#webview--remote-commands-experimental)
    - [Cross-platform](#cross-platform)
- [Getting Started](#getting-started)
  - [Usage](#usage)
    - [(Alpha) Windows](#alpha-windows)
    - [(*Unstable*) Linux](#unstable-linux)
- [What's working right now?](#whats-working-right-now)
- [What's being worked on?](#whats-being-worked-on)
    - [For developers](#for-developers)
    - [For users](#for-users)
- [Notice](#notice)
  
# Introduction

Shard Projector is a user-friendly, 64bit, multi-threaded desktop app for running Don't Starve Together servers on Windows & Linux. 

Run worlds of all kinds easily for you & your friends; on dedicated servers that are simple to setup, manage, moderate and access- even when you're not online. Works great with both online and LAN servers, and supports all kinds of server setups.

If you have a PC and internet connection from this decade, you might be able to drop your monthly hosting bill for good. No technical expertise necessary. 

# Dev Journal

These are the main feature goals for Shard Projector that are still in progress. Alot is already present, but I want to see the entire process even simpler, and for everybody.

Check back for notes and dates for their implementation, I'll be journaling here as I work!

## Simple Setup 
Automated installation of everything you need to run your own dedicated servers. Just download the game from steam, the latest version of Shard Projector, and it will take care of the rest.

- Installers
  - [ ] Automatic, guided installer for SteamCMD and a version of DST that servers run on
  - [ ] Auto-updating to make sure your servers stay current

## In-app World Configuration
Tools and a design that makes world management simple, just like in Don't Starve Together's interface. No need to trackdown setups from 5-year-old forum posts or mess around with text files (or terminals!).


- Easy Menus
  - [x] Settings (general) cluster.ini/server.ini
  - [ ] Settings (mods) modoverrides.lua 
  - [ ] Settings (worldgen) worldgenoverride.lua

## No Limitation Remote Access







# Features

### Modern Interface & Architecture


Simple yet powerful controls for running, monitoring, and configuring your server.

![Shard Projector](img/sp-running-preview.png)

### Webview & Remote commands (experimental)

Connect to a machine running a Shard Projector server remotely to check status (http), or send commands remotely

### Cross-platform

Developed with Tkinter, a framework for creating user-interfaces. Its a standard python library, and is packaged with all Python installations.

# Getting Started


## Usage

### (Alpha) Windows 

Requires a steamcmd installation of Don't Starve Together Dedicated Server! 

- Easy: Users can download Shard Projector from releases. No installation necessary. Unzip to a convenient location and run as expected. 
- Other: Building isn't necessary. Clone the repo and run with model.py as an entry point. Might need to install a few packages using pip.

*Known issue (v0.1a): if targeted server configuration folder is not located in (..Documents\Klei\DoNotStarveTogether) the server may fail to start.*

### (*Unstable*) Linux

- Clone the repo and run with model.py as an entry point. Unstable and not optimized, but not far off :)

# What's working right now?

*Note: many of these are present but still in early stages of development. Bugs all over.* 

- Windows support
- Simple targeting of server configuration folders. ex 'MyDediServer'
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
- 'Mover' ui tool for development
- Cluster-token generation out-of-game (may not be feasible)

### For users
- 2-way implementation of the web interface
- Better scrolling
- Better resizing (sorry!)
- Viewing & configuration of mods
- Generation of new servers

# Notice

Klei Entertainment is not associated with this project in any way. 
