# Startup scripts in e3

## Lesson overview

In this lesson, you'll learn how to do the following:

* Build the startup script for an IOC in e3.
* Understand different methods of using EPICS functions within startup scripts.
* Understand the local setup for *database* and *protocol* files.
* Add common (global) modules to the IOC.

---

## Preliminaries

Before working on this chapter, please clone the following repository, as it has some necessary files to work with.
```console
[iocuser@host:~]$ git clone --recursive -b 1.0.0 https://gitlab.esss.lu.se/e3/e3-training-material.git
```
In particular, it includes a simulator based on *[Kameleon](https://github.com/jeonghanlee/kameleon.git)* to simulate
a serial device for an IOC to communicate with. Note that this repository is already included as a submodule of the
trianing material, so you do not need to clone it.

:::{note}
Kameleon has been written for Python2 (tested on 2.7), and so you must have an installation of Python2 installed.
:::

To begin with, open a separate terminal and run the following to start the simulator.
```console
[iocuser@host:e3-training-material]$ bash 4_startup_scripts_in_e3/simulator.bash
```
This will start the simulator running, which you can then test with `telnet` via
```console
[iocuser@host:~]$ telnet 127.0.0.1 9999
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
CPS, 1, CPM, 4, uSv/hr, 0.04, SLOW
CPS, 4, CPM, 18, uSv/hr, 0.052, SLOW
CPS, 3, CPM, 19, uSv/hr, 0.035, SLOW
CPS, 2, CPM, 1, uSv/hr, 0.032, SLOW
CPS, 4, CPM, 4, uSv/hr, 0.083, SLOW
# --- snip snip ---
```
You can always quit the `telnet` session by hitting `^]`:
```console
^]
telnet> quit
Connection closed.
```
This will likely kill the simulator which you should then restart. In general, this simulator does have a tendency to die and so may 
need to be restarted between tests.

:::{tip}
The key combination `^]` will depend a lot on your keyboard layout. For a US keyboard layout, this is Ctrl + `]`. For
a Swedish keybaord layout, this is Ctrl + `¨` (they are located in the same physical location of they keyboard). You
may have to try a few different options to see what works.
:::


## Example IOCs

In the directory `4_startup_scripts_in_e3/cmds/` you will find a number of startup scripts that can be used for the following steps.

For each of these scripts, it will be good practicce to examine the script in order to try to predict what will happen, and then
examine every line of the output when running the startup script with `iocsh.bash`. Before you begin, of course, make sure that
you have sourced the correct e3 environment's `setE3Env.bash`, at which point you can start the IOC with
```console
[iocuser@host:cmds]$ iocsh.bash $EXERCISE_NUMBER.cmd
```

### First IOC

The first startup script is called `1.cmd`. As stated above, you should examine this script first and then start it with
```console
[iocuser@host:cmds]$ iocsh.bash 1.cmd
```

* Can you see where `E3_IOCSH_TOP` and `E3_CMD_TOP` are defined?
* How are these two variables changed if you instead execute `iocsh.bash` from the parent directory `4_startup_scripts_in_e3/`?
* How many dependent modules of stream are loaded?
* Were there any warning messages? What do you think they mean?

### Second IOC

Start the second IOC with the startup script `2.cmd`.
```console
[iocuser@host:cmds]$ iocsh.bash 2.cmd
```

* What is the purpose of `iocInit()`?
  :::{tip}
  More information can be found in the [EPICS Application Developer's Guide](https://epics.anl.gov/base/R3-16/2-docs/AppDevGuide/IOCInitialization.html#x8-2810007.4).
  :::
* What happens if you remove the `iocInit()` line?
* Can you spot the warning? And can you explain what kind of warning it is?
* You should have had the simulator running in a separate terminal. If so, what did you notice between the two of these
  scripts? What was the cause of that?

### 3-1.cmd

Execute the next command:

```console
[iocuser@host:ch4_supplementary_training]$ iocsh.bash cmds/3-1.cmd 
```

* The IOC is running, but it doesn't connect to anything. Can you see anything in the output that explains this?

  > Beware that the application launches regardless of if it finds hardware or not. In `3-1.cmd` there are no `.db.`-files to specify records and fields, which is why no errors appear.

This script contains the correct *Asyn* configuration for the simulated device:

```bash
drvAsynIPPortConfigure("CGONPI", "127.0.0.1:9999", 0, 0, 0)
```

<!-- This is pointing out a) we don't have STREAM_PROTOCOL_PATH set and we have not loaded any db files that do anything -->

### 3-2.cmd

This script contains a fully working IOC - inspect it thouroughly.

* Can you find the warning? 
* How does this script use `E3_CMD_TOP`? Is it useful to define where other files are? 
* What is the *stream protocol* file? 

<!-- Note that this uses random.bash and random.cmd here, which we do not need. So cut those out -->

### 4.cmd

By now we have a functioning IOC which can communicate with our simulated device. We would, however, generally want to tie more EPICS modules into that IOC, such as `iocStats`, `autosave`, and `recsync`. For this, we will need the specific module's name, its' version, as well as its' corresponding configuration files (database files and so forth).

Execute the next script:

```console
[iocuser@host:ch4_supplementary_path]$ iocsh.bash cmds/4.cmd
```

1. Type `dbl` to see the IOC's PVs.
2. Get the *heartbeat* of your IOC:

   ```
   350b5cb.kaffee.4355 > dbpr IOC-80159276:IocStat:HEARTBEAT
   ```

   > The number `80159276` is here randomly generated. If you happen to see the same number on your machine, today is your lucky day!

3. Look at the heartbeat again. Is it the same? Why not?

Spend some time thinking about the following:

* `epicsEnvSet` Can you see two different ways for it to be used? 

* Can you think of another syntax by which you can call `dbLoadRecords`?

* Could you rewrite startup scripts using only one method? 

<!-- This just adds iocstats -->

### 5.cmd

Here we add `iocStats` in a slightly different way, and have furthermore added more default e3 modules.

0. Go to **E3_TOP** and run the following commands:

    ```console
   [iocuser@host:e3-3.15.5]$ make -C e3-iocStats/ existent
   [iocuser@host:e3-3.15.5]$ make -C e3-recsync/  existent
   [iocuser@host:e3-3.15.5]$ make -C e3-autosave/ existent
   ```

   * Can we see the `*.iocsh` files with the installation path of e3?

   The e3 function `loadIocsh` is a function similar to EPICS' function `iocshLoad`. It supplies us with a reusable modularized startup script to simplify development.

   > `loadIocsh` can of course still be used, but `iocshLoad` is highly recommended. 

1. Run the following command to print your PVs, and inspect the output file:

   ```console
   [iocuser@home:ch4_supplementary_path]$ bash ../tools/caget_pvs.bash -l IOC-NNNNNNNN_PVs.list 
   ```

   (where `NNNNNNNN` is your IOC's random number.) 

<!-- This basically adds essioc -->

---

## Assignments

* Could you improve on the startup script further? Explain to yourself how.
* What does the `-C` flag do when used with make rules?

