# Installing e3

Building EPICS with "common modules" (to see what the various module groups contain, have a look at the [inventory](https://gitlab.esss.lu.se/e3/e3/-/blob/master/tools/e3-inventory.txt)) using e3 is fairly easy. Note, however, that the workflow (and tools) listed below typically isn't what you would do for a production build.

## Building a local e3 environment

To build EPICS base 7.0.4 with *require* 3.3.0 and the *common* module group and install it at `/opt/epics`, you would only need to run (note `sudo` as we are installing to a subdirectory of `/opt` which generally is owned by `root`):

```bash
$ git clone https://gitlab.esss.lu.se/e3/e3.git
$ cd e3
$ ./e3_building_config.bash -b 7.0.4 -r 3.3.0 -t /opt/epics setup
$ sudo ./e3.bash base
$ sudo ./e3.bash req
$ sudo ./e3.bash -c mod
```

For more information, see {ref}`e3_bash`

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

## Installing an e3 module

To install an existing e3 module in *deployment mode*[^depmode], only a few steps are required. First clone the repository (we will use use the *caenelfastps* for this example):

```bash
$ git clone https://gitlab.esss.lu.se/e3/ps/e3-caenelfastps.git
```

Next, modify `configure/RELEASE` to point towards the correct installation path. If you followed the above steps to install, it should like the following:

```makefile
#
EPICS_BASE:=/opt/epics/base-7.0.4

E3_REQUIRE_NAME:=require
E3_REQUIRE_VERSION:=3.3.0

# The definitions shown below can also be placed in an untracked RELEASE.local
-include $(TOP)/../../RELEASE.local
-include $(TOP)/../RELEASE.local
-include $(TOP)/configure/RELEASE.local
```

:::{note}
Notice the change to ${EPICS_BSAE} from the default `/epics/base-7.0.4` to `/opt/epics/base-7.0.4`.
:::

Finally, we would run all of the make rules that: clones the submodule, applies patches (if there are any valid ones for this version), build the module, and finally install it;

```
$ cd e3-caenelfastps
$ make init patch build
$ sudo make install
```

We should finally validate that everything is working as expected:

```bash
$ # this assumes you have sourced setenv or setE3Env.bash
$ iocsh.bash -r caenelfastps
```

Done!

:::{tip}
If you here wanted to use a different version of the module than the most recent one, you could simply check out a specific commit or tag.
:::


[^depmode]: More on this in the e3 tutorial.
