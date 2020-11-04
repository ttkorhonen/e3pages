(build_process)=

# Building and installing

```{admonition} Under Construction
:class: warning

Please note that this portal currently is being set-up, and that content is evolving fairly rapidly. This specific warning will be removed once this page is in a reasonable state. 
```

## The EPICS tree

Building EPICS with e3 generates a hierarhical tree, where different versions of base form individual sub-trees, and different versions of *require* form sub-trees within these sub-trees. Due to our decision to call everything (modules, applications, and libraries) simply modules, there's technically yet another embedded sub-tree under `${siteMods}`. A graphical representation of this (where `MODULE` and `MODULE_VERSION` are placeholders) is:

```bash
epics
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
└── base-7.0.4
    └── require
        ├── 3.2.0
        │   └── siteMods
        │       └── MODULE
        │           └── MODULE_VERSION
        └── 3.3.0
            └── siteMods
                └── MODULE
                    └── MODULE_VERSION
```

A real tree is of course orders of magnitude larger than the above example, and would not fit very well on this page.

One benefit of having this approach is that we easily can "keep tabs" of what version (of base and *require*) a module has been built for. We can thus fairly easily move from using e.g. *asyn* 4.36.0 with base 7.0.3.1 and *require* 3.2.0 to using *asyn* 4.40.0 with the same versions of base and *require*, or use the same version of *asyn* with base 7.0.4 with *require* 3.3.0. Once we have migrated away from older versions, we can simply delete that entire sub-tree.

Each `MODULE_VERSION` then contains the database files, templates, snippets, headers, and shared libraries associated with that version of that module (for the selected architectures). We will use the example given in {ref}`iocstats_tree`:

```bash
$ tree /epics/base-7.0.4/require/3.3.0/siteMods/iocstats/3.1.16/
/epics/base-7.0.4/require/3.3.0/siteMods/iocstats/3.1.16/
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

Due to it's origin, e3 makes use of *require*'s build facilities.

## The build process

Removed
<!-- content was way too technical for this page -->
