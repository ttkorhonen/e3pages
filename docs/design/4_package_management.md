(build_process)=

# Building and installing

## Package management

A built EPICS module is nothing more than executable and linkable files,
data files (like database files or snippets), and metadata. An EPICS module
prior to being built is composed of files to generate the built files. The
act of installing is just to copy built files into a specific location; typically
a standardised directory where your computer knows to look for libraries and
binaries.

A package manager, or a package management system, is a collection of software
tools to---as the name suggests---manage packages; that knows how to build
software according to some standard, that knows where packages should go if
building them as well as where to find them if installing them, and that knows
where to install as well as where to find installed packages for a machine.
In order to manage packages, four key components are necessary outside of the
actual project code:

* An installation/an intended target for installation
* A registry for packages or for source code to produce packages
* A (build) back-end
* A front-end

When you use a package manager, like `apt` or `npm` or `pip`, you typically only
see the front-end; you do not have to specify where the packages can be found
(although you can often modify this path if you so wish; for example if you have
a custom registry), and you do not have to know about how packages actually have
been built---the only thing of importance is that there exists a built package
that is compatible with your system.

In the case of e3, there are currently two different management solutions.
They use the same back-end (composed of the EPICS base build system
and `driver.makefile` from *require*), but are otherwise different; one uses
custom tooling, and the other one uses existing community tooling. These solutions
require different project structures, and the *wrappers* for the latter solution
are referred to as *conda recipes*.

### The `e3` python package, a source code registry, git tags, and *GitLab* CI

This is the default e3 management solution in use at ESS, which is based on the
solution in use at PSI. Here, only source code and (select) *references* are stored,
as git tags. There is thus no package registry but only a *source code* registry,
i.e. users will instead have to compile their own modules, and will have to rely
on so-called *specifications* to know which module versions can generate a working
environment. The installation is then (typically) shared by multiple hosts by
having them on a single machine that exports them as mount points over NFS.

#### The front-end

The front-end for this solution is primarily two constituents:

* The `e3` python package
* A working specification - a description of an environment

Users who wish to set up their own full environments will need to either acquire
specifications from others (for example from ESS), or will need to compile a list
of module versions that are all internally compatible. The user(s) will then build
one or several environments, and can activate the environment of interest. Environments
can be local (e.g. in ones' own userspace) or be global (for example installed under
`/opt`), and can be installed on network machines to guarantee a shared installation,
which is the strategy used at ESS; there are servers that distribute e3 installations
over NFS.

#### The installation

Building EPICS with the `e3` package generates a hierarchical tree, where different
versions of base form individual sub-trees, and different versions of *require* form
sub-trees within these sub-trees. A graphical representation of this (where
`MODULE` and `MODULE_VERSION` are placeholders) is:

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
└── base-7.0.6.1
    └── require
        └── 4.0.0
            └── siteMods
                └── MODULE
                    └── MODULE_VERSION
```

A real tree is of course orders of magnitude larger than the above example, with
many instances of `MODULE`, and potentially multiple `MODULE_VERSION`s for some
modules, and would not fit very well on this page.

With this approach, each intalled module will relate to an environment through
file system relationships; what folder structure it exists under. Each `MODULE`
will then contain all of the built versions of that module. This could look like
the following:

```console
[iocuser@host:~]$ tree -L 2 /epics/base-7.0.6.1/require/4.0.0/siteMods/iocstats
/epics/base-7.0.6.1/require/4.0.0/siteMods/iocstats
├── 3.1.16+2
│   ├── db
│   ├── dbd
│   ├── include
│   ├── iocReleaseCreateDb.py
│   ├── iocStats.iocsh
│   ├── iocstats_meta.yaml
│   └── lib
└── 3.1.16+4
    ├── db
    ├── dbd
    ├── include
    ├── iocReleaseCreateDb.py
    ├── iocStats.iocsh
    ├── iocstats_meta.yaml
    └── lib
```

With this solution, a local installation can be done on a central server,
and can be shared with relevant hosts using e.g. NFS (or using `rsync`, etc.),
which is the primary distribution method used at ESS.

#### The "registry"

With this distribution method, there is no real registry containing compiled packages---
at ESS we store source code in a fixed *GitLab* group structure. Packages are built
manually, or for deployment at ESS as part of GitLab CI pipelines by so-called
"runners" that have direct access to a specific server. Once the package has been
built (and tested, etc.), it is placed on that server through a manual approval action.
Hosts that need access to these packages mount the installation and can make the
relevant environment/release available by mounting it over NFS.

To identify or reproduce compilations, we make use of git tags that encode some
key metadata. It is, however, up to the user to ensure a compatible environment---
i.e.  that all dependencies can be satisfied. Specifications exist for this purpose;
to describe e3 module references that can be combined into a working installation.

### *Conda*, *Artifactory*, *conda-bot* and *GitLab* CI

This is a more experimental e3 management system, that primarily is used by a smaller
group at ESS. Here, the key component is *[conda](https://docs.conda.io/en/latest/)*,
which is an OS-agnostic package and environment manager. Packages are uploaded to,
and downloaded from, an instance of *[Artifactory](https://jfrog.com/artifactory/)*
as *conda channels*.

#### The front-end

The front-end for this solution is conda's ana- or miniconda, and it is primarily
the second option that is used. Conda is available for most platforms, and users
can choose to either define entire or partial environments in environment-files,
or can install (and uninstall) package of their choosing. As in the other solution,
we use *GitLab* CI at ESS to automate building packages, and we also have a *[conda-bot]
(https://gitlab.esss.lu.se/ics-infrastructure/conda-bot)* that is used to trigger
builds of dependent packages (or rather *recipes*, to be more exact).

#### The installation

Conda typically installs local environments that can be activated. These installations
could technically be placed on shared servers, but since conda only allows for a
singular version of a given package it is typically preferred to remove the dependency
on a specific shared server and instead manage the local environments using standard
configuration management tooling (like *ansible*).

#### The registry

Conda has its package lists in so-called *conda channels*. There is a large community
project called *[conda-forge](https://conda-forge.org/)* that contains at least EPICS
base, but ESS also hosts its own channels using an instance of Artifactory, where
all packages are uploaded to/downloaded from.

## The package/a built module

Each `MODULE_VERSION` contains the database files, templates, snippets,
headers, and shared libraries associated with that version of that module (for
the selected architectures). We will use the example given in
{ref}`iocstats_tree`:

```console
[iocuser@host:~]$ tree /epics/base-7.0.6.1/require/4.0.0/siteMods/iocstats/3.1.16+4/
/epics/base-7.0.6.1/require/4.0.0/siteMods/iocstats/3.1.16+4/
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

## The back-end

The "common ground" for both management solutions of e3 is the use of
*require*'s build facilities. For a dive into these, visit {ref}`require_build`.
