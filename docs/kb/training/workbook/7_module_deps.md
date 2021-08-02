# Understanding module dependence

## Lesson Overview

In this lesson, you'll learn how to do the following:

* Understand which e3 environment variables that define module dependency.
* Understand the dependency chain during module building.
* Change dependency versions when a module needs to be recompiled.
* Make more informed decisions when deciding on module versions.

---

## Dependent environment variables

One of the key ideas with e3 (arguably, *the* key idea) is the manage dependencies of a given module in a common, structured way. That is,
if a module A depends on a module B, then you should only need to load A; module B should be loaded and handled automatically (and so on, 
recursively). There are a few pieces that manage this.

Begin by switching to `e3-stream/`. Run `make vars`, and look at the variables `*_DEP_VERSION` in the output:
```console
[iocuser@host:e3-stream]$ make vars | grep DEP_VERSION
ASYN_DEP_VERSION = 4.41.0
CALC_DEP_VERSION = 3.7.4
EXPORT_VARS = E3_MODULES_VENDOR_LIBS_LOCATION E3_MODULES_INSTALL_LOCATION_LIB TEMP_CELL_PATH EPICS_HOST_ARCH EPICS_BASE MSI E3_MODULE_NAME E3_MODULE_VERSION E3_SITEMODS_PATH E3_SITEAPPS_PATH E3_SITELIBS_PATH E3_REQUIRE_MAKEFILE_INPUT_OPTIONS E3_REQUIRE_NAME E3_REQUIRE_CONFIG E3_REQUIRE_DB E3_REQUIRE_LOCATION E3_REQUIRE_DBD E3_REQUIRE_VERSION E3_REQUIRE_TOOLS E3_REQUIRE_INC E3_REQUIRE_LIB E3_REQUIRE_BIN QUIET PCRE_DEP_VERSION CALC_DEP_VERSION ASYN_DEP_VERSION  
PCRE_DEP_VERSION = 8.44.0
```

These variables are defined and used, respectively, in `configure/CONFIG_MODULE` and `StreamDevice.Makefile`.

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

Let's see where these variables are used. Run `make build` and look for (something like) the following in the output.

