# Introduction

:::{warning} Under Construction
Please note that this portal currently is being set-up, and that content is evolving fairly rapidly. This specific warning will be removed once this page is in a reasonable state. 
:::

ESS has gone through a few different EPICS environments during it's developmental phase. The latter of these have been referred to as *EEE*---"ESS EPICS Environment". The current setup is the 3rd version - thus e3. In a single sentence, e3 is an EPICS front-end for users and developers at ESS and a collection of utilities to set up and maintain ESS' EPICS environment.

Two of the key design considerations for e3 were dependency and quality management. EPICS modules vary in structure and in quality, and each Site that uses EPICS have their own particularities, which will need to be imposed on and/or coupled to the source code. Furthermore, each module release will have dependencies upon specific releases of other modules. ESS' e3 started off based on PSI's EPICS environment, which is heavily built around the [*require*](https://github.com/paulscherrerinstitute/require) module to more easily manage these dependencies. The intention was thus twofold with e3: to simplify life for integrators, but also for a central team managing available modules. At the core of e3 is usage of *git*, *Makefile* rules, and *module wrappers* (as a standardized front-end to non-standard modules).

The aforementioned wrapper is an EPICS-like structure that links to the module, and which contains our Site specific modifications; patches, database files, GUIs, etc.

