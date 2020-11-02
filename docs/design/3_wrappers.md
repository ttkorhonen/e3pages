# Module wrappers

```{admonition} Under Construction
:class: warning

Please note that this portal currently is being set-up, and that content is evolving fairly rapidly. This specific warning will be removed once this page is in a reasonable state. 
```

At the core of e3 is the module wrapper. This allows us to apply site specific changes - whether those are source code changes in the form of patches, different PV naming structure, or custom GUIs - to modules of any source without needing to modify that source directly.

```bash
$ tree
.
├── Makefile
├── README.md
├── cmds
├── configure
├── docs
├── patch
├── opi
├── template
├── <module>
├── <module>.Makefile
└── tools
```

In the above output, `<module>` is the name of the EPICS module/application/library. For community modules, this would be a git submodule. For ESS-specific application, it can be a normal directory (i.e. both the wrapper and the wrapped module are controlled in the same repository).

## Creating an e3 wrapper

To create the wrapper, please follow the direction in How to use cookiecutter to create an E3 wrapper. <!-- TODO: fixme --> You can also use the e3 template generator found in <https://github.com/icshwi/e3-tools>, although that is intended to be deprecated. After having created a template, you would generally modify the `<module>.Makefile`, and typically some of the data in the `configure/` directory.

## The configure directory

The configuration of the EPICS base, require version, and module version should have been done already when the e3 wrapper was created. In case you need to change them, these are located in configure/RELEASE and configure/CONFIG_MODULE.

If your module depends on other modules (for example, it may depend on asyn, StreamDevice, Area Detector, or any other number of modules), then you should specify the version in configure/CONFIG_MODULE. This is done like so:

```makefile
# DEPENDENT MODULE VERSION
ASYN_DEP_VERSION:=4.37.0
STREAM_DEP_VERSION:=2.8.10
ADCORE_DEP_VERSION:=3.9.0
```

Note that these variables do not do anything special, but we will reference them later.

## The module Makefile

The module makefile is where we configure what gets built and how it gets built. For concreteness' sake, let us focus on a specific module: iocStats; the makefile for version 3.1.16, built by require 3.3.0, is iocStats.Makefile.

This includes some boilerplate code at the start which sets the build stage correctly:

```bash
where_am_I := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
include ${E3_REQUIRE_TOOLS}/driver.makefile
include $(E3_REQUIRE_CONFIG)/DECOUPLE_FLAGS
```

`driver.makefile` is the workhorse that does 99% of the build process, using the information provided in the makefile.

Before we move on, we should look at the output of this process, i.e. a compiled and installed module. For iocStats 3.1.16 built under require 3.3.0, we find the following:

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

The build process installs (potentially) several things to be available at run-time:

- Database/template/protocol files
- DBD (Database definition) files
- Header files for dependent modules
- Iocsh snippets
- Compiled libraries

The database files are ones that you want available to an IOC at run-time. These are defined by the variable TEMPLATES:

```makefile
TEMPLATES += $(wildcard $(IOCADMINDB)/*.db)
TEMPLATES += $(wildcard $(IOCADMINDB)/*.template)
```

Make allows for wildcards using the function above, so this will include all .db and .template files included in the directory specified by the variable IOCADMINDB.

The Iocsh snippets are portions of a startup script that you would like to call to configure your module; for example, they may contain a call to drvAsynIPPortConfigure for a device that depends on asyn. These are simply installed in the top-level module directory, and are controlled by the variable SCRIPTS:

```makefile
SCRIPTS += $(IOCADMINSRC)/iocReleaseCreateDb.py
SCRIPTS += ../iocsh/iocStats.iocsh
```

Note that the second line refers to the parent directory of the module, i.e. the wrapper directory. It may often be the case that we want to install ESS-specific .iocsh files, which are best kept in the E3 wrapper and not the module directory itself.

The header files are only usually necessary for a module that is a dependency of other modules; for example, asyn has a lot of header files since other modules depend on that library. These are installed via the HEADERS variable.

```makefile
HEADERS += $(DEVIOCSTATS)/os/default/devIocStatsOSD.h
HEADERS += $(DEVIOCSTATS)/devIocStats.h
```

