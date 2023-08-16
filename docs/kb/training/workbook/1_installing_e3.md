# 1. Installing e3

It's recommended to first read the [design documents](../../../design/1_intro.md)
before following this training.

## Lesson overview

In this lesson, you'll learn how to do the following:

* Download e3 from the ESS artifactory using pip.
* Install an e3 environment using `e3-build`
* Test your installation

:::{note}
This chapter teaches you how to install an e3 environment from a specification.
If you are working with a pre-built e3 environment, then this chapter can be
skimmed or skipped.
:::

---

## Downloading e3

:::{note}
ESS' EPICS environment e3 is developed primarily for CentOS, and it is thus
recommended to use CentOS7 while working through this tutorial. Note that e3
cannot currently be natively installed for Windows or MacOS.
:::

:::{note}
As e3 heavily relies on git, it is recommended to first be familiar with git,
and especially [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules).
:::

If you are on a mostly blank CentOS7 machine, you can copy, paste, and run the
following code segment before beginning. This will install all of the necessary
packages that are needed for the majority of EPICS modules that are in use with
e3.[^prereqpkg]

```{include} ../../../includes/deps.md
```

---

Start by downloading e3 from the artifactory.

```console
[iocuser@host:~]$ pip3 install --user e3 -i https://artifactory.esss.lu.se/artifactory/api/pypi/pypi-virtual/simple
```

This will install a number of utilities, most importantly `e3-build` which will
allow you to install an e3 environment on your local machine.

## Selecting a specification

An e3 environment is described using a *specification*. This is a file that contains
references to a version of EPICS base, *require*, and a collection of modules to
install. These are intended to provide a mechanism to build consistent and reproducible
environments that can be shared between different users and sites. These files will
look something like the following.

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

One can obtain the official specifications used at ESS by cloning the following
[repository](https://gitlab.esss.lu.se/e3/specifications.git):

```console
[iocuser@host:~]$ git clone https://gitlab.esss.lu.se/e3/specifications.git
```

The latest environment is `specifications/2022q1.yml`.

## Building an e3 environment

:::{note}
You can install epics where you want. The normal side-wide location is `/epics`
which the rest of the tutorial expects as the location. For user installs
`~/epics` is a better location.
:::

To build EPICS run the following command.

```console
[iocuser@host:specifications]$ e3-build -t ~/epics specifications/2022q1.yml
```

EPICS base takes some time to build, so once you have run the above command,
it is a good time to go and get a coffee.

## Sourcing and testing the built environment

Once the environment is built, you can activate the environment (similar to
activating a python virtual environment or a conda environment) using the
shell script `setE3Env.bash` which is installed with the new environment.

```console
[iocuser@host:~]$ source /epics/base-7.0.6.1/require/4.0.0/bin/setE3Env.bash

Set the ESS EPICS Environment as follows:
THIS Source NAME    : setE3Env.bash
THIS Source PATH    : /epics/base-7.0.6.1/require/4.0.0/bin
EPICS_BASE          : /epics/base-7.0.6.1
EPICS_HOST_ARCH     : linux-x86_64
E3_REQUIRE_LOCATION : /epics/base-7.0.6.1/require/4.0.0
PATH                : /epics/base-7.0.6.1/require/4.0.0/bin:/epics/base-7.0.6.1/bin/linux-x86_64:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/iocuser/.local/bin:/home/iocuser/bin
LD_LIBRARY_PATH     : /epics/base-7.0.6.1/lib/linux-x86_64:/epics/base-7.0.6.1/require/4.0.0/lib/linux-x86_64

Enjoy E3!
```

You can now test that this worked by starting an IOC:

```console
[iocuser@host:~]$ iocsh
# --- snip snip ---

# Set REQUIRE_IOC for its internal PVs
epicsEnvSet REQUIRE_IOC "REQMOD:host-15636"
#
# Enable an exit subroutine for sotfioc
dbLoadRecords "/epics/base-7.0.6.1/db/softIocExit.db" "IOC=REQMOD:host-15636"
#
# Set E3_IOCSH_TOP for the absolute path where iocsh is executed.
epicsEnvSet E3_IOCSH_TOP "/home/iocuser/specifications"
#
#
# Load require module, which has the version 4.0.0
#
dlload /epics/base-7.0.6.1/require/4.0.0/lib/linux-x86_64/librequire.so
dbLoadDatabase /epics/base-7.0.6.1/require/4.0.0/dbd/require.dbd
require_registerRecordDeviceDriver
Loading module info records for require
#
# Set the IOC Prompt String One
epicsEnvSet IOCSH_PS1 "host-15636 > "
#
#
iocInit
Starting iocInit
############################################################################
## EPICS R7.0.6.1-E3-7.0.6.1-patch
## Rev. 2022-03-09T15:26+0100
############################################################################
iocRun: All initialization complete
host-15636 >
```

Exit the IOC by typing `exit` at the console.

You can see which modules and versions have been installed by running

```console
[iocuser@host:~]$ ls /epics/base-7.0.6.1/require/4.0.0/siteMods/*
/epics/base-7.0.6.1/require/4.0.0/siteMods/adcore:
3.12.1+0

/epics/base-7.0.6.1/require/4.0.0/siteMods/adsupport:
1.10.0+0

/epics/base-7.0.6.1/require/4.0.0/siteMods/asyn:
4.42.0+0

# --- snip snip ---
```

You can test any of these modules by running, for example,

```console
[iocuser@host:~]$ iocsh -r asyn
```

---

## Assignments

1. Develop some understanding of how
  [GNU Make](https://www.gnu.org/software/make/manual/html_node/index.html)
  and Makefiles work.
2. Develop some understanding of how git submodules work.
3. How are git submodules are used in e3?
4. Install both EPICS base `7.0.5` and `7.0.6.1` (separately) on your host
   using two of the specifications included.

[^prereqpkg]: `ethercat-generic-dkms-1.5.2.ESS1-1` is an ESS internal package.
  It can be found at:
  <https://artifactory.esss.lu.se/artifactory/rpm-ics/centos/7/x86_64/>. For ESS
  internal users, this package can be installed the same way as installing
  standard CentOS packages. For external users, one will need to add this
  repository to package manager’s repository-search-list to install this
  package.
