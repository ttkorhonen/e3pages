# Installing e3

Building a core e3 installation using standard tools is relatively straightforward.
To see which modules are included in such an installation, see the contents of
[2022q1](https://gitlab.esss.lu.se/e3/specifications/-/blob/main/specifications/2022q1.yml);
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
The latest environment built at ESS is [2023q1](https://gitlab.esss.lu.se/e3/specifications/-/blob/main/specifications/2023q1.yml).
For a local installation, you will likely want to trim down this list manually,
to reduce the size of the installation.

These files will look something like the following.

```yaml
config:
  base: 7.0.7-NA/7.0.7-37d472c-20221216T170326
  require: 7.0.7-5.0.0/5.0.0-6a40805-20230130T100914
metadata:
  type: specification
  version: 1
modules:
  adandor:
    versions:
    - 7.0.7-5.0.0/2.8.0-6f3a1f4+1-319be25-20230130T150218
    - 7.0.7-5.0.0/2.8.0-6f3a1f4+2-9ef4e0d-20230810T151940
  adandor3:
    versions:
    - 7.0.7-5.0.0/2.2.0-6030b0b+1-67d79f9-20230130T150255
  adcore:
    versions:
    - 7.0.7-5.0.0/3.12.1+2-50b90f0-20230130T131903
  ...
```

They contain information including which version of EPICS base to install (7.0.7),
which version of require to install (5.0.0), as well as a list of modules to install
into that environment.

These can be built (assuming you have installed the specification handler as above)

```console
[iocuser@host:specifications]$ e3-build -t /opt/epics specifications/2023q1.yml
```

assuming that you would like to build your local environment at `/opt/epics`. Note
that you will need to have permission to write to this location, which may necessitate
the use of `sudo`.

## Sourcing a specific e3 environment

It is possible to have several e3 installations available (either at different root
locations, or with different versions of EPICS base or require). You need to explicitly
activate the e3 environment you intend to use:

```console
[iocuser@host:~]$ source /path/to/epics/${EPICS_BASE_VERSION}/require/${REQUIRE_VERSION}/bin/activate
```

:::{note}
The script `activate` was called `setE3Env.bash` up until require 4.0.0.
:::

If you installed the above specification at `/opt/epics`, then this would be

```console
[iocuser@host:~]$ source /opt/epics/7.0.7/require/5.0.0/bin/activate
```

## Installing an e3 module

To install an existing e3 module, only a few steps are required. First clone the
repository (we will use use the [*caenelfastps*](https://gitlab.esss.lu.se/e3/ps/e3-caenelfastps)
module for this example):

```console
[iocuser@host:e3]$ git clone https://gitlab.esss.lu.se/e3/ps/e3-caenelfastps.git
```

Next, modify `configure/RELEASE` to point towards the correct installation path.
If you followed the above steps to install, it should look like the following:

```makefile
EPICS_BASE:=/opt/epics/base-7.0.7

E3_REQUIRE_NAME:=require
E3_REQUIRE_VERSION:=5.0.0

# The definitions shown below can also be placed in an untracked RELEASE.local
-include $(TOP)/../../RELEASE.local
-include $(TOP)/../RELEASE.local
-include $(TOP)/configure/RELEASE.local
```

:::{note}
Notice the change to `${EPICS_BASE}` from the default `/epics/base-7.0.7` to `/opt/epics/base-7.0.7`.
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
# this assumes you have sourced the environment
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