```bash
make[4]: Entering directory `/home/simonrose/data/git/e3/modules/core/e3-stream/StreamDevice/O.7.0.5_linux-x86_64'
/usr/bin/gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE         -DUSE_TYPED_RSET            -D_X86_64_  -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration               -mtune=generic      -m64 -fPIC           -I. -I../src/ -I.././src/   -I/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0+0/include                -I/epics/base-7.0.5/require/3.4.1/siteMods/pcre/8.44.0+0/include            -I/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4+0/include  -I/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0+0/include                -I/epics/base-7.0.5/require/3.4.1/siteMods/pcre/8.44.0+0/include            -I/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4+0/include -I/epics/base-7.0.5/include  -I/epics/base-7.0.5/include/compiler/gcc -I/epics/base-7.0.5/include/os/Linux                           -c  .././src/StreamVersion.c
/usr/bin/g++  -D_GNU_SOURCE -D_DEFAULT_SOURCE         -DUSE_TYPED_RSET            -D_X86_64_  -DUNIX  -Dlinux             -MD   -O3 -g   -Wall         -std=c++11     -std=c++11  -mtune=generic               -m64 -fPIC          -I. -I../src/ -I.././src/   -I/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0+0/include                -I/epics/base-7.0.5/require/3.4.1/siteMods/pcre/8.44.0+0/include            -I/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4+0/include  -I/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0+0/include                -I/epics/base-7.0.5/require/3.4.1/siteMods/pcre/8.44.0+0/include            -I/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4+0/include -I/epics/base-7.0.5/include  -I/epics/base-7.0.5/include/compiler/gcc -I/epics/base-7.0.5/include/os/Linux                           -c  ../src/StreamFormatConverter.cc
/usr/bin/g++  -D_GNU_SOURCE -D_DEFAULT_SOURCE         -DUSE_TYPED_RSET            -D_X86_64_  -DUNIX  -Dlinux             -MD   -O3 -g   -Wall         -std=c++11     -std=c++11  -mtune=generic               -m64 -fPIC          -I. -I../src/ -I.././src/   -I/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0+0/include                -I/epics/base-7.0.5/require/3.4.1/siteMods/pcre/8.44.0+0/include            -I/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4+0/include  -I/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0+0/include                -I/epics/base-7.0.5/require/3.4.1/siteMods/pcre/8.44.0+0/include            -I/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4+0/include -I/epics/base-7.0.5/include  -I/epics/base-7.0.5/include/compiler/gcc -I/epics/base-7.0.5/include/os/Linux                           -c  ../src/StreamProtocol.cc
```

In particular, note the following segments:

```
-I/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0/include
-I/epics/base-7.0.5/require/3.4.1/siteMods/pcre/8.44.0/include
-I/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4/include
```

These variables are used by the build system to locate the necessary header files. To see this, let us clear the definition of `ASYN_DEP_VERSION` and re-run the build.

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

If you look at this output, you'll find that `-I/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0/include` now is missing. At this point, the build system cannot find `asynDriver.h` (which is used in `src/AsynDriverInterface.cc`). If you revert your changes and rebuild, then everything should work correctly.

```console
[iocuser@host:e3-stream]$ rm configure/CONFIG_MODULE.local
[iocuser@host:e3-stream]$ make clean
[iocuser@host:e3-stream]$ make build
```

Exercise:
* What is the purpose of creating the `CONFIG_MODULE.local` file? Why do we modify `ASYN_DEP_VERSION` there instead of just modifying `CONFIG_MODULE`?

## New dependency module

If we postulate that we (due to new requirements or critical bugs in an existent IOC) need to swap from *StreamDevice* version `2.7.14p` to `2.8.4`, we have to consider two dependency modules (*asyn* and *pcre*). Here, for the sake of brevity, we will only consider the *asyn* dependence. Before swapping, we need to consider if the existing *asyn* module is both sufficient for our needs and compatible with *StreamDevice* `2.8.4`.

* If it is, recall what we did in [Chapter 3](3_module_versions.md).

  > Note that this makes a strong assumption that the list of source files in `2.7.14p` and `2.8.4` are the same. If some files have been added or removed between the versions, we have to modify `StreamDevice.Makefile` accordingly. Whenever this is the case, contact the maintainer of e3.

* If it isn't, we have to install a new *asyn* version using our current e3 environment. The procedure is here the same with *StreamDevice* in [Chapter 3](3_module_versions.md). In our case, there are neither new files nor deleted files between *asyn* versions `4.33` and `4.34`, and we can thus build the new version of asyn with the same `asyn.Makefile`:

  ```console
  [iocuser@host:e3-asyn]$ make vars
  [iocuser@host:e3-asyn]$ make existent
  /epics/base-3.15.5/require/3.0.4/siteMods/asyn
  └── 4.33.0
      ├── db
      ├── dbd
      ├── include
      └── lib
  [iocuser@host:e3-asyn]$ echo "EPICS_MODULE_TAG:=tags/R4-34" > configure/CONFIG_MODULE.local
  [iocuser@host:e3-asyn]$ echo "E3_MODULE_VERSION:=4.34.0" >> configure/CONFIG_MODULE.local
  [iocuser@host:e3-asyn]$ make vars
  [iocuser@host:e3-asyn]$ make init
  [iocuser@host:e3-asyn]$ make rebuild
  [iocuser@host:e3-asyn]$ make existent
  /epics/base-3.15.5/require/3.0.4/siteMods/asyn
  ├── 4.33.0
  │   ├── db
  │   ├── dbd
  │   ├── include
  │   └── lib
  └── 4.34.0
      ├── db
      ├── dbd
      ├── include
      └── lib
  ```

  Next, we can install *StreamDevice* `2.8.4`, which will be using *asyn* `4.34.0`.

  > This step is exactly the same as we what did in [Chapter 3](3_module_versions.md).

  ```console
  [iocuser@host:e3-3.15.5]$ make -C e3-StreamDevice/ existent
  make: Entering directory '/home/iocuser/e3-3.15.5/e3-StreamDevice'
  /epics/base-3.15.5/require/3.0.4/siteMods/stream
  └── 2.7.14p
      ├── dbd
      ├── include
      ├── lib
      └── SetSerialPort.iocsh

  4 directories, 1 file
  make: Leaving directory '/home/iocuser/e3-3.15.5/e3-StreamDevice'
  [iocuser@host:e3-3.15.5]$ make -C e3-StreamDevice/ vars
  [iocuser@host:e3-3.15.5]$ echo "EPICS_MODULE_TAG:=tags/2.8.4" > e3-StreamDevice/configure/CONFIG_MODULE.local
  [iocuser@host:e3-3.15.5]$ echo "E3_MODULE_VERSION:=2.8.4" >> e3-StreamDevice/configure/CONFIG_MODULE.local
  [iocuser@host:e3-3.15.5]$ echo "ASYN_DEP_VERSION:=4.34.0" >> e3-StreamDevice/configure/CONFIG_MODULE.local
  [iocuser@host:e3-3.15.5]$ make -C e3-StreamDevice  vars 
  [iocuser@host:e3-3.15.5]$ make -C e3-StreamDevice/ init
  [iocuser@host:e3-3.15.5]$ make -C e3-StreamDevice/ rebuild
  [iocuser@host:e3-3.15.5]$ $ make -C e3-StreamDevice/ existent
  make: Entering directory '/home/iocuser/e3-3.15.5/e3-StreamDevice'
  /epics/base-3.15.5/require/3.0.4/siteMods/stream
  ├── 2.7.14p
  │   ├── dbd
  │   ├── include
  │   ├── lib
  │   └── SetSerialPort.iocsh
  └── 2.8.4
      ├── dbd
      ├── include
      ├── lib
      └── SetSerialPort.iocsh

  8 directories, 2 files
  make: Leaving directory '/home/iocuser/e3-3.15.5/e3-StreamDevice'
  ``` 

  Here it is good to validate that *StreamDevice* `2.8.4` can be loaded.

  > Remember that you can initiate an IOC shell just like `iocsh.bash -r stream,2.8.4`.

  > Can you see the *asyn* version you've just set up in the output? Try loading *StreamDevice* version `2.7.14p` to compare.

  As you have just seen, dependencies are defined when we compile the module.

## Aggressive tests

More technical pitfalls exist when we are building or writing startup scripts. Here we will see some combinations which the current *require* module fails to handle properly.

> If you find further cases, please inform the e3 maintainer.

* How modules are loaded.

  Let's first uninstall the `2.8.4` version.

  ```console
  [iocuser@host:e3-3.15.5]$ make -C e3-StreamDevice/ uninstall
  [iocuser@host:e3-3.15.5]$ make -C e3-StreamDevice/ existent
  ```

  Let's try to load the module:

  ```console
  [iocuser@host:e3-3.15.5]$ iocsh.bash -r stream,2.7.14p
  ```

  What do you see? What if we don't define a specific version number of the `stream` module?

  > Remember: `iocsh.bash -r stream`.

  And what happens if we do the same after `make install` and `make vars`? (Test it.)

  What you have just seen is the default behavior when a module version number isn't specified; loading a module with no specified version will **only** work when the system has a numeric `X.Y.Z` version. In our last example, the system has *StreamDevice* version `2.8.4`, which **is** numeric, but `2.7.14p` is **not** numeric.
  
  > Also note that, in either of these cases, the *StreamDevice* module will use the version of *asyn* which was specified when building the *StreamDevice* module. 

* How we require dependency modules within startup scripts.

  Have a look at the differences between the startup scripts in `ch7_supplementary_path`:

  ```console
  [iocuser@host:e3training]$ iocsh.bash ch7_supplementary_path/7-1.cmd
  [iocuser@host:e3training]$ iocsh.bash ch7_supplementary_path/7-2.cmd
  ```

  ```console
  [iocuser@host:e3training]$ iocsh.bash ch7_supplementary_path/7-3.cmd 
  [iocuser@host:e3training]$ iocsh.bash ch7_supplementary_path/7-4.cmd
  ```

  ```console
  [iocuser@host:e3training]$ iocsh.bash ch7_supplementary_path/7-5.cmd 
  [iocuser@host:e3training]$ iocsh.bash ch7_supplementary_path/7-6.cmd 
  ```

  ```console
  [iocuser@host:e3training]$ iocsh.bash ch7_supplementary_path/7-7.cmd 
  [iocuser@host:e3training]$ iocsh.bash ch7_supplementary_path/7-8.cmd
  [iocuser@host:e3training]$ iocsh.bash ch7_supplementary_path/7-9.cmd
  ```

## Identify potential risks early

The current implementation of e3 can't handle these aforementioned cases properly (technically it is *require* that cannot). We must thus attempt to mitigate them, in part by following best practice when writing startup script. 

* Use specific version numbers for modules. That way if something wrong you will not be able to start the IOC.

* Use the highest version dependency module that you know will work. In the above examples, this would mean only using `stream`, and not both `asyn` and `stream` (as *StreamDevice* already depends on *asyn*).

## Dependence, dependence, and dependence

In this chapter, we only discuss one kind of dependency that arises when compiling a module, a so-called *build time dependency*. That is, the module `stream` uses functions which are defined in the `asyn` header files. We can see these in certain files that are generated at build-time:

```
e3-StreamDevice/StreamDevice/O.3.15.5_linux-x86_64/AsynDriverInterface.d: 
/epics/base-3.15.5/require/3.0.4/siteMods/asyn/4.34.0/include/asynDriver.h \
/epics/base-3.15.5/require/3.0.4/siteMods/asyn/4.34.0/include/asynOctet.h \
/epics/base-3.15.5/require/3.0.4/siteMods/asyn/4.34.0/include/asynInt32.h \
/epics/base-3.15.5/require/3.0.4/siteMods/asyn/4.34.0/include/asynUInt32Digital.h \
/epics/base-3.15.5/require/3.0.4/siteMods/asyn/4.34.0/include/asynGpibDriver.h \
/epics/base-3.15.5/require/3.0.4/siteMods/asyn/4.34.0/include/asynDriver.h \
/epics/base-3.15.5/require/3.0.4/siteMods/asyn/4.34.0/include/asynInt32.h \
```

By contrast, we also can have *run-time dependencies*. These often arise in particular with *StreamDevice*, and are in this case often signified by the existence of protocol files (`*.proto`), but they can also result from needing to use functionality from another module at run time, for example if you need to use the function `drvAsynIPPortConfigure` during your startup script.

In both cases, the module (*StreamDevice*, in this case) must load the correct version of the dependent module (*asyn*, in this case) when the IOC starts up.

---

## Assignments

* Think about how you figure out which versions of modules are available to you.
* What would a version that looks like `2.8.4-1` mean and imply?

