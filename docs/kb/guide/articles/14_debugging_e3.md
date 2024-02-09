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