# 2. An e3 IOC

## Lesson overview

In this lesson, you will learn how to do the following:

* Load an e3 environment using utility scripts.
* Switch between different e3 environments.
* Run a simple IOC with an example startup script.

---

## The e3 environment

In order to facilitate the development process, e3 supports using multiple EPICS
environments. Such an environment consists of a collection of shell variables in
the current terminal. When you install *require*, it will install an activation
script called `setE3Env.bash`. To activate the environment, you must source the
relevant `setE3Env.bash`.

Using a default configuration (presently EPICS base 7.0.5 with *require* 3.4.1
installed at `/epics`) the full path for this script would then be
`/epics/base-7.0.5/require/3.4.1/bin/setE3Env.bash`.

For your convenience, the e3 building system - at the end of installation
procedure of *require* and modules - creates a utility script within the
`tools/` directory called `setenv`:

```console
[iocuser@host:e3]$ source tools/setenv
```

:::{note}
If such a file already exists, the old file will be renamed to `setenv_YYMMDDHHMM`.
:::

Thus, one can easily switch between environments. For example:

```console
[iocuser@host:e3]$ source tools/setenv
[iocuser@host:e3]$ source /epics/base-7.0.3.1/require/3.4.1/bin/setE3Env.bash
```

This will first load the latest environment installed with `e3.bash`, and then
it will load the environment corresponding to EPICS base 7.0.3.1 and *require*
3.4.1 (assuming that that has been installed).

## Run an example IOC

Starting an IOC in e3 is done by running the script `iocsh.bash` which is
installed with *require* at `/epics/base-7.0.5/require/3.4.1/bin/iocsh.bash`. If
you have sourced the correct `setE3Env.bash`, then this will be on `$PATH`.
`iocsh.bash` is a wrapper to `softIocPVA` from EPICS base and takes a number of
possible arguments, the most basic of which is a startup command file, which
consists of a sequence of commands that will be executed by the IOC upon
startup.

:::{warning}
The last line of the file must end in a newline or that line will not be executed.
:::

### The simplest example

In order to run a very basic IOC, run the following command after sourcing
`setE3Env.bash` as described above.

```console
[iocuser@host:e3]$ iocsh.bash
```

Congratulations, you have run your first e3 IOC!

To exit the IOC, type `exit` at the prompt.

### A more complicated example

Open your favourite text editor and copy and paste the following into a new file:

```bash
require iocstats

epicsEnvSet("TOP", "$(E3_CMD_TOP)")

epicsEnvSet("NUM", "9999")

epicsEnvSet("P", "IOC-$(NUM)")
epicsEnvSet("IOCNAME", "$(P)")

iocshLoad("$(iocstats_DIR)/iocStats.iocsh", "IOCNAME=$(IOCNAME)")

iocInit()

dbl > "$(TOP)/${IOCNAME}_PVs.list"

```

Save this file as `iocstats.cmd`, and then run

```console
[iocuser@host:e3]$ iocsh.bash iocstats.cmd
```

If the IOC starts up correctly (you will have to have installed the core modules
during the last chapter), then do the following

1. Check the IOC name:

   ```console
   localhost-31462> echo ${IOCNAME}
   ```

   This should output IOC-9999.

2. Run the following command:

   ```console
   localhost-31462> system "ls $(E3_CMD_TOP)"
   ```

   What does it represent?

3. Open another terminal and source the same e3 configuration.

   ```console
   [iocuser@host:e3]$ source tools/setenv
   ```

4. Print all of the PVs to a file and skim through it:

   ```console
   [iocuser@host:e3]$ while IFS= read -r pv; do caget $pv; done < IOC-9999_PVs.list
   ```

5. Check the heartbeat of your IOC.

   ```console
   [iocuser@host:e3]$ camonitor ${IOCNAME}:HEARTBEAT
   ```

## Play around with the example IOC

* Return to the contents of `iocstats.cmd` and make sure you understand all of it:

  ```bash
  require iocstats

  epicsEnvSet("TOP", "$(E3_CMD_TOP)")

  epicsEnvSet("NUM", "9999")

  epicsEnvSet("P", "IOC-$(NUM)")
  epicsEnvSet("IOCNAME", "$(P)")

  iocshLoad("$(iocstats_DIR)/iocStats.iocsh", "IOCNAME=$(IOCNAME)")

  iocInit()

  dbl > "$(TOP)/${IOCNAME}_PVs.list"

  ```

* Try the following commands in the IOC shell:
   * `help`
   * `var`
   * `dbl`
   * `dbsr`
   * `echo ${IOCNAME}`
   * `epicsEnvShow`

---

## Assignments

1. What is the meaning of each of the following expressions in a startup script?
   What function do they serve, or what action do they perform?
   * `require`
   * `E3_CMD_TOP`
   * `system`
   * `iocshLoad`
   * `iocInit`
   * `>`
   * `<`

2. What happens if you place the commands in a different order in the startup
   script?
