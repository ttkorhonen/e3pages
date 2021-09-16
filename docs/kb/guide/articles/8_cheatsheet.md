# Article: e3 Makefile Cheatsheet

## Module makefile cheatsheet

The `<module>.Makefile` that is used to build an e3 module has a number of standard variables that are used to direct the build process. The main variables that are relevant are the following. For more detail, see {ref}`makefile_variables`.

The first variables define what to build and install with the module.
* `SOURCES` - Source files to compile into the shared library
* `DBDS` - Database definition (`.dbd`) files to include in `$(module).dbd`
* `HEADERS` - Header files that should be installed with the module
* `TEMPLATES` - Database or template files that should be installed in the `$(module_DB)` path
* `SCRIPTS` - Script files that are installed in `$(module_DIR)`
* `BINS` - Programs to install in `$(module_DIR)/bin/$(T_A)`

The following variables affect which architectures are built.
* `EXCLUDE_ARCHS` - Architectures to skip
* `ARCH_FILTER` - Architectures to restrict build to

The following variables are related to module dependencies.
* `<module>_VERSION` - This defines which version of a dependent module to link or compile against. This should be specified with the boilerplate
  ```make
  ifneq ($(strip <MODULE>_DEP_VERSION),)
  <module>_VERSION:=$(<MODULE>_DEP_VERSION)
  endif
  ```
  and `<MODULE>_DEP_VERSION` should be defined in `configure/CONFIG_MODULE`.
* `REQUIRED` - This is used to specify any non source-based dependencies. *StreamDevice* is perhaps the most common such dependency.

There are also the following variables/macros of interest
* `KEEP_HEADER_SUBDIRS` - On the odd chance that you want to preserve the structure of your header files (for example, if you have any inclues that are expected to be of the form `#include "some_directory/some_header.h"`), then this will install the header files while keeping the subdirectory structure.
* `FETCH_BUILD_NUMBER` - This is useful if you need to refer to specific module path, but you do not care which build number. For example, if you want to include a particular path from another module for database expansion, you might include something like
  ```make
  USR_DBFLAGS += -I$(E3_SITEMODS_PATH)/<other_module>$(call FETCH_BUILD_NUMBER,$(E3_SITEMODS_PATH),<other_module>/db)
  ```
  which will set the inclue path that is passed to `MSI` correctly.
