# Quickstart

Building EPICS with "common modules" (to see what the various module groups contain, have a look at the [inventory](https://gitlab.esss.lu.se/e3/e3/-/blob/master/tools/e3-inventory.txt)) using e3 is fairly easy. Note, however, that the workflow (and tools) listed below typically isn't what you would do for a production build.

## Building a local e3 environment

To build EPICS base 7.0.4 with *require* 3.3.0 and the *common* module group and install it at `/opt/epics`, you would only need to run (note `sudo` as we are installing to a subdirectory of `/opt` which generally is owned by `root`):

```bash
$ git clone https://gitlab.esss.lu.se/e3/e3.git
$ cd e3
$ ./e3_building_config.bash -b 7.0.4 -r 3.3.0 -t /opt/epics
$ sudo ./e3.bash base
$ sudo ./e3.bash req
$ sudo ./e3.bash -c mod
```

:::{tip}
If you leave out the flags `-b` (version of EPICS base) and `-r` (version of *require*) it will default to the latest stable release, but it's always good practice to be explicit.
:::

As you may realise, this allows a user to have multiple EPICS trees installed at various locations.

## Sourcing a specific e3 environment

As you with e3 may have several EPICS "environments" available, you need to explicitly source your environment or call on binaries (such as `iocsh.bash`) explicitly.

```bash
$ source /path/to/epics/${EPICS_BASE_VERSION}/require/${REQUIRE_VERSION}/bin/setE3Env.bash
```

or, alternatively:

```bash
$ source /path/to/e3/repository/tools/setenv
```
