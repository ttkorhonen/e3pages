# Introduction

ESS has gone through a few different EPICS environments during its construction
phase. First *CODAC* (from *[ITER](https://www.iter.org/)*), then *EEE* (short
for ESS EPICS Environment), then EEE version 2, and then finally a major revamp
to *e3*. Both EEE and e3 were based off of *[PSI](https://www.psi.ch/en)*'s
EPICS environment.

In short, e3 is a number of EPICS environments and a front-end for users
and developers at ESS to use these, as well as a collection of utilities to set up
and maintain said environments. The intention was twofold with e3: to
simplify life for integrators, but also for a central team managing the
environment. At the core of e3 is a fork of PSI's
[*require*](https://github.com/paulscherrerinstitute/require) module, *git*,
and *module wrappers*.

Two of the key design considerations for e3 were dependency management and
quality management. EPICS modules vary in structure and in quality, and each
site that uses EPICS has their own style and conventions, which will be
reflected in the source code. Furthermore, each module release will have
dependencies upon specific releases of other modules. How e3 deals with these is
to interface all community "modules" with a wrapper. This wrapper links to the
module source code, identifies module dependencies and versions, and contains
our site-specific modifications; patches, database files, GUIs, etc. When a
build occurs, e3 parses these dependency chains to find the necessary
dependencies, compiles shared libraries, inflates and copies database files, and
finally manages installations. This allows us to keep track of what
module version has been built for what version of EPICS base
and *require*, as well as allows for removal of deprecated versions. At
ESS, there is a shared (network mounted) EPICS installation that all
IOCs utilise the binaries from.

:::{note}
Although ESS uses a shared build (using, for example, NFS) and dynamically
linked binaries, e3 in itself is not bound to this distribution
approach.[^conda] Similarly, there's an associated toolsuite (*systemd*,
*procServ*, *conserver*, etc.) used to manage IOCs at ESS, but these are
decoupled from e3, just as client and service applications (such as *CS-Studio*,
*DisplayBuilder*, *ChannelFinder*, and so on) are.
:::

## Terminology and definitions

### IOC

An e3 IOC is broadly defined by just a startup script, that:

* identifies the modules needed by the IOC,
* defines the values for variables required by the module startup script
  snippets, and
* calls the module startup script snippets.

Database templates and shared libraries are obtained from EPICS modules.

An e3 IOC is started using the `iocsh` script, uses the `softIocPVA`
executable from EPICS base, and dynamically loads any additional modules using
`require`.

### Module

An EPICS module is a set of code, databases, sequences, and/or startup script
snippets that provides generic functionality for a particular device type or
logical function. In e3, an EPICS module can also be specific to one instance of
a device type. Of note here is that e3 does not differentiate between types of
EPICS modules (applications, libraries).

An IOC is built up from one or more modules, based on the requirements of that
particular IOC. A module is not a functional IOC application on its own.

The databases provided by the module are typically in the form of templates. The
template includes macro values for the PV name prefix and potentially other
parameters. These macro values must be defined by the IOC.

[^conda]: ESS have also experimented with using *conda* to distribute, and some
  of our groups still make use of it. This approach uses a separate wrapper
  (making it decoupled from the non-conda ones) which are referred to as
  *recipes*.
