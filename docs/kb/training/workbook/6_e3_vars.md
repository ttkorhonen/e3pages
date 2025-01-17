# 6. Variables within e3

## Lesson Overview

In this lesson, you will learn how to do the following:

* Understand variables and parameters within an IOC.
* Run commands to access variables and parameters from within an IOC.
* Understand EPICS and e3 environment variables used when a module is
  configured.
* Combine variable commands to access path or files of any module within an IOC.

---

## Running an IOC

The following variables are defined when an IOC is running from within startup
and iocsh scripts.

### General `iocsh` variables

* `REQUIRE_IOC`: A unique name of the IOC that can be used to track certain
  variables in a certain IOC. For example, an e3 IOC will generate on startup a
  number of PVs of the form `$(REQUIRE_IOC):MODULES` that list the modules that
  are loaded in a given IOC.  :::{note} If `IOCNAME` is defined in the
  environment prior to the IOC starting, then `REQUIRE_IOC` will be a (possibly
  truncated) copy of that. Otherwise, it will be a name which depends on the
  process ID for the running IOC and so will not be consistent from one run to
  the next of the IOC.  :::

* `E3_CMD_TOP`: The absolute path to the startup script (cmd file), if one
  exists.

* `E3_IOCSH_TOP`: The absolute path to where `iocsh` was executed from;
  equivalent to running `pwd`.

* `IOCSH_PS1`: The IOC Prompt String. Defaults to `$HOSTNAME-$PID >`.

### Variables created by *require*

Whenever an e3 module is dynamically loaded, *require* generates a number of
module-specific variables that are useful in scripts. For `mrfioc2` these would
be

* `mrfioc2_VERSION` - The version of `mrfioc2` that was loaded.
* `mrfioc2_DIR` - The absolute path where `mrfioc2` is located. Useful for
  loading `.iocsh` snippets and other files installed with the module.
* `mrfioc2_DB` - The absolute path where the database, template, protocol, and
  substitutions files for `mrfioc2` have been installed.

Let us see these in action. Copy the following into a new `ch6.cmd` file.

```bash
require iocstats

iocInit

epicsEnvShow E3_IOCSH_TOP
epicsEnvShow E3_CMD_TOP
epicsEnvShow iocstats_DIR
epicsEnvShow iocstats_VERSION
epicsEnvShow iocstats_DB
```

```console
[iocuser@host:e3training/workbook]$ iocsh ch6.cmd

# --- snip snip ---

Starting iocInit
############################################################################
## EPICS R7.0.6.1-E3-7.0.6.1-patch
## Rev. 2021-03-15T09:48+0100
############################################################################
iocRun: All initialization complete
epicsEnvShow E3_IOCSH_TOP
E3_IOCSH_TOP=/home/iocuser/data/git/e3.pages.esss.lu.se
epicsEnvShow E3_CMD_TOP
E3_CMD_TOP=/home/iocuser/data/git/e3.pages.esss.lu.se
epicsEnvShow iocstats_DIR
iocstats_DIR=/epics/base-7.0.6.1/require/4.0.0/siteMods/iocstats/3.1.16+0/
epicsEnvShow iocstats_VERSION
iocstats_VERSION=3.1.16+0
epicsEnvShow iocstats_DB
iocstats_DB=/epics/base-7.0.6.1/require/4.0.0/siteMods/iocstats/3.1.16+0/db/
# --- snip snip ---
```

As stated before, these variables are needed if you want to use database or
protocol files that have been installed with a given module. For example,
*StreamDevice* uses a variable `STREAM_PROTOCOL_PATH` when searching for
`.proto` files, and so a common idiom in a startup script is a line such as

```bash
epicsEnvSet("STREAM_PROTOCOL_PATH", "$(mymodule_DB)")
```

Note however that if a module depends on *StreamDevice*, then this variable
is automatically set by *require* when the module is loaded.

Exercise:

* Modify the above startup script to add some other modules, and look at the
  resulting paths. For example, load `stream` and see what paths `module_DIR`
  are available within the IOC shell.

### EPICS variables, parameters, and environment variables

You can see EPICS parameters and environment variables from within an IOC using
`epicsParamShow` (or `epicsPrtEnvParams`) and `epicsEnvShow`.

```console
localhost-15716 > epicsParamShow
localhost-15716 > epicsEnvShow
```

Exercises:

* How do we print only one variable - for example `TOP`?
* What is the difference between `$(TOP)` and `${TOP}`? Is it the same inside of
  the IOC shell as in UNIX?

In the IOC shell, run `var`. This provides a list of variables that are defined
within the IOC environment; these can be modified or set by running `var
<variable> <value>`.

