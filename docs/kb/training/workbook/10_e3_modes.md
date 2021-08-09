# Additional working modes

## Lesson overview

In this lesson you'll figure some stuff out.

## Cell mode

asdf

## Development mode

The development mode is instead intended to allow the developer to modify the source module, and utilizes `git clone` instead of `git submodule`. This provides
a method to use a forked copy of the source module, which allows you to commit changes even if you lack permission to push to the remote repository.

The configuration for **Development mode** is modified in the files `CONFIG_MODULE_DEV` and `RELEASE_DEV` contained in the `configure/` directory. If
these files do not exist, you can create them from the original `CONFIG_MODULE` and `RELEASE` files with some minor modifications. They key differences are

* `E3_MODULE_DEV_GITURL`: The remote path to the module repository. This allows you to use a forked version of a module that you do not have permission to commit to.

* `E3_MODULE_SRC_PATH`: The local path used for the deployment mode, which with default settings is the module's name with the added suffix `-dev`; for example, `e3-iocStats` has `iocStats` source path in the deployment, and `iocStats-dev` one in the development mode. Note that since `-dev` will be added, you can use the same module name as in development mode.

Development mode allows a user to work with (and commit changes to) a remote module without needing to have permissions to commit to the standard one. This is a
good method to make changes in order to create a pull/merge request to a community EPICS module.

To use development mode, you simply prefix the usual commands with `dev`. That is, to build and install a module in development mode you would run
```console
[iocuser@host:e3-iocStats]$ make devinit devpatch devbuild devinstall
```

As in standard mode, there are also `dev` versions of many targets, such as `devvars, devexistent, devclean`, etc. There is also an additional target,
`make devdistclean` which removes the cloned source directory.

Finally, note that `make existent` and `make devexistent` are (essentially) identical in that they both provide information for what has been installed.

:::{admonition} Exercise
How are those two commands actually different? That is, when will they produce different output?
:::

### Setting up the development module

In order to learn to work both with development mode and with modules in general, we will work with our own forked copy of the
community EPICS module *iocStats*.

