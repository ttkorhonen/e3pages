(build_process)=

# Building and installing

This page contains information about how to build and install an EPICS module into an e3 environment.

## The EPICS tree

Building EPICS with e3 generates a hierarchical tree, where different versions of base form individual sub-trees, and different versions of *require* form sub-trees within these sub-trees. At ESS, we only use `${siteMods}`, but `${siteApps}` and `${siteLibs}` could also be used. A graphical representation of this (where `MODULE` and `MODULE_VERSION` are placeholders) is:

```console
[iocuser@host:~]$ tree /epics
/epics
├── base-7.0.3.1
│   └── require
│       ├── 3.2.0
│       │   └── siteMods
│       │       └── MODULE
│       │           └── MODULE_VERSION
│       └── 3.3.0
│           └── siteMods
│               └── MODULE
│                   └── MODULE_VERSION
└── base-7.0.5
    └── require
        ├── 3.4.0
        │   └── siteMods
        │       └── MODULE
        │           └── MODULE_VERSION
        └── 3.4.1
            └── siteMods
                └── MODULE
                    └── MODULE_VERSION
```

A real tree is of course orders of magnitude larger than the above example, with many instances of `MODULE`, and potentially multiple `MODULE_VERSION`s for some modules, and would not fit very well on this page.

One benefit of having this approach is that we easily can "keep tabs" of what version (of base and *require*) a module has been built for. We can thus fairly easily move from using e.g., *asyn* 4.36.0 with base 7.0.3.1 and *require* 3.2.0 to using *asyn* 4.41.0 with the same versions of base and *require*, or use the same version of *asyn* with base 7.0.5 with *require* 3.4.1. Once we have migrated away from older versions, we can simply delete that entire sub-tree.

Each `MODULE` will then, as indicated above, contain all of the built versions of that module. This could look like the following:

```console
[iocuser@host:~]$ tree -L 2 /epics/base-7.0.5/require/3.4.1/siteMods/ecmc
/epics/base-7.0.5/require/3.4.1/siteMods/ecmc
├── 6.2.1
│   ├── dbd
│   ├── include
│   └── lib
├── 6.2.1-1
│   ├── dbd
│   ├── include
│   └── lib
├── 6.2.2
│   ├── dbd
│   ├── include
│   └── lib
└── 6.2.3
    ├── dbd
    ├── include
    └── lib
```

Each `MODULE_VERSION` then contains the database files, templates, snippets, headers, and shared libraries associated with that version of that module (for the selected architectures). We will use the example given in {ref}`iocstats_tree`:

```console
[iocuser@host:~]$ tree /epics/base-7.0.5/require/3.4.1/siteMods/iocstats/3.1.16/
/epics/base-7.0.5/require/3.4.1/siteMods/iocstats/3.1.16/
├── db
|   ├── access.db
|   ├── ...
|   └── iocVxWorksOnly.template
├── dbd
|   └── iocstats.dbd
├── include
|   ├── devIocStats.h
|   └── devIocStatsOSD.h
├── iocReleaseCreateDb.py
├── iocStats.iocsh
├── iocstats_meta.yaml
└── lib
    └── linux-x86_64
        ├── iocstats.dep
        └── libiocstats.so
```

## The build tool

e3 makes use of *require*'s build facilities. For a dive into *require*'s build facilities, visit {ref}`require_build`. We will in this section give a brief description and overview of some of the targets that are available in e3.

To begin with, if you are in an e3 wrapper directory you can see some of the main targets available by typing `make help`
```console
[iocuser@host:e3-iocStats]$ make help
--------------------------------------- 
Available targets
--------------------------------------- 
install         Install current module to $(EPICS_BASE)/require/$(E3_REQUIRE_VERSION)/siteMods
uninstall       Uninstall the current module
build           Build current module
prebuild        Run module-specific commands before building
debug           Displays information about the build process
rebuild         Clean, build, and install the current module
clean           Deletes temporary build files
all             Initializes, patches, builds, and installs
init            Syncs and checks out the tag $(EPICS_MODULE_TAG) for the submodule 
cellbuild       Builds the module while also searching in $(E3_CELL_PATH) for dependencies
cellinstall     Installs the module in a local directory $(E3_CELL_PATH)
celluninstall   Remove the module from the local directory $(E3_CELL_PATH)
cellvars        Print relevant environment variables for the local install
patch           Apply Patch Files 
patchrevert     Revert Patch Files 
test            Tests the current build
existent        Show installed versions of the current module
devinit         Initializes a dev setup, defined with configure/CONFIG_MODULE_DEV and configure/RELEASE_DEV
devdebug        Displays information about the build process (development mode)
devbuild        Build current module (development mode)
devclean        Deletes temporary build files (development mode)
devinstall      Install the current module (development mode)
devuninstall    Uninstall the current module (development mode)
```
Note that this list will depend on the version of require specified in `configure/RELEASE`.

The targets fall into several categories.

### Main targets

### Cellmode targets

### Dev targets