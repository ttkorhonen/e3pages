# 1. Installing e3

## Lesson overview

In this lesson, you'll learn how to do the following:

* Download e3 using git.
* Configure the e3 environment.
* Set up e3 EPICS base.
* Set up the e3 *require* module.
* Set up common e3 module packs.
* Test your installation.

:::{note}
This chapter teaches you how to create your own e3 environment from scratch. If
you are working with a pre-built e3 environment, then this chapter can be
skimmed or skipped.
:::

---

## Downloading e3

:::{note}
ESS' EPICS environment e3 is developed primarily for CentOS, and it is thus
recommended to use CentOS7 while working through this tutorial.
:::

:::{note}
As e3 heavily relies on git, it is recommended to first be familiar with git,
and especially git submodules.
:::

If you are on a mostly blank CentOS7 machine, you can copy, paste, and run the
following code segment before beginning. This will install all of the necessary
packages that are needed for the majority of EPICS modules that are in use with
e3.[^prereqpkg]

```{include} ../../../includes/deps.md
```

---

Start by downloading e3 from GitLab. For the purposes of this documentation, we
will be using v0.4.1 of e3.

```console
[iocuser@host:~]$ git clone --depth 1 --branch 0.4.1 https://gitlab.esss.lu.se/e3/e3.git
```

As e3 by design can have multiple different configurations in a host, it is
recommended to use self-explanatory source directory names. This will allow you
to easily switch between e.g. EPICS base versions 7.0.3.1 and 7.0.5 during
development. For example, if one would like to use EPICS base 7.0.3.1, then you
should clone it using:

```console
[iocuser@host:~]$ git clone --depth 1 --branch 0.4.1 https://gitlab.esss.lu.se/e3/e3.git e3-7.0.3.1
```

Throughout the tutorial, we will assume that the default version of EPICS base
is 7.0.5, which has been cloned in the directory `/home/iocuser/e3`. This path
will henceforth be referred to as **E3_TOP**.

Typical paths for EPICS installations tend to be `/epics` or `/opt/epics`. For
this tutorial series, e3 will be cloned to `$HOME` and EPICS will be installed
at `/epics`.

## Configure e3

Configuring an e3 build with default settings can be done like:

```console
[iocuser@host:e3]$ ./e3_building_config.bash setup
```

The utility can be launched with a number of arguments. To see these, simply run
the script without any arguments, i.e. `./e3_building_config.bash`; you can
modify the building path (e.g. `-t <path/to/install>`) as well as define
versions.

As always with EPICS, versions are important. Especially pay attention to:

* The version of EPICS base
* The version of *require*

---

Examples:

```console
[iocuser@host:e3]$ ./e3_building_config.bash -b 7.0.5 setup
>>
  The following configuration for e3 installation
  will be generated :

>> Set the global configuration as follows:
>>
  EPICS TARGET                     : /epics
  EPICS_BASE                       : /epics/base-7.0.5
  EPICS_BASE VERSION               : 7.0.5
  EPICS_MODULE_TAG                 : 7.0.5
  E3_REQUIRE_VERSION               : 3.4.1
  E3_REQUIRE_LOCATION              : /epics/base-7.0.5/require/3.4.1
  E3_CC_IFC14XX_TOOLCHAIN_PATH     : /opt/ifc14xx
  E3_CC_IFC14XX_TOOLCHAIN_VER      : 2.6-4.14
  E3_CC_POKY_TOOLCHAIN_PATH        : /opt/cct
  E3_CC_POKY_TOOLCHAIN_VER         : 2.6-4.14
```

```console
[iocuser@host:e3]$ ./e3_building_config.bash -b 7.0.5 -t /opt/epics setup
>>
  The following configuration for e3 installation
  will be generated :

>> Set the global configuration as follows:
>>
  EPICS TARGET                     : /opt/epics
  EPICS_BASE                       : /opt/epics/base-7.0.5
  EPICS_BASE VERSION               : 7.0.5
  EPICS_MODULE_TAG                 : 7.0.5
  E3_REQUIRE_VERSION               : 3.4.1
  E3_REQUIRE_LOCATION              : /opt/epics/base-7.0.5/require/3.4.1
  E3_CC_IFC14XX_TOOLCHAIN_PATH     : /opt/ifc14xx
  E3_CC_IFC14XX_TOOLCHAIN_VER      : 2.6-4.14
  E3_CC_POKY_TOOLCHAIN_PATH        : /opt/cct
  E3_CC_POKY_TOOLCHAIN_VER         : 2.6-4.14
```

## Global e3 environment settings

Configuring EPICS per above directions will generate the following three
`*.local` files.

