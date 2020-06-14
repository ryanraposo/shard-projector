<p align="center">
  <a href="" rel="noopener">
 <img width=400px height=400px src="img\sp-icon-header.png" alt="Shard Projector"></a>
</p>

<p align="center" style="font-size: 300%"> Shard Projector
</p>
<p align="center" style="font-size: 140%"> Desktop dedicated servers for Don't Starve Together
</p>
<br>

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Features](#features)
    - [Modern Interface](#modern-interface)
    - [Web Access](#web-access)
    - [Cross-platform](#cross-platform)
- [Getting Started](#getting-started)
  - [Usage](#usage)
- [What's working right now?](#whats-working-right-now)
- [What's being worked on?](#whats-being-worked-on)
    - [For developers:](#for-developers)
    - [For users:](#for-users)
- [Notice](#notice)
  
# Features

### Modern Interface

Simple yet powerful controls for running, monitoring, and configuring your server.

![Shard Projector](img/sp-running-preview.png)

### Web Access

Connect to a machine running a Shard Projector server and check status remotely via HTTP.

### Cross-platform

Developed with Tkinter, a framework for creating user-interfaces. Its included with Python by default, and works on all platforms.

# Getting Started

## Usage

(*Pre-alpha*) Windows 

- Easy: Users can download Shard Projector from releases. No installation necessary. Unzip to a convenient location and run as expected. 
- Other: Building isn't necessary. Clone the repo and run with model.py as an entry point. Might need to install a few packages using pip.

(*Unstable*) Linux

- Clone the repo and run with model.py as an entry point. Unstable and not optimized, but not far off :)

# What's working right now?

*Note: many of these are present but still in early stages of development. Bugs all over.* 

- Windows support
- Simple targeting of server configuration folders. ex 'MyDediServer'
- Shard input/output
- In-app configuration of servers (cluster.ini, server.ini(s))
- In-app configuration of application (environment, paths, etc) 
- Web Interface (http, non-internet)

# What's being worked on?

### For developers:
- MVC (Model, View, Controller) architecture
- Class architecture
- Custom ttk widgets
- Config-to-widget strategies
- 'Mover' ui tool for development
- 2-way implementation of the web interface
- Viewing, configuration of mods
- Generation of new servers
- Cluster-token generation out-of-game (may not be feasible)

### For users:
- Mod features
- Better scrolling (sorry!)
- Better resizing (sorry!)
- Documentation
- Whatever else you want! If its doable and you're patient, this is the time to let me know!

# Notice

Klei Entertainment is not associated with this project in any way. 
