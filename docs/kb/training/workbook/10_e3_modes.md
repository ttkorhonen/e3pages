# 10. Additional working modes

## Lesson overview

In this lesson you will learn about two additional ways to work with e3:

* Cell mode, where you can install modules locally instead of into the global e3
  environment
* Dev mode, where you can work with a separate copy of the module source
  repository in order to facilitate module development.

:::{note}
This chapter covers several ways to work with e3 when building modules. If you
are working with a pre-built environment, then this chapter can be omitted.
:::

---

(cell_mode)=

## Cell mode

Depending on your deployment settings, it is possible that you may have
restricted access to deploy modules to an e3 environment. For example, there may
be a global e3 shared filesystem with read-only privileges. In such a case you
might still want to be able to work with e3 without having to build an entire
environment on your local machine, which is what *cell mode* allows. This is
done by the use of several make targets (`cellbuild`, `cellinstall`, `cellvars`,
and `celluninstall`) that modify the build and install paths for modules.

### Building in cell mode

Suppose that we want to build `e3-linconv` from [the previous
chapter](9_other_deps.md) in cell mode. Let us start by modifying the version of
the module.

```console
[iocuser@host:e3-linconv]$ echo "E3_MODULE_VERSION:=celltest" > configure/CONFIG_MODULE.local
```

Installing this new module version locally is as simple as running the following
commands.

```console
[iocuser@host:e3-linconv]$ make init patch build   # Of course, you should initialise, patch, and build first
[iocuser@host:e3-linconv]$ make cellinstall
```

In this case, the *linconv* module will be built and installed into the path
`e3-linconv/cellMods`:

```console
[iocuser@host:e3-linconv]$ tree cellMods/
cellMods/
`-- base-7.0.6.1
    `-- require-4.0.0
        `-- linconv
            `-- celltest
                |-- db
                |   `-- linconv.db
                |-- lib
                |   `-- linux-x86_64
                |       `-- linconv.dep
                `-- linconv_meta.yaml
```

:::{note}
This includes paths for EPICS base and *require* so that you can build the same
module for multiple versions of base/require with no conflict.
:::

### Running an IOC in cell mode

If you try to run an IOC and load this module with `iocsh -r
linconv,celltest` you should see

```console
[iocuser@host:e3-linconv]$ iosh.bash -r linconv,celltest
# --- snip snip ---
require linconv,celltest
Module linconv version celltest not available (but other versions are available)
Aborting startup script
```

This fails, since *require* by default will only search in `E3_SITEMODS_PATH`
for modules to load, not in your local `cellMods` path. In order to search
there, we pass the directory `cellMods` with the flag `-l` to `iocsh`:

```console
[iocuser@host:e3-linconv]$ iocsh -l cellMods -r linconv,celltest
# --- snip snip ---
epicsEnvSet EPICS_DRIVER_PATH cellMods/base-7.0.6.1/require-4.0.0:/epics/base-7.0.6.1/require/4.0.0/siteMods
require linconv,celltest
Module linconv version celltest found in cellMods/base-7.0.6.1/require-4.0.0/linconv/celltest/
Module linconv depends on calc 3.7.4+1
Module calc version 3.7.4+1 found in /epics/base-7.0.6.1/require/4.0.0/siteMods/calc/3.7.4+1/
Module calc depends on sequencer 2.2.9+0
Module sequencer version 2.2.9+0 found in /epics/base-7.0.6.1/require/4.0.0/siteMods/sequencer/2.2.9+0/
Loading library /epics/base-7.0.6.1/require/4.0.0/siteMods/sequencer/2.2.9+0/lib/linux-x86_64/libsequencer.so
Loaded sequencer version 2.2.9+0
sequencer has no dbd file
Loading module info records for sequencer
Module calc depends on sscan 2.11.5+0
Module sscan version 2.11.5+0 found in /epics/base-7.0.6.1/require/4.0.0/siteMods/sscan/2.11.5+0/
Module sscan depends on sequencer 2.2.9+0
Module sequencer version 2.2.9+0 already loaded
Loading library /epics/base-7.0.6.1/require/4.0.0/siteMods/sscan/2.11.5+0/lib/linux-x86_64/libsscan.so
Loaded sscan version 2.11.5+0
Loading dbd file /epics/base-7.0.6.1/require/4.0.0/siteMods/sscan/2.11.5+0/dbd/sscan.dbd
Calling function sscan_registerRecordDeviceDriver
Loading module info records for sscan
Loading library /epics/base-7.0.6.1/require/4.0.0/siteMods/calc/3.7.4+1/lib/linux-x86_64/libcalc.so
Loaded calc version 3.7.4+1
Loading dbd file /epics/base-7.0.6.1/require/4.0.0/siteMods/calc/3.7.4+1/dbd/calc.dbd
Calling function calc_registerRecordDeviceDriver
Loading module info records for calc
Module linconv has no library
Loading module info records for linconv
# Set the IOC Prompt String One 
epicsEnvSet IOCSH_PS1 "localhost-15630 > "
#
#
iocInit
Starting iocInit
############################################################################
## EPICS R7.0.6.1-E3-7.0.6.1-patch
## Rev. 2022-02-14T09:48+0100
############################################################################
iocRun: All initialization complete
```

