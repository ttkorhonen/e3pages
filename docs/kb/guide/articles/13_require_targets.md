# Article: *require* targets

In this article, we will give a brief
description and overview of some of the targets that are available in e3.

To begin with, if you are in an e3 wrapper directory, you can see some of the
main targets available by typing `make help`

```console
[iocuser@host:e3-iocStats]$ make help
---------------------------------------
Available targets
---------------------------------------
install         Install module to $(E3_MODULES_INSTALL_LOCATION)
uninstall       Uninstall the current module
build           Build current module
prebuild        Run module-specific commands before building
debug           Displays information about the build process
rebuild         Clean, build, and install the current module
clean           Deletes temporary build files
all             Initializes, patches, builds, and installs
init            Syncs and checks out the tag $(EPICS_MODULE_TAG) for the submodule
cellbuild       Builds the module while also searching in $(E3_CELL_PATH) for dependencies
cellinstall     Installs the module in a local directory $(E3_CELL_PATH)
celluninstall   Remove the module from the local directory $(E3_CELL_PATH)
cellvars        Print relevant environment variables for the local install
patch           Apply Patch Files
patchrevert     Revert Patch Files
test            Tests the current build
existent        Show installed versions of the current module
devinit         Initializes a dev setup, defined with configure/CONFIG_MODULE_DEV and configure/RELEASE_DEV
devdebug        Displays information about the build process (development mode)
devbuild        Build current module (development mode)
devclean        Deletes temporary build files (development mode)
devinstall      Install the current module (development mode)
devuninstall    Uninstall the current module (development mode)
```

Note that this list will depend on the version of *require* specified in
`configure/RELEASE`.

The targets fall into several categories.

## Main targets

These are the targets that are used in most cases when building, debugging,
testing, and deploying a module. They are related to the EPICS targets of the
same names, but with some differences.

* `make init`: This target depends on whether the wrapper includes a submodule
  or not. If it does, then this will initialise and clone the EPICS submodule in
  order to allow it to be built, as well as check out the correct commit hash.
  This is a necessary first stage for these modules. Otherwise, this target does
  nothing.
* `make patch`: This target will apply any module-specific patches. Patches are
  stored in `patch/Site/`. While not every module needs patches, it is an
  extremely good habit to start building a module with `make init patch` before
  building the module, since if you do not apply expected patches it is possible
  that the module will not build correctly. Patches can be removed with `make
  patchrevert`.
* `make build`: This will build the module. This will compile all of the files
  specified in the variable `SOURCES` from the module makefile, as well as
  generate a number of necessary files for the installation process.
* `make test`: This will perform a local installation of the module, and then
  try to start an IOC with that module.[^runiocsh] It will also perform any
  module-specific tests that are defined for that module. For more information,
  see {ref}`module_tests`.

  For a more detailed example, see the
  *[opcua](https://gitlab.esss.lu.se/e3/wrappers/communication/e3-opcua/-/blob/master/configure/module/RULES_MODULE#L21)*
  module.
* `make install`: This will install the compiled and generated files into the
  target location described above. This will also perform any template and
  substitution file expansion.

:::{note}
The target `build` is a dependency of `install` within *require*, so you can
technically run `make init patch install`. However, it can be beneficial to
separate these two stages, particularly during development.
:::

A few variations on this are the following.

* `make clean`: Deletes all of the temporary files.
* `make rebuild`: Cleans, then rebuilds and reinstalls the module.
* `make all`: Initialises, patches, and then rebuilds the module.
* `make prebuild`: Allows you to run custom tasks before `build` happens. This
  is specified in the module makefile, possibly as

  ```make
  prebuild:
      @echo ">>> This is the prebuild target <<<"
  ```

  which will run automatically before you run build.

  ```console
  [iocuser@host:e3-iocStats]$ make build
  cd iocStats && git checkout tags/3.1.16
  M       devIocStats/Makefile
  HEAD is now at 4df9e87 Merge pull request #30 from mark0n/callbackQueueStatus
  make[1]: Entering directory `/home/simonrose/data/git/e3/modules/core/e3-iocStats/iocStats'
  >>> This is the prebuild target <<<
  make[1]: Leaving directory `/home/simonrose/data/git/e3/modules/core/e3-iocStats/iocStats'
  make[1]: Entering directory `/home/simonrose/data/git/e3/modules/core/e3-iocStats/iocStats'
  make[2]: Entering directory `/home/simonrose/data/git/e3/modules/core/e3-iocStats/iocStats'
  # --- snip snip ---
  ```

## Additional targets

These are targets that are useful to help diagnose issues, debug, or display
information about the module.

* `make debug`: Runs through the build process, but instead displays data that
  is collected and used throughout the build process (e.g. exactly which files
  are compiled)
* `make vars`: Displays a list of environment variables including the module
  install locations.
* `make existent`: Displays the installed versions of the given module.

## Cellmode targets

Cellmode is used to allow for local builds of an e3 module. This can be for
testing purposes, or because you do not have permission to deploy modules to the
e3 environment. As such, there are a separate set of targets that are used to
create these local builds.

* `make cellinstall`: Installs the module in the path defined by
  `$(E3_CELL_PATH)`. The default is `$(TOP)/cellMods`. An IOC can be loaded with
  this module by running `iocsh -l ${E3_CELL_PATH}` to allow *require* to
  search in that path.
* `make cellbuild`: In case you have multiple modules that you are testing
  locally that all depend on each other, `cellbuild` will use `$(E3_CELL_PATH)`
  to search for module dependencies.
* `make cellvars`: Same as `make vars`, but uses `$(E3_CELL_PATH)` as the
  installation path.
* `make celluninstall`: Uninstalls the module from the installed location in
  `$(E3_CELL_PATH)`.

## Dev targets

Development (dev) mode is used to allow for separate development and
installation of an e3 module in parallel to the main installation. It uses the
variables defined in `CONFIG_MODULE_DEV` and `RELEASE_DEV`.

* `make devinit`: Initialises the development module. This clones the URL
  specified in `E3_MODULE_DEV_GITURL` in `CONFIG_MODULE_DEV`. This needs to be
  run before any other `dev` targets can be run.

The following targets, once `make devinit` has been run, are available. They
each do the same as the regular targets, but they instead use the cloned `dev`
version.

* `make devdebug`
* `make devbuild`
* `make devclean`
* `make devinstall`
* `make devuninstall`

[^runiocsh]: In order to use this, you first need to have installed
  [run-iocsh](https://gitlab.esss.lu.se/ics-infrastructure/run-iocsh).
