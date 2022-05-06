# 9. Other dependencies

## Lessons overview

In this lesson, you will learn how to do the following:

* Use a record type from another module in your module.
* Use a db or template file from another module to generate a new db file in
  your module.

---

## Using a new record type

When building an IOC, you may want to include records that are not part of EPICS
base. As an example, you may want to use an *acalcout* record (from the
[*calc*](https://github.com/epics-modules/calc) modules), which is like the
*calc* record from EPICS base, but for arrays. This can be used, for example, to
perform linear conversions on *waveform* records.

### Create a new module

Let us begin by creating a module to work with, following the instructions in
[Chapter 8](8_building_modules.md). We want to create a local module called
*linconv*, which will sit in a wrapper called *e3-linconv*. Within that wrapper,
create a `linconv.db` file with the following contents.

```none
record(ao, "OFFSET") {
    field(VAL,"0.5")
    field(PINI,"YES")
    field(FLNK, "LINCONV_create")
}

record(ao, "SLOPE") {
    field(VAL,"3")
    field(PINI,"YES")
    field(FLNK, "LINCONV_create")
}

record(acalcout, "LINCONV_create") {
    field(INPA, "OFFSET")
    field(INPB, "SLOPE")
    field(NELM, "100")
    field(CALC, "(IX*B)+A")
    field(OUT, "LINCONV PP")
}

record(waveform, "LINCONV"){
    field(FTVL, "FLOAT")
    field(NELM, "100")
}
```

:::{note}
Documentation for the *acalcout* record (a part of
[synApps](https://www.aps.anl.gov/BCDA/synApps)) can be found
[here](https://epics.anl.gov/bcda/synApps/calc/aCalcoutRecord.html).
:::

In this example `OFFSET` will be the offset value and `SLOPE` the slope value
applied to a waveform with values `0..99`. The record `LINCONV_create` is the
*acalcout* record which calculates the resultant waveform. Then the resultant
waveform is directed to record `LINCONV`.

In order to include the `linconv.db` file into the module, you will have to
update `linconv.Makefile` in order to include it as described in [Chapter
8](8_building_modules.md).

Once you have built and installed the module, you should create a basic startup
script to load the module, which could look like

```bash
require linconv
dbLoadRecords("$(linconv_DB)/linconv.db")
```

Let us try run this and see what happens.

```console
[iocuser@host:e3-linconv]$ iocsh -l cellMods st.cmd
# --- snip snip ---
require linconv
Module linconv version master found in cellMods/base-7.0.6.1/require-4.0.0/linconv/master/
Module linconv has no library
Loading module info records for linconv
dbLoadRecords(/home/iocuser/data/git/e3.pages.esss.lu.se/e3-linconv/cellMods/base-7.0.6.1/require-4.0.0/linconv/master/db/linconv.db)
Record "LINCONV_create" is of unknown type "acalcout"
Error at or before ")" in file "/home/iocuser/data/git/e3.pages.esss.lu.se/e3-linconv/cellMods/base-7.0.6.1/require-4.0.0/linconv/master/db/linconv.db" line 13
Error: syntax error
dbLoadRecords: failed to load '/home/iocuser/data/git/e3.pages.esss.lu.se/e3-linconv/cellMods/base-7.0.6.1/require-4.0.0/linconv/master/db/linconv.db'
# --- snip snip ---
```

### Fixing the dependency

So what happened here? The issue is that we need to also load the *calc* module
at the same time in order for the *acalcout* record to be made available. We can
do this in one of several different ways:

* Run `iocsh -r calc st.cmd` instead, to force it to load *calc* on
  startup. This is the worst of the ways since we have to modify the command we
  use to start the IOC, but it can be useful for quick and dirty testing.
* Modify your `st.cmd` to load *calc*:

  ```bash
  require calc
  require linconv
  dbLoadRecords("$(linconv_DB)/linconv.db")
  ```

  This is better, since starting the IOC will always load all of the necessary
  modules. However, it means that every time you create an IOC that needs this
  module you must still remember to do include the `require calc` line.
* The best option is to remember from [Chapter 8](8_building_modules.md) that we
  can add *calc* as a run-time dependency of *linconv*. We do this by adding
  `CALC_DEP_VERSION:=3.7.4` to `configure/CONFIG_MODULE`, and then we add

  ```make
  REQUIRED += calc
  ifneq ($(strip $(CALC_DEP_VERSION)),)
  calc_VERSION:=$(CALC_DEP_VERSION)
  endif
  ```

  to `linconv.Makefile`. This registers `calc` as a (run-time) dependency of
  *linconv*, ensuring that it will be loaded every time.

If we now re-install the module and re-start it

```console
[iocuser@host:e3-linconv]$ make uninstall  # A good idea in general
[iocuser@host:e3-linconv]$ make clean build install
[iocuser@host:e3-linconv]$ iocsh st.cmd
```

then we should see that the records load as expected. Moreover, you should be
able to read the `LINCONV` PV and set `SLOPE` and `OFFSET` to modify it.

:::{admonition} Exercise
Why do we not need to run `make patch` or `make init`?
:::

## Using an external db/template file

Another sort of dependency that can occur is due to needing `.db` files from
other modules. One common source is from *Area Detector*, but we will use a
different one in this case. We will create a simple PID (Proportional Integral
Derivative) controller using the EPID record defined in the community EPICS
module [std](https://github.com/epics-modules/std).

### Create a new module

This is the same as above. Use *cookiecutter* to create a new local e3 module
called *mypid*.

Instead of adding a database file, we will create a substitution file based off
of `pid_control.db` from *std*. Create a file with the contents

```none
file "pid_control.db"
{
pattern { P,        PID,    INP,        OUT,        LOPR,   HOPR,   DRVL,   DRVH,   PREC,   KP,     KI, KD, SCAN        }
        { mypid:,   PID1,   pidDemoInp, pidDemoOut, 0,      100,    0,      5,      3,      0.2,    3., 0., ".1 second" }
}
```

and save it as `pid.substitutions` in the `Db/` directory of your new module.

:::{note}
In order to inflate the `.substitutions` file, you need to let the e3 build
system know about it. In the `mypid.Makefile` the `SUBS` variable is defined
in the specific line `SUBS = $(wildcard $(APPDB)/*.substitutions)`
:::

Try to build and install the module, you should see the following.

```console
[iocuser@host:e3-mypid]$ make build install
# --- snip snip ---
make[1]: Entering directory `/home/iocuser/data/git/e3.pages.esss.lu.se/e3-mypid/mypid'
Inflating database ...                mypidApp/Db/pid.substitutions >>>                       mypidApp/Db/pid.db
msi: Can't open file 'pid_control.db'
input: '' at
make[1]: *** [mypidApp/Db/pid.substitutions] Error 1
make[1]: Leaving directory `/home/iocuser/data/git/e3.pages.esss.lu.se/e3-mypid/mypid'
make: *** [db] Error 2
```

:::{note}
The database inflation is performed by `make db_internal`, which is a dependency of the
`install` target. So to inflate the `.substitutions` file you can simply run
`make db_internal`.
:::

As in other situations, we need to tell the build system where to look for
`pid_control.db` so that the `.substitutions` file can be inflated properly. To
begin, follow what was done for the *calc* module above, but with the *std*
module. That is,

* Define `STD_DEP_VERSION` in `configure/CONFIG_MODULE`
* Add a `REQUIRED += std` and other associated lines in `mypid.Makefile`
* We also need to update `USR_DBFLAGS` so that `msi` can find any necessary
  `.db` or `.template` files. So add the line
  `make USR_DBFLAGS += -I $(E3_SITEMODS_PATH)/std/$(std_VERSION)/db ` and then
  run `make db_internal` again

Unfortunately, this does not work. If you look at the installed versions of
*std*, you will see the following:

```console
[iocuser@host:e3-mypid]$ ls /epics/base-7.0.6.1/require/4.0.0/siteMods/std
3.6.2+0
```

What is that `+0` doing there?

### A digression about build numbers

You should have noticed by now that when you load a module (e.g. *asyn*
version `4.42.0`) it is actually loaded as `4.42.0+0`. What is this `+0`?
This is the *build number*. These are used in a number of different deployment
systems to distinguish between builds where, for example, the source code may
not have changed but some of the metadata or dependencies have. This allows us
to have, for example, two copies of the same version of *StreamDevice* that may
depend on different versions of *asyn*.

The default behaviour in e3 is the following.

* If you request a specific version inclusive of a build number, that version
  will be loaded or built against.
* If you do not request a build number, then the highest matching build number
  will be used.

:::{warning}
Even though you do not have to specify build numbers when loading a module, you
_must_ specify a build number for `E3_MODULE_VERSION` in `CONFIG_MODULE` when
building a module.
:::

Most of this all happens under the hood. One main exception is any references to
other modules within, for example, `mypid.Makefile`. To deal with that case,
there is a function called `FETCH_BUILD_NUMBER` that can be used to determine
the correct build number. In this particular case, we need to replace the
`USR_DBFLAGS` line above with the following.

```make
USR_DBFLAGS += -I $(E3_SITEMODS_PATH)/std/$(call FETCH_BUILD_NUMBER,$(E3_SITEMODS_PATH),std)/db
```

which will take the specified version (`3.6.2` in this case) and add the correct
build number.

### Checking if everything is ok

After the above changes, you should be able to build your module correctly. That
is, you should see the following

```console
[iocuser@host:e3-pid]$ make install
# --- snip snip ---
make[1]: Entering directory `/home/iocuser/data/git/e3.pages.esss.lu.se/e3-mypid/mypid'
Inflating database ...                mypidApp/Db/pid.substitutions >>>                       mypidApp/Db/pid.db
make[1]: Leaving directory `/home/iocuser/data/git/e3.pages.esss.lu.se/e3-mypid/mypid'
# --- snip snip ---
```

indicating that the `.substitutions` file has been inflated correctly. You
should now be able to look in the installed module directory and see the
generated `pid.db` file.

---

## Assignments

1. If you try to actually load the `pid.db` database file, it does not load.
   What dependency are you missing?
2. Where is `FETCH_BUILD_NUMBER` defined?
3. Can you think of another way to load the records in the `.substitutions` file
   that does not involve the build-time database expansion?
4. Find which modules arise as run-time dependencies for the modules in the `ps`
   group (installed with `e3.bash -s mod`). Can you identify why they are
   run-time and not build-time dependencies?
