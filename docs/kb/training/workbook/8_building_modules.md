# Building an e3 module

## Lesson Overview

In this lesson, you'll learn how to do the following:

* Understand the difference between modules and applications.
* Understand the e3 wrapper directory structure.
* Create an e3 wrapper using the *e3TemplateGenerator*.
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

Unlike standard EPICS where an IOC is a compiled binary, in e3 an IOC is just a startup script. This means that there are no specialised utilities required to build
an IOC, simply a text-editor.

The simplest such repository can look something like the following.

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
a Python-based templating utility.

In order to create an e3 wrapper, one should use [this template](https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-wrapper). This can be installed with
```console
[iocuser@host:~]$ pip3 install cookiecutter
```
You may need to add a `--user`, depending on your system permissions.

:::{note}
This wrapper requires that you use Python 3, so when you install cookiecutter make sure you do so with `pip3`, or with a conda/virtual environment
that has `python3` installed.
:::

There are two main types of wrappers: wrappers that link to external code (the types that we have seen so far), and wrappers in *local mode*.

### External modules

If you are needing to use a module from the EPICS community or one that may be used outside of a purely e3 context, then the e3 wrapper should point to that
repository. This could be located e.g. in the [epics-modules](https://github.com/epics-modules) group on Github, or elsewhere.

When you use the cookiecutter recipe it will prompt you for some information needed to build the wrapper.
```console
[iocuser@host:~]$ cookiecutter git+https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-wrapper.git
company [European Spallation Source ERIC]: 
module_name [mymodule]: fimscb                                 # Update the module name
summary [EPICS fimscb module]: 
full_name [Your name]: 
email [your.name@ess.eu]: 
epics_base_version [7.0.5]: 
epics_base_location [/epics/base-7.0.5]: 
require_version [3.4.1]: 
git_repository [ ... ]: https://github.com/icshwi/fimscb.git   # And update the URL
```

They key things to fill in here are highlighted above, namely the module name and git url.

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
file to start an IOC in regular EPICS, and does not need to be comipled in with the e3 module `fimscb` (recall that we use `iocsh.bash` to
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
# Add any files that should be copied to $(module)/Db
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

### Module/application with local source code

Let's assume that we have found an EPICS application that we would like to integrate into e3, where the source is an archive (e.g. `.tar.gz`) that we received from a collaborator or that we downloaded from a (non-git) internet source.

> We will be using an example from http://www-linac.kek.jp/cont/epics/second.

1. Create a new configuration file:

   ```console
   [iocuser@host:e3TemplateGenerator]$ cat modules_conf/Clock.conf
   EPICS_MODULE_NAME:=Clock
   E3_TARGET_URL:=https://github.com/jeonghanlee
   E3_MODULE_SRC_PATH:=Clock
   ```

   > Change `E3_TARGET_URL` to point to your own account.

2. Create a repository called *e3-Clock* on your GitHub (or GitLab or whatever else you prefer and use) account.

3. Run e3TemplateGenerator just as earlier:

   ```console
   [iocuser@host:e3TemplateGenerator]$ bash e3TemplateGenerator -m modules_conf/Clock.conf -d ~
   ```

4. Inspect your application:

   ```console
   [iocuser@host:e3TemplateGenerator]$ tree -L 1 ~/e3-Clock
   .
   |-- Clock-loc
   |-- cmds
   |-- configure
   |-- docs
   |-- iocsh
   |-- opi
   |-- patch
   |-- template
   |-- Clock.Makefile
   |-- Makefile
   `-- README.md
   ```

As you may notice, we now have a directory called `Clock-loc/` in the wrapper (which contains a standard EPICS structure with `ClockApp/`,  `ClockApp/Db/` and `ClockApp/src/`). In this directory, you can place your source code. For our example:

```console
[iocuser@host:e3TemplateGenerator] cd ~/e3-Clock/Clock-loc
[iocuser@host:Clock-loc]$ wget -c http://www-linac.kek.jp/cont/epics/second/second-devsup.tar.gz
[iocuser@host:Clock-loc]$ tar xvzf second-devsup.tar.gz
```

> This example application we are using contains a `Clock1App` instead of `ClockApp`. To make things easy, we can just delete `ClockApp` and leave `Clock1App`; `rm -rf ClockApp/`.

Modify configuration files as earlier. If you were to try to `make init` here, you would find that it does nothing:

```console
[iocuser@host:e3-Clock]$ make init
>> You are in the local source mode.
>> Nothing happens
```

> As we now have all of our source code locally, we can choose `E3_MODULE_VERSION` and `EPICS_MODULE_TAG` rather freely.

Now we will set up, build, and install our application.

1. Edit the makefile as follows:

   ```console
   [iocuser@host:e3-Clock]$ cat Clock.Makefile
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

   db:

   .PHONY: db

   vlibs:

   .PHONY: vlibs
   ```

2. Build and install the app:

   ```console
   [iocuser@host:e3-Clock]$ make build
   [iocuser@host:e3-Clock]$ make install
   ```

3. Inspect with `iocsh.bash`:

   ```console
   effbc10.kaffee.10034 > require Clock,master
   Module Clock version master found in /epics/base-3.15.5/require/3.0.4/siteApps/Clock/master/
   Loading library /epics/base-3.15.5/require/3.0.4/siteApps/Clock/master/lib/linux-x86_64/libClock.so
   Loaded Clock version master
   Loading dbd file /epics/base-3.15.5/require/3.0.4/siteApps/Clock/master/dbd/Clock.dbd
   Calling function Clock_registerRecordDeviceDriver
   ```

### Module/application created in the standard way (using `makeBaseApp`)

> This is basically the same as with the local source code example above, so the steps will be shortened.

1. Create a configuration file:

   ```console
   [iocuser@host:e3TemplateGenerator]$ cat modules_conf/epicsExample.conf
   E3_TARGET_URL:=https://github.com/icshwi
   EPICS_MODULE_NAME:=epicsExample
   E3_MODULE_SRC_PATH:=epicsExample
   ```

2. Create repository in your target URL.

3. Run e3TemplateGenerator.

4. Create application:

   ```console
   [iocuser@host:epicsExample-loc]$ rm -rf epicsExampleApp/
   [iocuser@host:epicsExample-loc]$ makeBaseApp.pl -t ioc epicsExample
   [iocuser@host:epicsExample-loc]$ makeBaseApp.pl -i -p epicsExample -t ioc epicsExample
   ```

5. Copy your source, sequencer, etc. files to `epicsExampleApp/src/`, and your database (and protocol) files to `episcExampleApp/Db/`.

6. Modify `configure/RELEASE`, `configure/MODULE_RELEASE`, and `epicsExample.Makefile`.

7. Commit and push.

---

##  Assignments

* Write startup scripts for `e3-Clock` and for `e3-fimscb`.
* Build an e3 application with a remote repository:
  
  1. Can you build [e3-ch8](https://github.com/icshwi/ch8) as an application?
  2. Try to create a startup script for it.

* Build [e3-myexample](https://github.com/icshwi/myexample) and an associated IOC. 
  
  > Note that this is a challenging task.

