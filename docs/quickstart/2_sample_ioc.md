# An e3 IOC

The following assumes that you already have EPICS base, *require* (`3.3.0` or later as the module version has been left out in the `require` call[^require]), and *iocStats* installed.

An IOC in e3 is typically (minimally) just a startup script which is passed to `softIocPVA`[^epics7].

## Create the startup script

A very minimal startup script to illustrate what "a typical" IOC in e3 looks like:

```console
[iocuser@host:~]$ touch st.cmd
[iocuser@host:~]$ echo "require iocstats" >> st.cmd  # iocInit() is called implicitly
```

## Start the IOC

```console
[iocuser@host:~]$ /opt/epics/base-7.0.5/require/3.4.1/bin/iocsh.bash st.cmd
```

## Conventions

To set correct PV-names, the environment variable `$IOCNAME` must be set before starting your IOC. Up until *require* 3.4.1, this could be done in a file `env.sh` which needed to be in the same directory as your startup script. For later versions of require, the variable must be set through other mechanisms (where the easiest option is to just write `export IOCNAME=yourIocName` prior to starting the IOC).

There should preferably also be a `README.md` documenting the controlled hardware, the host machine (if the IOC is running in a lab), etc., and the IOC should be version controlled in the proper [subgroup](https://gitlab.esss.lu.se/ioc).

Thus you may end up with something like the following:

### Directory

```console
[iocuser@host:~]$ tree e3-ioc-test
e3-ioc-test
├── README.md
├── env.sh  # depending on the version of require you are using
└── st.cmd
```

### Startup script (`st.cmd`)

```console
[iocuser@host:~]$ cd e3-ioc-test
[iocuser@host:e3-ioc-test]$ cat st.cmd
require common
require module

epicsEnvSet(${IOCNAME},                 "${IOCNAME:NoName}")

iocshLoad(${module_DIR}snippet.iocsh,   "IOCNAME=${IOCNAME})

iocInit()

dbl > PVs.list
date
```

:::{note}
Note that `st.cmd` must end with a newline---this will be explained in {ref}`the_require_module`.
:::

### Environment file (`env.sh`)

```console
[iocuser@host:e3-ioc-test]$ cat env.sh
export IOCNAME="SomeName"
```


[^require]: In version 3.3.0 of *require*, version pinning became optional; i.e., from `require MODULE,MODULE_VERSION` to `require MODULE[,MODULE_VERSION]`.

[^epics7]: ESS only uses EPICS base 7 for production, and thus only uses `softIocPVA`. Earlier iterations of e3 also supported use of `softIoc`, but that functionality has been removed from scope.
