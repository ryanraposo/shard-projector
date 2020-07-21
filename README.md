<h1 align="center">
  <br>
  <a href="" rel="noopener">
  <img src="img\sp-icon-header.png"></a>
  <br>
  Shard Projector
  <br>
</h1>

<h4 align="center">Desktop dedicated servers for Don't Starve Together</h4>
<p align="center">
  <a href="#features">Features</a> | 
  <a href="#usage">Usage</a> |
  <a href="#contributing">Contributing</a> |
  <a href="#notice">Notice</a>
</p>

# Notes

Shard Projector is in active development. While efforts will be made to keep documentation informative and accurate, it too is subject to drastic changes. Some lapses in reliability may arise during this phase.

It is currently being developed to run **Don't Starve Together** servers. Users should look forward to using it for other games with SteamCMD-based servers. This will coincide with a release on or around v1.0.

Developers & contributors should feel free to work without meticulous consideration of every single title for now, but lets try to have the API foundations firm and yet adaptable for that milestone. 

Thank you for your patience, and remember to report issues where able!

<b>07/21/20</b> - 'The Add-In Update' #3

Oh, hi mark(down). 

  - [Dropped] 'Literal' approach to Add-Ins. Will reimplement a generalized system once more info comes in on compelling cases and v1.0 draws near.
    - [Dropped] ResourceManager
    - [Dropped] ADDIN datatype
  - [Dropped] "nullrenderer" references/tooling.
  - [Added] SteamCMD object. Designed as an interface to SteamCMD on the user's machine, installed as an Add-In or somewhere locally. Manages 'gameservers'.
  - [Added] Job object. From the docstring: "A system job with threaded output queueing. Has methods for controlling and monitoring a supplied subprocess."
    - Destined to take its place in the model.py heirarchy, serving all the subproccess needs in Shard Projector. Add-In stuff started, with Shards next.
  - [Added] DialogStatus object. Very friendly with Jobs, and adaptable to activities that involve progress and important milestones/stipulations.
    - Basically a dialog that takes care of itself once told:
      - Where its dynamic text comes from. 
      - How to tell if the related activity is still running
      - How to end things when users *really* want it to go away. 
      - :'[
      - If it should hog focus or be allowed to run behind the scenes.
  - [Git] Recently fought 'git rebase -i' and lost. I apologize for any issues that might cause anyone pulling. More likely just a messy looking history because I didn't use force. But boy, I would have had I thought of it.
  - [Git] Not so sure about the --no-ff merge approach anymore. Might save us if the git police come around but I can't even read the history in a GUI at present. I came for the pretty graphs so cya.
  - [Git] I feel okay making choices based on results/usefulness, but unsure if a few things are due to my specific setup or going to be uncommon on others and I don't want to alienate. Some challenges: 

    -  On top of steadily learning, I'm down to one machine/os and my git use varies ranging from basic CLI to a (highly debauched) integrated IDE prompt. Maybe some historical cases of GitHub-on-my-phone-on-the-couch.
    
    - Some pressure to limit time/energy spent strategizing sadly, and I'm sure (hoping) someone could talk alot of that down. Advice/a few minutes of time would be very much appreciated.
  
In other news, very excited to announce some contributor-related things I've been working on that aren't visible yet. 
  
Incoming is a workflow plan & consistency on my part. And, if your earthly-body has survived the heat of sentence 1: a big idea very near to my heart. Among other things, it involves a set of unique paths for [getting involved](img\moves.png)! Some more traditional, others new, and one... for the brave. 😈

Thanks for reading!

<details><summary><b>07/03/20</b> - 'The Add-In Update' #2</summary>
<p>
Hi! Thought I would give another status update on the next release v0.2.0, aka "The Add-In Update".

This time around I wanted to share some notes! These are the highlights, challenges, and considerations guiding
development at the moment:

- Installations/downloads for Add-Ins are sensitive to cancellation.

- Using Shard Projector while they are in progress may A) not work or B) interrupt/corrupt installations.

- Would like to show status/output while preventing or heavily discouraging using/closing Shard Projector.

- Need to account for installations that fail or otherwise result in a sensible reason to end or restart. 

- Need to maintain/diligently indicate 3rd party nature of any Add-Ins (most immediately: SteamCMD, a non-graphical, compact version of Steam). This includes displaying their output and placing reminders in Shard Projector where appropriate.

- Some Add-In related CLI processes started with robust Python built-in ```subproccess.Popen``` pose monitoring challenges using typical methods, and novel methods:

- Must not significantly disturb current interactions/methods of handling subprocesses because they are:
  -  A) The basis of Shard Projector, *and* 

  -  B) Its primary design challenges. These interactions are threaded (run in parallel) the way they are currently because GUI frameworks tend to demand and depend on an uninterrupted execution loop. We are using a framework that was chosen because it is shipped with Python, and it is no exception to these restrictions by *any* stretch of the imagination. 

- Would like to implement a scalable and elegant combination of classes and methods that will handle this sensitive, multi-stage, multi-resource process with its numerous potential points-of-failure.

This update is a big one! It is a (rather ironic) manifestation of this project's primary goals: fewer dependencies, fewer downloads, and fewer explanations.

Shard Projector depends, however, on some graciously provided tools and as such, this update seeks to gather and set them up for users.

I decided that although it's nice to use and can be made to work on my machine and others where those tools might already exist, further work was misplaced until Shard Projector was made useful to those who have trouble with technical stuff. Having a server of your own is awesome, and this app was designed to get those users all the way there.

Thanks for reading!
</p>
</details>

<details><summary><b>07/02/20</b> - 'The Add-In Update'</summary>
<p>
Development/prep for v0.2.0 is moving along well. Needs a little more time.  
</p>
</details>

<details><summary><b>06/28/20</b> - Initial Release</summary>
<p>

- Shard Projector v0.1a may require technical knowledge to work on your system. 

- Incoming (1-3 days) release v0.2.0 introduces a feature (Add-Ins) that enables, reliable circumvention of the related issues. There are no releases planned before then.

</p>
</details>

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


