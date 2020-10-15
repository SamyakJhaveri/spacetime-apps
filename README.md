# Multi-player Snake Game on top of the Spacetime Framework
Project done as Undergraduate Reseacrh Intern in 2019 at University of California, Irvine at the ICS Lab under the guidance and mentorship of Prof. Cristina Lopes

## Table of Contents
- Introduction
- The Spacetime Framework
- The Snake Game
  - Architecture and Process
  - Results
- Demo
- Implications and Uses
- Citations

## Introduction
Quoting the Original Paper introducing the Spacetime Framework:
>Distributed computing is the backbone of many large-scale applications seen today, from online
gaming to machine learning. All distributed computing scenarios revolve around a shared
computation state that is worked upon by distributed components. Over the years, several architectural
styles have emerged for distributed applications: client-server, peer-to-peer, map-reduce, etc.
Different architectural styles are suited for different categories of distributed applications. State
synchronization, however, is a common problem that all distributed systems need to address to
some extent; different architectural styles impose different constraints to how to solve it. <br> 
In this work, we are particularly interested in a category of distributed applications characterized
by the existence of many components collaborating, and competing, over shared, long-lived, highly
mutable state. Examples include multiplayer gaming and distributed multi-agent simulations. In
these applications, the components executing or representing agents need to know the state of
the world more or less constantly, so the shared state needs to be available locally. When the
state of the world changes, those changes may need to propagate to all agents, and inconsistent
changes made by different agents need to be resolved. Moreover, the appropriate semantics for
resolving inconsistencies is highly dependent on what the logic of the application. 
