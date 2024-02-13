(debugging_e3)=

# Debugging e3

The e3 build system is configured to build two "architectures" for x86_64
machines: one is the normal linux-x86_64 with `-O3` optimization for production,
and another (linux-x86_64-debug) with GCC debugging option `-g` turned on to
export debugging symbols in the result object to facilitate debugging. With
these, variable and function names will be available when debugging with GDB or
valgrind.

Inside `$EPICS_BASE/lib`  directory you'll see a `linux-x86_64-debug` artifact
if EPICS with debug options target was built. This default in for environments
7.0.6.1/4.0.0 onwards.

## Using the debug artifact

Set your `EPICS_HOST_ARCH` variable

```console
$ export EPICS_HOST_ARCH=linux-x86_64-debug
```

Run iocsh using the `-dg` flag to start your IOC under GDB.

```console
$ iocsh -dg st.cmd
```

## Running an IOC withing GDB

The syntax to use the iocsh to start a GDB debugging session is:

```console
$ iocsh -dg [--dgarg='any-GDB-options'] st.cmd
```

Other GDB options can be passed using the `--dgarg=` optional argument.  Even in
with `-dg` other options as `-l` and `-r` works as expected. Which is an useful
way to debug modules.

```console
$ iocsh -dg -l='/path/to/myModule' -r myModule
```

It's possible to debug EPICS base by calling iocsh under GDB without a
startup script or `-r` will run softIocPVA alone.

```console
$ iocsh -dg [--dgarg='any-gdb-options']
```

### Adding breakpoints

To add breakpoints, you have two options.

* Break out of the IOC into gdb and add a breakpoint
* Start the IOC with a gdb startup script that defines the breakpoints

If you are trying to debug the IOC's behaviour at runtime, then the first option
works fine. If you want to debug anything during the IOC startup (or if you want
to set the same series of breakpoints regularly), then the second option is
best.

To break out of the IOC shell and back into gdb, simply type `^C`:

```console
$ iocsh -dg st.cmd
Warning: environment variable IOCNAME is not set.
███████╗██████╗     ██╗ ██████╗  ██████╗    ███████╗██╗  ██╗███████╗██╗     ██╗
██╔════╝╚════██╗    ██║██╔═══██╗██╔════╝    ██╔════╝██║  ██║██╔════╝██║     ██║
█████╗   █████╔╝    ██║██║   ██║██║         ███████╗███████║█████╗  ██║     ██║
██╔══╝   ╚═══██╗    ██║██║   ██║██║         ╚════██║██╔══██║██╔══╝  ██║     ██║
███████╗██████╔╝    ██║╚██████╔╝╚██████╗    ███████║██║  ██║███████╗███████╗███████╗
╚══════╝╚═════╝     ╚═╝ ╚═════╝  ╚═════╝    ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝

GNU gdb (GDB) Red Hat Enterprise Linux 7.6.1-120.el7
Copyright (C) 2013 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-redhat-linux-gnu".
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>...
Reading symbols from /epics/base-7.0.7/bin/linux-x86_64/softIocPVA...done.
Starting program: /epics/base-7.0.7/bin/linux-x86_64/softIocPVA -D /epics/base-7.0.7/dbd/softIocPVA.dbd /tmp/systemd-private-e3-iocsh-simonrose/tmp.ZKEYHfKzvv_iocsh_5.0.0-PID-16905
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".
[New Thread 0x7ffff4d3b700 (LWP 16930)]
[Thread 0x7ffff4d3b700 (LWP 16930) exited]
[Detaching after fork from child process 16931]

################ snip snip snip ################

iocInit
Starting iocInit
############################################################################
## EPICS R7.0.7-E3-7.0.7-patch
## Rev. 2023-01-30T16:37+0000
## Rev. Date build date/time:
############################################################################
[New Thread 0x7ffff7f63700 (LWP 16933)]
[New Thread 0x7ffff432d700 (LWP 16934)]
[New Thread 0x7ffff4d3b700 (LWP 16935)]

################ snip snip snip ################

[New Thread 0x7fffe5869700 (LWP 16960)]
[New Thread 0x7fffe5668700 (LWP 16961)]
[New Thread 0x7fffe5467700 (LWP 16962)]
16905 >
Program received signal SIGINT, Interrupt.
0x00007ffff58c3b5d in read () from /lib64/libc.so.6
Missing separate debuginfos, use: debuginfo-install glibc-2.17-326.el7_9.x86_64 libgcc-4.8.5-44.el7.x86_64 libstdc++-4.8.5-44.el7.x86_64 ncurses-libs-5.9-14.20130511.el7_4.x86_64 readline-6.2-11.el7.x86_64
(gdb)
```

From this point, you can then add breakpoints either at specific line numbers
or at function calls, and continue the IOC running:

```console
(gdb) b db_event_enable
Breakpoint 1 at 0x7ffff68da240: file ../db/dbEvent.c, line 520.
(gdb) c
Continuing
```

These breakpoint (or any other gdb commands) can be added to a script file to be
loaded at startup, and then run via

```console
$ iocsh -dg --dgarg="-x <command_file> --args" st.cmd
```

Note that `--args` is supplied by default, but needs to be supplied extra here.

For more information, see [gdb man page](https://man7.org/linux/man-pages/man1/gdb.1.html).

## Running an IOC under valgrind

In the same way as GDB, the `-dv` argument will startup the IOC under valgrind.
Using the optional `--dvarg=` it's possible to pass arguments for valgrind. The
argument `--leak-check=full` is enabled by default.

```console
$ iocsh -dv [--dvarg='valgrind-options'] st.cmd
```

Even in with `-dv` other options as `-l` and `-r` works as expected. Which is
useful way to debug modules.

```console
$ iocsh -dv -l='/path/to/myModule' -r myModule
```

It's possible to debug EPICS base by calling iocsh under valgrind without a
startup script or `-r` will run softIocPVA alone.

```console
$ iocsh -dv [--dvarg='any-valgrind-options']
```

## Debugging a core file

In case you want to debug a crash after it has happened, then we need to do two
things:

* Ensure that core dumps are being generated
* Use `gdb` to investigate the core dump

### Activating core dumps

In order to activate core dumps, you need to ensure that the `ulimit -c` is set
correctly. By default, this is set to 0 (do not produce core dumps), but it can
be changed simply by running

```console
$ ulimit -S -c unlimited
```

You can choose a smaller limit, but if you do the core dump files might be
truncated and thus miss some necessary data.

### Running gdb on a core dump file

Once a core file is generated, in order to expect you pass it as an argument to
`gdb`:

```console
$ gdb --core=path/to/core/file --exec=path/to/softIocPVA
```

Some clarifications:

* The core path is the location of the core file on disc. Depending on how you
  have your system configured, the core dump file could end up in the current
  working directory of the IOC, or possibly elsewhere; see
  [core](https://man7.org/linux/man-pages/man5/core.5.html) for more details.
* The path to `softIocPVA` is the location of the actual executable that was
  running the IOC. For example, if your e3 environment is located at
  `/opt/epics/base-7.0.7/require/5.0.0`, then you would pass
  `--exec=/opt/epics/base-7.0.7/bin/linux-x86_64/softIocPVA`. This is necessary
  in order to ensure that `gdb` knows what debug symbols to use.