```console
localhost-15716 > var
CASDEBUG = 0
PDBProviderDebug = 0
asCaDebug = 0
asCheckClientIP = 0
atExitDebug = 0
boHIGHlimit = 100000
boHIGHprecision = 2
calcoutODLYlimit = 100000
calcoutODLYprecision = 2
callbackParallelThreadsDefault = 2
dbAccessDebugPUTF = 0
dbBptNotMonotonic = 0
dbConvertStrict = 0
dbJLinkDebug = 0
dbQuietMacroWarnings = 0
dbRecordsAbcSorted = 0
dbRecordsOnceOnly = 0
dbTemplateMaxVars = 100
dbThreadRealtimeLock = 1
exprDebug = 0
histogramSDELprecision = 2
lnkDebug_debug = 0
logClientDebug = 0
pvaLinkNWorkers = 1
requireDebug = 0
runScriptDebug = 0
seqDLYlimit = 100000
seqDLYprecision = 2
```

Note that there are four UNIX commands that can be used from within the IOC
shell: `date`, `pwd`, `cd`, and `echo`.

:::{note}
For more information about EPICS functions, check out the [App Developers
Guide](https://epics.anl.gov/base/R3-15/6-docs/AppDevGuide/IOCShell.html).
:::

As described in the [design documentation](../../../design/2_require.md),
*require* is used to dynamically load EPICS modules during the startup of an
IOC. This is what the line `require iocstats` does above; `iocstats` can be
replaced with any other EPICS module that is installed in your e3 environment.

First, let us start up an IOC that has *iocstats* loaded in it as before. You
can do this in one of two ways:

```console
[iocuser@host:~]$ iocsh ch6.cmd
```

or

```console
[iocuser@host:~]$ iocsh -r iocstats
```

Exercise:

* What is the difference between these two commands? Take a look at the output
  of the IOC shell as it starts up.

As a second experiment, try to load *iostats* a second time as follows.

```console
[iocuser@host:~]$ iocsh -r iocstats -r iocstats

# --- snip snip ---

require iocstats
Module iocstats version 3.1.16+4 found in /epics/base-7.0.6.1/require/4.0.0/siteMods/iocstats/3.1.16+4/
Module iocstats depends on calc 3.7.4+1

# --- snip snip ---

Calling function iocstats_registerRecordDeviceDriver
Loading module info records for iocstats
require iocstats
Module iocstats version 3.1.16+4 already loaded

# --- snip snip ---

```

Nothing happens due to the fact that *require* will only load a module a single
time. It is possible to have multiple configured *instances* of a module (for
example, an IOC can control multiple copies of the same device) by loading the
appropriate `.iocsh` snippet with different parameters, but that is a topic for
another time.

Next, in the running IOC, let us try to load the *recsync* module. Run

```console
localhost-15965 > require recsync
Error! Modules can only be loaded before iocIint!
```

*require* cannot load modules after `iocInit` has been called. This is due to the
fact that a lot of setup and initialisation must be done before the call to
`iocInit`.

It can be useful to see a bit of extra information when *require* is loading a
module to understand exactly where it is coming from (and to see why it loads
the version that it does). Create a new file, `ch6-2.cmd`, with the following
contents:

```bash
var requireDebug 1
require recsync
```

and then load it with `iocsh`:

```console
[iocuser@host:~]$ iocsh ch6-2.cmd

# --- snip snip ---

iocshLoad 'ch6-2.cmd',''
var requireDebug 1
require recsync
require: putenv("T_A=linux-x86_64")
require: putenv("EPICS_HOST_ARCH=linux-x86_64")
require: putenv("EPICS_RELEASE=7.0.6")
require: putenv("OS_CLASS=Linux")
require: versionstr = ""
require: module="recsync" version="(null)" args="(null)"
require: searchpath=/epics/base-7.0.6.1/require/4.0.0/siteMods
require: no recsync version loaded yet
require: trying /epics/base-7.0.6.1/require/4.0.0/siteMods
require: found directory /epics/base-7.0.6.1/require/4.0.0/siteMods/recsync/
require: checking version 1.4.0+0 against required (null)
require: compareVersions(found=1.4.0+0, request=(null))
require: compareVersions: MATCH empty version requested
require: recsync 1.4.0+0 may match (null)
require: directory /epics/base-7.0.6.1/require/4.0.0/siteMods/recsync/1.4.0+0/lib/linux-x86_64/
         exists
require: recsync 1.4.0+0 looks promising
Module recsync version 1.4.0+0 found in /epics/base-7.0.6.1/require/4.0.0/siteMods/recsync/1.4.0+0/
require: looking for dependency file
require: file /epics/base-7.0.6.1/require/4.0.0/siteMods/recsync/1.4.0+0/lib/linux-x86_64/recsync.dep
         exists, size 31 bytes
require: parsing dependency file /epics/base-7.0.6.1/require/4.0.0/siteMods/recsync/1.4.0+0/lib/linux-x86_64/recsync.dep
require: looking for library file
require: file /epics/base-7.0.6.1/require/4.0.0/siteMods/recsync/1.4.0+0/lib/linux-x86_64/librecsync.so
         exists, size 114720 bytes
Loading library /epics/base-7.0.6.1/require/4.0.0/siteMods/recsync/1.4.0+0/lib/linux-x86_64/librecsync.so
Loaded recsync version 1.4.0+0
require: compare requested version (null) with loaded version 1.4.0+0
require: compareVersions(found=1.4.0+0, request=(null))
require: compareVersions: MATCH empty version requested
require: file /epics/base-7.0.6.1/require/4.0.0/siteMods/recsync/1.4.0+0/dbd/recsync.dbd
         exists, size 207 bytes
Loading dbd file /epics/base-7.0.6.1/require/4.0.0/siteMods/recsync/1.4.0+0/dbd/recsync.dbd
Calling function recsync_registerRecordDeviceDriver
require: registerModule(recsync,1.4.0+0,/epics/base-7.0.6.1/require/4.0.0/siteMods/recsync/1.4.0+0/)
require: putenv("MODULE=recsync")
require: putenv("recsync_VERSION=1.4.0+0")
require: putenv("recsync_DIR=/epics/base-7.0.6.1/require/4.0.0/siteMods/recsync/1.4.0+0/")
require: putenv("SCRIPT_PATH=.:/epics/base-7.0.6.1/require/4.0.0/siteMods/recsync/1.4.0+0/:/epics/base-7.0.6.1/require/4.0.0/")
Loading module info records for recsync

# --- snip snip ---
```

As you can see, there is a lot of output that describes, for example, the search
process for the requested module as well as information about which environment
variables are set during the loading process.

It should be noted that `requireDebug` (as its name suggests) is a variable
defined within the require module. Other modules have similar functionality.

Exercise:

* Find at least one other modules installed in the core specification that has a
  debug variable.

:::{note}
Like any well-behaved shell, you should be able to use the up/down arrows to
re-run previous commands.
:::

## Building a module or an application

Back in [Chapter 3](3_module_versions.md) we looked at the two e3 variables
`E3_MODULE_VERSION` and  `EPICS_MODULE_TAG`. As you will see, there are many
more environment variables that are used by e3 for configuring and installing
modules.

### e3 environment variables

You can print out all environment variables of a module with the rule `make
vars`:

```console
[iocuser@host:e3-caputlog]$ make vars

------------------------------------------------------------
>>>>     Current EPICS and E3 Environment Variables     <<<<
------------------------------------------------------------

E3_MODULES_INSTALL_LOCATION = /epics/base-7.0.6.1/require/4.0.0/siteMods/caputlog/3.7.0+0
E3_MODULES_INSTALL_LOCATION_BIN = /epics/base-7.0.6.1/require/4.0.0/siteMods/caputlog/3.7.0+0/bin
E3_MODULES_INSTALL_LOCATION_DB = /epics/base-7.0.6.1/require/4.0.0/siteMods/caputlog/3.7.0+0/db
E3_MODULES_INSTALL_LOCATION_INC = /epics/base-7.0.6.1/require/4.0.0/siteMods/caputlog/3.7.0+0/include
E3_MODULES_INSTALL_LOCATION_LIB = /epics/base-7.0.6.1/require/4.0.0/siteMods/caputlog/3.7.0+0/lib
E3_MODULES_PATH = /epics/base-7.0.6.1/require/4.0.0/siteMods
E3_MODULE_MAKEFILE = caPutLog.Makefile
E3_MODULE_MAKE_CMDS = make -C caPutLog -f caPutLog.Makefile LIBVERSION="3.7.0+0"
                      PROJECT="caputlog"
                      EPICS_MODULES="/epics/base-7.0.6.1/require/4.0.0/siteMods"
                      EPICS_LOCATION="/epics/base-7.0.6.1" BUILDCLASSES="Linux"
                      E3_SITEMODS_PATH="/epics/base-7.0.6.1/require/4.0.0/siteMods"
                      caputlog_E3_GIT_DESC="7.0.6.1-4.0.0/3.7.0-20f7c82-20220210T112335-2-gaab774b"
                      caputlog_E3_GIT_STATUS="[ ]"
                      caputlog_E3_GIT_URL="git@gitlab.esss.lu.se:e3/wrappers/core/e3-caPutLog.git"
E3_MODULE_NAME = caputlog
E3_MODULE_SRC_PATH = caPutLog
E3_MODULE_VERSION = 3.7.0+0
E3_REQUIRE_CONFIG = /epics/base-7.0.6.1/require/4.0.0/configure
E3_REQUIRE_TOOLS = /epics/base-7.0.6.1/require/4.0.0/tools
EPICS_MODULE_NAME = caPutLog
EPICS_MODULE_TAG = R3.7
EPICS_SHORT_VERSION = 7.0.6.1
EPICS_VERSION_NUMBER = 7.0.6.1
EPICS_VERSION_STRING = "EPICS Version 7.0.6.1"
EXPORT_VARS = E3_MODULES_INSTALL_LOCATION_LIB TEMP_CELL_PATH EPICS_HOST_ARCH EPICS_BASE
              MSI E3_MODULE_NAME E3_MODULE_VERSION E3_SITEMODS_PATH E3_REQUIRE_MAKEFILE_INPUT_OPTIONS
              E3_REQUIRE_NAME E3_REQUIRE_CONFIG E3_REQUIRE_DB E3_REQUIRE_LOCATION
              E3_REQUIRE_DBD E3_REQUIRE_VERSION E3_REQUIRE_TOOLS E3_REQUIRE_INC E3_REQUIRE_LIB
              E3_REQUIRE_BIN QUIET
MSI = /epics/base-7.0.6.1/bin/linux-x86_64/msi
REQUIRE_CONFIG = /epics/base-7.0.6.1/require/4.0.0/configure
```

Many of these variables fall into one of several different categories: EPICS
environment variables, e3 environment variables, and e3 module-related
variables.

### e3 environment variables

These are variables generated by *require* or EPICS base and are used to reference
important paths for modules and for builds.

* `EPICS_*VERSION*`: Version of EPICS base
* `E3_MODULES_PATH`: Installation path for modules.
* `E3_REQUIRE_CONFIG`: *require* configure path.
* `E3_REQUIRE_TOOLS`: *require* tools path.
* `REQUIRE_CONFIG`: *require* configuration path used for by module
  configurations. It is typically the same as `E3_REQUIRE_CONFIG`, but is
  defined before `E3_REQUIRE_CONFIG`.

### e3 module/application core environment variables

These are variables that related to a given e3 module. Most of these are set in
`CONFIG_MODULE`, and some of them are generated by *require*.

The following are set in `CONFIG_MODULE` in the wrapper directory.

* `EPICS_MODULE_NAME`: The module name of the *community* module. See also
  `E3_MODULE_NAME`. <!-- TODO: This should be removed. It serves no purpose -->
* `EPICS_MODULE_TAG`: A string representing a valid git reference to the version
  of the module that will be built.  :::{note} This can be any valid git
  reference, but best practice is that this is a commit hash or even better a
  tag. Mutable references should be avoided.  :::
* `E3_MODULE_NAME`: The module name used *require* to install and to load the
  module.  :::{note} This is usually the same as `EPICS_MODULE_NAME`. However,
  there are two additional restrictions:
  1. Only lower-case characters, numbers, and underscores are allowed.
  2. The resulting string must be a valid C identifier :::
* `E3_MODULE_SRC_PATH`: Location of the module code within the wrapper
  repository.
* `E3_MODULE_VERSION`: Module version used for installing and loading the
  module.
* `E3_MODULE_MAKEFILE`: Name of the module/application makefile. <!-- TODO: This
  should be removed, it could be defined by require -->

The following variables are set by *require*.

* `E3_MODULES_INSTALL_LOCATION`: Parent path to installation directories.
* `E3_MODULES_INSTALL_LOCATION_BIN`: Binary installation path.
* `E3_MODULES_INSTALL_LOCATION_DB`: Database installation path.
* `E3_MODULES_INSTALL_LOCATION_INC`: Include installation path.
* `E3_MODULES_INSTALL_LOCATION_LIB`: Library installation path.

---

##  Assignments

1. Use the command `iocsh -r asyn` to load *asyn* into a fresh IOC. From
   the IOC shell, print out all of the database files that are included with
   *asyn*. Hint: There is a command that lets you run an external shell command
   within an IOC. See [chapter 2](2_e3_ioc.md).
2. Can you find out which file it is that allows us to run `make vars` within
   the e3 building system? Try adding the `--debug` flag when executing `make`.
