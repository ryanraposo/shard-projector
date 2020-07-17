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


<!-- <a align="center">

![built-with-love](https://gist.githubusercontent.com/ryanraposo/4aad8e64cd9c91db72b1b641cce4c90b/raw/5cbddb10fed1f0bb02a8632ea83a06a325b2d9a8/built-with-love.svg) ![might-just-ship-it](img/might-just-ship-it.png)

</a> -->


# Notes

Shard Projector is in active development. While efforts will be made to keep documentation informative and accurate, it too is subject to drastic changes. Some lapses in reliability may arise during this phase.

Shard Projector is currently being developed to run **Don't Starve Together** servers. Users should look forward to using Shard Projector for other games with SteamCMD-based servers. This will coincide with a release on or around v1.0.

Developers & contributors should feel free to work without meticulous consideration of every single title for now, but lets try to have the API foundations firm and yet adaptable for that milestone.     

Thank you for your patience, and remember to report issues where able!

**07/03/20**

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

**07/02/20**

- Update: development/prep for v0.2.0 is moving along well. Needs a little more time.  

**06/28/20**

- Shard Projector v0.1a may require technical knowledge to work on your system. 

- Incoming (1-3 days) release v0.2.0 introduces a feature (Add-Ins) that enables, reliable circumvention of the related issues. There are no releases planned before then.

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
- a nullrenderer based at C:/steamcmd is expected by Shard Projector even when the UI suggests otherwise

# Contributing

At this stage, the most prized contribution would be guidance and project-specific insight on the following topics:

- Version control
- Managing of a public repository in the initial development phase (I have experience, but with a far more stable first release)
- Accomplishing the above wiith allowance for personal freedom of direction and style; but with informed regard for those taking the time to support, and the ettiquete they might expect or rely on.

Given that these 'meta-contributions' are difficult to initiate through normal channels and rooted in discussion, I'd ask those willing to oblige to contact me at raposo.ryan@gmail.com. You can also just add me on Discord: ryanraposo#6339

Other contributions to Shard Projector are welcome, but I'd like to learn about my options and space to move with tact as lead maintainer before fleshing out this section properly. For now I'd check out the dev notes to see if there's an in for you. In the near future I plan on formalizing that approach a little bit and going with that for this project.

<details><summary>Read more...</summary>
<p>

It can feel hard for me to reconcile a few things with strong aspirations to work with more teams and willing contributors. And I want to, because... well it's the best! 

I've spent a lot of time solo-developing this application with head-buried and several facets of it are not "on paper" but none-the-less quite real, planned for and built around. If anyone can suggest tools or other for documenting from this vantage point for others, like mind/road-mapping made for the purpose that'd be really cool. 

I feel no reservations about keeping the front-facing control I want, but don't see similar expressed or in form on this site very often. I sometimes think that GitHub's lack of intimate messaging and other features are ok as-is, but only because if you manage on trend, contribution is so open that comments on already laboured over-work will always be enough to maintain respect for time *and* wishes. This is a neutral point and the situation suits many no matter one's take, but for this project, thats not in the cards just yet.

Shard Projector is a project very receptive to collaboration. Perhaps not easy and predictable for new, issue-targeted drop-in collaboration; but in a way that is involved and so broader in possiblity.

Your particular implementation may see red-tape on the way in, but thats just because I'd like to see what you see first. In my view, no matter how restrictive or open my style, I'm supposed to lead and account for and understand these differences as they crop up, else where would these judgements on direction come from? So please, know that your contributions are valued. If I call for pause, its because I stand to learn.

I could throw in a to-do list, but what if I want to forumulate a to-do list with someone similarly passionate, who likes whats been done so far and wants to respectfully learn the vision? I feel this all the time, and I want to signal those who relate. What I don't want, is wasted effort on the part of well-meaning, talented people on great work that ultimately doesn't mesh and so won't be included. I would rather scare a contributor away then have that happen and it be avoidable, had I represented things a little better. 

Later on, I would love to see more miscellaneous, small or clear-cut issues picked up and solved by those with only the time or ability or interest for those things, but right now, love is needed. It can be a beautiful hellscape in those source folders on occasion, but carefully planned architecture is laid out where it counts and is rolling through. As a learning project at least in part, to think of casual collaboration that I can facilitate efficiently... we're just not there yet. Not without a chat. Or five. Same for rapid development at the expense of my understanding. I have users and potential contributors to thank for patience on that, to be sure. 

A lot of this is translating to some lacking documentation, and possibly an appearance of hard-headedness. If so, it couldn't be more off the mark so to restate, this is what would mean the most to the project. This is what is possible and wanted. There are walls at a glance (no style-guide for another example) but behind a small extra step is very potentially a core position on this team. Please forgive lack of proper signage if need be and know that I would love to grow and build on this vision with anyone who'd like to co-create it. If I'm among friends, tripping for the most part and some words like these will more than sort the issue, well that'd be just fine, too.

Anyways, this stuff can nag at me a little while coding, but thats whats on the agenda if I can help it. Side-effects of "Make Repository Public" buttons, I think. Reserve judgement by all means while I get back to it :)

Thanks for reading,  
Ryan

</p>
</details>

# Notice

Valve is not associated with this project in any way. 

Klei Entertainment is not associated with this project in any way. 


