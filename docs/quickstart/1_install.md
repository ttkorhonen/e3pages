# Installing e3

Building EPICS with the so-called *core* modules (to see what the various module groups contain, have a look at the [inventory](https://gitlab.esss.lu.se/e3/e3/-/blob/master/tools/e3-inventory.yaml)) using e3 is fairly easy. Note, however, that the workflow (and tools) listed below typically isn't what you would use for a production build.

## Prerequisites

You should start with a mostly blank CentOS 7 machine, and then install all the necessary packages via the following command.[^prereqlist]

```{include} ../includes/deps.md
```

:::{note}
Note that this package list is more than is strictly needed to install e3, but also contains the necessary packages for many of the e3 modules that are supported.
:::

## Building a local e3 environment

To build EPICS base 7.0.5 with *require* 3.4.1 and the *core* module group and install it at `/opt/epics`, you would only need to run (note `sudo` as we are installing to a subdirectory of `/opt` which generally is owned by `root`):

```console
[iocuser@host:~]$ git clone https://gitlab.esss.lu.se/e3/e3.git
[iocuser@host:~]$ cd e3
[iocuser@host:e3]$ ./e3_building_config.bash -b 7.0.5 -r 3.4.1 -t /opt/epics setup
[iocuser@host:e3]$ sudo ./e3.bash base
[iocuser@host:e3]$ sudo ./e3.bash req
[iocuser@host:e3]$ sudo ./e3.bash -c mod
```

:::{tip}
If you leave out the flags `-b` (version of EPICS base) and `-r` (version of *require*) it will default to the latest stable release, but it's always good practice to be explicit.
:::

As you may realise, this allows a user to have multiple EPICS trees installed at various locations.

## Sourcing a specific e3 environment

With e3, you may have several EPICS environments available, so you need to explicitly activate the e3 environment you intend to use.

```console
[iocuser@host:e3]$ source /path/to/epics/${EPICS_BASE_VERSION}/require/${REQUIRE_VERSION}/bin/setE3Env.bash
```

or, alternatively:

```console
[iocuser@host:e3]$ source /path/to/e3/repository/tools/setenv
```

## Installing an e3 module

To install an existing e3 module in *deployment mode*[^depmode], only a few steps are required. First clone the repository (we will use use the *caenelfastps* module for this example):

```console
[iocuser@host:e3]$ git clone https://gitlab.esss.lu.se/e3/ps/e3-caenelfastps.git
```

Next, modify `configure/RELEASE` to point towards the correct installation path. If you followed the above steps to install, it should look like the following:

```makefile
#
EPICS_BASE:=/opt/epics/base-7.0.5

E3_REQUIRE_NAME:=require
E3_REQUIRE_VERSION:=3.4.1

# The definitions shown below can also be placed in an untracked RELEASE.local
-include $(TOP)/../../RELEASE.local
-include $(TOP)/../RELEASE.local
-include $(TOP)/configure/RELEASE.local
```

:::{note}
Notice the change to `${EPICS_BASE}` from the default `/epics/base-7.0.5` to `/opt/epics/base-7.0.5`.
:::

Finally, we would run all of the make rules that: clones the submodule, applies patches (if there are any valid ones for this version), builds the module, and finally installs it;

```console
[iocuser@host:e3]$ cd e3-caenelfastps
[iocuser@host:e3-caenelfastps]$ make init patch build
[iocuser@host:e3-caenelfastps]$ sudo make install
```

We should finally validate that everything is working as expected:

```console
# this assumes you have sourced setenv or setE3Env.bash
[iocuser@host:e3-caenelfastps]$ iocsh.bash -r caenelfastps
```

Done!

:::{tip}
If you here wanted to use a different version of the module than the most recent one, you could simply check out a specific commit or tag of the wrapper, prior to running `make init`.
:::


[^prereqlist]: `ethercat-generic-dkms-1.5.2.ESS1-1` is an ESS internal package. It can be found at: <https://artifactory.esss.lu.se/artifactory/rpm-ics/centos/7/x86_64/>. For ESS internal users, this package can be installed the same way as installing standard CentOS packages. For external users, one will need to add this repository to package manager’s repository-search-list to install this package.
[^depmode]: More on this in the e3 tutorial.
