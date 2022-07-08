(the_require_module)=

# The *require* module

* Provides a method to start a soft IOC.
* Provides a mechanism to dynamically load shared libraries for use within an
  IOC.
* Provides a build process (more on this in {ref}`build_process`).

:::{note}
Each of the above-mentioned features are linked to each other; the dynamic
loading depends on the build process, and it also depends on how the soft IOC
has been started.
:::

## IOC startup

IOC startup is run from the bash script `iocsh`, which is installed in
`${E3_REQUIRE_LOCATION}/bin/iocsh`. This script generates a temporary
startup script which is passed to `softIocPVA` from EPICS base. This temporary
startup script:

* Sets some environment variables, e.g. `${IOCSH_TOP}` and `${REQUIRE_IOC}`
* Prints a list of EPICS environment variables into the startup log
* Loads *require*
* Initialises PVs to track which modules and versions are loaded

:::{note}
At ESS, we have decided to only use EPICS base 7, and thus we only make use of
`softIocPVA` (and not `softIoc`).
:::

There are number of option flags and arguments that `iocsh` accepts, the
most common being:

* `iocsh st.cmd`---Run the commands in `st.cmd`.
* `iocsh -r module[,version]`---Load the given module/version upon startup.
  Equivalent to including the line `require module[,version]` in your startup
  script.
* `iocsh -c 'some command'`---Executes the command `some command` in the
  IOC shell.
* `iocsh filename` -- If the file is a `.db` file, a `.dbd` file, a `.subs`
  file, or a `.subst` file, then the file will be appropriately loaded at
  startup.

:::{note}
If the command `iocInit` is not explicitly called in `st.cmd`, it will be
implicitly called by the end of the process (after running the contents of
`st.cmd`).
:::

:::{warning}
The file `st.cmd` above **must** have a newline at the end of the
file---otherwise the last line will be ignored.
:::

Most of the functionality for this is contained in the file
`tools/iocsh_functions` in the [require repository](https://gitlab.esss.lu.se/e3/e3-require).
There are also *gdb* and *valgrind* options if you would like to run an IOC with
either of those utilities. More information can be found at {ref} `debugging_e3`.

## Dynamic loading of modules

This is the most obviously visible part of *require* from the perspective of an
IOC developer; one must include the line `require $MODULE[,$MODULE_VERSION]` in
the startup script (`st.cmd`) in order to load a module in e3. If a version is
specified, *require* will try to load that version. If you leave `version`
blank, it will load the version with the highest numerical version available,
else the first test version it finds.

### Versioning

#### Numerical versions

Versioning of modules mostly follows the [semantic
versioning](https://semver.org/) (semver) scheme. A numerical version is
specified in one of two ways:

* MAJOR.MINOR.PATCH (e.g. `require asyn,4.41.0`)
* MAJOR.MINOR.PATCH+BUILD (e.g. `require sis8300llrf,3.17.1+1`)

If you do not specify a BUILD number, then *require* will load the version with
the highest build number. Otherwise, *require* will match the version exactly.

Note that `1.0.0 < 1.0.0+0 < 1.0.0+1 < ... < 1.0.1 < ...`.

:::{note}
The syntax for build numbers changed between require 3.3.0 and require 3.4.0.
Initially the separator was a `-`, but in order to be more consistent with
[semantic versioning](https://semver.org/), the e3 team decided to change it to
a `+`.
:::

#### Test versions

A test version is any version that does not conform to the above pattern. So
`simonrose` is a test version, but so is `1.0.0-test` or even `1.0`.

:::{tip}
As *require* will load the first test version it finds when there are no numeric
versions, it is best practice to specify the exact version you would like to
load when working with test versions.
:::

### Dependency resolution

If one module depends on another one, both of these will be loaded. For example,
*StreamDevice* depends on *asyn*, so loading *StreamDevice* will automatically
load *asyn* as well. Dependencies are version-specific; *StreamDevice* 2.8.22 in
its current incarnation has been built against *asyn* 4.42.0---if you load that
version of *StreamDevice* then it will try to load specifically version 4.42.0
of *asyn*, and if it cannot find that version, or if another version of *asyn*
has already been loaded, then the IOC will exit with an error.

These dependencies are generated at build time and are stored in
`$(module)/$(version)/lib/$(T_A)/$(module).dep`. For example, the dependencies
for *StreamDevice* 2.8.22 are (directly from the aforementioned file):

```bash
# Generated file. Do not edit.
asyn 4.42.0+0
calc 3.7.4+1
pcre 8.44.0+0
```

The reader should be aware that *require* is limited in the degree to which it
can perform dependency resolution; all it can do is a simple check against
existing loaded versions. This is why build numbers are necessary. As an
example, consider the following scenario.

#### Example scenario

The module *sis8300llrf* version 3.16.1 depends on the module *scaling*, and has
been built against version 1.7.0. We update *scaling* to version 1.7.1. There is
no new version of *sis8300llrf*, but an IOC integrator would like to use the new
version of *scaling*. What should happen to the existing installed version of
*sis8300llrf*?

1. We could uninstall it and rebuild/install it against the new version of
   scaling. However, this prevents anyone who needs that version combination for
   any reason from being able to use it. In general, we want to avoid removing
   any installed modules---we should only add new versions.
2. We could try to update the version of *sis8300llrf* to 3.16.2 despite the
   fact that no changes have been made. If this is an ESS module, then this is
   possible, but not ideal. It is particularly bad if it is a module that is not
   being developed in-house, as our version will be out of sync with the
   community module.
3. We could instead update the version to 3.16.1+1, i.e. add a build number.
   This way, the existing version has not been modified. Moreover, you can use
   *sis8300llrf* version 3.16.1 with either version of scaling by specifying the
   build number.
