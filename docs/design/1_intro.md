# Introduction

ESS has gone through a few different EPICS environments during its construction phase. First *CODAC* (from *[ITER](https://www.iter.org/)*), then *EEE* (short for ESS EPICS Environment), then EEE version 2, and then finally a major revamp to *e3*. Both EEE and e3 were based off of *[PSI](https://www.psi.ch/en)*'s EPICS environment.

In short, e3 is a packaged EPICS environment---but e3 also offers much more. Part of e3 is also a common front-end for users and developers at ESS, a collection of utilities to set up and maintain the environment, and a framework to facilitate dependency management. The intention was twofold with e3: to simplify life for integrators, but also for a central team managing the environment. At the core of e3 is a fork of PSI's [*require*](https://github.com/paulscherrerinstitute/require) module, *git*, *GNU Make*, and *module wrappers* (to bring standard community EPICS modules into the e3 environment).

Two of the key design considerations for e3 were dependency management and quality management. EPICS modules vary in structure and in quality, and each site that uses EPICS has their own style and conventions, which will be reflected in the source code. Furthermore, each module release will have dependencies upon specific releases of other modules. How e3 deals with these is to wrap all community "packages" in a wrapper. This wrapper links to the module source code, identifies module dependencies and versions, and contains our site-specific modifications; patches, database files, GUIs, etc. When a build occurs, e3 parses these dependency chains to find the necessary dependencies, compiles shared libraries, inflates and copies database files, and finally installs into a hierarchical EPICS "tree." This tree allows us to easily keep track of what module version has been built for what version of base and *require*, and allows removal of deprecated versions. At ESS, there is a shared (network mounted) EPICS tree that all IOCs utilize the binaries from.

:::{note}
Although ESS uses a shared build (using e.g., NFS) and dynamically linked binaries, e3 in itself is not bound to this distribution approach.[^conda] Similarly, there's an associated toolsuite (*systemd*, *procServ*, *conserver*, etc.) used to manage IOCs at ESS, but these are decoupled from e3, just as client and service applications (such as *CS-Studio*, *DisplayBuilder*, *ChannelFinder*, and so on) are.
:::

## Terminology and definitions
### IOC

An e3 IOC is defined by a startup script that:
* identifies the modules needed by the IOC,
* defines the values for variables required by the module startup script snippets, and
* calls the module startup script snippets.

Database templates and shared libraries are obtained from EPICS modules.

A running e3 IOC uses the `softIocPVA` executable from EPICS base, and dynamically loads any additional modules using `require`.

### Module

An EPICS module is a set of code, databases, sequences, and/or startup script snippets that provides generic functionality for a particular device type or logical function. In e3, an EPICS module can also be specific to one instance of a device type.

An IOC is built up from one or more modules, based on the requirements of that IOC. A module is not a functional IOC application on its own.

The databases provided by the module are typically in the form of templates. The template includes macro values for the PV name prefix and potentially other parameters. These macro values must be defined by the IOC.

### EPICS base

EPICS base provides the core EPICS functionality, including database management, a standard set of basic records, IOC functionality, etc. All IOCs require EPICS base.

[^conda]: ESS have also experimented with using *conda* to distribute.
