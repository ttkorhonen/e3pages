# Article: e3 Cheatsheet


## What to build and install

* `SOURCES` - Source files to compile into the shared library
* `DBDS` - Database definition (`.dbd`) files to include in `$(module).dbd`
* `HEADERS` - Header files that should be installed with the module
* `TEMPLATES` - Database or template files that should be installed in the `$(module_DB)` path
* `SCRIPTS` - Script files that are installed in `$(module_DIR)`
* `BINS` - Programs to install in `$(module_DIR)/bin/$(T_A)`

## What architectures to build

* `EXCLUDE_ARCHS` - Architectures to skip
* `ARCH_FILTER` - Architectures to restrict build to

## Module dependencies

* `<module>_VERSION` - Which version of a dependent module to link or compile against
* `REQUIRED` - Specifies any non source-based dependencies

## Other macros

* `KEEP_HEADER_SUBDIRS` - Preserves the tree structure of the given header directories
* `FETCH_BUILD_NUMBER` - Lets you find the correct build number for a module

## e3 build targets

* `init` - Initialises the EPICS submodule
* `patch` - Applies any version-specific patches
* `build` - Builds the module
* `install` - Installs the module
* `clean` - Removes temporary build files
* `test` - Runs basic test as well as any user-specified tests
* `cellinstall` - Installs locally at `$(E3_CELL_PATH)`
* `debug` - Prints out build variables
* `existent` - Shows the versions that are installed
* `vars` - Prints environment variables

## custom build targets

* `prebuild` - Runs a set of commands before each build
* `module_tests` - User-defined tests that run as a part of `make test`