* `CONFIG_BASE.local`

  ```bash
  E3_EPICS_PATH:=/epics
  EPICS_BASE_TAG:=tags/R7.0.5
  E3_BASE_VERSION:=7.0.5
  E3_CC_IFC14XX_TOOLCHAIN_PATH:=/opt/ifc14xx
  E3_CC_IFC14XX_TOOLCHAIN_VER:=2.6-4.14
  E3_CC_POKY_TOOLCHAIN_PATH:=/opt/cct
  E3_CC_POKY_TOOLCHAIN_VER:=2.6-4.14
  ```

* `RELEASE.local`

  ```bash
  EPICS_BASE:=/epics/base-7.0.5
  E3_REQUIRE_NAME:=require
  E3_REQUIRE_VERSION:=3.4.1
  ```

* `REQUIRE_CONFIG_MODULE.local`

  ```bash
  EPICS_MODULE_TAG:=tags/3.4.1
  ```

These will help us to change base, require, and all modules' configuration
without having to change any source files.

:::{note}
Modifying versions in the `*.local` files above will override versions listed in
the module configuration files.
:::

## Building and installing EPICS base and require

For EPICS base and *require*, it is as simple as running:

```console
[iocuser@host:e3]$ ./e3.bash base
```

```console
[iocuser@host:e3]$ ./e3.bash req
```

Remember to run these with elevated status (`sudo`) if you want to install in
`/opt`.

## Module packs

As with installing EPICS base and *require*, you can use the `e3.bash` utility
to install certain module groups. Note that the groupings themselves are
somewhat arbitrary and based on the judgement of the e3 team.

* core (c)
* communication (n)
* ts (t)
* psi (p)
* ifc (i)
* ecat (e)
* area (a)
* ps (s)
* devices
* vac (v)
* rf (l)
* bi (b)
* mps (m)

To see the contents of any of these groups, you can run

```console
[iocuser@host:e3]$ ./e3.bash -<groups> vars
```

where `<groups>` are in brackets next to the names. Some examples of the groups
are shown in the following sections; run the command with the other groups to
see all of what they contain.

### Core group

This group contains the common EPICS modules, and is more or less a standard
install; nearly every other group depends on at least one module in this group,
so you will need to install at least some of this group before you can install
any other groups. Note that there are a few ESS-specific modules in here, most
notably `e3-auth` and `e3-essioc`.

```console
[iocuser@host:e3]$ ./e3.bash -c vars
>> Vertical display for the selected modules :

 Modules List
    0 : core/e3-auth
    1 : core/e3-autosave
    2 : core/e3-caPutLog
    3 : core/e3-asyn
    4 : core/e3-busy
    5 : core/e3-seq
    6 : core/e3-sscan
    7 : core/e3-std
    8 : core/e3-calc
    9 : core/e3-iocStats
   10 : core/e3-pcre
   11 : core/e3-stream
   12 : core/e3-recsync
   13 : core/e3-essioc
   14 : core/e3-MCoreUtils
   15 : core/e3-nds3
   16 : core/e3-nds3epics
   17 : core/e3-devlib2
```

### Communication group

This group contains those EPICS modules that are used for communication with
specific devices and device types.

```console
[iocuser@host:e3]$ bash e3.bash -n vars
>> Vertical display for the selected modules :

 Modules List
    0 : core/e3-auth
    1 : core/e3-autosave
    2 : core/e3-caPutLog
    3 : core/e3-asyn
    4 : core/e3-busy
    5 : core/e3-seq
    6 : core/e3-sscan
    7 : core/e3-std
    8 : core/e3-calc
    9 : core/e3-iocStats
   10 : core/e3-pcre
   11 : core/e3-stream
   12 : core/e3-recsync
   13 : core/e3-essioc
   14 : core/e3-MCoreUtils
   15 : core/e3-nds3
   16 : core/e3-nds3epics
   17 : core/e3-devlib2
   18 : communication/e3-modbus
   19 : communication/e3-ipmiComm
   20 : communication/e3-motor
   21 : communication/e3-ip
   22 : communication/e3-delaygen
   23 : communication/e3-s7plc
   24 : communication/e3-opcua
   25 : communication/e3-mca
   26 : communication/e3-snmp
```

:::{note}
Note that this includes a duplication of the core modules: this is due to the
fact that this module group depends on the core group as stated above. If you
want to see only those modules that are from this group, you should add the `-o`
flag like

```console
[iocuser@host:e3]$ bash e3.bash -no vars
>> Vertical display for the selected modules :
Modules List
   0 : communication/e3-modbus
   1 : communication/e3-ipmiComm
   2 : communication/e3-motor
   3 : communication/e3-ip
   4 : communication/e3-delaygen
   5 : communication/e3-s7plc
   6 : communication/e3-opcua
   7 : communication/e3-mca
   8 : communication/e3-snmp
```

:::

### AreaDetector Group

This group contains the necessary modules to work with camera-type sensors. This
group also depends on the **core** group.

