# 13. Working with conda and e3

In this lesson, you'll learn how to do the following:

* Create a simple environment with epics.
* Install new packages.
* Create different environments for other epics versions.
* Create, build and install an e3 module in a conda environment.
* Create and build locally a e3-recipe

:::{note}
This chapter contains detailed information as to work with conda and e3.
If you intend to work only with e3 environment, then this chapter can be skipped.
:::

## Quickstart

Conda is used to package and deploy e3 modules.

To work with e3, the only requirement is to have conda installed and configured
to use the `conda-e3-virtual` channel on Artifactory.  Please refer to the
[conda requirements](12_conda_environment.md).

As explained in the
[user-guide](https://conda.io/projects/conda/en/latest/user-guide/concepts.html),
a conda environment is just a directory that contains a specific collection of
conda packages that you have installed. You could have one environment with
EPICS base 7 and another one with EPICS base 3. You can easily switch between
environments (by activating or deactivating them). When installing packages in
an environment, others are not impacted. To avoid conflicts, conda ensures that
there is only one version of each package in an environment.

To create an environment with EPICS base 7 and *stream*, run:

```console
[iocuser@host:~]$ conda create -y -n epics epics-base=7 stream
# --- snip snip ---

The following NEW packages will be INSTALLED:

  _libgcc_mutex      conda-e3-virtual/linux-64::_libgcc_mutex-0.1-conda_forge
  _openmp_mutex      conda-e3-virtual/linux-64::_openmp_mutex-4.5-0_gnu
  asyn               conda-e3-virtual/linux-64::asyn-4.43.0-h3f0f509_0
  calc               conda-e3-virtual/linux-64::calc-3.7.4-h0e1289a_0
  epics-base         conda-e3-virtual/linux-64::epics-base-7.0.7-h68659b9_2
  libgcc-ng          conda-e3-virtual/linux-64::libgcc-ng-9.3.0-h2828fa1_19
  libgomp            conda-e3-virtual/linux-64::libgomp-9.3.0-h2828fa1_19
  libstdcxx-ng       conda-e3-virtual/linux-64::libstdcxx-ng-9.3.0-h6de172a_19
  libusb             conda-e3-virtual/linux-64::libusb-1.0.22-he1b5a44_0
  ncurses            conda-e3-virtual/linux-64::ncurses-6.1-hf484d3e_1002
  pcre               conda-e3-virtual/linux-64::pcre-8.45-h9c3ff4c_0
  perl               conda-e3-virtual/linux-64::perl-5.26.2-h516909a_1006
  readline           conda-e3-virtual/linux-64::readline-8.0-hf8c457e_0
  require            conda-e3-virtual/linux-64::require-5.0.0-h426397f_5
  sequencer          conda-e3-virtual/linux-64::sequencer-2.2.9-h910a07a_1
  sscan              conda-e3-virtual/linux-64::sscan-2.11.5-hdc5059e_2
  stream             conda-e3-virtual/linux-64::stream-2.8.24-hbceeb4b_0
  # --- snip snip ---
```

Note tconda will automatically select the latest version of `epics-base`
from the conda-e3-virtual channel. This selection will be made in a manner
that ensures compatibility with the rest of the packages, including,
for example, the `stream` package.

As you see, it will download all the required dependencies to install the
requested packages. To start working in this environment, just activate it. The
name of the active environment will be displayed in your prompt. You can then
run `iocsh`.

```console
[iocuser@host:~]$ conda activate epics
(epics) [iocuser@host:~]$ iocsh -r stream
Warning: environment variable IOCNAME is not set.
███████╗██████╗     ██╗ ██████╗  ██████╗    ███████╗██╗  ██╗███████╗██╗     ██╗
██╔════╝╚════██╗    ██║██╔═══██╗██╔════╝    ██╔════╝██║  ██║██╔════╝██║     ██║
█████╗   █████╔╝    ██║██║   ██║██║         ███████╗███████║█████╗  ██║     ██║
██╔══╝   ╚═══██╗    ██║██║   ██║██║         ╚════██║██╔══██║██╔══╝  ██║     ██║
███████╗██████╔╝    ██║╚██████╔╝╚██████╗    ███████║██║  ██║███████╗███████╗███████╗
╚══════╝╚═════╝     ╚═╝ ╚═════╝  ╚═════╝    ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝

# Start at "2024-W06-feb09-0955-52-CET"
# European Spallation Source ERIC : iocsh (5.0.0-PID-90020)
#
############################################################################
##  Shell and environment variables
############################################################################
# PWD = "/home/iocuser"
# USER = "iocuser"
# LOGNAME = "iocuser"
# PATH = "/home/iocuser/miniconda/envs/epics/epics/bin/linux-x86_64:/home/iocuser/miniconda/envs/epics/bin:/home/iocuser/.local/bin:/opt/conda/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin"
#
############################################################################
##  EPICS variables
############################################################################
# EPICS_BASE = "/home/iocuser/miniconda/envs/epics/epics"
# EPICS_HOST_ARCH = "linux-x86_64"
# EPICS_DRIVER_PATH = "/home/iocuser/miniconda/envs/epics/modules"
# EPICS_CA_AUTO_ADDR_LIST = ""
# EPICS_CA_ADDR_LIST = "127.255.255.255 172.30.38.20"
# EPICS_PVA_AUTO_ADDR_LIST = ""
# EPICS_PVA_ADDR_LIST = ""
#
############################################################################
##  e3-specific variables
############################################################################
# E3_REQUIRE_VERSION = "5.0.0"
# E3_REQUIRE_LOCATION = "/home/iocuser/miniconda/envs/epics/modules/require/5.0.0"
# E3_REQUIRE_BIN = "/home/iocuser/miniconda/envs/epics/bin"
# E3_REQUIRE_DB = "/home/iocuser/miniconda/envs/epics/modules/require/5.0.0/db"
# E3_REQUIRE_DBD = "/home/iocuser/miniconda/envs/epics/modules/require/5.0.0/dbd"
# E3_REQUIRE_INC = "/home/iocuser/miniconda/envs/epics/modules/require/5.0.0/include"
# E3_REQUIRE_LIB = "/home/iocuser/miniconda/envs/epics/modules/require/5.0.0/lib"
#
############################################################################
##  IOC startup commands
############################################################################
# // Set REQUIRE_IOC for its internal PVs
epicsEnvSet REQUIRE_IOC "REQMOD:skywalker-90020"
#
# // Set E3_IOCSH_TOP for the absolute path where iocsh is executed.
epicsEnvSet E3_IOCSH_TOP "/home/iocuser"
#
# // Load require module, version 5.0.0
#
dlload /home/iocuser/miniconda/envs/epics/modules/require/5.0.0/lib/linux-x86_64/librequire.so
dbLoadDatabase /home/iocuser/miniconda/envs/epics/modules/require/5.0.0/dbd/require.dbd
require_registerRecordDeviceDriver
Loading module info records for require
#
require stream
Module stream version 2.8.24 found in /home/iocuser/miniconda/envs/epics/modules/stream/2.8.24/
Module stream depends on asyn 4.43.0
Module asyn version 4.43.0 found in /home/iocuser/miniconda/envs/epics/modules/asyn/4.43.0/
Loading library /home/iocuser/miniconda/envs/epics/modules/asyn/4.43.0/lib/linux-x86_64/libasyn.so
Loaded asyn version 4.43.0
Loading dbd file /home/iocuser/miniconda/envs/epics/modules/asyn/4.43.0/dbd/asyn.dbd
Calling function asyn_registerRecordDeviceDriver
Loading module info records for asyn
Module stream depends on calc 3.7.4
Module calc version 3.7.4 found in /home/iocuser/miniconda/envs/epics/modules/calc/3.7.4/
Module calc depends on sequencer 2.2.9
Module sequencer version 2.2.9 found in /home/iocuser/miniconda/envs/epics/modules/sequencer/2.2.9/
Loading library /home/iocuser/miniconda/envs/epics/modules/sequencer/2.2.9/lib/linux-x86_64/libsequencer.so
Loaded sequencer version 2.2.9
sequencer has no dbd file
Loading module info records for sequencer
Module calc depends on sscan 2.11.5
Module sscan version 2.11.5 found in /home/iocuser/miniconda/envs/epics/modules/sscan/2.11.5/
Module sscan depends on sequencer 2.2.9
Module sequencer version 2.2.9 already loaded
Loading library /home/iocuser/miniconda/envs/epics/modules/sscan/2.11.5/lib/linux-x86_64/libsscan.so
Loaded sscan version 2.11.5
Loading dbd file /home/iocuser/miniconda/envs/epics/modules/sscan/2.11.5/dbd/sscan.dbd
Calling function sscan_registerRecordDeviceDriver
Loading module info records for sscan
Loading library /home/iocuser/miniconda/envs/epics/modules/calc/3.7.4/lib/linux-x86_64/libcalc.so
Loaded calc version 3.7.4
Loading dbd file /home/iocuser/miniconda/envs/epics/modules/calc/3.7.4/dbd/calc.dbd
Calling function calc_registerRecordDeviceDriver
Loading module info records for calc
Loading library /home/iocuser/miniconda/envs/epics/modules/stream/2.8.24/lib/linux-x86_64/libstream.so
Loaded stream version 2.8.24
Loading dbd file /home/iocuser/miniconda/envs/epics/modules/stream/2.8.24/dbd/stream.dbd
Calling function stream_registerRecordDeviceDriver
Loading module info records for stream
# // Set the IOC Prompt String
epicsEnvSet IOCSH_PS1 "90020 > "
#
iocInit
Starting iocInit
############################################################################
## EPICS R7.0.7
## Rev. 2023-05-02T11:44+0000
## Rev. Date build date/time:
############################################################################
drvStreamInit: Warning! STREAM_PROTOCOL_PATH not set.
iocRun: All initialization complete
90020 >
```

Once you are in an environment you can install new packages or change the
version of the installed packages. Let's add *iocstats* and *recsync* to our epics
environment:

```console
(epics) [iocuser@host:~]$ conda install iocstats recsync
Collecting package metadata (repodata.json): done
Solving environment: done

## Package Plan ##

  environment location: /home/iocuser/miniconda/envs/epics

    added / updated specs:
    - iocstats
    - recsync

The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    iocstats-3.1.16            |      h910a07a_11          94 KB  conda-e3-virtual
    recsync-1.5.0              |       h910a07a_0          65 KB  conda-e3-virtual
    ------------------------------------------------------------
                                           Total:         160 KB

The following NEW packages will be INSTALLED:

  iocstats           conda-e3-virtual/linux-64::iocstats-3.1.16-h910a07a_11
  recsync            conda-e3-virtual/linux-64::recsync-1.5.0-h910a07a_0
```

`conda list` will show you the list of installed packages in the environment:

```console
(epics) [iocuser@host:~]$ conda list
# packages in environment at /home/iocuser/miniconda/envs/epics:
#
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                 conda_forge    conda-e3-virtual
_openmp_mutex             4.5                       0_gnu    conda-e3-virtual
asyn                      4.43.0               h3f0f509_0    conda-e3-virtual
calc                      3.7.4                h0e1289a_0    conda-e3-virtual
epics-base                7.0.7                h68659b9_2    conda-e3-virtual
iocstats                  3.1.16              h910a07a_11    conda-e3-virtual
libgcc-ng                 9.3.0               h2828fa1_19    conda-e3-virtual
libgomp                   9.3.0               h2828fa1_19    conda-e3-virtual
libstdcxx-ng              9.3.0               h6de172a_19    conda-e3-virtual
libusb                    1.0.22               he1b5a44_0    conda-e3-virtual
ncurses                   6.1               hf484d3e_1002    conda-e3-virtual
pcre                      8.45                 h9c3ff4c_0    conda-e3-virtual
perl                      5.26.2            h516909a_1006    conda-e3-virtual
readline                  8.0                  hf8c457e_0    conda-e3-virtual
recsync                   1.5.0                h910a07a_0    conda-e3-virtual
require                   5.0.0                h426397f_5    conda-e3-virtual
sequencer                 2.2.9                h910a07a_1    conda-e3-virtual
sscan                     2.11.5               hdc5059e_2    conda-e3-virtual
stream                    2.8.24               hbceeb4b_0    conda-e3-virtua
```

Let's say you want to switch to another version of stream. You could
create a new environment or just replace the version installed in this one. You
can search for available versions by running `conda search`:

```console
(epics) [iocuser@host:~]$ conda search stream
Loading channels: done
# Name                       Version           Build  Channel
stream                        2.8.10      h2feebe4_0  conda-e3-virtual
stream                        2.8.10      hbaf0b60_1  conda-e3-virtual
stream                        2.8.22      h74e095f_2  conda-e3-virtual
stream                        2.8.22      ha977fd6_2  conda-e3-virtual
stream                        2.8.24      hbceeb4b_0  conda-e3-virtual
```

Let's switch to `2.8.10`

```console
(epics) [iocuser@host:~]$ conda install stream=2.8.10
Collecting package metadata (repodata.json): done
Solving environment: done

## Package Plan ##

  environment location: /home/iocuser/miniconda/envs/epics

  added / updated specs:
    - stream=2.8.10


The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    asyn-4.41.0                |      hceeaaa5_10         1.1 MB  conda-e3-virtual
    calc-3.7.1                 |       h6ca1cf9_3         365 KB  conda-e3-virtual
    epics-base-7.0.5.0         |       h68659b9_4        28.6 MB  conda-e3-virtual
    iocstats-3.1.16            |       h2c1926d_5          92 KB  conda-e3-virtual
    recsync-1.3.0.post1        |       h60aecf9_1          59 KB  conda-e3-virtual
    require-3.1.3              |       h9bea806_1         114 KB  conda-e3-virtual
    seq-2.2.7                  |       h60aecf9_1         378 KB  conda-e3-virtual
    sscan-2.11.2               |       h44690a7_1         288 KB  conda-e3-virtual
    stream-2.8.10              |       hbaf0b60_1         498 KB  conda-e3-virtual
    ------------------------------------------------------------
                                           Total:        31.5 MB

The following NEW packages will be INSTALLED:

  seq                conda-e3-virtual/linux-64::seq-2.2.7-h60aecf9_1

The following packages will be REMOVED:

  sequencer-2.2.9-h910a07a_1

The following packages will be DOWNGRADED:

  asyn                                    4.43.0-h3f0f509_0 --> 4.41.0-hceeaaa5_10
  calc                                     3.7.4-h0e1289a_0 --> 3.7.1-h6ca1cf9_3
  epics-base                               7.0.7-h68659b9_2 --> 7.0.5.0-h68659b9_4
  iocstats                               3.1.16-h910a07a_11 --> 3.1.16-h2c1926d_5
  recsync                                  1.5.0-h910a07a_0 --> 1.3.0.post1-h60aecf9_1
  require                                  5.0.0-h426397f_5 --> 3.1.3-h9bea806_1
  sscan                                   2.11.5-hdc5059e_2 --> 2.11.2-h44690a7_1
  stream                                  2.8.24-hbceeb4b_0 --> 2.8.10-hbaf0b60_1

```

Let's now create a separate environment with EPICS Base `3.15`. Note that this is
only as an example. EPICS Base  3 isn't supported anymore at ESS. You should use
EPICS 7.  This is to demonstrate you can work on separate environments with
different EPICS Base  version.

```console
(epics) [iocuser@host:~]$ conda create -y -n epics3 epics-base=3 iocstats
Collecting package metadata (repodata.json): done
Solving environment: done

## Package Plan ##

  environment location: /home/iocuser/miniconda/envs/epics3

  added / updated specs:
    - epics-base=3
    - iocstats
# --- snip snip ---

The following NEW packages will be INSTALLED:

  _libgcc_mutex      conda-e3-virtual/linux-64::_libgcc_mutex-0.1-conda_forge
  _openmp_mutex      conda-e3-virtual/linux-64::_openmp_mutex-4.5-0_gnu
  epics-base         conda-e3-virtual/linux-64::epics-base-3.15.6-h68659b9_0
  iocstats           conda-e3-virtual/linux-64::iocstats-3.1.15.post1-h666eb74_0
  libgcc-ng          conda-e3-virtual/linux-64::libgcc-ng-9.3.0-h2828fa1_19
  libgomp            conda-e3-virtual/linux-64::libgomp-9.3.0-h2828fa1_19
  libstdcxx-ng       conda-e3-virtual/linux-64::libstdcxx-ng-9.3.0-h6de172a_19
  ncurses            conda-e3-virtual/linux-64::ncurses-6.1-hf484d3e_1002
  perl               conda-e3-virtual/linux-64::perl-5.26.2-h516909a_1006
  readline           conda-e3-virtual/linux-64::readline-8.0-hf8c457e_0
  require            conda-e3-virtual/linux-64::require-3.1.0-h4714b6a_0
  tclx               conda-e3-virtual/linux-64::tclx-8.4.1-h628b354_2
  tk                 conda-e3-virtual/linux-64::tk-8.6.10-hed695b0_0
  zlib               conda-e3-virtual/linux-64::zlib-1.2.11-h516909a_1006
```

Switch to this new environment:

```console
(epics) [iocuser@host:~]$ conda deactivate
[iocuser@host:~]$ conda activate epics3
(epics3) [iocuser@host:~]$ conda list
# packages in environment at /home/iocuser/miniconda/envs/epics3:
#
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                 conda_forge    conda-e3-virtual
_openmp_mutex             4.5                       0_gnu    conda-e3-virtual
epics-base                3.15.6               h68659b9_0    conda-e3-virtual
iocstats                  3.1.15.post1         h666eb74_0    conda-e3-virtual
libgcc-ng                 9.3.0               h2828fa1_19    conda-e3-virtual
libgomp                   9.3.0               h2828fa1_19    conda-e3-virtual
libstdcxx-ng              9.3.0               h6de172a_19    conda-e3-virtual
ncurses                   6.1               hf484d3e_1002    conda-e3-virtual
perl                      5.26.2            h516909a_1006    conda-e3-virtual
readline                  8.0                  hf8c457e_0    conda-e3-virtual
require                   3.1.0                h4714b6a_0    conda-e3-virtual
tclx                      8.4.1                h628b354_2    conda-e3-virtual
tk                        8.6.10               hed695b0_0    conda-e3-virtual
zlib                      1.2.11            h516909a_1006    conda-e3-virtual
```

We saw earlier that you can check if a package exists using `conda search`. If
the given name doesn't exist, conda will try to find a match using wildcard:

```console
[iocuser@host:~]$ conda search iocstat
Loading channels: done
No match found for: iocstat. Search: *iocstat*
# Name                       Version           Build  Channel
iocstats                3.1.15.post1      h0f5667f_0  conda-e3-virtual
# --- snip snip ---
iocstats                3.1.15.post1      hd2b67a6_0  conda-e3-virtual
iocstats                3.1.15.post1      he422a75_0  conda-e3-virtual
iocstats                3.1.15.post1      hf85dc0c_0  conda-e3-virtual
iocstats                      3.1.16      h76d1a4d_1  conda-e3-virtual
iocstats                      3.1.16      hd2b67a6_0  conda-e3-virtual
```

You can get more information about a package and its dependencies with the `-i` flag:

```console
[iocuser@host:~]$ conda search iocstat -i
iocstats 3.1.15.post1 h0f5667f_0
--------------------------------
file name   : iocstats-3.1.15.post1-h0f5667f_0.tar.bz2
name        : iocstats
version     : 3.1.15.post1
build       : h0f5667f_0
build number: 0
size        : 82 KB
license     : EPICS Open License
subdir      : linux-64
url         : https://artifactory.esss.lu.se/artifactory/api/conda/conda-e3-virtual/linux-64/iocstats-3.1.15.post1-h0f5667f_0.tar.bz2
md5         : d70d9f3b626b3718ef853f368a4080ee
timestamp   : 2019-03-20 14:27:19 UTC
dependencies:
  - epics-base >=3.15.5,<3.15.6.0a0
  - libgcc-ng >=7.3.0
  - libstdcxx-ng >=7.3.0
  - require >=3.1.0,<3.2.0a0

# --- snip snip ---

iocstats 3.1.16 h910a07a_11
--------------------------
file name   : iocstats-3.1.16-h910a07a_11.tar.bz2
name        : iocstats
version     : 3.1.16
build       : h910a07a_11
build number: 11
size        : 94 KB
license     : EPICS Open License
subdir      : linux-64
url         : https://artifactory.esss.lu.se/artifactory/api/conda/conda-e3-virtual/linux-64/iocstats-3.1.16-h910a07a_11.tar.bz2
md5         : a541cc0b58e5da469ee55cda6ca165ba
timestamp   : 2023-09-08 14:13:29 UTC
dependencies:
  - epics-base >=7.0.7,<7.0.8.0a0
  - libgcc-ng >=7.3.0
  - libstdcxx-ng >=7.3.0
  - require >=5.0.0,<5.1.0a0
```

You can see above that the first package was compiled with EPICS Base  `3.15.5` and
the last with EPICS Base  `7.0.7`.

Note that conda package names are always **lowercase**. When searching or
installing a package, conda is case-insensitive. Running `conda install
iocStats` or `conda install iocstats` will perform exactly the same operation.
But when using a module with require, you should use the lowercase name:

```console
(epics3) [iocuser@host:~]$ iocsh.bash
# --- snip snip ---
8ef3d5671aef.3038 > require iocStats
Module iocStats not available
8ef3d5671aef.3038 > require iocstats
Module iocstats version 3.1.15 found in /home/iocuser/miniconda/envs/epics3/modules/iocstats/3.1.15/
Loading library /home/iocuser/miniconda/envs/epics3/modules/iocstats/3.1.15/lib/linux-x86_64/libiocstats.so
Loaded iocstats version 3.1.15
Loading dbd file /home/iocuser/miniconda/envs/epics3/modules/iocstats/3.1.15/dbd/iocstats.dbd
Calling function iocstats_registerRecordDeviceDriver
```

## e3 module creation

e3 uses [*require*](https://gitlab.esss.lu.se/epics-modules/require), originally
developed by [PSI](https://github.com/paulscherrerinstitute/require) to
dynamically load modules at runtime. The *require* also includes a
[driver.Makefile](https://gitlab.esss.lu.se/epics-modules/require/-/blob/master/App/tools/driver.makefile)
that shall be used to build a module.  This requires a specific `{module_name}.Makefile`
file that includes this `driver.Makefile`.

To make it easy to create a new e3 module, we provide a cookiecutter template.

## Create the e3 module

Use the `e3-module` alias to create a new module (refer to [cookiecutter_configuration]
to create this alias).  You'll be prompted to enter some values
Press enter to keep the default.

```console
[iocuser@host:dev]$ e3-module
You've downloaded /home/iocuser/.cookiecutters/cookiecutter-e3-module before. Is it okay to delete and re-download it? [yes]: yes
company [European Spallation Source ERIC]:
module_name [mymodule]: foo
full_name [Your name]: John Doe
email [john.doe@ess.eu]:
documentation_page [https://confluence.esss.lu.se/display/IS/Integration+by+ICS]:
Select keep_epics_base_makefiles:
1 - N
2 - Y
Choose from 1, 2 [1]: 2
```

This will create a new module. You can reach the same behavior generating a
template using `makeBaseApp.pl` from EPICS base.

```console
[iocuser@host:dev]$ tree foo/
foo/
├── cmds
│   └── st.cmd
├── configure
│   ├── CONFIG
│   ├── CONFIG_SITE
│   ├── Makefile
│   ├── RELEASE
│   ├── RULES
│   ├── RULES_DIRS
│   ├── RULES.ioc
│   └── RULES_TOP
├── fooApp
│   ├── Db
│   │   └── Makefile
│   ├── Makefile
│   └── src
│       ├── fooMain.cpp
│       └── Makefile
├── foo.Makefile
├── iocsh
│   └── foo.iocsh
├── LICENSE
├── Makefile
├── README.md
└── RELEASE.md
```

Notice the `foo.Makefile` file, this is the main file used to
build and install a conda e3 module.  The standard `Makefile`
allows you to compile the module using the default EPICS build
system if you want. BHowever, to maintain the e3-module as closely
as possible to the EPICS vanilla mode, it is advisable to include
`foo.Makefile` in the `.gitignore` file.

## Update the module

Include the necessary files in your module and ensure that you update
the `foo.Makefile` file in accordance with the new changes or updates made
to your module.

## Compile the module

To compile an e3 module in a conda environment, the following packages are
required:

* `make`
* `compilers`
* `tclx`
* `epics-base`
* `require`

Create the `e3-dev` environment with those packages.  If you have other
depencies, like `asyn`, install them as well.

```console
[iocuser@host:dev]$ conda create -y -n e3-dev epics-base require compilers make tclx
Collecting package metadata (repodata.json): done
Solving environment: done
# --- snip snip ---
```

Activate the `e3-dev` environment and compile your module.
Note that when using the make command, it is essential to specify the MODULE name.
Additionally, you have the option to specify the version; if omitted, the require
command will automatically generate the version as `dev`.

```console
[iocuser@host:dev]$ conda activate e3-dev
(e3-dev) [iocuser@host:dev]$ cd foo
(e3-dev) [iocuser@host: foo]$ make -f foo.Makefile MODULE=foo
MAKING EPICS VERSION 7.0.7
mkdir -p O.7.0.7_Common
make -f foo.Makefile T_A=linux-x86_64 build
make[1]: Entering directory '/home/iocuser/dev/foo'
mkdir -p O.7.0.7_linux-x86_64
make[2]: Entering directory '/home/iocuser/dev/foo/O.7.0.7_linux-x86_64'
/home/iocsuser/miniconda/envs/e3-dev/bin/x86_64-conda_cos6-linux-gnu-g++  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET           -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall              -mtune=generic              -m64  -fPIC          -I. -I../fooApp/src/ -I/home/iocsuser/miniconda/envs/e3-dev/modules/require/5.0.0/include -I/home/iocsuser/miniconda/envs/e3-dev/epics/include -I/home/iocsuser/miniconda/envs/e3-dev/epics/include/compiler/gcc -I/home/iocsuser/miniconda/envs/e3-dev/epics/include/os/Linux              -I/home/iocsuser/miniconda/envs/e3-dev/include           -c  ../fooApp/src/fooMain.cpp
echo "char _fooLibRelease[] = \"dev\";" >> foo_version_dev.c
/home/iocsuser/miniconda/envs/e3-dev/bin/x86_64-conda_cos6-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET           -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration              -mtune=generic     -m64  -fPIC           -I. -I../fooApp/src/ -I/home/iocsuser/miniconda/envs/e3-dev/modules/require/5.0.0/include -I/home/iocsuser/miniconda/envs/e3-dev/epics/include -I/home/iocsuser/miniconda/envs/e3-dev/epics/include/compiler/gcc -I/home/iocsuser/miniconda/envs/e3-dev/epics/include/os/Linux              -I/home/iocsuser/miniconda/envs/e3-dev/include           -c foo_version_dev.c
Collecting dependencies
rm -f foo.dep.tmp
cat *.d 2>/dev/null | sed 's/ /\n/g' | sed -n 's%/home/iocsuser/miniconda/envs/e3-dev/modules/*\([^/]*\)/\([0-9]*\.[0-9]*\.[0-9]*\)/.*%\1 \2%p;s%/home/iocsuser/miniconda/envs/e3-dev/modules/*\([^/]*\)/\([^/]*\)/.*%\1 \2%p'| grep -v "include" | sort -u > foo.dep.tmp
cat foo.dep.tmp | sort -u >> foo.dep
/home/iocsuser/miniconda/envs/e3-dev/bin/x86_64-conda_cos6-linux-gnu-g++ -o libfoo.so  -shared -fPIC -Wl,-hlibfoo.so -L/home/iocsuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64 -Wl,-rpath,/home/iocsuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64                  -rdynamic -m64 -Wl,--disable-new-dtags -Wl,-rpath,/home/iocsuser/miniconda/envs/e3-dev/lib -Wl,-rpath-link,/home/iocsuser/miniconda/envs/e3-dev/lib -L/home/iocsuser/miniconda/envs/e3-dev/lib -Wl,-rpath-link,/home/iocsuser/miniconda/envs/e3-dev/epics/lib/linux-x86_64                   fooMain.o foo_version_dev.o      -lpthread    -lm -lrt -ldl -lgcc
make[2]: Leaving directory '/home/iocuser/dev/foo/O.7.0.7_linux-x86_64'
make[1]: Leaving directory '/home/iocuser/dev/foo'
```

If you have some database to generate, run `make -f foo.Makefile MODULE=foo db_internal`.
In our case, we don't have any template, so the command won't do anything.

```console
(e3-dev) [iocuser@host: foo]$ make -f foo.Makefile MODULE=foo db_internal
make: Nothing to be done for 'db_internal'.
```

Install the module in the current environment.

```console
(e3-dev) [iocuser@host: foo]$ make -f foo.Makefile MODULE=foo install
MAKING EPICS VERSION 7.0.7
make -f foo.Makefile T_A=linux-x86_64 install
make[1]: Entering directory '/home/iocuser/dev/foo'
make[2]: Entering directory '/home/iocuser/dev/foo/O.7.0.7_linux-x86_64'
Collecting dependencies
rm -f foo.dep.tmp
cat *.d 2>/dev/null | sed 's/ /\n/g' | sed -n 's%/home/iocuser/miniconda/envs/e3-dev/modules/*\([^/]*\)/\([0-9]*\.[0-9]*\.[0-9]*\)/.*%\1 \2%p;s%/home/iocuser/miniconda/envs/e3-dev/modules/*\([^/]*\)/\([^/]*\)/.*%\1 \2%p'| grep -v "include" | sort -u > foo.dep.tmp
cat foo.dep.tmp | sort -u >> foo.dep
make[2]: Leaving directory '/home/iocuser/dev/foo/O.7.0.7_linux-x86_64'
make[2]: Entering directory '/home/iocuser/dev/foo/O.7.0.7_linux-x86_64'
Collecting dependencies
rm -f foo.dep.tmp
cat *.d 2>/dev/null | sed 's/ /\n/g' | sed -n 's%/home/iocuser/miniconda/envs/e3-dev/modules/*\([^/]*\)/\([0-9]*\.[0-9]*\.[0-9]*\)/.*%\1 \2%p;s%/home/iocuser/miniconda/envs/e3-dev/modules/*\([^/]*\)/\([^/]*\)/.*%\1 \2%p'| grep -v "include" | sort -u > foo.dep.tmp
cat foo.dep.tmp | sort -u >> foo.dep
Installing scripts ../iocsh/foo.iocsh to /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev
perl -CSD /home/iocuser/miniconda/envs/e3-dev/epics/bin/linux-x86_64/installEpics.pl  -d -m755 ../iocsh/foo.iocsh /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev
mkdir /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev
Installing module library /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64/libfoo.so
perl -CSD /home/iocuser/miniconda/envs/e3-dev/epics/bin/linux-x86_64/installEpics.pl  -d -m755 libfoo.so /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64
mkdir /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/lib
mkdir /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64
Installing module dependency file /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64/foo.dep
perl -CSD /home/iocuser/miniconda/envs/e3-dev/epics/bin/linux-x86_64/installEpics.pl  -d -m644 foo.dep /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64
make[2]: Leaving directory '/home/iocuser/dev/foo/O.7.0.7_linux-x86_64'
make[1]: Leaving directory '/home/iocuser/dev/foo'
```

The module was installed as _dev_ version.  You can check that you can load it:

```console
(e3-dev) [iocuser@host:foo]$ iocsh -r foo
# --- snip snip ---
require foo
Module foo version dev found in /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/
Loading library /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64/libfoo.so
Loaded foo version dev
foo has no dbd file
Loading module info records for foo
# --- snip snip ---
```

You can also use the `cmds/st.cmd` file to test your module.

```console
(e3-dev) [iocuser@host:foo]$ iocsh.bash cmds/st.cmd
# --- snip snip ---
iocshLoad 'cmds/st.cmd',''
# This should be a test startup script
require foo
Module foo version dev found in /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/
Loading library /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64/libfoo.so
Loaded foo version dev
foo has no dbd file
Loading module info records for foo
iocshLoad("/home/iocuser/miniconda/envs/e3-dev/modules/foo/dev//foo.iocsh")
# --- snip snip ---
```

You can uninstall the module by running `make -f foo.Makefile uninstall`.

```console
(e3-dev) [iocuser@host:foo]$ make -f foo.Makefile MODULE=foo uninstall
rm -rf /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev
```

During development, you can modify your code, re-compile and re-install as many
times as you want:

```console
make -f foo.Makefile MODULE=foo uninstall
make -f foo.Makefile MODULE=foo
make -f foo.Makefile MODULE=foo db_internal
make -f foo.Makefile MODULE=foo install
```

## Upload the module to GitLab

You should upload your module to <https://gitlab.esss.lu.se/epics-modules>

To distribute your module, you need to package it with conda.

## e3 recipe creation

To package a module with conda, you have to create a conda recipe.

Use the `e3-recipe` alias to create a new recipe (refer to
[cookiecutter_configuration] to create this alias).  You'll be prompted to
enter some values. Press enter to keep the default.

:::note
You can use your own module, as created above or earlier if you have uploaded
it to your own repository. Here we use `fakemodule` as a working example.
:::

```console
[iocuser@host:dev]$ e3-recipe
company [European Spallation Source ERIC]:
module_name [mymodule]: fakemodule
summary [EPICS fakemodule module]:
module_home [https://gitlab.esss.lu.se/epics-modules]:
module_version [1.0.0]:
```

The `module_home` variable shall point to the group in GitLab where your module
is stored.

This will create the following project:

```console
[iocuser@host:dev]$ tree fakemodule-recipe/
fakemodule-recipe/
├── LICENSE
├── README.md
├── recipe
│   ├── build.sh
│   └── meta.yaml
└── src
    └── fakemodule.Makefile
```

## Update the recipe

Typically, you should only need to update the `recipe/meta.yaml` and the
`fakemodule.Makefile` files.

### meta.yaml

The `meta.yaml` file is the file that defines the recipe.  It describes where to
get the source of the module and the dependencies to build and run the modules.
The file contains many hints in comments. Follow them and remove them when
you've finalized your recipe.

```{note}
The final recipe shouldn't contain any comments!
```

### module.Makefile

The `module.Makefile` should have the same content of the epics-module
`module.Makefile` that you used before in the build/install development stage.

## Build the recipe

To build the recipe, run:

```console
[iocuser@host:foo-recipe]$ conda build recipe
```

In case of failure, check the error message and update your `meta.yaml` file.

If the build was successful, you should see something like that:

````bash
# --- snip snip ---
TEST END: /home/iocuser/miniconda/conda-bld/linux-64/foo-1.0.0-hbd7620e_0.tar.bz2
Renaming work directory,  /home/iocuser/miniconda/conda-bld/foo_1591215967088/work  to  /home/iocuser/miniconda/conda-bld/foo_1591215967088/work_moved_foo-1.0.0-hbd7620e_0_linux-64_main_build_loop
# Automatic uploading is disabled
# If you want to upload package(s) to anaconda.org later, type:

anaconda upload /home/iocuser/miniconda/conda-bld/linux-64/foo-1.0.0-hbd7620e_0.tar.bz2

# To have conda build upload to anaconda.org automatically, use
# $ conda config --set anaconda_upload yes

anaconda_upload is not set.  Not uploading wheels: []
####################################################################################
Resource usage summary:

Total time: 0:00:07.2
CPU usage: sys=0:00:00.0, user=0:00:00.0
Maximum memory usage observed: 2.4M
Total disk usage observed (not including envs): 52B


####################################################################################<<<<<<<<<<<<<<<<s>>>>>>>>>>>>>>>>
````

## Test the built package

You can install the package you built locally by using the `-c local` argument
(to use the local channel).

```console
[iocuser@host:foo-recipe]$ conda create -y -n test -c local foo
# --- snip snip ---
The following NEW packages will be INSTALLED:

  foo                home/iocuser/miniconda/conda-bld/linux-64::foo-1.0.0-hbd7620e_0
# --- snip snip ---
```

Activate your test environment and test your package.

## Upload the recipe to GitLab

Upload your recipe to <https://gitlab.esss.lu.se/e3-recipes>.
GitLab CI will automatically build it and provide the necessary job action
to release the package into the conda-e3-channel in the Artifactory.

[cookiecutter_configuration]: 12_conda_environment.md#cookiecutter
