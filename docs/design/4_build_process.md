(build_process)=

# Building and installing

```{admonition} Under Construction
:class: warning

This page is still being written.
```

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

Due to its origin, e3 makes use of *require*'s build facilities. For a dive into *require*'s build facilities, visit {ref}`require_build`.
