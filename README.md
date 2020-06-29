<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="img\sp-icon-header.png" alt="Shard Projector"></a>
</p>

<p align="center" style="font-size: 300%"> <b>Shard Projector</b>
</p>
<p align="center" style="font-size: 140%"> Desktop dedicated servers for Don't Starve Together. 
</p>
<br>

# Note (28/06/20)

Shard Projector may require technical knowledge to play around with at the moment. In simple terms, it runs like a dream if you have a rather predictable setup. Addressing that (localization) is a top priority and well underway. Its also the key to welcoming our non-windows friends and thats important. Even yours truly likes getting weird with filepaths on occasion. If the dual-boot fits, I like to say.

Dark-arts aside: some tech knowledge an asset, at least for the alpha phase. Users looking forward to more of the ease-of-use aspects don't have long to wait, and shouldn't expect to. The development branch build just above this readme can make better detections steadily, but more excitingly is beginning to retrieve everything it needs to run with only permission neccesary from users. Auto-installing SteamCMD as an Add-In is now possible. Look to the next release for that. Beyond that, there is a single command entered into that SteamCMD Add-in outstanding, before Shard Projector can run servers on a brand new PC, immediately on logging in for the first time (not accounting for bugs or unintended behaviour, of course). 

For now, though, let it be known that (v0.1a) can be a tricky, picky mistress. It's in the very last state where I can (maybe) get feedback on it before its able to fend for itself/self-integrate but for that reason its of questionable use or symbolic significance for those who aren't a) a hobbyist b) me. It is deceptively bad at one of its main jobs. 

I plan to revisit the decision to release now in the future. Low risk let me make the decision but my judgement today said said the considerations were first impressions, data/good engineering, and chance with all three driving AND being driven by eachother, resulting in: freedom to not fret over it. 

It wasn't my first release going in with limited wisdom but boy, knowing it too can really take the edge off. That was the highlight, for sure. Another project of mine of mine got some love today, and it made me think of the nerves I had releasing it last year, the sweetness of of today would have been lost on me entirely.

So, the 'good times' for each project  (read: life?) are unpredictable and my gut says that will never change, and today in a rare twist: it was nice.

On a another front, for those who do wander into the repo this early: I'm hard at work on robust implementations of several things in this project but I will 'slack-off' to help an early user get up & running in a heartbeat! Just shoot an email about your issue for that sort of help. Janky, emergency Python written just for you can be had.

I released because its been in use at my apartment daily and without glaring issues, running servers for some time now. When it gets off the ground, its pretty neat! But, it needs curveballs and non-unicorn environments to be improved intelligently at this point; at least by me. Probably true *of* me, also. 

So please, criticize generously, tell me your best (and wIlDeSt) Shard Projector uninstall stories. Help a guy and his code-thing grow.

Thanks for reading and supporting the project, I'll likely be writing & archiving notes like this in the repo going forward. I'll set up a related branch that can be followed, or something like that.

Ryan

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

Its being developed to bridge the gap for non-technical players who want to host worlds of their own, and provide an option other than a monthly server-subscription (it will always be free!). Use it to run worlds of all kinds easily for you & your friends on dedicated servers that are simple to setup, manage, moderate and access- even when you're not online!

Whether you're running a LAN server at the house, hosting a 24-player online for your region, or debugging mods, Shard Projector has features you'll appreciate.

# Features

### Modern Interface

Simple yet powerful controls for running, monitoring, and configuring your server.

![Shard Projector](img/sp-running-preview.png)

### Cross-platform

Developed with Tkinter, a framework for creating user-interfaces that works wherever Python can run.

Shard Projector currently supports Windows. Linux and MACOSX users should check back often. 

Users with Python knowledge could very well have it running on those platforms in an afternoon. I'd love to hear about any such endevours and even assist with your specific patch, doesn't need to be release-ready code in any sense. 

*Note: get in touch with me at raposo.ryan@gmail.com if you'd like to assist with MACOSX optimization/testing. Early-access to new versions a guarantee!*

# Getting Started

## Usage

### (Alpha) Windows

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

# Contributing 

For contribution efforts generally, message me first so I can send all the latest and swap notes. I want contributors to know their work is going to be included if they put the time in, and during this stage a quick email first would be best.

When development becomes less-volatile and my intentions are better documented, I'll provide standard docs & a familiar license.

I'm excited to work with you and your interest is highly-valued, that much is certain. :)

# Notice

Klei Entertainment is not associated with this project in any way. 
