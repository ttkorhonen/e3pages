# Article: e3 Makefile Cheatsheet


(makefile_vars_cheatsheet)=
## Module makefile variables cheatsheet

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
  ```makefile
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

## Configuring the cell path

By default, the cell path for running `cellinstall` (and all of its friends) is `$(TOP)/cellMods`, where `$(TOP)` is the current module wrapper path. This can be configured either by adding the line
```makefile
E3_CELL_PATH:=/absolute/path/to/new/cellMods
```
to either `configure/CONFIG_CELL.local` or to a `CONFIG_CELL.local` file one directory up from the wrapper directory. Note that the path listed in the configure file must be absolute.

## Database inflation

In *require* version `3.4.1` and earlier, it was necessary to have the target `db` specified in the module makefile (this is triggered by the `db` rule in `configure/module/RULES_MODULE`, and is a dependency of `install`). This allows for database expansion to occur at install time.

The default rule that is added by the cookiecutter recipe is
```makefile
.PHONY: db
db: $(SUBS) $(TMPS)

.PHONY: $(SUBS)
$(SUBS):
	@printf "Inflating database ... %44s >>> %40s \n" "$@" "$(basename $(@)).db"
	@rm -f  $(basename $(@)).db.d  $(basename $(@)).db
	@$(MSI) -D $(USR_DBFLAGS) -o $(basename $(@)).db -S $@ > $(basename $(@)).db.d
	@$(MSI)    $(USR_DBFLAGS) -o $(basename $(@)).db -S $@

.PHONY: $(TMPS)
$(TMPS):
	@printf "Inflating database ... %44s >>> %40s \n" "$@" "$(basename $(@)).db"
	@rm -f  $(basename $(@)).db.d  $(basename $(@)).db
	@$(MSI) -D $(USR_DBFLAGS) -o $(basename $(@)).db $@  > $(basename $(@)).db.d
	@$(MSI)    $(USR_DBFLAGS) -o $(basename $(@)).db $@
```
If you do not have any `.template` or `.substitutions` files that you will expand at install time, then all of this can be replace by
```makefile
.PHONY: db
db:
```

## Prebuild target

In case you need to have any tasks run *before* the build process, there is a `prebuild` target that runs before the build. For example, if you need to have some external utility compiled before the build happens (perhaps in order to install it using `BINS` as described in {ref}`makefile_vars_cheatsheet`), then you can use `prebuild`:
```makefile
prebuild:
    # some tasks to perform before build
    echo "What a wonderful prebuild task"
```
Note that this will be run each time before the build phase.