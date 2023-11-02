# Article: e3 Cheatsheet

## What to build and install

* `SOURCES` - Source files to compile into the shared library
* `DBDS` - Database definition (`.dbd`) files to include in `$(module).dbd`
* `HEADERS` - Header files that should be installed with the module
* `TEMPLATES` - Database or template files that should be installed in the
  `$(module_DB)` path
* `TMPS` - Templates files to inflate to db-file and install in in the
  `$(module_DB)` path
* `SUBS` - Substitutions files to inflate the template file to db-file and
  install in the `$(module_DB)` path
* `SCRIPTS` - Script files that are installed in `$(module_DIR)`
* `BINS` - Programs to install in `$(module_DIR)/bin/$(T_A)`
* `VENDOR_LIBS` - Vendor libraries that are installed in
  `$(module_DIR)/lib/$(T_A)/vendor`

## What architectures to build

* `EXCLUDE_ARCHS` - Architectures to skip

## Module dependencies

* `<module>_VERSION` - Which version of a dependent module to link or compile
  against
* `REQUIRED` - Specifies any non source-based dependencies

## Other macros

* `KEEP_HEADER_SUBDIRS` - Preserves the tree structure of the given header
  directories
* `FETCH_BUILD_NUMBER` - Lets you find the correct revision number for a module
