# E3 quickstart

Conda is used to package and deploy E3 modules.

To work with E3, the only requirement is to have conda installed and configured
to use the `conda-e3-virtual` channel on Artifactory.  Please refer to the
[conda requirements](../references/requirements.md).

As explained in the
[user-guide](https://conda.io/projects/conda/en/latest/user-guide/concepts.html),
a conda environment is just a directory that contains a specific collection of
conda packages that you have installed. You could have one environment with
epics-base 7 and another one with epics-base 3.15. You can easily switch between
environments (by activating or deactivating them). When installing packages in
an environment, others are not impacted. To avoid conflicts, conda ensures that
there is only one version of each package in an environment.

To create an environment with epics-base 7 and stream, run:

```bash
[csi@8ef3d5671aef ~]$ conda create -y -n epics epics-base=7 stream
...

The following NEW packages will be INSTALLED:

  _libgcc_mutex      conda-e3-virtual/linux-64::_libgcc_mutex-0.1-conda_forge
  _openmp_mutex      conda-e3-virtual/linux-64::_openmp_mutex-4.5-0_gnu
  asyn               conda-e3-virtual/linux-64::asyn-4.41.0-h0468fb3_10
  calc               conda-e3-virtual/linux-64::calc-3.7.1-h3f5c933_3
  epics-base         conda-e3-virtual/linux-64::epics-base-7.0.6.1-h68659b9_4
  libgcc-ng          conda-e3-virtual/linux-64::libgcc-ng-9.3.0-h2828fa1_19
  libgomp            conda-e3-virtual/linux-64::libgomp-9.3.0-h2828fa1_19
  libstdcxx-ng       conda-e3-virtual/linux-64::libstdcxx-ng-9.3.0-h6de172a_19
  libusb             conda-e3-virtual/linux-64::libusb-1.0.22-he1b5a44_0
  ncurses            conda-e3-virtual/linux-64::ncurses-6.1-hf484d3e_1002
  pcre               conda-e3-virtual/linux-64::pcre-8.44-he1b5a44_0
  perl               conda-e3-virtual/linux-64::perl-5.26.2-h516909a_1006
  readline           conda-e3-virtual/linux-64::readline-8.0-hf8c457e_0
  require            conda-e3-virtual/linux-64::require-3.1.4-hba1cc46_3
  seq                conda-e3-virtual/linux-64::seq-2.2.7-hfba5578_2
  sscan              conda-e3-virtual/linux-64::sscan-2.11.5-hd0a8fca_1
  stream             conda-e3-virtual/linux-64::stream-2.8.22-h74e095f_2
  ...
```

As you see, it will download all the required dependencies to install the
requested packages. To start working in this environment, just activate it. The
name of the active environment will be displayed in your prompt. You can then
run `iocsh.bash`.

```bash
[csi@8ef3d5671aef ~]$ conda activate epics
(epics) [csi@8ef3d5671aef ~]$ iocsh.bash -r stream
registerChannelProviderLocal firstTime true
#
# Start at "2020-W23-Jun03-0809-25-UTC"
#
# Version information:
# European Spallation Source ERIC : iocsh.bash (3.1.3-PID-2667)
#
...
# Load require module, which has the version 3.1.3
#
dlload /home/csi/miniconda/envs/epics/modules/require/3.1.3/lib/linux-x86_64/librequire.so
dbLoadDatabase /home/csi/miniconda/envs/epics/modules/require/3.1.3/dbd/require.dbd
require_registerRecordDeviceDriver
Loading module info records for require
#
require stream
Module stream version 2.8.22 found in /home/csi/miniconda/envs/epics/modules/stream/2.8.22/
Module stream depends on asyn 4.41.0
Module asyn version 4.41.0 found in /home/csi/miniconda/envs/epics/modules/asyn/4.41.0/
Loading library /home/csi/miniconda/envs/epics/modules/asyn/4.41.0/lib/linux-x86_64/libasyn.so
Loaded asyn version 4.41.0
Loading dbd file /home/csi/miniconda/envs/epics/modules/asyn/4.41.0/dbd/asyn.dbd
Calling function asyn_registerRecordDeviceDriver
Loading module info records for asyn
Module stream depends on calc 3.7.1
Module calc version 3.7.1 found in /home/csi/miniconda/envs/epics/modules/calc/3.7.1/
Module calc depends on seq 2.2.7
Module seq version 2.2.7 found in /home/csi/miniconda/envs/epics/modules/seq/2.2.7/
Loading library /home/csi/miniconda/envs/epics/modules/seq/2.2.7/lib/linux-x86_64/libseq.so
Loaded seq version 2.2.7
seq has no dbd file
Loading module info records for seq
Module calc depends on sscan 2.11.5
Module sscan version 2.11.5 found in /home/csi/miniconda/envs/epics/modules/sscan/2.11.5/
Module sscan depends on seq 2.2.7
Module seq version 2.2.7 already loaded
Loading library /home/csi/miniconda/envs/epics/modules/sscan/2.11.5/lib/linux-x86_64/libsscan.so
Loaded sscan version 2.11.5
Loading dbd file /home/csi/miniconda/envs/epics/modules/sscan/2.11.5/dbd/sscan.dbd
Calling function sscan_registerRecordDeviceDriver
Loading module info records for sscan
Loading library /home/csi/miniconda/envs/epics/modules/calc/3.7.1/lib/linux-x86_64/libcalc.so
Loaded calc version 3.7.1
Loading dbd file /home/csi/miniconda/envs/epics/modules/calc/3.7.1/dbd/calc.dbd
Calling function calc_registerRecordDeviceDriver
Loading module info records for calc
Loading library /home/csi/miniconda/envs/epics/modules/stream/2.8.22/lib/linux-x86_64/libstream.so
Loaded stream version 2.8.22
Loading dbd file /home/csi/miniconda/envs/epics/modules/stream/2.8.22/dbd/stream.dbd
Calling function stream_registerRecordDeviceDriver
Loading module info records for stream
# Set the IOC Prompt String One
epicsEnvSet IOCSH_PS1 "8ef3d5671aef-2667 > "
#
#
iocInit
Starting iocInit
############################################################################
## EPICS R7.0.6.1
## Rev. 2022-03-04T15:55+0000
############################################################################
drvStreamInit: Warning! STREAM_PROTOCOL_PATH not set.
iocRun: All initialization complete
8ef3d5671aef-2667 >
```

Once you are in an environment you can install new packages or change the
version of the installed packages. Let's add iocstats and recsync to our epics
environment:

```bash
(epics) [csi@8ef3d5671aef ~]$ conda install iocstats recsync
Collecting package metadata (repodata.json): done
Solving environment: done

## Package Plan ##

  environment location: /home/csi/miniconda/envs/epics

  added / updated specs:
    - iocstats
    - recsync

...

The following NEW packages will be INSTALLED:

  iocstats           conda-e3-virtual/linux-64::iocstats-3.1.16-h2bcc261_6
  recsync            conda-e3-virtual/linux-64::recsync-1.4.0-hfba5578_0
```

`conda list` will show you the list of installed packages in the environment:

```bash
(epics) [csi@8ef3d5671aef ~]$ conda list
# packages in environment at /home/csi/miniconda/envs/epics:
#
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                 conda_forge    conda-e3-virtual
_openmp_mutex             4.5                       0_gnu    conda-e3-virtual
asyn                      4.41.0              h0468fb3_10    conda-e3-virtual
calc                      3.7.1                h3f5c933_3    conda-e3-virtual
epics-base                7.0.6.1              h68659b9_4    conda-e3-virtual
iocstats                  3.1.16               h2bcc261_6    conda-e3-virtual
libgcc-ng                 9.3.0               h2828fa1_19    conda-e3-virtual
libgomp                   9.3.0               h2828fa1_19    conda-e3-virtual
libstdcxx-ng              9.3.0               h6de172a_19    conda-e3-virtual
libusb                    1.0.22               he1b5a44_0    conda-e3-virtual
ncurses                   6.1               hf484d3e_1002    conda-e3-virtual
pcre                      8.44                 he1b5a44_0    conda-e3-virtual
perl                      5.26.2            h516909a_1006    conda-e3-virtual
readline                  8.0                  hf8c457e_0    conda-e3-virtual
recsync                   1.4.0                hfba5578_0    conda-e3-virtual
require                   3.1.4                hba1cc46_3    conda-e3-virtual
seq                       2.2.7                hfba5578_2    conda-e3-virtual
sscan                     2.11.5               hd0a8fca_1    conda-e3-virtual
stream                    2.8.22               h74e095f_2    conda-e3-virtual
```

Let's say you want to switch to another version of stream. You could
create a new environment or just replace the version installed in this one. You
can search for available versions by running `conda search`:

```bash
(epics) [csi@8ef3d5671aef ~]$ conda search stream
Loading channels: done
# Name                       Version           Build  Channel
stream                        2.8.10      h2feebe4_0  conda-e3-virtual    
stream                        2.8.10      hbaf0b60_1  conda-e3-virtual    
stream                        2.8.22      h74e095f_2  conda-e3-virtual
```

Let's switch to 2.8.10

```bash
(epics) [csi@8ef3d5671aef ~]$ conda install stream=2.8.10
Collecting package metadata (repodata.json): done
Solving environment: done

## Package Plan ##

  environment location: /home/csi/miniconda/envs/epics

  added / updated specs:
    - stream=2.8.10


The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    iocstats-3.1.16            |       h2c1926d_5          92 KB  conda-e3-virtual
    ------------------------------------------------------------
                                           Total:          92 KB

The following packages will be DOWNGRADED:

  asyn                                   4.41.0-h0468fb3_10 --> 4.41.0-hceeaaa5_10
  calc                                     3.7.1-h3f5c933_3 --> 3.7.1-h6ca1cf9_3
  epics-base                             7.0.6.1-h68659b9_4 --> 7.0.5.0-h68659b9_4
  iocstats                                3.1.16-h2bcc261_6 --> 3.1.16-h2c1926d_5
  recsync                                  1.4.0-hfba5578_0 --> 1.3.0.post1-h60aecf9_1
  require                                  3.1.4-hba1cc46_3 --> 3.1.3-h9bea806_1
  seq                                      2.2.7-hfba5578_2 --> 2.2.7-h60aecf9_1
  sscan                                   2.11.5-hd0a8fca_1 --> 2.11.2-h44690a7_1
  stream                                  2.8.22-h74e095f_2 --> 2.8.10-hbaf0b60_1

```

Let's now create a separate environment with epics-base 3.15. Note that this is
only as an example. epics-base 3 isn't supported anymore at ESS. You should use
EPICS 7.  This is to demonstrate you can work on separate environments with
different epics-base version.

```bash
(epics) [csi@8ef3d5671aef ~]$ conda create -y -n epics3 epics-base=3 iocstats
Collecting package metadata (repodata.json): done
Solving environment: done

## Package Plan ##

  environment location: /home/csi/miniconda/envs/epics3

  added / updated specs:
    - epics-base=3
    - iocstats
...

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

```bash
(epics) [csi@8ef3d5671aef ~]$ conda deactivate
[csi@8ef3d5671aef ~]$ conda activate epics3
(epics3) [csi@8ef3d5671aef ~]$ conda list
# packages in environment at /home/csi/miniconda/envs/epics3:
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

```bash
[csi@8ef3d5671aef ~]$ conda search iocstat
Loading channels: done
No match found for: iocstat. Search: *iocstat*
# Name                       Version           Build  Channel
iocstats                3.1.15.post1      h0f5667f_0  conda-e3-virtual
...
iocstats                3.1.15.post1      hd2b67a6_0  conda-e3-virtual
iocstats                3.1.15.post1      he422a75_0  conda-e3-virtual
iocstats                3.1.15.post1      hf85dc0c_0  conda-e3-virtual
iocstats                      3.1.16      h76d1a4d_1  conda-e3-virtual
iocstats                      3.1.16      hd2b67a6_0  conda-e3-virtual
```

You can get more information about a package and its dependencies with the `-i`
flag:
[csi@8ef3d5671aef ~]$ conda search iocstat -i
```bash
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

...

iocstats 3.1.16 h2bcc261_6
--------------------------
file name   : iocstats-3.1.16-h2bcc261_6.tar.bz2
name        : iocstats
version     : 3.1.16
build       : h2bcc261_6
build number: 6
size        : 93 KB
license     : EPICS Open License
subdir      : linux-64
url         : https://artifactory.esss.lu.se/artifactory/api/conda/conda-e3-virtual/linux-64/iocstats-3.1.16-h2bcc261_6.tar.bz2
md5         : 73d062648a0c5c767def3798a514fdfe
timestamp   : 2022-03-04 18:50:11 UTC
dependencies: 
  - calc >=3.7.1,<3.7.2.0a0
  - epics-base >=7.0.6.1,<7.0.6.2.0a0
  - libgcc-ng >=7.3.0
  - libstdcxx-ng >=7.3.0
  - require >=3.1.4,<3.2.0a0
```

You can see above that the first package was compiled with epics-base 3.15.5 and
the last with epics-base 7.0.6.1. The last one also has `calc` has run
dependency.

Note that conda package names are always **lowercase**. When searching or
installing a package, conda is case-insensitive. Running `conda install
iocStats` or `conda install iocstats` will perform exactly the same operation.
But when using a module with require, you should use the lowercase name:

```bash
(epics3) [csi@8ef3d5671aef ~]$ iocsh.bash
...
8ef3d5671aef.3038 > require iocStats
Module iocStats not available
8ef3d5671aef.3038 > require iocstats
Module iocstats version 3.1.15 found in /home/csi/miniconda/envs/epics3/modules/iocstats/3.1.15/
Loading library /home/csi/miniconda/envs/epics3/modules/iocstats/3.1.15/lib/linux-x86_64/libiocstats.so
Loaded iocstats version 3.1.15
Loading dbd file /home/csi/miniconda/envs/epics3/modules/iocstats/3.1.15/dbd/iocstats.dbd
Calling function iocstats_registerRecordDeviceDriver
```

Note that when working with E3, you aren't limited to work with conda packages.
During development, you can compile a module locally in a conda environment. See
{ref}`how to compile a module <e3_module_compilation>`.
