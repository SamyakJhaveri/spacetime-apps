# Multi-player Snake Game on top of the Spacetime Framework
Project done as **Undergraduate Reseacrh Intern** in 2019 at **University of California, Irvine** at the ICS Lab under the guidance and mentorship of **Prof. Cristina Lopes**

## Table of Contents
- [Introduction](#introduction)
- [The Spacetime Framework](#the-spacetime-framework)
- [The Snake Game](#the-snake-game)
  - Architecture and Process
  - Results
- [Demo](#demo)
- [Outcomes](#outcomes)
- [Citations](#citations)

## Introduction

Quoting the Original Paper introducing the Spacetime Framework:
> Distributed computing is the backbone of many large-scale applications seen today, from online gaming to machine learning. All distributed computing scenarios revolve around a shared computation state that is worked upon by distributed components. Over the years, several architectural styles have emerged for distributed applications: client-server, peer-to-peer, map-reduce, etc. 
>  Different architectural styles are suited for different categories of distributed applications. State synchronization, however, is a common problem that all distributed systems need to address to some extent; different architectural styles impose different constraints to how to solve it. <br> 
> In this work, we are particularly interested in a category of distributed applications characterized by the existence of many components collaborating, and competing, over shared, long-lived, highly mutable state. Examples include multiplayer gaming and distributed multi-agent simulations. <br>
> In these applications, the components executing or representing agents need to know the state of the world more or less constantly, so the shared state needs to be available locally. When the state of the world changes, those changes may need to propagate to all agents, and inconsistent changes made by different agents need to be resolved. Moreover, the appropriate semantics for resolving inconsistencies is highly dependent on what the logic of the application. 

![enter image description here](images/GoTnode%20architecture.JPG)
[Back to Top](#table-of-contents)

## The Spacetime Framework
The ‘Spacetime’ framework is a **Global Object Tracking (GoT) framework** that pushes the limits of distributed shared state. The GoT framework addresses the **problem of object state synchronization** among the components of a distributed application. It is an **object-oriented programming model** based on **causal consistency** with application-level conflict resolution strategies whose elements and interfaces **mirror** those found in **decentralized version control systems**: a version graph, working data, diffs, commit, checkout, fetch, push, and merge. Essentially, the Spacetime GoT model is Git, but for objects.

[Back to Top](#table-of-contents)

## The Snake Game
### Architecture and Process
1. Made the game’s **dataframe**, an object heap that consists of “checked-out” in-memory objects under version control, similar to Git repositories.  
2. Built the **Data Model** that identifies the types of actual programming language-level objects that the dataframe should track. 
This is done statically to avoid synchronization issues during runtime. 
3. Built the nodes that essentially constitute the application
	  - **Physics node** - The node that simulates the ’world’ for the game and enforces the rules of the game. It has a ‘play’ method with a loop that iteratively performs a checkout of the objects, implements the logic, and commits the changes at the end. 
  It also checks for a new player in the game by looking for new Player node objects in the dataframe.
	  - **Player node** - Hosts all the human and bot players and shares their movements and states to the dataframe. The Player node also has its own ‘remote’ dataframe from where objects are pulled, and Player objects are created to be added to the local dataframe. 
	  - **Visualizer/Viewer node** - Viewer nodes are the observers of the simulated world, and their local changes are not supposed to be propagated to other nodes. I used PyGame to display the state of the simulated world graphically. Rather than being in lockstep with the other nodes, the Viewer node assumes its role as an autonomous component that operates on its copy of the shared state.
4. Designed a bot that can navigate its way to the ‘apple’ object.

![enter image description here](images/snake%20game%20structure.png)
![enter image description here](images/snake%202.JPG)

[Back to Top](#table-of-contents)

## Results
- The bot snake players **circumvented the game rules** when playing with human snake players and made movements that we did not expect
-  Even at varied frequencies of dataframe checkouts, the application was **resilient enough** to continue normal functioning in single-player, all-human multiplayer, human-bot multiplayer, and all-bot multiplayer settings. 

[Back to Top](#table-of-contents)

## Outcomes
Besides being a **means to test the usability** of the ‘Spacetime’ Framework, Prof. Cristina Lopes and her team plan to use the 
**‘snake’ game** as a **platform for worldwide competition on reinforcement learning ‘bots’**.

[Back to Top](#table-of-contents)

## Citations
GoT: Git, but for Objects, ROHAN ACHAR, University of California, Irvine, USA; 
CRISTINA V. LOPES, University of California, Irvine, USA (arXiv:1904.06584v1 [cs.PL] 13 Apr 2019)

[Back to Top](#table-of-contents)

 
