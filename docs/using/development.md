(e3_development)=

# Development

E3 uses [require](https://gitlab.esss.lu.se/epics-modules/require), originally developed by [PSI](https://github.com/paulscherrerinstitute/require) to dynamically load modules at runtime.
require also includes a [driver.Makefile](https://gitlab.esss.lu.se/epics-modules/require/-/blob/master/App/tools/driver.makefile) that shall be used to build a module.
This requires a specific `Makefile.E3` file that includes this `driver.Makefile`.

When working with E3, you aren't limited to work with conda packages.
During development, you can compile a module locally in a conda environment.
You only have to install a few extra dev packages:

- compilers
- make
- tclx

Let's create an `e3-dev` environment to compile an existing module.

```bash
[csi@8ef3d5671aef Dev]$ conda create -y -n e3-dev epics-base require streamdevice compilers make tclx
Collecting package metadata (repodata.json): done
Solving environment: done
...
```

We installed `epics-base`, `require` and `streamdevice` as standard modules.
If you have other depencies, just install them in the environment.

Let's take the [fug](https://gitlab.esss.lu.se/epics-modules/fug) module as example.

```bash
[csi@8ef3d5671aef Dev]$ git clone https://gitlab.esss.lu.se/epics-modules/fug.git
Cloning into 'fug'...
remote: Enumerating objects: 100, done.
remote: Counting objects: 100% (100/100), done.
remote: Compressing objects: 100% (73/73), done.
remote: Total 100 (delta 16), reused 53 (delta 10), pack-reused 0
Receiving objects: 100% (100/100), 6.81 MiB | 2.68 MiB/s, done.
Resolving deltas: 100% (16/16), done.
[csi@8ef3d5671aef Dev]$ cd fug
[csi@8ef3d5671aef fug]$ ls
LICENSE  Makefile  Makefile.E3  README.md  cmds  configure  fugApp  iocsh
```

You can see that this module includes the needed `Makefile.E3`.
Let's compile it. Don't forget to activate the `e3-dev` environment.

```bash
[csi@8ef3d5671aef fug]$ conda activate e3-dev
(e3-dev) [csi@8ef3d5671aef fug]$ make -f Makefile.E3
make[1]: Entering directory '/home/csi/Dev/fug'
MAKING EPICS VERSION 7.0.3.1
MAKING ARCH linux-x86_64
make[2]: Entering directory '/home/csi/Dev/fug'
mkdir -p O.7.0.3.1_Common
mkdir -p O.7.0.3.1_linux-x86_64
make[3]: Entering directory '/home/csi/Dev/fug/O.7.0.3.1_linux-x86_64'
Collecting dependencies
rm -f fug.dep
cat *.d 2>/dev/null | sed 's/ /\n/g' | sed -n 's%/home/csi/miniconda/envs/e3-dev/modules/*\([^/]*\)/\([0-9]*\.[0-9]*\.[0-9]*\)/.*%\1 \2%p;s%/home/csi/miniconda/envs/e3-dev/modules/*\([^/]*\)/\([^/]*\)/.*%\1 \2%p'| grep -v "include" | sort -u >> fug.dep
rm -f MakefileInclude
make[3]: Leaving directory '/home/csi/Dev/fug/O.7.0.3.1_linux-x86_64'
make[2]: Leaving directory '/home/csi/Dev/fug'
make[1]: Leaving directory '/home/csi/Dev/fug'
```

If you had some database to generate, you should run `make -f Makefile.E3 db`. This module doesn't have any, so it's not required.

Install the module in the environment:

```bash
(e3-dev) [csi@8ef3d5671aef fug]$ make -f Makefile.E3 install
make[1]: Entering directory '/home/csi/Dev/fug'
MAKING EPICS VERSION 7.0.3.1
MAKING ARCH linux-x86_64
make[2]: Entering directory '/home/csi/Dev/fug'
make[3]: Entering directory '/home/csi/Dev/fug/O.7.0.3.1_linux-x86_64'
rm -f MakefileInclude
make[3]: Leaving directory '/home/csi/Dev/fug/O.7.0.3.1_linux-x86_64'
make[3]: Entering directory '/home/csi/Dev/fug/O.7.0.3.1_linux-x86_64'
rm -f MakefileInclude
Installing scripts ../iocsh/fug.iocsh to /home/csi/miniconda/envs/e3-dev/modules/fug/dev
perl -CSD /home/csi/miniconda/envs/e3-dev/base/bin/linux-x86_64/installEpics.pl  -d -m755 ../iocsh/fug.iocsh /home/csi/miniconda/envs/e3-dev/modules/fug/dev
mkdir /home/csi/miniconda/envs/e3-dev/modules/fug/dev
Installing module template files ../fugApp/Db/fug.proto ../fugApp/Db/fug.template to /home/csi/miniconda/envs/e3-dev/modules/fug/dev/db
perl -CSD /home/csi/miniconda/envs/e3-dev/base/bin/linux-x86_64/installEpics.pl  -d -m644 ../fugApp/Db/fug.proto ../fugApp/Db/fug.template /home/csi/miniconda/envs/e3-dev/modules/fug/dev/db
mkdir /home/csi/miniconda/envs/e3-dev/modules/fug/dev/db
Installing module dependency file /home/csi/miniconda/envs/e3-dev/modules/fug/dev/lib/linux-x86_64/fug.dep
perl -CSD /home/csi/miniconda/envs/e3-dev/base/bin/linux-x86_64/installEpics.pl  -d -m644 fug.dep /home/csi/miniconda/envs/e3-dev/modules/fug/dev/lib/linux-x86_64
mkdir /home/csi/miniconda/envs/e3-dev/modules/fug/dev/lib
mkdir /home/csi/miniconda/envs/e3-dev/modules/fug/dev/lib/linux-x86_64
make[3]: Leaving directory '/home/csi/Dev/fug/O.7.0.3.1_linux-x86_64'
make[2]: Leaving directory '/home/csi/Dev/fug'
make[1]: Leaving directory '/home/csi/Dev/fug'
```

The module was installed as _dev_ version.
You can check that you can load it:

```bash
(e3-dev) [csi@8ef3d5671aef fug]$ iocsh.bash -r fug
...
require fug
Module fug version dev found in /home/csi/miniconda/envs/e3-dev/modules/fug/dev/
Module fug depends on streamdevice 2.8.10
Module streamdevice version 2.8.10 found in /home/csi/miniconda/envs/e3-dev/modules/streamdevice/2.8.10/
Module streamdevice depends on asyn 4.36.0
...
```

During development, you can modify your code, re-compile and re-install as many times as you want:

```bash
make -f Makefile.E3
make -f Makefile.E3 db
make -f Makefile.E3 install
```
