# 7. Understanding module dependence

## Lesson Overview

In this lesson, you will learn how to do the following:

* Understand the environment variables used to manage dependencies
* Understand how dependencies are determined at build-time
* Install a new module version with different dependencies
* Understand how incompatible dependencies can cause issues when loading an IOC

---

## Dependent environment variables

:::{note}
The versions of the modules mentioned below may be different that you will
see in your environment, because the e3 tool that installs the modules packs
gets the latest version of each module.
:::

One of the key ideas with e3 (arguably, *the* key idea) is the management of
dependencies of a given module in a common, structured way. That is, if a module
A depends on a module B, then you should only need to load A; module B should be
loaded and handled automatically (and so on, recursively). There are a few
pieces that manage this.

Begin by switching to `e3-stream/`. Run `make vars`, and look at the variables
`*DEP_VERSION` in the output:

```console
[iocuser@host:e3-stream]$ make vars | grep DEP_VERSION
ASYN_DEP_VERSION = 4.41.0
CALC_DEP_VERSION = 3.7.4
EXPORT_VARS = E3_MODULES_VENDOR_LIBS_LOCATION E3_MODULES_INSTALL_LOCATION_LIB TEMP_CELL_PATH EPICS_HOST_ARCH EPICS_BASE MSI E3_MODULE_NAME E3_MODULE_VERSION E3_SITEMODS_PATH E3_SITEAPPS_PATH E3_SITELIBS_PATH E3_REQUIRE_MAKEFILE_INPUT_OPTIONS E3_REQUIRE_NAME E3_REQUIRE_CONFIG E3_REQUIRE_DB E3_REQUIRE_LOCATION E3_REQUIRE_DBD E3_REQUIRE_VERSION E3_REQUIRE_TOOLS E3_REQUIRE_INC E3_REQUIRE_LIB E3_REQUIRE_BIN QUIET PCRE_DEP_VERSION CALC_DEP_VERSION ASYN_DEP_VERSION
PCRE_DEP_VERSION = 8.44.0
```

These variables are defined and used, respectively, in `configure/CONFIG_MODULE`
and `StreamDevice.Makefile`.

```console
[iocuser@host:e3-stream]$ cat configure/CONFIG_MODULE | grep DEP_VERSION
ASYN_DEP_VERSION:=4.41.0
PCRE_DEP_VERSION:=8.44.0
CALC_DEP_VERSION:=3.7.4
```

```console
[iocuser@host:e3-stream]$ cat StreamDevice.Makefile  | grep DEP_VERSION
ifneq ($(strip $(ASYN_DEP_VERSION)),)
asyn_VERSION=$(ASYN_DEP_VERSION)
ifneq ($(strip $(PCRE_DEP_VERSION)),)
pcre_VERSION=$(PCRE_DEP_VERSION)
ifneq ($(strip $(CALC_DEP_VERSION)),)
calc_VERSION=$(CALC_DEP_VERSION)
```

Let us see where these variables are used. Run `make build` and look for
(something like) the following in the output.