These two pieces allow an e3 user to be able to install and load modules even if
they do not have write permissions to a shared e3 environment.

(development_mode)=

## Development mode

The development mode is instead intended to allow the developer to modify the
source module, and utilizes `git clone` instead of `git submodule`. This
provides a method to use a forked copy of the source module, which allows you to
commit changes even if you lack permission to push to the remote repository.

The configuration for **Development mode** is modified in the files
`CONFIG_MODULE_DEV` and `RELEASE_DEV` contained in the `configure/` directory.
If these files do not exist, you can create them from the original
`CONFIG_MODULE` and `RELEASE` files with some minor modifications. The key
differences are

* `E3_MODULE_DEV_GITURL`: The remote path to the module repository. This allows
  you to use a forked version of a module that you do not have permission to
  commit to.
* `E3_MODULE_SRC_PATH`: The path used for the local clone of the module source
  code repository. Note that this appears in both `CONFIG_MODULE` and
  `CONFIG_MODULE_DEV`, and the value in these two should be different. For
  example, for `e3-iocstats` in `CONFIG_MODULE` we define `E3_MODULE_SRC_PATH`
  as `iocStats`, while in `CONFIG_MODULE_DEV` we define it as `iocStats-dev`.

Development mode allows a user to work with (and commit changes to) a remote
module without needing to have permissions to commit to the standard one. This
is a good method to make changes in order to create a pull/merge request to a
community EPICS module.

To use development mode, you simply prefix the usual commands with `dev`. That
is, to build and install a module in development mode you would run

```console
[iocuser@host:e3-iocstats]$ make devinit devpatch devbuild devinstall
```

As in standard mode, there are also `dev` versions of many targets, such as
`devvars, devexistent, devclean`, etc. There is also an additional target, `make
devdistclean` which removes the cloned source directory.

Finally, note that `make existent` and `make devexistent` are (essentially)
identical in that they both provide information for what has been installed.

:::{admonition} Exercise
How are those two commands actually different? That is, when will they produce
different output?
:::

### Setting up the development module

In order to learn to work both with development mode and with modules in
general, we will work with our own forked copy of the community EPICS module
*iocStats*.

