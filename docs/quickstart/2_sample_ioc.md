# An e3 IOC

The following assumes that you already have EPICS base, *require* (`3.3.0` or later as the module version has been left out in the `require` call[^require]), and *iocStats* installed.

An IOC in e3 is typically (minimally) just a startup script---passed to `softIocPVA`[^epics7]---preferably also with an `env.sh` file to define environment variables (such as `${IOCNAME}`, and/or the architecture and versions to be used when calling `iocsh.bash` using macros).

## Create the startup script

A very minimal startup script to illustrate what "a typical" IOC in e3 looks like:

```bash
$ touch st.cmd
$ echo "require iocstats" >> st.cmd  # iocInit() is called implicitly
```

## Start the IOC

```bash
$ ./opt/epics/base-7.0.4/require/3.3.0/bin/iocsh.bash st.cmd
```

:::{tip}
With macros set in an environment file, you could instead do something like:

```bash
$ source env.sh
$ ./epics/${BASE_VERSION}/require/${REQUIRE_VERSION}/bin/iocsh.bash st.cmd
```
:::

## Conventions

As mentioned above, there should be an `env.sh` together with the startup script, that at minimum defines the `$IOCNAME`. There should preferably also be a `README.md` documenting the controlled hardware, the host machine (if the IOC is running in a lab), etc., and the IOC should be version controlled in the proper [subgroup](https://gitlab.esss.lu.se/ioc).

Thus you may end up with something like the following:

### Directory

```bash
$ tree e3-ioc-test
e3-ioc-test
├── README.md
├── env.sh
└── st.cmd
```

### Startup script (`st.cmd`)

```bash
$ cat st.cmd
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

```sh
$ cat env.sh
IOCNAME="SomeName"
```


[^require]: In version 3.3.0 of *require*, version pinning became optional; i.e., from `require MODULE,MODULE_VERSION` to `require MODULE[,MODULE_VERSION]`.

[^epics7]: ESS only uses EPICS base 7 for production, and thus only uses `softIocPVA`. Earlier iterations of e3 also supported use of `softIoc`, but that functionality has been removed from scope.