Note that by default, the headers are all flatly installed into the include/ directory; that is, the two files listed are both installed directly as follows:

```bash
$ tree /epics/base-7.0.4/require/3.3.0/siteMods/iocstats/3.1.16/include/
/epics/base-7.0.4/require/3.3.0/siteMods/iocstats/3.1.16/include/
|-- devIocStats.h
`-- devIocStatsOSD.h
```

If you have two files in separate directories but with the same name, then you cannot install them this way. However, there is another mechanism to install them described in the release notes for require 3.3.0.

The library that is built is a shared library that results from compiling and linking all of the source files into a single shared object. These are managed by the variable SOURCES.

```makefile
SOURCES += $(DEVIOCSTATS)/devIocStatsAnalog.c
SOURCES += $(DEVIOCSTATS)/devIocStatsString.c
SOURCES += $(DEVIOCSTATS)/devIocStatsWaveform.c
SOURCES += $(DEVIOCSTATS)/devIocStatsSub.c
SOURCES += $(DEVIOCSTATS)/devIocStatsTest.c
 
SOURCES += $(DEVIOCSTATS)/os/Linux/osdCpuUsage.c
SOURCES += $(DEVIOCSTATS)/os/Linux/osdCpuUtilization.c
SOURCES += $(DEVIOCSTATS)/os/Linux/osdFdUsage.c
SOURCES += $(DEVIOCSTATS)/os/Linux/osdMemUsage.c
SOURCES += $(DEVIOCSTATS)/os/default/osdWorkspaceUsage.c
SOURCES += $(DEVIOCSTATS)/os/default/osdClustInfo.c
SOURCES += $(DEVIOCSTATS)/os/default/osdSuspTasks.c
SOURCES += $(DEVIOCSTATS)/os/default/osdIFErrors.c
SOURCES += $(DEVIOCSTATS)/os/default/osdBootInfo.c
SOURCES += $(DEVIOCSTATS)/os/posix/osdSystemInfo.c
SOURCES += $(DEVIOCSTATS)/os/posix/osdHostInfo.c
SOURCES += $(DEVIOCSTATS)/os/posix/osdPIDInfo.c
```

Note that you can also include sequencer files, or C++ files here as well. The build process will understand based on the file extension how to compile it accordingly. If you use any sequencer files, then an appropriate .dbd file will be created with the correct database definitions to register your sequencer program.

Any .dbd files that you would like to add are combined into a single module .dbd file that is loaded when the module is loaded at IOC startup. These are governed by the variable DBDS:

```makefile
DBDS    += $(DEVIOCSTATS)/devIocStats.dbd
```

These will of course be joined with any other .dbd files generated during the build process, such as the sequencer ones described above.
Dependencies

The build process is smart enough to detect any code-based dependencies. For example, if you include the header files from iocStats above in one of your source code files, then driver.makefile will infer that your module depends on iocStats; as such when your module is loaded, it will also load the correct version of iocStats first (note that this does not distinguish between build-time and run-time dependencies). This raises two questions:

- How does it detect the correct version?
- What about non code-based dependencies?

The correct version is done with the following code:

```makefile
calc_VERSION=$(CALC_DEP_VERSION)
```

Note that CALC_DEP_VERSION should be specified in configure/CONFIG_MODULE. In principle it does not need to be there, but it is clearer and easier to maintain if the dependencies are consistently placed in the same file.

Note also that the variable name calc_VERSION must match exactly (including case) the name of the installed module; in require 3.3.0 we have switched to all modules being lowercase. So if you have a dependency on ADCore, then from require 3.3.0 onwards you should use the definition

```makefile
adcore_VERSION=$(ADCORE_DEP_VERSION)
```

while for earlier versions of require you would instead use

```makefile
ADCore_VERSION=$(ADCORE_DEP_VERSION)
```

For non-code based dependencies (such as StreamDevice and protocol files, or the records introduced in the cal module), you have to explicitly state the requirement with the REQUIRED variable:

```makefile
REQUIRED += calc
```

As above, the module name must exactly match the name of the installed module.