To begin with, fork your own copy from the community
*[iocStats](https://github.com/epics-modules/iocStats)*, and then update the
variable `E3_MODULE_DEV_GITURL` in `CONFIG_MODULE_DEV` to point towards your
fork.

Begin by running the command `make devvars`. This will show the e3 module
variables with the development mode, which should look something like the
following. Note that this example uses the ESS ICSHWI fork and compares it
against the community module, and so your output may be different.

```console
[iocuser@host:e3-iocstats]$ make devvars

------------------------------------------------------------
>>>>     Current EPICS and E3 Environment Variables     <<<<
------------------------------------------------------------

E3_MODULES_INSTALL_LOCATION = /epics/base-7.0.6.1/require/4.0.0/siteMods/iocstats/develop
E3_MODULES_INSTALL_LOCATION_BIN = /epics/base-7.0.6.1/require/4.0.0/siteMods/iocstats/develop/bin
E3_MODULES_INSTALL_LOCATION_DB = /epics/base-7.0.6.1/require/4.0.0/siteMods/iocstats/develop/db
E3_MODULES_INSTALL_LOCATION_INC = /epics/base-7.0.6.1/require/4.0.0/siteMods/iocstats/develop/include
E3_MODULES_INSTALL_LOCATION_LIB = /epics/base-7.0.6.1/require/4.0.0/siteMods/iocstats/develop/lib
E3_MODULES_PATH = /epics/base-7.0.6.1/require/4.0.0/siteMods
E3_MODULE_DEV_GITURL = "https://github.com/icshwi/iocStats"
E3_MODULE_MAKEFILE = iocStats.Makefile
E3_MODULE_MAKE_CMDS = make -C iocStats-dev -f iocStats.Makefile LIBVERSION="develop" PROJECT="iocstats" EPICS_MODULES="/epics/base-7.0.6.1/require/4.0.0/siteMods" EPICS_LOCATION="/epics/base-7.0.6.1" BUILDCLASSES="Linux" E3_SITEMODS_PATH="/epics/base-7.0.6.1/require/4.0.0/siteMods" iocstats_E3_GIT_DESC="7.0.6.1-4.0.0/3.1.16+4-70c2311-20220316T161418" iocstats_E3_GIT_STATUS="[ \\\" M configure/CONFIG_MODULE_DEV\\\",  \\\" M configure/RELEASE_DEV\\\", ]" iocstats_E3_GIT_URL="git@gitlab.esss.lu.se:e3/wrappers/core/e3-iocstats.git"
E3_MODULE_NAME = iocstats
E3_MODULE_SRC_PATH = iocStats-dev
E3_MODULE_VERSION = develop
E3_REQUIRE_CONFIG = /epics/base-7.0.6.1/require/4.0.0/configure
E3_REQUIRE_TOOLS = /epics/base-7.0.6.1/require/4.0.0/tools
EPICS_MODULE_NAME = iocStats
EPICS_MODULE_TAG = master
EPICS_SHORT_VERSION = 7.0.6.1
EPICS_VERSION_NUMBER = 7.0.6.1
EPICS_VERSION_STRING = "EPICS Version 7.0.6.1"
EXPORT_VARS = E3_MODULES_INSTALL_LOCATION_LIB TEMP_CELL_PATH EPICS_HOST_ARCH EPICS_BASE MSI E3_MODULE_NAME E3_MODULE_VERSION E3_SITEMODS_PATH E3_REQUIRE_MAKEFILE_INPUT_OPTIONS E3_REQUIRE_NAME E3_REQUIRE_CONFIG E3_REQUIRE_DB E3_REQUIRE_LOCATION E3_REQUIRE_DBD E3_REQUIRE_VERSION E3_REQUIRE_TOOLS E3_REQUIRE_INC E3_REQUIRE_LIB E3_REQUIRE_BIN QUIET   
MSI = /epics/base-7.0.6.1/bin/linux-x86_64/msi
REQUIRE_CONFIG = /epics/base-7.0.6.1/require/4.0.0/configure
```

Next, you must initialise the development mode. This is done using `make
devinit`, which will clone your fork into a directory with the name of
`iocStats-dev`. This is what the file tree will look like after:

```console
[iocuser@host:e3-iocstats]$ tree -L 1
.
|-- cmds
|-- configure
|-- docs
|-- iocsh
|-- iocStats
|-- iocStats-dev
|-- iocStats.Makefile
|-- Makefile
|-- patch
|-- README.md
`-- template
```

Confirm now that you have dev mod set up correctly by checking the remote URLs
for both the submodule and development directories by using `git remote -v`.

```console
[iocuser@host:iocStats]$ git remote -v
```

```console
[iocuser@host:iocStats-dev]$ git remote -v
```

:::{tip}
Note that by default, the `*-dev` path within an e3-module is ignored (which you
can see in the `.gitignore`). With this workflow, we can expand our repository
up to any number of use cases.
:::

One important point to remember is that both standard and development mode use
much of the same configuration/metadata in order to build and deploy a module.
In particular, they both use the same `module.Makefile`, even though some of the
configuration (`CONFIG_MODULE` versus `CONFIG_MODULE_DEV` and similarly for
`RELEASE`) may differ.

## Assignments

1. Can you change the install path used in *cell mode*?
2. How would you load more than one module installed in *cell mode* at the same
   time?
3. Can you override the default `E3_MODULE_DEV_GITURL` with your own forked
   repository without any `git status` changes in `e3-iocstats`? The output of
   `git status` should look like

   ```console
   [iocuser@host:e3-iocstats]$ git status
   On branch master
   Your branch is up-to-date with 'origin/master'.
   nothing to commit, working directory clean
   ```

4. Do we need `make devdistclean`? Is there any other way to clean or remove a
   cloned repository `iocStats-dev`? <!-- TODO: I feel like this is a question
   for us. Seriously, do we really need this? All it does is deletes the *-dev
   folder. -->
5. We have an `1.0.0-awesome.p0.patch` file. How would we apply it to
   Development mode source files?