```console
make[4]: Entering directory `/home/simonrose/data/git/e3/modules/core/e3-stream/StreamDevice/O.7.0.5_linux-x86_64'
/usr/bin/gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE         -DUSE_TYPED_RSET            -D_X86_64_  -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration               -mtune=generic      -m64 -fPIC           -I. -I../src/ -I.././src/   -I/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0+0/include                -I/epics/base-7.0.5/require/3.4.1/siteMods/pcre/8.44.0+0/include            -I/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4+0/include  -I/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0+0/include                -I/epics/base-7.0.5/require/3.4.1/siteMods/pcre/8.44.0+0/include            -I/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4+0/include -I/epics/base-7.0.5/include  -I/epics/base-7.0.5/include/compiler/gcc -I/epics/base-7.0.5/include/os/Linux                           -c  .././src/StreamVersion.c
/usr/bin/g++  -D_GNU_SOURCE -D_DEFAULT_SOURCE         -DUSE_TYPED_RSET            -D_X86_64_  -DUNIX  -Dlinux             -MD   -O3 -g   -Wall         -std=c++11     -std=c++11  -mtune=generic               -m64 -fPIC          -I. -I../src/ -I.././src/   -I/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0+0/include                -I/epics/base-7.0.5/require/3.4.1/siteMods/pcre/8.44.0+0/include            -I/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4+0/include  -I/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0+0/include                -I/epics/base-7.0.5/require/3.4.1/siteMods/pcre/8.44.0+0/include            -I/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4+0/include -I/epics/base-7.0.5/include  -I/epics/base-7.0.5/include/compiler/gcc -I/epics/base-7.0.5/include/os/Linux                           -c  ../src/StreamFormatConverter.cc
/usr/bin/g++  -D_GNU_SOURCE -D_DEFAULT_SOURCE         -DUSE_TYPED_RSET            -D_X86_64_  -DUNIX  -Dlinux             -MD   -O3 -g   -Wall         -std=c++11     -std=c++11  -mtune=generic               -m64 -fPIC          -I. -I../src/ -I.././src/   -I/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0+0/include                -I/epics/base-7.0.5/require/3.4.1/siteMods/pcre/8.44.0+0/include            -I/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4+0/include  -I/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0+0/include                -I/epics/base-7.0.5/require/3.4.1/siteMods/pcre/8.44.0+0/include            -I/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4+0/include -I/epics/base-7.0.5/include  -I/epics/base-7.0.5/include/compiler/gcc -I/epics/base-7.0.5/include/os/Linux                           -c  ../src/StreamProtocol.cc
```

In particular, note the following segments:

```none
-I/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0/include
-I/epics/base-7.0.5/require/3.4.1/siteMods/pcre/8.44.0/include
-I/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4/include
```

These variables are used by the build system to locate the necessary header
files. To see this, let us clear the definition of `ASYN_DEP_VERSION` and re-run
the build.

```console
[iocuser@host:e3-stream]$ echo "ASYN_DEP_VERSION:=" > configure/CONFIG_MODULE.local
[iocuser@host:e3-stream]$ make clean
[iocuser@host:e3-stream]$ make build

# --- snip snip ---

/usr/bin/g++  -D_GNU_SOURCE -D_DEFAULT_SOURCE         -DUSE_TYPED_RSET            -D_X86_64_  -DUNIX  -Dlinux             -MD   -O3 -g   -Wall         -std=c++11     -std=c++11  -mtune=generic               -m64 -fPIC          -I. -I../src/ -I.././src/                   -I/epics/base-7.0.5/require/3.4.1/siteMods/pcre/8.44.0+0/include            -I/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4+0/include                  -I/epics/base-7.0.5/require/3.4.1/siteMods/pcre/8.44.0+0/include            -I/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4+0/include -I/epics/base-7.0.5/include  -I/epics/base-7.0.5/include/compiler/gcc -I/epics/base-7.0.5/include/os/Linux                           -c  ../src/AsynDriverInterface.cc
../src/AsynDriverInterface.cc:41:24: fatal error: asynDriver.h: No such file or directory
 #include "asynDriver.h"
                        ^
compilation terminated.
```

If you look at this output, you will find that
`-I/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0/include` now is missing.
At this point, the build system cannot find `asynDriver.h` (which is used in
`src/AsynDriverInterface.cc`). If you revert your changes and rebuild, then
everything should work correctly.

```console
[iocuser@host:e3-stream]$ rm configure/CONFIG_MODULE.local
[iocuser@host:e3-stream]$ make clean
[iocuser@host:e3-stream]$ make build
```

:::{admonition} Exercise
What is the purpose of creating the `CONFIG_MODULE.local` file? Why do we modify
`ASYN_DEP_VERSION` there instead of just modifying `CONFIG_MODULE`?
:::

## Updating a dependency

Suppose that for some reason (perhaps due critical bugs in an IOC or new
features that are released) we need to upgrade from *StreamDevice* 2.8.18 to
2.8.20. When updating a dependency, we also have to consider all of its
dependencies (*asyn*, *pcre*, and *calc* in this case), although we will focus
only on *asyn*.

We first need to check that *StreamDevice* is compatible with the current
version of *asyn*. It is often useful to check release notes in this case, but
it is not a given that every possible combination has been tried, and this may
require some testing on your part.

If the new version of *StreamDevice* and the old version of *asyn* are
compatible, then all you need to do is what was done in [Chapter
3](3_module_versions.md).

:::{note}
This assumes that the list of source files for *StreamDevice* have not changed.
If they have, you will have to modify `StreamDevice.Makefile` to account for any
new or removed source files.
:::

If the new version of *StreamDevice* is not compatible with *asyn*, then you
will need to install a new version of *asyn* in the current e3 environment. The
procedure for that is also the same as in [Chapter 3](3_module_versions.md). We
can start by checking the current version and seeing what is installed, and then
installing the necessary version (4.42.0)

```console
[iocuser@host:e3-asyn]$ make vars # Check the current version
[iocuser@host:e3-asyn]$ make existent
/epics/base-7.0.5/require/3.4.1/siteMods/asyn
`-- 4.41.0+0
    |-- asyn_meta.yaml
    |-- db
    |-- dbd
    |-- include
    `-- lib