To begin with, fork your own copy from the community *[iocStats](https://github.com/epics-modules/iocStats)*, and then update the
variable `E3_MODULE_DEV_GITURL` in `CONFIG_MODULE_DEV` to point towards your fork.

Begin by running the command `make devvars`. This will show the e3 module variables with the development mode, which should look
something like the following. Note that this example uses the ESS ICSHWI fork and compares it against the community module, and
so your output may be different.

```console
[iocuser@host:e3-iocStats]$ make devvars

------------------------------------------------------------
>>>>     Current EPICS and E3 Environment Variables     <<<<
------------------------------------------------------------

BASE_3_14 = NO
BASE_3_15 = NO
BASE_3_16 = NO
BASE_7_0 = YES
E3_MODULES_INSTALL_LOCATION = /epics/base-7.0.5/require/3.4.1/siteMods/iocstats/jhlee
E3_MODULES_INSTALL_LOCATION_BIN = /epics/base-7.0.5/require/3.4.1/siteMods/iocstats/jhlee/bin
E3_MODULES_INSTALL_LOCATION_DB = /epics/base-7.0.5/require/3.4.1/siteMods/iocstats/jhlee/db
E3_MODULES_INSTALL_LOCATION_INC = /epics/base-7.0.5/require/3.4.1/siteMods/iocstats/jhlee/include
E3_MODULES_INSTALL_LOCATION_LIB = /epics/base-7.0.5/require/3.4.1/siteMods/iocstats/jhlee/lib
E3_MODULES_PATH = /epics/base-7.0.5/require/3.4.1/siteMods
E3_MODULES_VENDOR_LIBS_LOCATION = /epics/base-7.0.5/require/3.4.1/siteLibs/vendor/iocstats/jhlee
E3_MODULE_DEV_GITURL = "https://github.com/icshwi/iocStats"
E3_MODULE_MAKEFILE = iocStats.Makefile
E3_MODULE_MAKE_CMDS = make -C iocStats-dev -f iocStats.Makefile LIBVERSION="jhlee" PROJECT="iocstats" EPICS_MODULES="/epics/base-7.0.5/require/3.4.1/siteMods" EPICS_LOCATION="/epics/base-7.0.5" BUILDCLASSES="Linux" E3_SITEMODS_PATH="/epics/base-7.0.5/require/3.4.1/siteMods" E3_SITEAPPS_PATH="/epics/base-7.0.5/require/3.4.1/siteApps" E3_SITELIBS_PATH="/epics/base-7.0.5/require/3.4.1/siteLibs" iocstats_E3_GIT_DESC="7.0.5-3.4.1/3.1.16-2fd5f31-20210426T180403-8-gf4f95ba" iocstats_E3_GIT_STATUS="[ \\\" M configure/CONFIG_MODULE_DEV\\\",  \\\" M configure/RELEASE_DEV\\\", ]" iocstats_E3_GIT_URL="git@gitlab.esss.lu.se:e3/wrappers/core/e3-iocStats.git"
E3_MODULE_NAME = iocstats
E3_MODULE_SRC_PATH = iocStats-dev
E3_MODULE_VERSION = jhlee
E3_MODULE_VERSION_ORIG = jhlee
E3_REQUIRE_CONFIG = /epics/base-7.0.5/require/3.4.1/configure
E3_REQUIRE_TOOLS = /epics/base-7.0.5/require/3.4.1/tools
EPICS_MODULE_NAME = iocStats
EPICS_MODULE_TAG = master
EPICS_SHORT_VERSION = 7.0.5
EPICS_VERSION_NUMBER = 7.0.5
EPICS_VERSION_STRING = "EPICS Version 7.0.5"
EXPORT_VARS = E3_MODULES_VENDOR_LIBS_LOCATION E3_MODULES_INSTALL_LOCATION_LIB TEMP_CELL_PATH EPICS_HOST_ARCH EPICS_BASE MSI E3_MODULE_NAME E3_MODULE_VERSION E3_SITEMODS_PATH E3_SITEAPPS_PATH E3_SITELIBS_PATH E3_REQUIRE_MAKEFILE_INPUT_OPTIONS E3_REQUIRE_NAME E3_REQUIRE_CONFIG E3_REQUIRE_DB E3_REQUIRE_LOCATION E3_REQUIRE_DBD E3_REQUIRE_VERSION E3_REQUIRE_TOOLS E3_REQUIRE_INC E3_REQUIRE_LIB E3_REQUIRE_BIN QUIET   
GIT_REMOTE_NAME = origin
MSI = /epics/base-7.0.5/bin/linux-x86_64/msi
PROD_BIN_PATH = /epics/base-7.0.5/require/3.4.1/siteMods/iocstats/jhlee/bin/linux-x86_64
REQUIRE_CONFIG = /epics/base-7.0.5/require/3.4.1/configure
RMDIR = rm -f -rf
SUDOBASH = "bash -c"
TEMP_CELL_PATH = /home/simonrose/data/git/e3/modules/core/e3-iocStats/testMods-210730090422
```

Next, you must initialise the development mode. This is done using `make devinit`, which will clone your fork into a directory with
the name of `iocStats-dev`. This is what the file tree will look like after:

```console
[iocuser@host:e3-iocStats]$ tree -L 1
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

Confirm now that you have dev mod set up correctly by checking the remote urls for both the submodule and development directories by
using `git remote -v`.
```console
[iocuser@host:iocStats]$ git remote -v
```

```console
[iocuser@host:iocStats-dev]$ git remote -v 
```

:::{tip}
Note that by default, the `*-dev` path within an e3-module is ignored (which you can see in the `.gitignore`). With this workflow, we can expand our repository up to any number of use cases.
:::

One important point to remember is that both standard and development mode use much of the same configuration/metadata in order to build and deploy a module. In particular,
they both use the same `module.Makefile`, even though some of the configuration (`CONFIG_MODULE` versus `CONFIG_MODULE_DEV` and similarly for `RELEASE`) may differ.

## Assignments

* Can you override the default `E3_MODULE_DEV_GITURL` with your own forked repository without any `git status` changes in `e3-iocStats`? The output of `git status` should look like
  
  ```console
  [iocuser@host:e3-iocstats]$ git status
  On branch master
  Your branch is up-to-date with 'origin/master'.
  nothing to commit, working directory clean
  ```

* Do we need `make devdistclean`? Is there any other way to clean or remove a cloned repository `iocStats-dev`? <!-- TODO: I feel like this is a question for us. Seriously, do we really need this? All it does is deletes the *-dev folder. -->
* What's the difference between `make existent` and `make devexistent`?
* What is the difference between a `p0` patch and `p1` patch? Is it the same in EPICS as generally with UNIX patch files?
* We have an `1.0.0-awesome.p0.patch` file. How would we apply it to Development mode source files?

