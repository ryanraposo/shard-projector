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

# About

Shard Projector is in active development. While efforts will be made to keep documentation informative and accurate, it too is subject to drastic changes. Some lapses in reliability may arise during this phase. 

Current features target **Don't Starve Together** servers and development will keep that heading as a priority until Shard Projector could be considered a substantial benefit to the game's community. To that end several major updates are planned.

### Future Considerations

Contributors should feel free to work without meticulous consideration of other titles for now. The decision is just one thats begged of the project-- there are so few reasons not to allow it, so we'll take some simple steps to be ready.

As a rule of thumb: *its not about developing for the unique aspects of other games, but instead to be conscious of work that stands out as DST-specific.* 

I'm confident that if working with that guideline, you should be in the clear. This wasn't always the mantra, though. There is work to be done retroactively, but that also means your judgement needs to trump whats already written.

#### An Example

To name a less-obvious code example of "being conscious" and how loosely the rule is intended, see the CommandPanel in widgets.py. 

The custom widget is a flexible panel of buttons used to house easy-access server commands, that's easy to use/customize via code. The design isn't groundbreaking, and the behavior was implemented to one-day handle user setups (not other games), but it makes the point.

Paired with its early state of development, I also think its a good measure of the upper-limits of effort expected as far as accommodating the rule. Beyond that your willingness can be the guide, and **if it would be super cool for DST but paralyzing to progress to make a feature universal- I say let it live!**

I hope the community agrees, and that we can make the next decision on pacing together.

Thank you for your patience, and remember to report issues; even if they seem well-known or explainable consequences of development at the time.

# Log

<details><summary><b>07/02/22</b> - You there!</summary>
<p>
Hi! 

I'm taking a break from Shard Projector. If you have wondered in, please feel free to ring a bell, coding with some others would change things but as it stands I don't have the juice or even desire I had when I built the current state, with so much energy and momentum that I got excited one night and released it as broken as 0.1 is. So horrendously broken and just a tiny pathing bug. Lol. But, whats more important and concerning to me, is that I've lost my goal here so bad, thats still the latest release. Thats bad, but me being okay with it is my cue in real life.

My goals, needs, and motivators aren't in the repo at the moment. I had a lot of fun making weird widgets, figuring out Threads, playing WX with my girlfriend on SP, and really love the project. But it hurts these days. And I'm not learning which is my rocket fuel. Except maybe forcing myself to use git creatively on readme commits alone in this repository. Nah. I'll just bang that out when I need it.

I had hoped someone would have joined in by now, but can't really be mad cause I've told almost no one about it... and wouldn't, just not in a good state for that, nor am I in one to get it there, so what is there to say.

Just a stalemate, unfortunate. Honestly I've been having a great time, 'recklessly' so, but when I think on it, it can be sad shrugs. Just gunna do something else.

My favourite takeaway and also the demon of the times: ending up comfortable doin' a whole lot of writing, implementing/deimplementing and straight up goofin' on github. I guess I've proved myself to myself, and thats some good-good. 

Be back when it'll serve someone.
Ryan

</p>
</details>

<details><summary><b>07/03/20</b> - 'The Add-In Update' #3</summary>

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
  
Incoming is a workflow plan & consistency on my part. And, if your earthly-body has survived the heat of sentence 1: a big idea very near to my heart. Among other things, it involves a set of unique paths for [getting involved](img/moves.png)! Some more traditional, others new, and one... for the brave. 😈

Thanks for reading!

</p>
</details>

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