[iocuser@host:e3-asyn]$ echo "EPICS_MODULE_TAG:=tags/R4-42" > configure/CONFIG_MODULE.local
[iocuser@host:e3-asyn]$ echo "E3_MODULE_VERSION:=4.42.0" >> configure/CONFIG_MODULE.local
[iocuser@host:e3-asyn]$ make vars
[iocuser@host:e3-asyn]$ make init patch build install # You can do these all at once
[iocuser@host:e3-asyn]$ make existent
/epics/base-7.0.5/require/3.4.1/siteMods/asyn
|-- 4.41.0+0
|   |-- asyn_meta.yaml
|   |-- db
|   |-- dbd
|   |-- include
|   `-- lib
`-- 4.42.0+0
    |-- asyn_meta.yaml
    |-- db
    |-- dbd
    |-- include
    `-- lib
```

:::{note}
Between *asyn* 4-41 and 4-42 there actually are some source and `.dbd` files
that have been added; if this functionality is necessary for your purposes,
then you will have to add

```make
SOURCES += drvPrologixGPIB.c
DBDS += drvPrologixGPIB.dbd
```

to `asyn.Makefile`.
:::

This will now allow us to update *StreamDevice*'s dependencies and install it
properly. Save the following as `CONFIG_MODULE.local` in `e3-stream/configure/`:

```make
EPICS_MODULE_TAG:=master
E3_MODULE_VERSION:=e3training
ASYN_DEP_VERSION:=4.42.0
```

and then run

```console
[iocuser@host:e3-stream]$ make vars # Again, a good sanity check
[iocuser@host:e3-stream]$ make init patch build install
[iocuser@host:e3-stream]$ make existent
/epics/base-7.0.5/require/3.4.1/siteMods/stream
|-- 2.8.18+0
|   |-- dbd
|   |-- include
|   |-- lib
|   |-- SetSerialPort.iocsh
|   `-- stream_meta.yaml
`-- e3training
    |-- dbd
    |-- include
    |-- lib
    |-- SetSerialPort.iocsh
    `-- stream_meta.yaml
