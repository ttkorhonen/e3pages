# Installing e3

Building a core e3 installation using standard tools is relatively straightforward.
To see which modules are included in such an installation, see the contents of
[2022q1-core](https://gitlab.esss.lu.se/e3/specifications/-/blob/main/specifications/2022q1-core.yml);
more information will be provided below.

## Prerequisites

You should start with a mostly blank CentOS 7 machine, and then install all the
necessary packages via the following command.[^prereqlist]

```{include} ../includes/deps.md
```

:::{note}
Note that this package list is more than is strictly needed to install e3, but
also contains the necessary packages for many of the e3 modules that are
supported.
:::

## Building a local e3 environment

It is possible to build an e3 environment by hand by cloning and building the
necessary repositories ([e3-base](https://gitlab.esss.lu.se/e3/e3-base),
[e3-require](https://gitlab.esss.lu.se/e3/e3-require), followed by all of the
appropriate modules). This will require some custom configuration to ensure that
all of the versions and dependencies match up.

The prefered way of building an e3 environment is to use the *specification handler*,
which allows you to build a predefined environment by using a *specification*.

### Installing the specification handler

The specification handler is distributed on artifactory at ESS, and can be installed
via

```console
[iocuser@host:~]$ pip3 install --user e3 -i https://artifactory.esss.lu.se/artifactory/api/pypi/pypi-virtual/simple
```

One can also clone and install the specification handler directly:

```console
[iocuser@host:~]$ git clone https://gitlab.esss.lu.se/e3/e3.git
[iocuser@host:~]$ cd e3
[iocuser@host:e3]$ pip3 install --user .
```

### Selecting a specification

The specifications are stored in the repository [specifications](https://gitlab.esss.lu.se/e3/specifications).
The latest environment built at ESS is [2022q1-full](https://gitlab.esss.lu.se/e3/specifications/-/blob/main/specifications/2022q1-full.yml),
while a smaller environment which is more likely suitable for a local installation is found
at [2022q1-core](https://gitlab.esss.lu.se/e3/specifications/-/blob/main/specifications/2022q1-core.yml).

These files will look something like the following.

```yaml
config:
  base_version: 7.0.6.1-NA/7.0.6.1-ff3e2c9-20220209T143845
  require_version: 7.0.6.1-4.0.0/4.0.0-9b692d5-20220209T160204
meta:
  datestamp: 20220210T112407
modules:
  adcore:
    versions:
    - 7.0.6.1-4.0.0/3.10.0+2-52add63-20220210T112321
  adsupport:
    versions:
    - 7.0.6.1-4.0.0/1.9.0-c4b8ff4-20220210T112319
  ...
```

They contain information including which version of EPICS base to install (7.0.6.1),
which version of require to install (4.0.0), as well as a list of modules to install
into that environment.

These can be built (assuming you have installed the specification handler as above) via
```console
[iocuser@host:specifications]$ e3-build -t /opt/epics specifications/2022q1-core.yml
```
assuming that you would like to build your local environment at `/opt/epics`. Note
that you will need to have permission to write to this location, which may necessitate
the use of `sudo`.

## Sourcing a specific e3 environment

It is possible to have several e3 installations available (either at different root
locations, or with different versions of EPICS base or require). You need to explicitly
activate the e3 environment you intend to use:

```console
[iocuser@host:~]$ source /path/to/epics/${EPICS_BASE_VERSION}/require/${REQUIRE_VERSION}/bin/setE3Env.bash
```

If you installed the above specification at `/opt/epics`, then this would be

```console
[iocuser@host:~]$ source /opt/epics/7.0.6.1/require/4.0.0/bin/setE3Env.bash
```

## Installing an e3 module

To install an existing e3 module in *deployment mode*,[^depmode] only a few
steps are required. First clone the repository (we will use use the
[*caenelfastps*](https://gitlab.esss.lu.se/e3/ps/e3-caenelfastps) module for
this example):

```console
[iocuser@host:e3]$ git clone https://gitlab.esss.lu.se/e3/ps/e3-caenelfastps.git
```

Next, modify `configure/RELEASE` to point towards the correct installation path.
If you followed the above steps to install, it should look like the following:

```makefile
EPICS_BASE:=/opt/epics/base-7.0.6.1

E3_REQUIRE_NAME:=require
E3_REQUIRE_VERSION:=4.0.0

# The definitions shown below can also be placed in an untracked RELEASE.local
-include $(TOP)/../../RELEASE.local
-include $(TOP)/../RELEASE.local
-include $(TOP)/configure/RELEASE.local
```

:::{note}
Notice the change to `${EPICS_BASE}` from the default `/epics/base-7.0.6.1` to `/opt/epics/base-7.0.6.1`.
:::

Finally, we would run each of the make rules that clone the submodule, apply
patches (if there are any valid ones for this version), build the module, and
finally install it:

```console
[iocuser@host:e3]$ cd e3-caenelfastps
[iocuser@host:e3-caenelfastps]$ make init patch build
[iocuser@host:e3-caenelfastps]$ sudo make install
```

We should finally validate that everything is working as expected:

```console
# this assumes you have sourced setenv or setE3Env.bash
[iocuser@host:e3-caenelfastps]$ iocsh -r caenelfastps
```

Done!

:::{tip}
If you here wanted to use a different version of the module than the most recent
one, you could simply check out a specific commit or tag of the wrapper, prior
to running `make init`.
:::

[^prereqlist]: `ethercat-generic-dkms-1.5.2.ESS1-1` is an ESS internal package.
  It can be found at:
  <https://artifactory.esss.lu.se/artifactory/rpm-ics/centos/7/x86_64/>. For ESS
  internal users, this package can be installed the same way as installing
  standard CentOS packages. For external users, one will need to add this
  repository to package manager’s repository-search-list to install this
  package.

[^depmode]: More on this in the e3 tutorial.
