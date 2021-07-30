# Variables within e3

## Lesson Overview

In this lesson, you'll learn how to do the following:

* Understand variables and parameters within an IOC.
* Run commands to access access variables and parameters from within an IOC.
* Understand EPICS and e3 environment variables used when a module is configured.
* Combine variable commands to access path or files of any module within an IOC.

---

## Running an IOC

The following variables are defined when an IOC is running from within startup and iocsh scripts. 

### General `iocsh.bash` variables

* `REQUIRE_IOC`: A unique name of the IOC that can be used to track certain variables in a certain IOC. For example, an e3 IOC will generate on startup a number of PVs of the form
  `$(REQUIRE_IOC):MODULES` that list the modules that are loaded in a given IOC.
  :::{note}
  If `IOCNAME` is defined in the environment prior to the IOC starting, then `REQUIRE_IOC` will be a (possibly truncated) copy of that. Otherwise, it will be a name which depends on the process
  ID for the running IOC and so will not be consistent from one run to the next of the IOC.
  :::

* `E3_CMD_TOP`: The absolute path to the startup script (cmd file), if one exists.

* `E3_IOCSH_TOP`: The absolute path to where `iocsh.bash` was exectued from; equivalent to running `pwd`.

* `IOCSH_PS1`: The IOC Prompt String. Defaults to `$HOSTNAME-$PID > `.

### Variables created by *require*

Whenever an e3 module is dynamically loaded, require generates a number of module-specific variables that are useful in scripts. For `mrfioc2` these would be

* `mrfioc2_VERSION` - The version of `mrfioc2` that was loaded.
* `mrfioc2_DIR` - The absolute path where `mrfioc2` is located. Useful for loading `.iocsh` snippets and other files installed with the module.
* `mrfioc2_DB` - The absolute path where the database, template, protocol, and substitutions files for `mrfioc2` have been installed.
* `mrfioc2_TEMPLATES` - Same as above

:::{note}
One should pay attention to these strings somewhat: `mrfioc2_DIR` ends with a `/`, but `mrfioc2_DB` does not.
:::

Let's see these in action. Copy the following into a new `ch6.cmd` file.
```bash
require iocstats

iocInit

echo "E3_IOCSH_TOP       : $(E3_IOCSH_TOP)"
echo "E3_CMD_TOP         : $(E3_CMD_TOP)"
echo "iocstats_DIR       : $(iocstats_DIR)"
echo "iocstats_VERSION   : $(iocstats_VERSION)"
echo "iocstats_DB        : $(iocstats_DB)"
echo "iocstats_TEMPLATES : $(iocstats_TEMPLATES)"
```

```console
[iocuser@host:e3training/workbook]$ iocsh.bash ch6.cmd

# --- snip snip ---

Starting iocInit
############################################################################
## EPICS R7.0.5-E3-7.0.5-patch
## Rev. 2021-03-15T09:48+0100
############################################################################
iocRun: All initialization complete
echo "E3_IOCSH_TOP       : /home/simonrose/data/git/e3/modules/core/e3-iocStats"
E3_IOCSH_TOP       : /home/simonrose/data/git/e3/modules/core/e3-iocStats
echo "E3_CMD_TOP         : /home/simonrose/data/git/e3/modules/core/e3-iocStats"
E3_CMD_TOP         : /home/simonrose/data/git/e3/modules/core/e3-iocStats
echo "iocstats_DIR       : /epics/base-7.0.5/require/3.4.1/siteMods/iocstats/3.1.16+0/"
iocstats_DIR       : /epics/base-7.0.5/require/3.4.1/siteMods/iocstats/3.1.16+0/
echo "iocstats_VERSION   : 3.1.16+0"
iocstats_VERSION   : 3.1.16+0
echo "iocstats_DB        : /epics/base-7.0.5/require/3.4.1/siteMods/iocstats/3.1.16+0/db"
iocstats_DB        : /epics/base-7.0.5/require/3.4.1/siteMods/iocstats/3.1.16+0/db
echo "iocstats_TEMPLATES : /epics/base-7.0.5/require/3.4.1/siteMods/iocstats/3.1.16+0/db"
iocstats_TEMPLATES : /epics/base-7.0.5/require/3.4.1/siteMods/iocstats/3.1.16+0/db

# --- snip snip ---
```