```

Once you have installed a module, it is always a good idea to test that it can
be loaded; this is a minimal test that a module must pass! You can do this by
running any of the following:

```console
[iocuser@host:~]$ iocsh.bash -r stream,2.8.18
[iocuser@host:~]$ iocsh.bash -r stream,e3training
[iocuser@host:~]$ iocsh.bash -r stream
```

:::{admonition} Exercises

* Which version does the last one load, and why?
* Which version of *asyn* is loaded in each case?
* What happens if you run either of the following?

  ```console
  [iocuser@host:~]$ iocsh.bash -r stream -r asyn
  [iocuser@host:~]$ iocsh.bash -r asyn -r stream
  ```

  Can you explain the result?
* Where is the dependency information stored in the installed module?

:::

## Dependency resolution limitations

*require* is not perfect when it comes to dependency resolution. Consider the
following file:

```console
[iocuser@host:~]$ cat /epics/base-7.0.5/require/3.4.1/siteMods/stream/2.8.18+0/lib/linux-x86_64/stream.dep
# Generated file. Do not edit.
asyn 4.41.0+0
calc 3.7.4+0
pcre 8.44.0+0
```

This file is generated at build time, and lists the modules and versions that
*StreamDevice* depends on. *require* will attempt to load these modules (and
versions) when `require stream` occurs during IOC startup. In that sense,
*require* does not so much *resolve* dependencies as it does load them.

If there are any conflicts in this process, then *require* will shut the IOC
down. This is what happens when you run `iocsh.bash -r asyn -r stream` above:
since no version is specified for *asyn*, the latest version (4.42.0) is loaded.
Then when *StreamDevice* is loaded, it depends on *asyn* 4.41.0. The loaded
version of *asyn* and the requested version of *asyn* differ, so *require* shuts
the IOC down.

This is a sneak-preview of so-called *dependency hell*; in this case, the
solution is simple. Since *asyn* is only really being loaded due to
*StreamDevice*'s dependency, the solution is to only load *StreamDevice*
directly and let it take care of loading the correct version of *asyn*. However,
what happens if you need to use *StreamDevice*, which depends on *asyn* 4.42.0,
and a version of *modbus* which depends on a different version of *asyn*?

In general the best practice when writing a startup script for an IOC is only to
require the top-level modules. So instead of

```bash
require asyn
require sequencer
require sscan
require calc
require stream
```

it is much simpler to have

```bash
require stream
```

The resulting startup script will be much more maintainable over time and less
prone to errors when new module versions are installed.

:::{admonition} Exercise
Suppose that your IOC starts fine today with the startup script

```bash
require asyn
require stream
```

What simple and reasonable action could you take that would cause this IOC to
fail on startup without changing this script? Why is this a problem from the
perspective of the maintainer of a shared e3 environment?
:::

## Whence cometh the dependencies

We have so far only discussed the *build-time dependencies*. These are
dependencies that arise when compiling a module, indicated by the inclusion of a
`C/C++` header file: consider the file `AsynDriverInterface.cc` from
*StreamDevice*

```c
// --- snip --

#include "asynDriver.h"
#include "asynOctet.h"
#include "asynInt32.h"
#include "asynUInt32Digital.h"
#include "asynGpibDriver.h"

// --- snip ---
```

When this file is compiled, it generates a `.d` file that describes the
dependencies recognized by `make`:

```console
[iocuser@host:e3-stream]$ cat StreamDevice/O.7.0.5_linux-x86_64/AsynDriverInterface.d
AsynDriverInterface.o: ../src/AsynDriverInterface.cc \
# --- snip ---
 /epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.42.0+0/include/asynAPI.h \
 /epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.42.0+0/include/asynOctet.h \
 /epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.42.0+0/include/asynInt32.h \
 /epics/base-7.0.5/include/epicsTypes.h \
 /epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.42.0+0/include/asynUInt32Digital.h \
 /epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.42.0+0/include/asynGpibDriver.h \
 /epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.42.0+0/include/asynDriver.h \
 /epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.42.0+0/include/asynInt32.h \
```

*require* uses this file to detect build-time dependencies.

:::{admonition} Exercise
Similar to *asyn*, there are header files from *calc* and *pcre* that are
included which result in them being build-time dependencies. Determine which
files include header files from both *calc* and *pcre*.
:::

## Assignment

There is another kind of dependency, the *run-time dependency*. This is often
associated with dependencies such as *StreamDevice* where the dependency is
based on run-time functionality as connoted by the existence of `.proto`
(protocol) files. For example, consider the e3 module for communicating with a
[FuG power supply](https://gitlab.esss.lu.se/e3/wrappers/ps/e3-fug): if you look
at the [underlying module](https://gitlab.esss.lu.se/epics-modules/fug), you can
see that it includes such a protocol file,
[fug.proto](https://gitlab.esss.lu.se/epics-modules/fug/-/tree/master/fugApp/Db).

1. Clone the e3 wrapper above, and build and install it. Alternatively, `e3-fug`
   is included in one of the groups that can be installed with `e3.bash`.

   * Which group is it?
   * What are the advantages of installing it as a group versus as a single module?

2. Look through temporary build files. Can you see where *stream* is referenced
   there?
3. How did `e3-fug` know that *StreamDevice* is a dependency? Hint: The
   configuration files are only part of the story.
