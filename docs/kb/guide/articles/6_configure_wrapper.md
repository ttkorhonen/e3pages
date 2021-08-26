(wrapper_config)=

# Article: Configuring your wrapper

```{admonition} Under Construction
:class: warning

This page is still being written.
```

To create a wrapper, you should use *[cookiecutter](https://github.com/cookiecutter/cookiecutter)* (see {ref}`cookiecutter_wrapper`), or you could just create all the folders and the files yourself. After having created the folder structure and the relevant configuration files (in `configure/`), you would generally set up the `${MODULE}.Makefile`.

## The `configure/` directory

If you used one of the template generators, the configuration of the EPICS base, require version, and module version should have already been done for you. In case you need to change them, the most important ones are typically `configure/RELEASE` and `configure/CONFIG_MODULE`.

If your module depends on other modules (for example, it may depend on *asyn*, *StreamDevice*, *areaDetector*, or any other number of modules), then you should specify the dependencies in `configure/CONFIG_MODULE`. This is done like so:

```makefile
# DEPENDENT MODULE VERSION
ASYN_DEP_VERSION:=4.41.0
STREAM_DEP_VERSION:=2.8.18
ADCORE_DEP_VERSION:=3.10.0
```

(iocstats_tree)=

## The module Makefile

The module makefile (`${MODULE}.Makefile` in the wrapper root directory) is where we configure what gets built and how it gets built. For concreteness' sake, let us focus on a specific module: *iocStats*. To be explicit, we are currently looking at the makefile for version 3.1.16, built for *require* 3.4.1.

At the top of the makefile there is some boilerplate code which sets the build stage correctly:

```makefile
where_am_I := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
include ${E3_REQUIRE_TOOLS}/driver.makefile
include $(E3_REQUIRE_CONFIG)/DECOUPLE_FLAGS
```

---

Before we move on, we should take a brief detour to look at the output of this process (this will be covered more in-depth in {ref}`build_process`), i.e., a compiled and installed module. For *iocStats* 3.1.16 built under *require* 3.4.1, we find the following:

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

---

The build process installs (potentially) several things to be available at run-time:
- Database/template/substitution/protocol files
- DBD (database definition) files
- Header files for dependent modules
- iocsh snippets
- Compiled libraries

:::{note}
At ESS, startup scripts are modularized, and the convention is to separate out functionality into separate startup *snippets*, that are named `*.iocsh`.[^ccdb] These are often colloquially referred to as *iocsh files*.
:::

### Database files

The database files are ones that you want available to an IOC at run-time. These are defined by the variable `${TEMPLATES}`:

```makefile
TEMPLATES += $(wildcard $(IOCADMINDB)/*.db)
TEMPLATES += $(wildcard $(IOCADMINDB)/*.template)
```

:::{note}
Make allows for wildcards using the function above, so this will include all `.db` and `.template` files included in the directory specified by the variable `${IOCADMINDB}`.
:::

### Snippets

The snippets are portions of a startup script that you would like to call to configure your module; for example, they may contain a call to `drvAsynIPPortConfigure` for a device that depends on *asyn*. These are simply installed in the top-level module directory, and are controlled by the variable `${SCRIPTS}`:

```makefile
SCRIPTS += $(IOCADMINSRC)/iocReleaseCreateDb.py
SCRIPTS += ../iocsh/iocStats.iocsh
```

Note that the second line refers to the parent directory of the module, i.e., the wrapper directory. It may often be the case that we want to install ESS-specific iocsh files, which are best kept in the e3 wrapper and not the module directory itself.

### Header files

The header files are usually only necessary for a module that is a dependency of other modules; for example, *asyn* declares many header files since many other modules depend on that library. These are declared via the `${HEADERS}` variable.

```makefile
HEADERS += $(DEVIOCSTATS)/os/default/devIocStatsOSD.h
HEADERS += $(DEVIOCSTATS)/devIocStats.h
```

:::{warning}
By default, the headers are all flatly installed into the `include/` directory; that is, the two files listed are both installed directly as follows:

```console
[iocuser@host:~]$ tree /epics/base-7.0.5/require/3.4.1/siteMods/iocstats/3.1.16/include/
/epics/base-7.0.5/require/3.4.1/siteMods/iocstats/3.1.16/include/
├── devIocStats.h
└── devIocStatsOSD.h
```

If you have two files in separate directories but with the same name, then you cannot install them this way. 

From require 3.3.0 onwards, you can define the `KEEP_HEADER_SUBDIRS` variable in the module Makefile. `KEEP_HEADER_SUBDIRS` should contain the list of top-level header directories where you want to train the directory structure in the installation process. <!-- TODO: find link and fixme -->

```makefile
KEEP_HEADER_SUBDIRS += $(GMTOP)
```
where you have defined `GMTOP` elsewhere in the module Makefile.
:::

### Compiled libraries

The library that is built is a shared library that results from compiling and linking all of the source files into a single shared object. These are managed by the variable `${SOURCES}`.

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

Note that you can also include sequencer files or C++ files here as well. The build process will understand based on the file extension how to compile it accordingly. If you use any sequencer files, then an appropriate `.dbd` file will be created with the correct database definitions to register your sequencer program.

### Database definition files

Any `.dbd` files that you would like to add are combined into a single module `.dbd` file that is loaded when the module is loaded at IOC startup. These are governed by the variable `${DBDS}`:

```makefile
DBDS    += $(DEVIOCSTATS)/devIocStats.dbd
```

### Dependencies

The build process is smart enough to detect any code-based dependencies. For example, if you include the header files from *iocStats* above in one of your source code files, then `driver.makefile` will infer that your module depends on *iocStats*; when your module is loaded, it will also load the correct version of *iocStats* first.[^deps] This raises two questions:
- How does it detect the correct version?
- What about non code-based dependencies?

The correct version is detected with the following code:

```makefile
calc_VERSION=$(CALC_DEP_VERSION)
```

Note that `${CALC_DEP_VERSION}` should be specified in `configure/CONFIG_MODULE`. In principle it does not need to be there, but it is clearer and easier to maintain if the dependencies are consistently placed in the same file.

Especially note that the variable name `${calc_VERSION}` must match exactly (including case) the name of the installed module. 

:::{warning}
Joint with the release of *require* 3.3.0 there was a switch to all modules being lowercase. So if you have a dependency on ADCore, then from *require* 3.3.0 onwards you should use the definition:

```makefile
adcore_VERSION=$(ADCORE_DEP_VERSION)
```

while for earlier versions of require you would instead use:

```makefile
ADCore_VERSION=$(ADCORE_DEP_VERSION)
```
:::

For non-code based dependencies (such as *StreamDevice* and *protocol* files, or the records introduced in the *calc* module), you have to explicitly state the requirement using the `${REQUIRED}` variable:

```makefile
REQUIRED += calc
```

:::{note}
As in the example above, the module name must exactly match the name of the installed module.
:::


[^ccdb]: ESS uses a fairly intricate software stack for deployment and management of IOCs. One of these tools builds startup scripts by including snippets.
[^deps]: This does not distinguish between build-time and run-time dependencies.
