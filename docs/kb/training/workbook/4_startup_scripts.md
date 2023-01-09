# 4. Startup scripts in e3

## Lesson overview

In this lesson, you will learn how to do the following:

* Have an IOC communicate with a (simulated) device
* How to load and configure certain common EPICS modules

---

## Preliminaries

Before working on this chapter, please clone the following repository, as it has
some necessary files to work with.

```console
[iocuser@host:~]$ git clone -b 1.0.0 https://gitlab.esss.lu.se/e3/e3-training-material.git
```

You will also need to install the
[LeWIS](https://lewis.readthedocs.io/en/latest/index.html) simulator, which is
used to simulate a device that your IOC will communicate with.

```console
[iocuser@host:~]$ pip3 install --user lewis
```

To start the simulator, open another terminal and run

```console
[iocuser@host:~]$ lewis -k lewis.examples example_motor
2021-08-12 17:15:48,902 INFO lewis.DeviceBase: Creating device, setting up state machine
2021-08-12 17:15:48,903 INFO lewis.Simulation: Changed cycle delay to 0.1
2021-08-12 17:15:48,903 INFO lewis.Simulation: Changed speed to 1.0
2021-08-12 17:15:48,903 INFO lewis.Simulation: Starting simulation
2021-08-12 17:15:48,903 INFO lewis.AdapterCollection: Connecting device interface for protocol 'stream'
2021-08-12 17:15:48,904 INFO lewis.ExampleMotorStreamInterface.StreamServer: Listening on 0.0.0.0:9999
```

This will start the simulator running, which you can then test with `telnet` via

:::{note}
You may need to install telnet with

```console
sudo yum install telnet -y
```

:::

```console
[iocuser@host:~]$ telnet 127.0.0.1 9999
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
P?
0.0
```

The commands that the motor takes are `P?`, `T?`, and `S?` to query information,
`T=<num>` to set its target, and `H` to halt the motor from moving.

You can always quit the `telnet` session by hitting `^]`:

```console
^]
telnet> quit
Connection closed.
```

:::{tip}
The key combination `^]` will depend a lot on your keyboard layout. For a US
keyboard layout, this is Ctrl + `]`. For a Swedish keyboard layout, this is
Ctrl + `¨` (they are located in the same physical location of the keyboard). You
may have to try a few different options to see what works.
:::

## Example IOCs

In the directory `4_startup_scripts_in_e3/cmds/` you will find a number of
startup scripts that can be used for the following steps.

For each of these scripts, it will be good practise to examine the script in
order to try to predict what will happen, and then examine every line of the
output when running the startup script with `iocsh`. Before you begin, of
course, make sure that you have sourced the correct e3 environment's
`setE3Env.bash`.

### First IOC

The first startup script is called `1.cmd`. As stated above, you should examine
this script first and then start it with

```console
[iocuser@host:e3-training-material]$ cd 4_startup_scripts_in_e3/cmds
[iocuser@host:cmds]$ iocsh 1.cmd
```

* Can you see where `E3_IOCSH_TOP` and `E3_CMD_TOP` are defined?
* How are these two variables changed if you instead execute `iocsh` from
  the parent directory `4_startup_scripts_in_e3/`?
* How many dependent modules of stream are loaded?
* Were there any warning messages? What do you think they mean?

### Second IOC

Start the second IOC with the startup script `2.cmd`.

```console
[iocuser@host:cmds]$ iocsh 2.cmd
```

* What is the purpose of `iocInit()`?

  :::{tip}
  More information can be found in the [EPICS Application Developer's
  Guide](https://epics.anl.gov/base/R3-16/2-docs/AppDevGuide/IOCInitialization.html#x8-2810007.4).
  :::

* What happens if you remove the `iocInit()` line?
* Can you spot the warning? And can you explain what kind of warning it is?
* You should have had the simulator running in a separate terminal. If so, what
  changed between when you ran the first script and when you ran the second?
  What could have been the cause of that change?

### IOC the three

Start the third IOC with the startup script `3.cmd`.

```console
[iocuser@host:cmds]$ iocsh 3.cmd
```

This script contains a fully working IOC, and so you should read through the
startup script carefully in order to understand what it is doing.

* How does this script use `E3_CMD_TOP`?
* What is the purpose of `random.bash` and `random.cmd` in this script?
* What is the *stream protocol* file?
* If you have your simulator running in another terminal, what do you notice
  about it?
* Try running the following commands in the IOC shell:

  ```console
  localhost-10414 > dbpf IOC-NNNNNNNN:SetTarget 100
  localhost-10414 > dbgf IOC-NNNNNNNN:State
  localhost-10414 > dbpf IOC-NNNNNNNN:Halt 1
  ```

### For the fourth

By now we have a functioning IOC which can communicate with our simulated
device. We would, however, generally want to tie more EPICS modules into that
IOC, for example `iocStats`, `autosave`, and `recsync`. For simplicity, let us
start with `iocStats`.

In order to load the functionality from one of these modules, we will need to
configure it. This is defined by some mix of `.db` files, `.dbd` files, and
others.

Execute the next script:

```console
[iocuser@host:cmds]$ iocsh 4.cmd
```

Start with typing `dbl` at the IOC prompt in order to see a full list of the
IOC's PVs. Within those PVs should be a *heartbeat* PV, named something like
`IOC-29051174:IocStat:HEARTBEAT`. Fetch its value:

```console
localhost-1593 > dbpr IOC-29051174:IocStat:HEARTBEAT
A   : 40            AMSG:               ASG :               B   : 0
C   : 0             CALC: (A<2147483647)?A+1:1              D   : 0
DESC: 1 Hz counter since startup        DISA: 0             DISP: 0
DISV: 1             DLYA: 0             E   : 0             F   : 0
G   : 0             H   : 0             I   : 0             J   : 0
K   : 0             L   : 0             NAME: IOC-29051174:IocStat:HEARTBEAT
NAMSG:              OCAL: 0             OEVT:               OVAL: 41
POVL: 41            PVAL: 41            SEVR: NO_ALARM      STAT: NO_ALARM
TPRO: 0             VAL : 41

```

Then fetch it
again.

* What does this represent? How can the heartbeat of the IOC, much like a real
  heartbeat, be used?
* Where does the file `iocAdminSoft.db` come from? Can you find it in your
  filesystem? Can you guess at how the file was found?

### Pleading the fifth

For this last IOC, we add in the other modules mentioned above, and modify how
we load the database file from `iocStats`.

```console
[iocuser@host:cmds]$ iocsh 5.cmd
```

* Can you see the how database file for `iocStats` is loaded? Is it the same
  database file as last time?

Run the following command to print your PVs, and inspect the output file:

```console
[iocuser@home:cmds]$ cd ..
[iocuser@home:4_startup_scripts_in_e3]$ bash ../tools/caget_pvs.bash -l IOC-NNNNNNNN_PVs.list
```

(where `NNNNNNNN` is your IOC's random number.)

---

## Assignments

1. What other parameters can be passed to `iocStats`, `recsync`, and `autosave`?
2. Are there any improvements that can be made to the last script, `5.cmd`?
3. Can you modify this script to communicate with more than one simulated device
   at the same time?
