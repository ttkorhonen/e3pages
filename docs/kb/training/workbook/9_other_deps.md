# Other dependencies

## Lessons overview

In this lesson, you'll learn how to do the following:

* Use a record type from another module in your module.
* Use a db or template file from another module to generate a new db file in your module.
<!-- todo: add contents from 9.md in Han's last commit -->

---

## Using a new record type

When building an IOC, you may want to include records that are not part of EPICS base. As an example, you may want to use an *acalcout* record (from
the [calc](https://github.com/epics-modules/calc) modules), which is like the *calc* record from EPICS base, but for arrays. This can be used, for
example, to perform linear conversions on *waveform* records.

### Create a new module 

Let us begin by creating a module to work with, following the instructions in [Chapter 8](8_building_modules.md). We want to create a local module called
*linconv*, which will sit in a wraper called *e3-linconv*. Within that wrapper, create a `linconv.db` file with the following contents.

```
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
Documentation for the *acalcout* record (a part of [synapps](https://www.aps.anl.gov/BCDA/synApps)) can be found [here](https://epics.anl.gov/bcda/synApps/calc/aCalcoutRecord.html).
:::

In this example `OFFSET` will be the offset value and `SLOPE` the slope value applied to a waveform with values `0..99`. The record `LINCONV_create` is the *acalcout* record which
calculates the resultant waveform. Then the resultant waveform is directed to record `LINCONV`.

In order to include the `linconv.db` file into the module, you will have to update `linconv.Makefile` in order to include it as described in [Chapter 8](8_building_modules.md).

Once you have built and installed the module, you should create a basic startup script to load the module, which could look like
```bash
require linconv
dbLoadRecords("$(linconv_DB)/linconv.db")
```

Let's try run this and see what happens.
```console
[iocuser@host:e3-linconv]$ iocsh.bash st.cmd
# --- snip snip ---
require linconv
Module linconv version master found in cellMods//base-7.0.5/require-3.4.1/linconv/master/
Module linconv has no library
Loading module info records for linconv
dbLoadRecords(/home/simonrose/data/git/e3.pages.esss.lu.se/e3-linconv/cellMods/base-7.0.5/require-3.4.1/linconv/master/db/linconv.db)
Record "LINCONV_create" is of unknown type "acalcout"
Error at or before ")" in file "/home/simonrose/data/git/e3.pages.esss.lu.se/e3-linconv/cellMods/base-7.0.5/require-3.4.1/linconv/master/db/linconv.db" line 13
Error: syntax error
dbLoadRecords: failed to load '/home/simonrose/data/git/e3.pages.esss.lu.se/e3-linconv/cellMods/base-7.0.5/require-3.4.1/linconv/master/db/linconv.db'
# --- snip snip ---
```

### Fixing the dependency

So what happened here? The issue is that we need to also load the *calc* module at the same time in order for the *acalcout* record to be made available. We can do this in
one of several different ways:

* Run `iocsh.bash -r calc st.cmd` instead, to force it to load *calc* on startup. This is the worst of the ways since we have to modify the command we use to start the IOC,
  but it can be useful for quick and dirty testing.
* Modify your `st.cmd` to load *calc*:
  ```bash
  require calc
  require linconv
  dbLoadRecords("$(linconv_DB)/linconv.db")
  ```
  This is better, since starting the IOC will always load all of the necessary modules. However, it means that every time you create an IOC that needs this module
  you must still remember to do include the `require calc` line.
* The best option is to remember from [Chapter 8](8_building_modules.md) that we can add *calc* as a run-time dependency of *linconv*. We do this by adding
  `CALC_DEP_VERSION:=3.7.4` to `configure/CONFIG_MODULE`, and then we add
  ```make
  REQUIRED += calc
  ifneq ($(strip $(CALC_DEP_VERSION)),)
  calc_VERSION:=$(CALC_DEP_VERSION)
  endif
  ```
  to `linconv.Makefile`. This registers `calc` as a (run-time) dependency of *linconv*, ensuring that it will be loaded every time.

If we now re-install the module and re-start it
```console
[iocuser@host:e3-linconv]$ make uninstall  # A good idea in general
[iocuser@host:e3-linconv]$ make clean build install
[iocuser@host:e3-linconv]$ iocsh.bash st.cmd
```
then we should see that the records load as expected. Moreover, you should be able to read the `LINCONV` PV and set `SLOPE` and `OFFSET` to modify it.

:::{admonition} Exercise
Why don't we need to run `make patch` or `make init`?
:::

## Using an external db/template file

For this part of the training we will create a simple PID controller using the record type EPID defined on [std module](https://github.com/epics-modules/std). Besides the EPID record we will use one db file present on std module.

In our module we will do something similar to the IOC example present at std module on the files `pid_slow.template` and `st.cmd` on [iocStdTest](https://github.com/epics-modules/std/tree/master/iocBoot/iocStdTest). Our plan is to use the file `pid_control.db` [1] from the std module.

### Create a new module 

To start this you will need to create a new module, to do this follow the instructions on [Chapter 8](8_building_modules.md). For our setup the module name will be considered *mypid*.

### Create a substitution file

Now we will create in our module a substitution file that uses the `pid_control.db` file as a template file (find the file [here](https://github.com/epics-modules/std/blob/master/stdApp/Db/pid_control.db)). You should create a `pid.substitutions` file within this content:

```
file "pid_control.db"
{
pattern { P,        PID,    INP,        OUT,        LOPR,   HOPR,   DRVL,   DRVH,   PREC,   KP,     KI, KD, SCAN        }
        { mypid:,   PID1,   pidDemoInp, pidDemoOut, 0,      100,    0,      5,      3,      0.2,    3., 0., ".1 second" }
}
```

This file is just an example, and uses as `INP` and `OUT` in existent PVs, but it suffices for our test. Note that there is no hard-code path or variable within the substitution file. 

If you change the `mypid.Makefile` and try to compile this module you should receive a message like this:

```console
msi: Can't open file 'pid_control.db'
```

This is because `MSI` has no idea where `pid_control.db` file is. You need to tell the building system where it is. 

### Add std as a dependency

To solve the above, the first step is to set *std* as a dependency. As we've see on previous lesson you should edit `mypid.Makefile` and `CONFIGURE_MODULE`.

On `mypid.Makefile` you should add:

```bash
REQUIRED += std

ifneq ($(strip $(STD_DEP_VERSION)),)
std_VERSION=$(STD_DEP_VERSION)
endif
```

And add the following line into `CONFIG_MODULE`:

```python
STD_DEP_VERSION:=3.5.0
```

### Add std on `USR_DBFLAGS`

To allow that your substitutions file uses db files from *std* you should include the std db folder on `USR_DBFLAGS`. So in `mypid.Makefile` you add this line:

```
USR_DBFLAGS += -I $(E3_SITEMODS_PATH)/std/$(std_VERSION)/db
```

This line will tell to `MSI` where find the `pid_control.db`.

### Checking if everything is ok

After these changes you can compile your module and you shouldn't see any error.

If you would like to, you can go to your module folder and see the `pid.db` generated file, the file should be at `$(E3_REQUIRE_LOCATION)/siteMods/mypid/master/db/pid.db`

## Example files

The example files showed in this tutorial could be found at 
[e3-moduleexample](https://gitlab.esss.lu.se/epics-examples/e3-moduleexample.git) and [moduleexample](https://gitlab.esss.lu.se/epics-examples/moduleexample.git). Note that the module name is moduleexample, but the db and substitutions
files are the same as the ones used in this tutorial.

---

## Assignments

* What does MSI stand for?
<!-- todo: figure out proper assignments -->

