# The *require* module

At its heart, the ESS Epics Environment (E3, not to be confused with EEE) *is* the `require` module. This does three things:

* It provides a consistent build process to package EPICS modules which is based on the EPICS build system
* It provides a method to start a soft IOC
* It provides a mechanism to dynamically load shared libraries for use within an IOC.

Each of these is linked to each other; the dynamic loading depends on the build process, and it also depends on how the soft IOC has been started. Nevertheless, these are separate purposes that `require` serves.

The most complicated is the build process, but each of these are important for the running and maintenance of the E3 environment.

## The build process

As stated above, this is by far the most complicated portion. We will provide here a brief overview of some of the pieces, but we will provide a separate more extensive document for those that are interested.

The input to the build process is essentially the following:

* A set of configuration files describing dependencies and for which version of EPICS you are building the module
* A file `${module}.Makefile` which collects all of the build instructions, including .db and .template files to install, .dbd files, and source files to compile.

The build process then runs in five passes, with the last four passes all managed in recursive calls with `driver.makefile`.

1. In the e3-wrapper directory: we collect some information and decide what build process we will perform (from `RULES_E3`), calling `make` in the module directory with information passed as in `CONFIG_E3_MAKEFILE`.
2. In the module directory: EPICSVERSION has not been defined, so determine which versions to build for.
3. In the module directory: Target architecture `${T_A}` has not been defined, so determine the architectures to build for.
4. In the module directory: Perform a final collection of the relevant files, create the directories `O.${EPICSVERSION}_Common` and `O.${EPICSVERSION}_${T_A}`.
5. In the directories `O.*`: Build/Install all of the required shared libraries and other files for the given version of EPICS base and target architecture.

[Details for the build process](driver.makefile.md)

## IOC Startup

IOC startup is run from the bash script `iocsh.bash`, which is installed in `$(E3_REQUIRE_LOCATION)/bin/iocsh.bash`.

This file generates a temporary startup script which is passed to `softIocPVA` from EPICS base (note that we use
`softIocPVA`, not `softIoc`, since we are restricting ourselves to EPICS base 7 at ESS). This temporary startup
script:
* Tries to load an environment file, if it exists
* Sets some environment variables e.g. `IOCSH_TOP`, `REQUIRE_IOC`
* Prints a list of EPICS environment variables into the startup log
* Loads `require`
* Initializes PVs to track which modules and versions are loaded

There are number of option flags and arguments that `iocsh.bash` takes, the most common being:
* `iocsh.bash st.cmd` -- Run the commands in `st.cmd`. If `iocInit` is not contained in
  `st.cmd`, then it will be added after the last line.
  > Note: If `st.cmd` does not have a line break on its last line, then that line will not be executed!
* `iocsh.bash -r module[,version]` -- Load the given module/version upon startup. Equivalent to including the line
  `require module[,version]` in your startup script.
* `iocsh.bash -c 'some command'` -- Executes the command `some command` in the IOC
  shell.
* `iocsh.bash filename` -- If the file is a .db file, a .dbd file, a .subs file, or a .subst file, then the file
  will be appropriately loaded at startup.

Most of the functionality for this is contained in the file `tools/iocsh_functions`. There is also a gdb/valgrind
option if you would like to run an IOC with either of those utilities.

## Dynamic loading of modules

This is the most obviously visible part of `require` from the perspective of an IOC developer; one must include the line
```bash
require $module[,$version]
```
in your `st.cmd` startup script in order to load a module in E3. If you specify a version, then require will try to load that version. If you
leave `version` blank, then it will load the version with the highest numerical version available, or the first test version it finds.

### Numerical versions

A numerical version is specified in one of two ways:

* MAJOR.MINOR.PATCH e.g. `require asyn,4.37.0`
* MAJOR.MINOR.PATCH-BUILD e.g. `require sis8300llrf,3.17.1-1`

If you do not specify a BUILD number, then `require` will load the version with the highest build number. Otherwise, 
require will match the version exactly.

Note that `1.0.0 < 1.0.0-0 < 1.0.0-1 < ... < 1.0.1 < ...`

### Test versions

A test version is any version that does not conform to the above pattern. So `simonrose` is a test version, but so
is `1.0.0-test` or even `1.0`.

Note that `require` will load the first test version it finds if there are no numeric versions, so if you want
to load a test version it is best practice to specify the exact version you would like to load.

### Dependency resolution

If one module depends on another one (for example, `StreamDevice` depends on `asyn`), then loading `StreamDevice`
will automatically load `asyn` as well. Dependencies are version-specific: For example, `StreamDevice` 2.8.10 in
its current incarnation has been built against `asyn` 4.37.0; if you load that version of `StreamDevice` then 
it will try to load `asyn` 4.37.0. If it cannot find that version, or if another version of `asyn` has already
been loaded, then the IOC will exit with an error.

These dependencies are generated at build time and are stored in `$(module)/$(version)/lib/$(T_A)/$(module).dep`.
For example, the one for StreamDevice is
```bash
# Generated file. Do not edit.
asyn 4.37.0
calc 3.7.3
pcre 8.41.0
```

`require` is limited in the degree to which it can perform dependency resolution; all it can do is a simple check
against existing loaded versions. This is why build numbers are necessary: as an example, consider the following
scenario.

`sis8300llrf` version 3.16.1 depends on `scaling`, and has been built against version 1.7.0. We update `scaling`
to version 1.7.1. There is no new version of `sis8300llrf`, but an IOC integrator would like to use the new
version of `scaling`. What should happen to the existing installed version of `sis8300llrf`?

1. We could uninstall it and rebuild/install it against the new version of scaling. However, this prevents anyone
   who needs that version combination for any reason from being able to use it; in general, we want to avoid
   removing any installed modules, we should only add new versions.
2. We could try to update the version of `sis8300llrf` to 3.16.2 despite the fact that no changes have been made.
   If this is an ESS module, then this is possible, but not ideal; it is particularly bad if it is a module that
   is not being developed in-house, as our version will be out of sync with the community module.
3. We could instead update the version to 3.16.1-1 i.e. add a build number. This way, the existing version has not
   been modified; moreover, you can use `sis8300llrf` version 3.16.1 with either version of scaling by specifying
   the build number.