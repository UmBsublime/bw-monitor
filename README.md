# bw-counter


For now this is very much Work-In-Progress, but this is what I intend the tool-set will be able to do.


This set of tools is there to help do fine-grain accounting of network traffic on your servers. It harnesses the power of iptc, which is a python library that interacts with iptables.

The core of this project is there to ease up creating new counters and managing them sanely.

When this project will be completed it will include a few small tools all built around the core. There will be :

- a daemon
- a configuration file parser
- a command line tool
- an on demand graph generator

---
### The daemon

This part of the tool-set will read configuration file and create the appropriate iptables counters and log their values in a file for later use.

---
### The configuration parser

The part of the tool-set will parse configuration files and generate the appropriate core objects to represent them.

---
### The command line tool

This part of the tool-set will do two things.

1. Monitor interactively the value of different counters.
2. Let the user create on demand counters and monitor them. Useful for on the go custom requirements.

---
### On-Demand graph generator

This part of the tool-set will be a command line tool that will ask the user to specify a log file and a start an end time and generate a graphic of the bandwidth usage over time of he contents of the log file.
