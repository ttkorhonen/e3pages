# Installing other versions of modules

## Lesson overview

In this lesson, you'll learn how to do the following:

* Print out, and understand some of, the various EPICS and e3 variables.
* Understand how different versions of the same module are mananaged in e3.
* Understand the difference between two important variables: `E3_MODULE_VERSION` and `EPICS_MODULE_TAG`.
* Install a different version of *StreamDevice* within e3.

---

## The version variables within e3

Various environment variables are used in EPICS and e3, and it is important to be aware of these and their difference(s). Please remember that e3 is a configuration tool around EPICS, and that we thus have some variables which are unique to e3.

0. Make sure you are in **E3_TOP**

> *We will reiterate starting directory a few last times, but please pay attention to the current working directory in the command prompt: [(user)@(hostname):(**current-working-directory**)]$ .*

1. Go to `e3-stream`, which should have been installed with the `core` group in chapter 1.
2. Run the following command:

   ```console
   [iocuser@host:e3-stream]$ make vars
   ```

The variables of interest here are:

* `E3_MODULE_VERSION`  is used as *Module/Application version* with require within an IOC startup script. We recommend using semantic versioning (also known as *semver*) for releases. 

* `EPICS_MODULE_TAG` is the *snapshot* of the source code repository, e.g. `tags/stream_2_7_14`, `tags/2.8.18`, `master`, `branch_name`, or `e0a24fe`. It is *strongly* recommended that
  only absolute references (either tags or commit hashes) are used, since otherwise it is much more difficult to have reproducible builds. However, in principle, any valid git reference
  works in this place.

These two variables are defined in `configure/CONFIG_MODULE`.

## List the installed version(s) of a module

0. Make sure you are in `e3-stream/`
1. Run the following rule:

   ```console
   [iocuser@host:e3-stream]$ make existent
   ```

2. Look at the output.
   The result show the installed version(s) of stream modules within e3:
   
   ```console
   /epics/base-7.0.5/require/3.4.1/siteMods/stream
   `-- 2.8.18+0
       |-- dbd
       |-- include
       |-- lib
       |-- SetSerialPort.iocsh
       `-- stream_meta.yaml
   ```

   > The default argument to `make existent` is LEVEL 2 - i.e. `make existent` is identical to `make LEVEL=2 existent`. This controls the depth of the subtree displayed. 

## Check the version of a module

Let's see what our current version of *StreamDevice* is:

```console
[iocuser@host:e3-stream]$ cd StreamDevice
[iocuser@host:StreamDevice]$ git describe --tags
```

> Pay attention to the current working directory above!

We could here download *StreamDevice* directly from PSI's GitHub account, and switch `EPICS_MODULE_TAG` when `make init` is executed:

1. Go back to `e3-stream/`
2. Run `make init` to see what kind of output you get.

   Can you guess what kind of process that is happening behind scenes?

3. Check `EPICS_MODULE_TAG` with `make vars`
4. Have a look at the `configure/CONFIG_MODULE` file

> Running `make init` will download all source files within StreamDevice as a git submodule, and will in our case switch back to the `2.8.18` version of StreamDevice.
> 
> *N.B.! You may have different versions than the author of these instructions.*

## Change `EPICS_MODULE_TAG` and `E3_MODULE_VERSION`

It is important to understand the relationship between `EPICS_MODULE_TAG` and `E3_MODULE_VERSION` as described above. Let us try to change them and see what happens.

First, let us modify `EPICS_MODULE_TAG`; Use `master` instead of `tags/2.8.18` (Note that, as above, this is not recommended practice for a release version, but
often makes sense during development).

> If you already have `master` as default, choose an arbitrary version and modify variables accordingly; available tags and branches can be found on the PSI StreamDevice release page: https://github.com/paulscherrerinstitute/StreamDevice/releases

Next, change `E3_MODULE_VERSION` to a different tag (e.g. `e3training`).  

> The convention here is to name the e3 module according to the module's version, but any name could technically be used during development. Note that there are some restrictions
> on valid module names.
  
Your modified `configure/CONFIG_MODULE` may then look like:

```make
# --- snip snip ---

EPICS_MODULE_TAG:=master
E3_MODULE_VERSION:=e3training

# --- snip snip ---
```

You could instead create a local `CONFIG_MODULE` file, `CONFIG_MODULE.local`, like:

```console
[iocuser@host:e3-stream]$ echo "EPICS_MODULE_TAG:=master" > configure/CONFIG_MODULE.local
[iocuser@host:e3-stream]$ echo "E3_MODULE_VERSION:=e3training" >> configure/CONFIG_MODULE.local
```

Files with the extension `.local` are generally not tracked by git (see the `.gitignore` file in the wrapper), and are
used to load custom local configuration.

Finally, verify your configuration with `make vars`.

## Build and install *StreamDevice* `b84655e`

Time to try out some makefile rules. See if you can spot the difference between before now. From `e3-stream/`, run:

1. `make vars`
2. `make init`
3. `make build`
4. `make install`
5. `make existent`
6. `make dep`
7. `make vers`
8. `make dep | head -1`

And it seldom hurts to try `make help` for new projects.

---

## Assignments

* Try out `make existent` with `LEVEL=4`.
* Do `make init` in **E3_TOP**. What do you see?
* What sort of restrictions exist for valid module names in e3?
* Which kind of make rule allows us to uninstall the installed module?
* Can we combine the following two steps? 
  
  1. `make build`
  2. `make install`

