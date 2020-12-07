# Introduction

ESS has gone through a few different EPICS environments during its construction phase. First *CODAC* (from *[ITER](https://www.iter.org/)*), then *EEE* (short for ESS EPICS Environment), then EEE version 2, and then finally a major revamp to *e3*. Both EEE and e3 were based off of *[PSI](https://www.psi.ch/en)*'s EPICS environment.

In short, e3 is a packaged EPICS environment---but e3 also offers much more. Part of e3 is also a common front-end for users and developers at ESS, a collection of utilities to set up and maintain the environment, and a framework to facilitate dependency management. The intention was twofold with e3: to simplify life for integrators, but also for a central team managing the environment. At the core of e3 is a fork of PSI's [*require*](https://github.com/paulscherrerinstitute/require) module, *git*, *GNU Make*, and *module wrappers* (to bring standard community EPICS modules into the e3 environment).

Two of the key design considerations for e3 were dependency management and quality management. EPICS modules vary in structure and in quality, and each site that uses EPICS has their own style and conventions, which will be reflected in the source code. Furthermore, each module release will have dependencies upon specific releases of other modules. How e3 deals with these is to wrap all community "packages" in a wrapper. This wrapper links to the module source code, identifies module dependencies and versions, and contains our site-specific modifications; patches, database files, GUIs, etc. When a build occurs, e3 parses these dependency chains to find the necessary dependencies, compiles shared libraries, inflates and copies database files, and finally installs into a hierarchical EPICS "tree." This tree allows us to easily keep track of what module version has been built for what version of base and *require*, and allows removal of deprecated versions. At ESS, there is a shared (network mounted) EPICS tree that all IOCs utilize the binaries from.

:::{note}
Although ESS uses a shared build (using e.g., NFS) and dynamically linked binaries, e3 in itself is not bound to this distribution approach.[^conda] Similarily, there's an associated toolsuite (*systemd*, *procServ*, *conserver*, etc.) used to manage IOCs at ESS, but these are decoupled from e3, just as client and service applications (such as *CS-Studio*, *DisplayBuilder*, *ChannelFinder*, and so on) are.
:::

Finally, ESS have made some design choices, where at least one is worth mentioning in the context of documentation: at ESS, everything is a **module**---meaning that IOC applications, libraries, and modules all will be referred to as modules on this portal as well as in associated documents. An IOC at ESS is generally just a startup script, since the built application (module) is shared (and thus can be used for several IOCs).


[^conda]: ESS have also experimented with using *conda* to distribute.