```console
[iocuser@host:e3]$ ./e3.bash -ao vars
>> Vertical display for the selected modules :

 Modules List
    0 : area/e3-ADSupport
    1 : area/e3-ADCore
    2 : area/e3-ADSimDetector
    3 : area/e3-ADCSimDetector
    4 : area/e3-NDDriverStdArrays
    5 : area/e3-ADAndor
    6 : area/e3-ADAndor3
    7 : area/e3-ADPointGrey
    8 : area/e3-ADProsilica
    9 : area/e3-ADGenICam
   10 : area/e3-ADPluginEdge
   11 : area/e3-ADPluginCalib
```

### Downloading and installing a group

You download, build, and install a group by using the `mod` argument (as in
**mod**ules). For example:

To install the core group:

```console
[iocuser@host:e3]$ ./e3.bash -c mod
```

To install the core, timing, and area detector groups

```console
[iocuser@host:e3]$ ./e3.bash -ctao mod
```

### Options

The mod argument contain these - individually accessible - steps:

* `cmod`: Clean
* `gmod`: Clone
* `imod`: Initiate
* `bmod`: Build and install

And the *makefile* rules that can be used for a module are:

* `make clean` - Cleans the temporary build files which are placed in the `O.*`
  directories.
* `make init` - Initialises (clones and checks out) the underlying EPICS module
* `make patch` - Applies any site-specific patches to the underlying EPICS
  module.
* `make build` - Builds the module (but does not install it)
* `make install` - Installs the built module including performing any specified
  database expansion.

The full installation sequence for building an e3 module is `make init patch
build install`. To see a more complete list of possible targets, simply type
`make` or `make help` within a module's wrapper directory.

### Test your installation

:::{note}
This does not work correctly in e3 0.4.1 due to the capitalisation of
`EPICS_MODULE_NAME` for a few of the modules.
:::

The following command will load all installed modules within a single
`iocsh.bash`. If, after executing `e3.bash -c load`, you see a clear console
prompt (`>`), you have successfully installed e3 on the host.

```console
[iocuser@host:e3]$ ./e3.bash -c load

# --- snip snip ---

require: fillModuleListRecord
require: REQMOD-791F5F3:FAISERV-21664:MODULES[0] = "require"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[0] = "3.0.5"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="require    3.0.5"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[1] = "ess"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[1] = "0.0.1"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="ess        0.0.1"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[2] = "iocStats"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[2] = "ae5d083"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="iocStats   ae5d083"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[3] = "autosave"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[3] = "5.9.0"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="autosave   5.9.0"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[4] = "caPutLog"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[4] = "3.6.0"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="caPutLog   3.6.0"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[5] = "asyn"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[5] = "4.33.0"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="asyn       4.33.0"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[6] = "busy"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[6] = "1.7.0"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="busy       1.7.0"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[7] = "modbus"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[7] = "2.11.0p"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="modbus     2.11.0p"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[8] = "ipmiComm"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[8] = "4.2.0"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="ipmiComm   4.2.0"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[9] = "sequencer"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[9] = "2.2.6"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="sequencer  2.2.6"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[10] = "sscan"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[10] = "1339922"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="sscan      1339922"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[11] = "std"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[11] = "3.5.0"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="std        3.5.0"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[12] = "ip"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[12] = "2.19.1"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="ip         2.19.1"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[13] = "calc"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[13] = "3.7.1"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="calc       3.7.1"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[14] = "delaygen"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[14] = "1.2.0"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="delaygen   1.2.0"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[15] = "pcre"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[15] = "8.41.0"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="pcre       8.41.0"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[16] = "stream"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[16] = "2.8.8"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="stream     2.8.8"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[17] = "s7plc"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[17] = "1.4.0p"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="s7plc      1.4.0p"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[18] = "recsync"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[18] = "1.3.0"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="recsync    1.3.0"
require: REQMOD-791F5F3:FAISERV-21664:MODULES[19] = "MCoreUtils"
require: REQMOD-791F5F3:FAISERV-21664:VERSIONS[19] = "1.2.1"
require: REQMOD-791F5F3:FAISERV-21664:MOD_VER+="MCoreUtils 1.2.1"
iocRun: All initialization complete
791f5f3.faiserv.21660 >
```

---

## Assignments

1. Develop some understanding of how GNU Make and Makefiles work. The standard
   reference for GNU make is
   [here](https://www.gnu.org/software/make/manual/html_node/index.html).
2. Develop some understanding of how git submodules work.
3. How are git submodules are used in e3?
4. Install both EPICS base 7.0.3.1 and 7.0.5 (separately) on your host.
5. See if you can find where the module groups are specified, and try to figure
   out how you could change these.

[^prereqpkg]: `ethercat-generic-dkms-1.5.2.ESS1-1` is an ESS internal package.
  It can be found at:
  <https://artifactory.esss.lu.se/artifactory/rpm-ics/centos/7/x86_64/>. For ESS
  internal users, this package can be installed the same way as installing
  standard CentOS packages. For external users, one will need to add this
  repository to package manager’s repository-search-list to install this
  package.
