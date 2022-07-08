(debugging_e3)=

# Debugging e3

EPICS base comes with build system which creates two artifacts when for
x86_64 machines, one is the normal build with `-O3` optimization for production,
and another with GCC debugging option `-g` turned on to export debugging
symbols in the result object to facilitate debugging. With these, variable
and function names will be available when debugging with GDB or valgrind.

Inside `$EPICS_BASE/lib`  directory you'll see a `linux-x86_64-debug` artifact
if EPICS with debug options target was built. This default in for environments
4.0.0/7.0.6.1 onwards.

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
$ iocsh -dv -l='/path/to/myModule' -r myModule
```

It's possible to debug the EPICS base by calling iocsh under GDB without a
startup script or `-r` will run softIocPVA alone.

```console
$ iocsh -dv [--dvarg='any-valgrind-options']
```

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

It's possible to debug the EPICS base by calling iocsh under valgrind without a
startup script or `-r` will run softIocPVA alone.

```console
$ iocsh -dv [--dvarg='any-valgrind-options']
```