As stated before, these variables are needed if you want to use database or protocol files that have been installed with a given module. For example, *StreamDevice*
uses a varaible `STREAM_PROTOCOL_PATH` when searching for `.proto` files, and so a common idiom in a startup script is a line such as

```bash
epicsEnvSet("STREAM_PROTOCOL_PATH", "$(mymodule_DB)")
```

Excercise:
* Modify the above startup script to add some other modules, and look at the resulting paths. For example, load `stream` and see what paths `module_DIR` are available within the IOC shell.

### EPICS variables, parameters, and environment variables

You can see EPICS parameters and environment variables from within an IOC using `epicsParamShow` and `epicsEnvShow`.

```console
# Set the IOC Prompt String One 
epicsEnvSet IOCSH_PS1 "58bef31.faiserv.18238 > "
#
58bef31.faiserv.18238 > epicsParamShow 
58bef31.faiserv.18238 > epicsEnvShow 
```
 <!-- fixme: clean up above -->

* Run `epicsPrtEnvParams`. Which other command returns the same result?

* How do we print only one variable - for example `TOP`?

  > For questions on EPICS functions, the [App Developers Guide](https://epics.anl.gov/base/R3-15/6-docs/AppDevGuide/IOCShell.html#x19-73300018) will usually have your answers.

  > There are four UNIX commands that can be used from within the IOC shell: `date`, `pwd`, `cd`, and `echo`.

* What is the difference between `$(TOP)` and `${TOP}`? Is it the same inside of the IOC shell as in UNIX?

* In the shell, please try to run `var`. What do you see? 

  ```console
  58bef31.faiserv.18238 > var
  sandbag = 0
  atExitDebug = 0
  boHIGHlimit = 100000
  boHIGHprecision = 2
  calcoutODLYlimit = 100000
  calcoutODLYprecision = 2
  callbackParallelThreadsDefault = 4
  dbBptNotMonotonic = 0
  dbQuietMacroWarnings = 0
  dbRecordsAbcSorted = 0
  dbRecordsOnceOnly = 0
  dbTemplateMaxVars = 100
  dbThreadRealtimeLock = 1
  exprDebug = 0
  histogramSDELprecision = 2
  requireDebug = 0
  runScriptDebug = 0
  seqDLYlimit = 100000
  seqDLYprecision = 2
  ```

In the running IOC, let's require the recsync module.

1. Run:

   ```console
   58bef31.faiserv.18238 > require recsync,1.3.0
   Module recsync version 1.3.0 found in /epics/base-3.15.5/require/3.0.4/siteMods/recsync/1.3.0/
   Loading library /epics/base-3.15.5/require/3.0.4/siteMods/recsync/1.3.0/lib/linux-x86_64/librecsync.so
   Loaded recsync version 1.3.0
   Loading dbd file /epics/base-3.15.5/require/3.0.4/siteMods/recsync/1.3.0/dbd/recsync.dbd
   Calling function recsync_registerRecordDeviceDriver
   ```

2. Redo require:

   ```console
   58bef31.faiserv.18238 > require recsync,1.3.0
   Module recsync version 1.3.0 already loaded
   ```

3. Type in the command `var requireDebug 1`:

   ```console
   58bef31.faiserv.18238 > var requireDebug 1
   ```

4. Redo require again:

   ```console
   58bef31.faiserv.18238 > require recsync,1.3.0
   require: versionstr = "-1.3.0"
   require: module="recsync" version="1.3.0" args="(null)"
   require: searchpath=/epics/base-3.15.5/require/3.0.4/siteMods:/epics/base-3.15.5/require/3.0.4/siteApps
   require: compareVersions(found=1.3.0, request=1.3.0)
   require: compareVersions: MATCH exactly
   Module recsync version 1.3.0 already loaded
   require: library found in /epics/base-3.15.5/require/3.0.4/siteMods/recsync/1.3.0/
   require: putenv("MODULE=recsync")
   require: looking for template directory
   require: directory /epics/base-3.15.5/require/3.0.4/siteMods/recsync/1.3.0/db exists
   require: found template directory /epics/base-3.15.5/require/3.0.4/siteMods/recsync/1.3.0/db
   require: putenv("recsync_DB=/epics/base-3.15.5/require/3.0.4/siteMods/recsync/1.3.0/db")
   require: putenv("recsync_TEMPLATES=/epics/base-3.15.5/require/3.0.4/siteMods/recsync/1.3.0/db")
   require: putenv("TEMPLATES=/epics/base-3.15.5/require/3.0.4/siteMods/recsync/1.3.0/db")
   ```

As you can see, `var` is defined as a variable within the *require* module. This variable is usually used as a debug message control variable, but can be used for more. 

5. Make sure to disable the debugging output again:

   ```console
   58bef31.faiserv.18238 > var requireDebug 0
   58bef31.faiserv.18238 > require recsync,1.3.0
   ```

> Note that the UP and DOWN keys can be used to navigate between historical commands.

## Building a module or an application 

Back in [Chapter 3](3_module_versions.md) we looked at the two e3 variables `E3_MODULE_VERSION` and  `EPICS_MODULE_TAG`. As you will see, there are many more environment variables that we can use together with e3 when configuring and installing modules.

### e3 environment variables

You can print out all environment variables of a module with the rule `make vars`:

```console
[iocuser@host:e3-caPutLog]$ make vars

------------------------------------------------------------
>>>>     Current EPICS and E3 Envrionment Variables     <<<<
------------------------------------------------------------

E3_MODULES_INSTALL_LOCATION = /epics/base-3.15.5/require/3.0.4/siteMods/caPutLog/3.6.0
E3_MODULES_INSTALL_LOCATION_BIN = /epics/base-3.15.5/require/3.0.4/siteMods/caPutLog/3.6.0/bin
E3_MODULES_INSTALL_LOCATION_BIN_LINK = /epics/base-3.15.5/require/3.0.4/siteLibs/caPutLog_3.6.0_bin
E3_MODULES_INSTALL_LOCATION_DB = /epics/base-3.15.5/require/3.0.4/siteMods/caPutLog/3.6.0/db
E3_MODULES_INSTALL_LOCATION_DBD_LINK = /epics/base-3.15.5/require/3.0.4/siteLibs/caPutLog.dbd.3.6.0
E3_MODULES_INSTALL_LOCATION_DB_LINK = /epics/base-3.15.5/require/3.0.4/siteLibs/caPutLog_3.6.0_db
E3_MODULES_INSTALL_LOCATION_INC = /epics/base-3.15.5/require/3.0.4/siteMods/caPutLog/3.6.0/include
E3_MODULES_INSTALL_LOCATION_INC_LINK = /epics/base-3.15.5/require/3.0.4/siteLibs/caPutLog_3.6.0_include
E3_MODULES_INSTALL_LOCATION_LIB = /epics/base-3.15.5/require/3.0.4/siteMods/caPutLog/3.6.0/lib
E3_MODULES_INSTALL_LOCATION_LIB_LINK = /epics/base-3.15.5/require/3.0.4/siteLibs/caPutLog_3.6.0_lib
E3_MODULES_LIBLINKNAME = libcaPutLog.so.3.6.0
E3_MODULES_LIBNAME = libcaPutLog.so
E3_MODULES_PATH = /epics/base-3.15.5/require/3.0.4/siteMods
E3_MODULES_VENDOR_LIBS_LOCATION = /epics/base-3.15.5/require/3.0.4/siteLibs/vendor/caPutLog/3.6.0
E3_MODULE_MAKEFILE = caPutLog.Makefile
E3_MODULE_MAKE_CMDS = make -C caPutLog -f caPutLog.Makefile LIBVERSION="3.6.0" PROJECT="caPutLog" EPICS_MODULES="/epics/base-3.15.5/require/3.0.4/siteMods" EPICS_LOCATION="/epics/base-3.15.5" BUILDCLASSES="Linux" E3_SITEMODS_PATH="/epics/base-3.15.5/require/3.0.4/siteMods" E3_SITEAPPS_PATH="/epics/base-3.15.5/require/3.0.4/siteApps" E3_SITELIBS_PATH="/epics/base-3.15.5/require/3.0.4/siteLibs"
E3_MODULE_NAME = caPutLog
E3_MODULE_SRC_PATH = caPutLog
E3_MODULE_VERSION = 3.6.0
E3_REQUIRE_CONFIG = /epics/base-3.15.5/require/3.0.4/configure
E3_REQUIRE_TOOLS = /epics/base-3.15.5/require/3.0.4/tools
EPICS_MODULE_NAME = caPutLog
EPICS_MODULE_TAG = tags/R3.6
EXPORT_VARS = E3_MODULES_VENDOR_LIBS_LOCATION E3_MODULES_INSTALL_LOCATION_LIB_LINK EPICS_HOST_ARCH EPICS_BASE MSI E3_MODULE_VERSION E3_SITEMODS_PATH E3_SITEAPPS_PATH E3_SITELIBS_PATH E3_REQUIRE_MAKEFILE_INPUT_OPTIONS E3_REQUIRE_NAME E3_REQUIRE_DB E3_REQUIRE_CONFIG E3_REQUIRE_LOCATION E3_REQUIRE_DBD E3_REQUIRE_VERSION E3_REQUIRE_TOOLS E3_REQUIRE_INC E3_REQUIRE_LIB E3_REQUIRE_BIN QUIET   SUDO2 SUDO_INFO SUDOBASH SUDO
INSTALLED_EPICS_BASE_ARCHS = linux-ppc64e6500 linux-x86_64
MSI = /epics/base-3.15.5/bin/linux-x86_64/msi
PROD_BIN_PATH = /epics/base-3.15.5/require/3.0.4/siteLibs/caPutLog_3.6.0_bin/linux-x86_64
REQUIRE_CONFIG = /epics/base-3.15.5/require/3.0.4/configure
```

### Customized EPICS environment variables

* `EPICS_BASE` is where EPICS base is installed (EPICS environment variable).

* `EPICS_HOST_ARCH` is the host system architecture (EPICS environment variable).

* `EPICS_MODULE_NAME` is the module name used by *require* and e3 (e3 environment variable). See also `E3_MODULE_NAME`. 

  *N.B.! This name should only consist of letters (upper and lower case) and digits. Underscore is also allowed.*
  
  > Technically, this name is coverted into a `char` in a C program, and much thus follow C programming rules.

* `EPICS_MODULE_TAG` is a point release information of the remote source code repository; i.e. what you would use together with `git checkout`, like: `master`, `tags/R3.6`, or `ae5d083`.

* `INSTALLED_EPICS_BASE_ARCHS` shows the EPICS base architecture installed in the local system.

  > At ESS, this will almost always be `linux-x86_64`.

### e3 environment variables

* `E3_SITEMODS_PATH`: e3 site module installation path. 

* `E3_SITEAPPS_PATH`: e3 site application installation path. 

* `E3_SITELIBS_PATH`: e3 site library path.

* `E3_REQUIRE_NAME`: unique e3 module name used by *require*. This variable should not be changed. 

* `E3_REQUIRE_VERSION`: *require* version number. 

* `E3_REQUIRE_BIN`: *require* binary path. 

* `E3_REQUIRE_CONFIG`: *require* configure path.

* `E3_REQUIRE_DB`: *require* database path. 

* `E3_REQUIRE_INC`: *require* include path. 

* `E3_REQUIRE_LIB`: *require* lib path.

* `E3_REQUIRE_LOCATION`: *require* root directory path. 

* `E3_REQUIRE_TOOLS`: *require* tools path. 

* `REQUIRE_CONFIG`: *require* configuration path used for by module configurations. It is typically the same as `E3_REQUIRE_CONFIG`, but is defined before `E3_REQUIRE_CONFIG`. 

### e3 module/application core environment variables

* `E3_MODULE_NAME`: Module name used by the command `require` within an IOC startup script, i.e. `require E3_MODULE_NAME, E3_MODULE_VERSION`. This is usually the same as `EPICS_MODULE_NAME`. 

* `E3_MODULE_SRC_PATH`: Where your source code is downloaded. Note that the location and usage depends on which mode you use (deployment, development, or local).

* `E3_MODULE_VERSION`: Module version used for `require E3_MODULE_NAME, E3_MODULE_VERSION`.

* `E3_MODULE_MAKEFILE`: Name of the module/application makefile. 

* `E3_MODULES_PATH`: Parent path of the installation location. This can be `E3_SITEMODS_PATH` or `E3_SITEAPPS_PATH`. 

* `E3_MODULES_LIBNAME`: Name of shared libraries.

* `E3_MODULES_INSTALL_LOCATION`: Parent path to installation directoriess.

* `E3_MODULES_INSTALL_LOCATION_BIN`: Binary installation path. 

* `E3_MODULES_INSTALL_LOCATION_DB`: Database installation path. 

* `E3_MODULES_INSTALL_LOCATION_INC`: Include installation path.

* `E3_MODULES_INSTALL_LOCATION_LIB`: Library installation path.

### e3 module/application auxilliary environment variables

The following variables are defined within a module or application by default.

> These are only used when necessitated by an applicaton.

* `E3_MODULES_LIBLINKNAME`: Symbolic link name to library files for a module. 

* `E3_MODULES_INSTALL_LOCATION_BIN_LINK`: Symbolic link name of the module binary path located in `E3_SITELIBS_PATH`, in the following form: `${E3_MODULE_NAME}_${E3_MODULE_VERSION}_bin`. 

* `E3_MODULES_INSTALL_LOCATION_DB_LINK`: Symbolic link name of the module database path located in `E3_SITELIBS_PATH`, in the following form: `${E3_MODULE_NAME}_${E3_MODULE_VERSION}_db`. 

* `E3_MODULES_INSTALL_LOCATION_INC_LINK`: Symbolic link name of the module include path located in `E3_SITELIBS_PATH`, in the following form: `${E3_MODULE_NAME}_${E3_MODULE_VERSION}_include`.

* `E3_MODULES_INSTALL_LOCATION_LIB_LINK`: Symbolic link name of the module library path located in `E3_SITELIBS_PATH`, in the following form: `${E3_MODULE_NAME}_${E3_MODULE_VERSION}_lib`. 

* `E3_MODULES_INSTALL_LOCATION_DBD_LINK`: Symbolic link name of the module database definition file located in `E3_SITELIBS_PATH`, in the following form: `${E3_MODULE_NAME}_dbd_${E3_MODULE_VERSION}`. 

* `E3_MODULES_VENDOR_LIBS_LOCATION`: Vendor or 3rd party library path located in `E3_SITELIBS_PATH`, in the following form: `vendor/E3_MODULE_NAME/E3_MODULE_VERSION`. 

* `PROD_BIN_PATH`: Short binary path to be used if users want to access module-specific executable commands. 

* `E3_MODULE_MAKE_CMDS`: Command to execute to build/install. 

* `EXPORT_VARS`: Collection of exported environment variables within e3's building system which are used by makefiles.

---

##  Assignments

* Using the startup script in `ch6_supplementary_paht/ch6.cmd`, print out all database files of the *asyn* module within an IOC.
  
  > If you get stuck, remember that there's a command to use any UNIX command from within an IOC shell. Can you remember what it is?

* Can you find out which file it is that allows us to run `make vars` or `make env` within the e3 building system? 
  
  > It is the same for all modules and applications, so where could be located?

