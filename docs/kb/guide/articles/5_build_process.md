(require_build)=

# Article: The build process with *require* (In-depth; advanced)

The e3 build process is a complicated bit of work. To recap, the overview is as follows:

1. In the e3-wrapper directory: we collect some information and decide what
   build process we will perform (from `RULES_E3`), calling `make` in the module
   directory with information passed as in `CONFIG_E3_MAKEFILE`.
2. In the module directory: `EPICSVERSION` has not been defined, so determine
   which versions to build for.
3. In the module directory: Target architecture `${T_A}` has not been defined,
   so determine the architectures to build for.
4. In the module directory: Perform a final collection of the relevant files,
   create the directories `O.${EPICSVERSION}_Common` and
   `O.${EPICSVERSION}_${T_A}`.
5. In the directories `O.*`: Build/Install all of the required shared libraries
   and other files for the given version of EPICS base and target architecture.

We will go over each of these steps in more detail, as well as go over an
example build to explain how information is collected and used by the build
process.

## Some details about `make`

Before we can describe the build process, we have to talk a little about how
`make` works. If you do not understand `make`, it is very *very* hard to
understand the e3 build process. For a reference, I can suggest [GNU make
reference](https://www.gnu.org/software/make/manual/html_node/index.html).

In short, `make` does two things:

1. It provides a framework to describe the tree structure of dependencies of a
   given project
2. It provides a way to give instructions how to build those dependencies if
   they are missing or out of date

These are built up of instructions that look like

```makefile
VARIABLE = value

target: dependency
    #actions
    echo $(VARIABLE)
```

If you ran the command `make target` it would check first that `dependency` is
up-to-date (i.e. newer than `target`), and if it is, it would run the commands
below.

```bash
$ make target
echo value
value
```

The key is in how `make` generates its dependency tree. Unlike many programming
languages (of which `make` is... not necessarily one?), `make` is decidedly
non-procedural: since lines are not evaluated and actions are not performed in a
linear order, it can be very difficult to trace exactly how a variable has
obtained its value, or why certain actions have been performed.

## The `make` process for e3

### Stage 1: The e3-wrapper

We start in the e3-wrapper directory, and run (for example) `make build`. The
first thing that happens is that we load the makefiles from the configure
directory; these in turn load `CONFIG_MODULE` and `RELEASE` which specify
dependencies and for which version of EPICS base and *require* we are building,
as well as `CONFIG` from the *require* module (located in
`configure/modules/CONFIG` in this repository).

We also load `RULES` which similarly loads a number of rules-related configure
files installed with `require`. The most important one in `RULES_E3` which
initiates most of the e3 build process. As an example, we have:

```makefile
## Build the EPICS Module : $(E3_MODULE_NAME)
# Build always the Module with the EPICS_MODULES_TAG
build: conf checkout
    $(QUIET) $(E3_MODULE_MAKE_CMDS) build
```

which first makes sure that `conf` and `checkout` are up to date (these copy the
`$(module).Makefile` into the module directory, and run a `git checkout` command
to make sure that the module is up-to-date). Note that `$(E3_MODULE_MAKE_CMDS)`
is defined in `CONFIG_E3_MAKEFILE` which specifies which arguments should be
passed to this recursive call of `make`.

### Stage 2: Defining `EPICSVERSION`

The first pass through is to determine the EPICS version that we are building
for. In e3, we build for one version at a time; this is taken from
`EPICS_LOCATION`:

```makefile
E3_EPICS_VERSION:=$(patsubst base-%,%,$(notdir $(EPICS_LOCATION)))
BUILD_EPICS_VERSIONS = $(E3_EPICS_VERSION)

# snip snip

build install debug:: ${IGNOREFILES}
    @+for VERSION in ${BUILD_EPICS_VERSIONS}; do ${MAKEVERSION} EPICSVERSION=$$VERSION $@; done
```

`EPICS_LOCATION` is defined in `CONFIG_E3_MAKEFILE` to be the same as
`EPICS_BASE` from the module configuration. That is, if `EPICS_BASE` is
specified to be `/home/iocuser/epics/base-7.0.6.1`, then the above code will run
the next stage of the build process once with `EPICSVERSION=7.0.6.1`.

Note that `build`, `install`, and `debug` all use the same recursive call to
`make`.

### Stage 3: Defining `T_A`

Now that we know which version of EPICS to build for, we go on to determine the
target architectures to build for. In this case, we may build for more than one
architecture at a time; at the moment, ESS supports `linux-x86_64`,
`linux-corei7-poky`, and `linux-ppc64e6500`. This is also where we include the
EPICS build rules: see the sequence

```makefile
EB:=${EPICS_BASE}
-include ${CONFIG}/CONFIG
EPICS_BASE:=${EB}
```

(The redefinition of `EPICS_BASE` is due to the fact that it is overwritten in
`CONFIG_SITE` from EPICS base)

This is also the place where we start collecting information about what to build
and install. For example, to begin collecting the source files to compile, we
have the following section:

```makefile
AUTOSRCS := $(filter-out ~%,$(wildcard *.c *.cc *.cpp *.st *.stt *.gt))
SRCS = $(if ${SOURCES},$(filter-out -none-,${SOURCES}),${AUTOSRCS})
export SRCS
```

Note in particular the `export SRCS` line: when make is called recursively,
variables from one run to the next do not persist unless they are `export`ed. It
is also extremely important to note when the variable being exported is
expanded: this happens right before the next iteration of recursive `make` is
called, so even if `SOURCES` will only be defined later (as is the case with the
e3 build process), it will `export` correctly.

The cross-compiler target architectures `CROSS_COMPILER_TARGET_ARCHS` are
defined in `$(EPICS_LOCATION)/configure/CONFIG_SITE`, which is generated when
you build EPICS base for the first time.

The next stage of the build is triggered by

```makefile
# Loop over all architectures.
install build debug::
    @+for ARCH in ${CROSS_COMPILER_TARGET_ARCHS}; do \
        umask 002; echo MAKING ARCH $$ARCH; ${MAKE} -f ${USERMAKEFILE} T_A=$$ARCH $@; \
    done
```

### Stage 4: Preparing to build `T_A`

For this stage of the build process, we are still in the module directory; the
next stages will be done in the directories `O.$(EPICSVERSION)_Common` or
`O.$(EPICSVERSION)_$(T_A)`, respectively. These directories will also be created
at this point, and are the destination of all intermediate and final output
files (e.g. any generated `.db` or `.dbd` files, `.o` files, and
`lib$(module).so`)

Note that `make clean` simply deletes these directories, removing all generated
files.

We make a final collection of what objects we should build, and a final
gathering of information:

```makefile
# Add sources for specific epics types or architectures.
ARCH_PARTS = ${T_A} $(subst -, ,${T_A}) ${OS_CLASS}
VAR_EXTENSIONS = ${EPICSVERSION} ${ARCH_PARTS} ${ARCH_PARTS:%=${EPICSVERSION}_%}
export VAR_EXTENSIONS
```

allows the developer to have architecture-specific files: for example, if `T_A =
linux-x86_64` then `ARCH_PARTS` will be `linux-x86_64 linux x86_64`: If we now
consider the next segment, we see

```makefile
REQ = ${REQUIRED} $(foreach x, ${VAR_EXTENSIONS}, ${REQUIRED_$x})
export REQ

SRCS += $(foreach x, ${VAR_EXTENSIONS}, ${SOURCES_$x})
USR_LIBOBJS += ${LIBOBJS} $(foreach x,${VAR_EXTENSIONS},${LIBOBJS_$x})
export USR_LIBOBJS
```

which tells us that we can have `REQUIRED_linux` or `SOURCES_x86_64` (or another
other part of `VAR_EXTENSIONS`) to selectively compile code or manage
dependencies based on architecture and version.

Finally, we run

```makefile
install build debug:: O.${EPICSVERSION}_Common O.${EPICSVERSION}_${T_A}
    @${MAKE} -C O.${EPICSVERSION}_${T_A} -f ../${USERMAKEFILE} $@
```

Note that due to the argument `-C O.${EPICSVERSION}_${T_A}` we switch to that
directory, using the same `${USERMAKEFILE}` to manage the build process.

### Stage 5: Building `T_A`

We have now collected the majority of the information that we need to build our
module. We will do a little more organisation and preparation, and then the
process will be handed over to the EPICS build system. Note that this part of
`driver.makefile` is by far the most complicated section, and takes some time to
digest.

To begin with, I would like to point out a couple sections of interest, followed
by tracing through what happens when you include a line such as `SOURCES +=
file.c` in your `$(module).Makefile`.

<!--
## Points of interest
FIXME (alo): leaving it here just in case, simonrose
-->

## Examples of the `make` process

We will provide a few examples of how `make` processes the data and produces the
desired result. The first is installing a header file, and the second is
actually compiling a source file.

### Installing a header file

Before we go on to the more complicated case of compiling source files, let us
go over the simpler step of having header files be installed so that other
modules may include them. As an example, there are many `.h` files that are
installed with *asyn* and are used by lots of other modules.

The simplest way of including a header file is to add the line `HEADERS +=
header.h` into your `$(module).Makefile`. Having done this, the build/install
process runs as follows.

1. In stage 3 we start with the following:

   ```makefile
   HDRS = ${HEADERS} $(addprefix ${COMMON_DIR}/,$(addsuffix Record.h,${RECORDS}))
   HDRS += ${HEADERS_${EPICSVERSION}}
   export HDRS
   ```

   which passes these on to the variable `HDRS` (as well as collecting a few
   other headers, including version-specific ones if necessary)

2. There is only one place in the build process that these are relevant: in
   stage 5 (within the directory `O.${EPICSVERSION}_{T_A}`) we have the
   following line:

   ```makefile
   SRC_INCLUDES = $(addprefix -I, $(wildcard $(foreach d,$(call uniq, $(filter-out /%,$(dir ${SRCS:%=../%} ${HDRS:%=../%}))), $d $(addprefix $d/, os/${OS_CLASS} $(POSIX_$(POSIX)) os/default))))
   ```

   or, simplified:

   ```makefile
   SRC_INCLUDES = $(addprefix -I, $(wildcard $(call uniq, $(filter-out /%,$(dir ${HDRS:%=../%})))))
   ```

   which adds the directory that the header files are located in to the search
   path for include files when compiling.

3. The next time the headers come up is during the install process, and are
   governed by the following:

   ```makefile
   vpath %.h $(addprefix ../,$(sort $(dir $(filter-out /%,${HDRS}) ${SRCS}))) $(sort $(dir $(filter /%,${HDRS})))
   # snip
   INSTALL_HDRS = $(addprefix ${INSTALL_INCLUDE}/,$(notdir ${HDRS}))
   # snip
   INSTALLS += ... ${INSTALL_HDRS} ...

   install: ${INSTALLS}
   ```

   and the following from EPICS base `RULES_BUILD`:

   ```makefile
   $(INSTALL_INCLUDE)/%: %
        $(ECHO) "Installing generic include file $@"
        @$(INSTALL) -d -m $(INSTALL_PERMISSIONS) $< $(@D)
   ```

   which says that any target within the directory `$(INSTALL_INCLUDE)` has the
   target as a dependency, i.e. `$(INSTALL_INCLUDE)/header.h` depends on
   `header.h`

4. Finally, the `vpath` line above tells `make` where to search for that file,
   and then the instructions tell `make` to run the program defined by
   `$(INSTALL)` to install the file in the target location. Note however that
   there is one potential source of problems here: the dependency is just the
   filename alone, and so if you have the following two header files you would
   like to include: `dir1/header.h` `dir2/header.h` i.e. the same filename, but
   different locations, then only one of these two will be installed.

   We have implemented a mechanism to get around this, please see the
   [changelog](https://gitlab.esss.lu.se/e3/e3-require/-/blob/master/CHANGELOG.md)
   for *require* 3.3.0.

### Compiling a `.c` file

Building source files at its heart is similar to the above, but the chain of
dependencies is significantly more complicated. As above however, the inclusion
of a source file to be compiled into the shared library is simple: add the line
`SOURCES += $(APPSRC)/file.c` in your module makefile.

The next steps are complicated due to being shared among different configure
files.

1. Initially in stage 3 above, we have the line `SRCS += $(if
   ${SOURCES},$(filter-out -none-,${SOURCES}),${AUTOSRCS})` which includes your
   file in the variable `SRCS`.

2. In the EPICS base configure file `CONFIG_COMMON`, we have the following two
   directives:

   ```makefile
   SRC_FILES = $(LIB_SRCS) $(LIBSRCS) $(SRCS) $(USR_SRCS) $(PROD_SRCS) $(TARGET_SRCS)
   HDEPENDS_FILES = $(addsuffix $(DEP),$(notdir $(basename $(SRC_FILES))))
   ```

   which converts `$(APPSRC)/file.c` into `file.d` in the variable
   `HDEPENDS_FILES`.

3. Next in stage 5, we include `RULES` from EPICS base which includes
   `RULES_BUILD`. This includes the following:

   ```makefile
   -include $(HDEPENDS_FILES)
   ```

   which seems quite innocuous, but it is a surprisingly important line: `make`,
   when trying to include a file, will first see if it exists, and if it does
   not, then it will see if it can generate that file. In this case, we have the
   rule

   ```makefile
   %$(DEP):%.c
       @$(RM) $@
       $(HDEPENDS.c) $<
   ```

   which provides a rule to create `file.d` from `file.c`: this runs (once
   again, from `CONFIG_COMMON`):

   ```makefile
   HDEPENDS_COMP.c   = $(COMPILE.c) $(HDEPENDS_COMPFLAGS) $(HDEPENDS_ARCHFLAGS)
   ```

   i.e. it compiles the source file with a special flag that produces not only
   `file.o`, but a dependency file `file.d`.

   To wit, on our first pass through in stage 5 we compile all of our source
   files to produce object files and dependency files.

4. We now need to connect the source files to the final shared library. The
   first step is the following from

   `driver.makefile`:

   ```makefile
   LIBRARY_OBJS = $(strip ${LIBOBJS} $(foreach l,${USR_LIBOBJS},$(addprefix ../,$(filter-out /%,$l))$(filter /%,$l)))

   LIBOBJS += $(addsuffix $(OBJ),$(notdir $(basename $(filter-out %.$(OBJ) %$(LIB_SUFFIX),$(sort ${SRCS})))))
   ```

   which adds `file.o` to `LIBRARY_OBJS`.

5. Next, we look at `LOADABLE_SHRLIBNAME`: roughly speaking, if you end up with
   a non-empty `LIBRARY_OBJS` (as we have above), then this will be
   `lib${PRJ}.so`. In particular, we obtain from `RULES_BUILD` the dependency
   and build rules:

   ```makefile
   $(LOADABLE_SHRLIBNAME): $(LIBRARY_OBJS) $(LIBRARY_RESS) $(SHRLIB_DEPLIBS)

   $(LOADABLE_SHRLIBNAME): $(LOADABLE_SHRLIB_PREFIX)%$(LOADABLE_SHRLIB_SUFFIX):
       @$(RM) $@
       $(LINK.shrlib)
       $(MT_DLL_COMMAND)
   ```

   where the linking command is provided in `CONFIG.Common.UnixCommon`:

   ```makefile
   LINK.shrlib = $(CCC) -o $@ $(TARGET_LIB_LDFLAGS) $(SHRLIBDIR_LDFLAGS) $(LDFLAGS)
   LINK.shrlib += $(LIB_LDFLAGS) $(LIBRARY_LD_OBJS) $(LIBRARY_LD_RESS) $(SHRLIB_LDLIBS)
   ```

6. Last but not least, we need to connect this to the target `build`. In
   `RULES_BUILD` we find:

   ```makefile
   LIBTARGETS += $(LIBNAME) $(INSTALL_LIBS) $(TESTLIBNAME) \
       $(SHRLIBNAME) $(INSTALL_SHRLIBS) $(TESTSHRLIBNAME) \
       $(DLLSTUB_LIBNAME) $(INSTALL_DLLSTUB_LIBS) $(TESTDLLSTUB_LIBNAME) \
       $(LOADABLE_SHRLIBNAME) $(INSTALL_LOADABLE_SHRLIBS)

   # snip snip
   build: $(OBJSNAME) $(LIBTARGETS) $(PRODTARGETS) $(TESTPRODTARGETS) \
       $(TARGETS) $(TESTSCRIPTS) $(INSTALL_LIB_INSTALLS)
   ```

   and in particular, that `build` depends on `$(LOADABLE_SHRLIBNAME)`.

7. Putting this all together, we have the following chain of dependencies:

   ```none
   build -> $(LOADABLE_SHRLIBNAME) -> $(LIBRARY_OBJS)
   ```

   where that last target includes `file.o`.

8. The magic now comes from the fact that we have already built this file back
   when we were creating `file.d`! As such, we can run the linking command, and
   we obtain our shared library, ready to install.
