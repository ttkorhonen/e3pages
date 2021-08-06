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

In this example `OFFSET` will be the offset value and `SLOPE` the slope value applied to a waveform with values `0..99`. The record `LINCONV_create` is the acalcout record which
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
Uh, oh, what happened?

### Change e3-linconv to uses acalcout
 
So, now with that db file, if you try to run an startup script like this:

```bash
require linconv, 0.0.1
dbLoadRecords("linconv.db")
```

You will receive a message like this:

```console
Record "LINCONV_create" is of unknown type "acalcout"
```

This error happens because the definition of acalcout type come from the *calc* module. 

So, what you should do to solve this? One possible approach is include in your startup script something like this:

```bash
require calc, 3.7.1
```

The problem with this approach is that every time you use your *linconv* module you need to include this. You would furthermore need to know what *calc* version to use. A better approach is to require the *calc* module when you require *linconv* - and this is the main new point on this lesson. To do this, you need to change a few files in your `e3-linconv` repository. First you need to change your `configure/CONFIG_MODULE` to define what *calc* version you want to use, by adding the following line:

```python
CALC_DEP_VERSION:=3.7.1
```

Next you need to change the `linconv Makefile` to recover the *calc* version and to require it, to do this you should add these lines to `linconv.Makefile`:

```bash
REQUIRED=calc

ifneq ($(strip $(CALC_DEP_VERSION)),)
calc_VERSION=$(CALC_DEP_VERSION)
endif
```

Here is the key line is the **`REQUIRED`** declaration, which allows the building system to add its dependency directly to a generated `dep` file in addition to a compiler calculated dependency. 

Now you can compile and install the module:

```console
[iocuser@host:e3-linconv]$ make vars
[iocuser@host:e3-linconv]$ make init
[iocuser@host:e3-linconv]$ make build
[iocuser@host:e3-linconv]$ make install
```

You can check to see if *calc* was included as a dependency for your *linconv* module. In the file `$(E3_REQUIRE_LOCATION)/siteMods/linconv/master/lib/linux-x86_64/linconv.dep` you should see this:

```bash
calc 3.7.1
```

### Testing linconv

Having changed this configuration you can try the same startup script:

```bash
require linconv, 0.0.1
dbLoadRecords("linconv.db")
```

Congratulations! Now you should be able to read `LINCONV` PVs and set `SLOPE` and `OFFSET`.

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

