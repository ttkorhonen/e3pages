# Building an e3 module

## Lesson Overview

In this lesson, you'll learn how to do the following:

* Understand the difference between modules and IOCs
* Understand the e3 wrapper directory structure.
* Create an e3 wrapper using *Cookiecutter*
* Edit a module makefile in order to build and install it into e3.

---

## Modules and IOCs

As stated in [the introduction](../../../design/1_intro.md), an EPICS module is a set of code, databases, sequences, and/or startup
script snippets that provides generic functionality for a particular device type or logical function. In e3, an EPICS module can
also be specific to one instance of a device type.

An IOC is built up from one or more modules, based on the requirements of that IOC. A module is not a functional IOC application on its own.

Modules within e3 are essentially the core component that enables building of an IOC, and consist of e.g. source code for specific
communication protocols. Modules will often be collected from the EPICS community (and sometimes modified), but are also developed
in-house.

### Modules 

Many module originate from the broader EPICS community. Some examples are [asyn](https://github.com/epics-modules/asyn), 
[iocStats](https://github.com/epics-modules/iocStats), [mrfioc2](https://github.com/epics-modules/mrfioc2), or any of the
[Area Detector modules](https://github.com/areaDetector). To see which of these modules are installed in an e3 environment, you can
simply look at the contents of `E3_SITEMODS_PATH` as previously discussed in [Chapter 6](6_e3_vars.md).

You can use this to easily list all of the modules (and versions) that are installed in an e3 environment:
```console
[iocuser@host:~]$ echo ${E3_SITEMODS_PATH}
[iocuser@host:~]$ ls ${E3_SITEMODS_PATH}
[iocuser@host:~]$ ls ${E3_SITEMODS_PATH}/*
```
If `E3_SITEMODS_PATH` is not set, then you must of course first source the appropriate `setenv` or `setE3Env.bash`.

In summary, e3's design is based on having *wrappers* as a front-end for EPICS modules. These can be thought of as storing metadata needed
to build and deploy a module, together with site-specific modifications to those community modules. This allows an e3 user to work with
community modules in a maximally flexible way.

### IOCs

Unlike standard EPICS, where creating an IOC requires compiling a custom executable file, within e3 we use the standard executable `softIocPVA`
from EPICS base. Thus, in order to create an IOC, all one needs to do is to create an appropriate startup script. This means that there are no
specialised utilities necessary, simply a text editor.

The simplest IOC repository can look something like the following.

```console
[iocuser@host:iocs]$ tree e3-ioc-<iocname>
e3-ioc-<iocname>
|-- README.md
`-- st.cmd
```

It is also possible to include some non-binary files such as `.db` files, `.proto` files and the like, depending on your local requirements.
```console
[iocuser@host:iocs]$ tree e3-ioc-<iocname>
e3-ioc-<iocname>
|-- db
|   |-- protocol.proto
|   `-- records.db
|-- env.sh
|-- README.md
`-- st.cmd
```

Exercise:
* When loading a module, you should use `$(module_DIR)` or `$(module_DB)` to refer to database and protocol files that are a part of that module. How
  can you refer to such files in relation to the location of `st.cmd`?

## How to build a module

The e3 team has developed a number of tools to facilitate creating new e3 wrappers. In particular, we use [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/),
a Python-based templating utility. This can be installed with
```console
[iocuser@host:~]$ python3 -m pip install cookiecutter
```
You may need to add a `--user`, depending on your system permissions.

In order to create an e3 wrapper, one should use [this template](https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-wrapper).

:::{note}
This cookiecutter recipe requires that you use Python 3, so when you install cookiecutter make sure you do so with `pip3`, or with a conda/virtual environment
that has `python3` installed.
:::

There are two main types of wrappers: wrappers that link to external code (the types that we have seen so far), and wrappers in *local mode*.

### External modules

If you are needing to use a module from the EPICS community or one that may be used outside of a purely e3 context, then the e3 wrapper should point to that
repository. This could be located e.g. in the epics-modules group on [Github](https://github.com/epics-modules), [Gitlab](https://gitlab.esss.lu.se/epics-modules), or elsewhere.

:::{note}
The idea behind this is that you do not need to maintain a local fork, but that you can simply point at existing repositories that are used within the community.
:::

When you use the cookiecutter recipe it will prompt you for some information needed to create the wrapper.
```console
[iocuser@host:~]$ cookiecutter git+https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-wrapper.git
company [European Spallation Source ERIC]: 
module_name [mymodule]: fimscb                                 # Update the module name
summary [EPICS fimscb module]: 
full_name [Your name]:                                         # Fill in your name
email [your.name@ess.eu]:                                      # and email
epics_base_version [7.0.5]: 
epics_base_location [/epics/base-7.0.5]: 
require_version [3.4.1]: 
git_repository [ ... ]: https://github.com/icshwi/fimscb.git   # And update the URL
```

They key things to fill in here are highlighted above, namely the module name and git url (as well as your name and email address).

:::{note}
If the git repository that you add exists and is public, then cookiecutter will add it as a submodule to the wrapper. Otherwise, a templated *local module* (see
next section) will be created.
:::

Congratulations, you have just created an e3 wrapper! However, the wrapper is not configured correctly yet. If you try to build the module then you should see the 
following output
```console
[iocuser@host:e3-fimscb]$ make init patch build install
[iocuser@host:e3-fimscb]$ make existent LEVEL=4
/epics/base-7.0.5/require/3.4.1/siteMods/fimscb
`-- master
    |-- fimscb_meta.yaml
    `-- lib
        `-- linux-x86_64
            |-- fimscb.dep
            `-- libfimscb.so
```

Exercise
* Why do we do `make init patch` as well as `build install`?

If you explore the `fimscb` you should see the following.
```console
[iocuser@host:e3-fimscb]$ tree fimscb
# --- snip snip ---
|-- fimscbApp
|   |-- Db
|   |   |-- fimscb.db
|   |   |-- fimscb.proto
|   |   |-- Makefile
|   |   |-- stream_raw.proto
|   |   `-- stream_raw.template
|   |-- Makefile
|   `-- src
|       |-- fimscbMain.cpp
|       `-- Makefile
|-- fimscb.Makefile
|-- iocBoot
|   |-- iocfimscb
|   |   |-- Makefile
|   |   `-- st.cmd
|   `-- Makefile
|-- Makefile
|-- README.md
# --- snip snip ---
```
In particular, the `.db`, `.proto`, and `.template` files have not been installed. Moreover, the `fimscpMain.cpp` file is a generic boilerplate
file to start an IOC in regular EPICS, and does not need to be compiled in with the e3 module `fimscb` (recall that we use `iocsh.bash` to
start an IOC instead of compiling a separate executable binary). In order to install the database and other files, as well as remove the
source file, you must make changes to `fimscb.Makefile`.

In the end, it should look something like
```make
where_am_I := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
include $(E3_REQUIRE_TOOLS)/driver.makefile
include $(E3_REQUIRE_CONFIG)/DECOUPLE_FLAGS

############################################################################
#
# Relevant directories to point to files
#
############################################################################

APP:=fimscbApp
APPDB:=$(APP)/Db


############################################################################
#
# Add any files that should be copied to $(module)/db
#
############################################################################

TEMPLATES += $(wildcard $(APPDB)/*.db)
TEMPLATES += $(wildcard $(APPDB)/*.proto)
TEMPLATES += $(wildcard $(APPDB)/*.template)

.PHONY: db
db:
```

If you now re-run the build, you should see the following
```console
[iocuser@host:e3-fimscb]$ make clean build install
[iocuser@host:e3-fimscb]$ make existent LEVEL=4
/epics/base-7.0.5/require/3.4.1/siteMods/fimscb
`-- master
    |-- db
    |   |-- fimscb.db
    |   |-- fimscb.proto
    |   |-- stream_raw.proto
    |   `-- stream_raw.template
    |-- fimscb_meta.yaml
    `-- lib
        `-- linux-x86_64
            `-- fimscb.dep
```
We can check that it works correctly by starting an IOC that loads this module.

```console
[iocuser@host:e3-fimscb]$ iocsh.bash -r fimscb
```
to make sure that it loads correctly. In this case there isn't much that can go wrong as this module consists only of database and
protocol files. But it is still good practice.

:::{tip}
Given that we now have a working `fimscb` e3 wrapper, this would be a good time to commit and push your changes to whatever
remote repository you use.
:::

Given that `e3-fimscb` depends on *StreamDevice* (note the existence of `.proto`) files, it would be good to include that dependency
so that every time `fimscb` is loaded, so will *StreamDevice*. Since we have no source files, this cannot be a build-time dependency
as discussed in [the last chapter](7_module_deps.md). Instead, it is a *run-time* dependency.

In order to configure this correctly, you must uncomment the `# REQUIRED += stream` line in `fimscb.Makefile` and, as for any other
dependency, ensure that the correct version is specified. This is done by adding the following to `CONFIG_MODULE`:
```make
STREAM_DEP_VERSION:=2.8.18
```
and to `fimscb.Makefile`
```make
REQUIRED += stream
ifneq ($(strip $(STREAM_DEP_VERSION)),)
stream_VERSION:=$(STREAM_DEP_VERSION)
endif
```
If you uninstall and reinstall `fimscb` and then run `iocsh.bash -r fimscb` you should see that *StreamDevice* and all of its dependencies
has been loaded now.

### Local modules

It may not be the case that every e3 module is one that is expected to be used outside of your local institution. In such cases, separating
your code into a submodule and a wrapper may not make the most sense, since it adds a fair amount of additional complexity. In that case,
we can use the *local source mode* when designing modules and wrappers.

:::{note}
That said, one advantage of separating the wrapper from the repository is that this ensures that your in-house developed
EPICS functionality can be shared with the broader community, instead of just those that use e3.
:::

Create a cookiecutter wrapper as above, but this time enter `none` for the git URL.
```console
[iocuser@host:~]$ cookiecutter git+https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-wrapper.git
company [European Spallation Source ERIC]: 
module_name [mymodule]: clock                     # Update the module name
summary [EPICS clock module]: 
full_name [Your name]: 
email [your.name@ess.eu]: 
epics_base_version [7.0.5]: 
epics_base_location [/epics/base-7.0.5]: 
require_version [3.4.1]: 
git_repository [ ... ]: none                      # Leave this as "none" or any non-valid URL
```
This will create a new wrapper. The default behaviour of cookiecutter is to put in a template based on `makeBaseApp.pl` from EPICS
base. In our case we will remove that and download a new set of source files.
```console
[iocuser@host:~]$ cd e3-clock
[iocuser@host:e3-clock]$ rm -rf clock/*  # Remove the generated files
[iocuser@host:e3-clock]$ wget -c http://www-linac.kek.jp/cont/epics/second/second-devsup.tar.gz
[iocuser@host:e3-clock]$ tar -zxvf second-devsup.tar.gz -C clock
```

So how does e3 know that we are in local source mode? The key variables is `EPICS_MODULE_TAG`. When building/initialising etc., the e3 build
system will check to see if this variable has been set. If it has, then it will try to check out that tag in the submodule. If it is not set,
then it assume that we are in local source mode. If we look at `CONFIG_MODULE` in the wrapper in this case, we see
```make
#
EPICS_MODULE_NAME:=clock

# EPICS_MODULE_TAG:=master
#
E3_MODULE_VERSION:=1.0.0

# Dependent module versions
# For example:
#ASYN_DEP_VERSION:=4.41.0

# In most cases, we don't need to touch the following variables.
E3_MODULE_NAME:=$(EPICS_MODULE_NAME)
E3_MODULE_SRC_PATH:=clock
E3_MODULE_MAKEFILE:=$(EPICS_MODULE_NAME).Makefile


-include $(TOP)/configure/CONFIG_OPTIONS
# The definitions can also be overridden an untracked CONFIG_MODULE.local
-include $(TOP)/configure/CONFIG_MODULE.local
```
i.e. the line which defines `EPICS_MODULE_TAG` has been commented out, so we are in local source mode.
:::{tip}
Even if you are using an external module, you can use this for testing purposes to avoid having the submodule checked out each time that you
run `make build`. This can be particularly useful if you have local modifications to the submodule.
:::

We can see that we are in local source mode if we run `make init`:
```console
[iocuser@host:e3-clock]$ make init
>> You are in the local source mode.
>> Nothing happens.
```

As before, in order to build this module we need to tell *require* which sources and other files we want to include from the module subdirectory.
Modify `clock.Makefile` so as to look like
```make
where_am_I := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
include $(E3_REQUIRE_TOOLS)/driver.makefile
include $(E3_REQUIRE_CONFIG)/DECOUPLE_FLAGS

APP:=Clock1App
APPDB:=$(APP)/Db
APPSRC:=$(APP)/src

USR_INCLUDES += -I$(where_am_I)$(APPSRC)

TEMPLATES += $(wildcard $(APPDB)/*.db)
SOURCES += $(APPSRC)/devAiSecond.c

DBDS += $(APPSRC)/aiSecond.dbd

.PHONY: db
db:
```
and then build and install it as usual. To test that your new module works correctly, create a new `ch8.cmd` with the following contents.
```bash
require clock

dbLoadRecords($(clock_DB)/aiSecond.db)

iocInit()
```
and then run `iocsh.bash ch8.cmd`.


---

##  Assignments

1. Write a startup script for `e3-fimscb`.
2. Create an e3 wrapper for the EPICS module [e3-ch8](https://gitlab.esss.lu.se/epics-modules/training/ch8).
3. Create a startup script for this module that will load all of the necessary functionality
4. Create an e3 wrapper for the EPICS module [e3-myexample](https://gitlab.esss.lu.se/epics-modules/training/myexample), as well as an associated IOC 
   (i.e. a startup script that loads the necessary functionality)
   :::{hint}
   This task is a lot more challenging. To get some ideas, try to build the module as a regular EPICS module
   by switching into the `myexample/` directory and trying to build it there to see how that works.
   ```console
   [iocuser@host:e3-myexample]$ cd myexample
   [iocuser@host:e3-myexample]$ make build
   ```
   You may need to modify the configuration files included in this repository in order to get it to build correctly.
   :::
