# E3 module creation

The following assumes you already installed [conda] and [cookiecutter].  Please
refer to the [e3_requirements](../references/requirements.md).

E3 uses [require](https://gitlab.esss.lu.se/epics-modules/require), originally
developed by [PSI](https://github.com/paulscherrerinstitute/require) to
dynamically load modules at runtime.  require also includes a
[driver.Makefile](https://gitlab.esss.lu.se/epics-modules/require/-/blob/master/App/tools/driver.makefile)
that shall be used to build a module.  This requires a specific `{module_name}.Makegile`
file that includes this `driver.Makefile`.

To make it easy to create a new E3 module, we provide a cookiecutter template.

## Create the module

Use the `e3-module` alias to create a new module (refer to [cookiecutter_configuration](../references/requirements.md#cookiecutter)
to create this alias).  You'll be prompted to enter some values
Press enter to keep the default.

```bash
[csi@8ef3d5671aef Dev]$ e3-module
You've downloaded /home/csi/.cookiecutters/cookiecutter-e3-module before. Is it okay to delete and re-download it? [yes]:
company [European Spallation Source ERIC]:
module_name [mymodule]: foo
full_name [Your name]: Douglas Araujo
email [your.name@ess.eu]: douglas.araujo@ess.eu
documentation_page [https://confluence.esss.lu.se/display/IS/Integration+by+ICS]: 
Select keep_epics_base_makefiles:
1 - N
2 - Y
Choose from 1, 2 [1]: 2
```

This will create a project based on `makeBaseApp.pl` from EPICS base but will
also include extra files needed for E3.

```bash
[csi@8ef3d5671aef Dev]$ tree foo/
foo
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
system if you want.

## Update the module

Add the needed files to your module.  You should also update the
`foo.Makefile` file. It includes comments to help you.

## Compile the module

To compile an E3 module in a conda environment, the following packages are
required:

- make
- compilers
- tclx
- epics-base
- require

Create the `e3-dev` environment with those packages.  If you have other
depencies, like `asyn`, install them as well.

```bash
[csi@8ef3d5671aef Dev]$ conda create -y -n e3-dev epics-base require compilers make tclx
Collecting package metadata (repodata.json): done
Solving environment: done
...
```

Activate the `e3-dev` environment and compile your module.

```bash
[csi@8ef3d5671aef Dev]$ conda activate e3-dev
(e3-dev) [csi@8ef3d5671aef Dev]$ cd foo
(e3-dev) [csi@8ef3d5671aef foo]$ make -f foo.Makefile
make[1]: Entering directory '/home/csi/Dev/foo'
MAKING EPICS VERSION 7.0.6.1
MAKING ARCH linux-x86_64
make[2]: Entering directory '/home/csi/Dev/foo'
mkdir -p O.7.0.6.1_Common
mkdir -p O.7.0.6.1_linux-x86_64
make[3]: Entering directory '/home/csi/Dev/foo/O.7.0.6.1_linux-x86_64'
/home/csi/miniconda/envs/e3-dev/bin/x86_64-conda_cos6-linux-gnu-g++  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET                -D_X86_64_ -DUNIX  -Dlinux                  -MD   -O3 -g   -Wall                   -mtune=generic                   -m64 -fPIC               -I. -I../fooApp/src/ -I/home/csi/miniconda/envs/e3-dev/modules/require/3.1.4/include -I/home/csi/miniconda/envs/e3-dev/epics/include  -I/home/csi/miniconda/envs/e3-dev/epics/include/compiler/gcc -I/home/csi/miniconda/envs/e3-dev/epics/include/os/Linux                   -I/home/csi/miniconda/envs/e3-dev/include                -c  ../fooApp/src/fooMain.cpp
echo "char _fooLibRelease[] = \"dev\";" >> foo_version_dev.c
/home/csi/miniconda/envs/e3-dev/bin/x86_64-conda_cos6-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET                -D_X86_64_ -DUNIX  -Dlinux                  -MD   -O3 -g   -Wall -Werror-implicit-function-declaration                   -mtune=generic     -m64 -fPIC                -I. -I../fooApp/src/ -I/home/csi/miniconda/envs/e3-dev/modules/require/3.1.4/include -I/home/csi/miniconda/envs/e3-dev/epics/include  -I/home/csi/miniconda/envs/e3-dev/epics/include/compiler/gcc -I/home/csi/miniconda/envs/e3-dev/epics/include/os/Linux                   -I/home/csi/miniconda/envs/e3-dev/include                -c foo_version_dev.c
Collecting dependencies
rm -f foo.dep
cat *.d 2>/dev/null | sed 's/ /\n/g' | sed -n 's%/home/csi/miniconda/envs/e3-dev/modules/*\([^/]*\)/\([0-9]*\.[0-9]*\.[0-9]*\)/.*%\1 \2%p;s%/home/csi/miniconda/envs/e3-dev/modules/*\([^/]*\)/\([^/]*\)/.*%\1 \2%p'| grep -v "include" | sort -u >> foo.dep
/home/csi/miniconda/envs/e3-dev/bin/x86_64-conda_cos6-linux-gnu-g++ -o libfoo.so -shared -fPIC -Wl,-hlibfoo.so -L/home/csi/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64 -Wl,-rpath,/home/csi/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64                       -rdynamic -m64 -Wl,--disable-new-dtags -Wl,-rpath,/home/csi/miniconda/envs/e3-dev/lib -Wl,-rpath-link,/home/csi/miniconda/envs/e3-dev/lib -L/home/csi/miniconda/envs/e3-dev/lib -Wl,-rpath-link,/home/csi/miniconda/envs/e3-dev/epics/lib/linux-x86_64                          fooMain.o foo_version_dev.o      -lpthread    -lm -lrt -ldl -lgcc
rm -f MakefileInclude
make[3]: Leaving directory '/home/csi/Dev/foo/O.7.0.6.1_linux-x86_64'
make[2]: Leaving directory '/home/csi/Dev/foo'
make[1]: Leaving directory '/home/csi/Dev/foo'
```

If you have some database to generate, run `make -f foo.Makefile`.  In our
case, we don't have any template, so the command won't do anything.

```bash
(e3-dev) [csi@8ef3d5671aef foo]$ make -f foo.Makefile db
make: Nothing to be done for 'db'.
```

Install the module in the current environment.

```bash
(e3-dev) [csi@8ef3d5671aef foo]$ make -f foo.Makefile install
make[1]: Entering directory '/home/csi/Dev/foo'
MAKING EPICS VERSION 7.0.6.1
MAKING ARCH linux-x86_64
make[2]: Entering directory '/home/csi/Dev/foo'
make[3]: Entering directory '/home/csi/Dev/foo/O.7.0.6.1_linux-x86_64'
rm -f MakefileInclude
make[3]: Leaving directory '/home/csi/Dev/foo/O.7.0.6.1_linux-x86_64'
make[3]: Entering directory '/home/csi/Dev/foo/O.7.0.6.1_linux-x86_64'
rm -f MakefileInclude
Installing scripts ../iocsh/foo.iocsh to /home/csi/miniconda/envs/e3-dev/modules/foo/dev
perl -CSD /home/csi/miniconda/envs/e3-dev/epics/bin/linux-x86_64/installEpics.pl  -d -m755 ../iocsh/foo.iocsh /home/csi/miniconda/envs/e3-dev/modules/foo/dev
mkdir /home/csi/miniconda/envs/e3-dev/modules/foo
mkdir /home/csi/miniconda/envs/e3-dev/modules/foo/dev
Installing module library /home/csi/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64/libfoo.so
perl -CSD /home/csi/miniconda/envs/e3-dev/epics/bin/linux-x86_64/installEpics.pl  -d -m755 libfoo.so /home/csi/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64
mkdir /home/csi/miniconda/envs/e3-dev/modules/foo/dev/lib
mkdir /home/csi/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64
Installing module dependency file /home/csi/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64/foo.dep
perl -CSD /home/csi/miniconda/envs/e3-dev/epics/bin/linux-x86_64/installEpics.pl  -d -m644 foo.dep /home/csi/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64
make[3]: Leaving directory '/home/csi/Dev/foo/O.7.0.6.1_linux-x86_64'
make[2]: Leaving directory '/home/csi/Dev/foo'
make[1]: Leaving directory '/home/csi/Dev/foo'
```

The module was installed as _dev_ version.  You can check that you can load it:

```bash
(e3-dev) [csi@8ef3d5671aef foo]$ iocsh.bash -r foo
...
require foo
Module foo version dev found in /home/csi/miniconda/envs/e3-dev/modules/foo/dev/
Loading library /home/csi/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64/libfoo.so
Loaded foo version dev
foo has no dbd file
Loading module info records for foo
...
```

You can also use the `cmds/st.cmd` file to test your module.

```bash
(e3-dev) [csi@8ef3d5671aef foo]$ iocsh.bash cmds/st.cmd
...
iocshLoad 'cmds/st.cmd',''
# This should be a test startup script
require foo
Module foo version dev found in /home/csi/miniconda/envs/e3-dev/modules/foo/dev/
Loading library /home/csi/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64/libfoo.so
Loaded foo version dev
foo has no dbd file
Loading module info records for foo
iocshLoad("/home/csi/miniconda/envs/e3-dev/modules/foo/dev//foo.iocsh")
...
```

During development, you can modify your code, re-compile and re-install as many
times as you want:

```bash
make -f foo.Makefile
make -f foo.Makefile db
make -f foo.Makefile install
```

You can uninstall the module by running `make -f foo.Makefile uninstall`.

```bash
(e3-dev) [csi@8ef3d5671aef foo]$ make -f foo.Makefile uninstall
rm -rf /home/csi/miniconda/envs/e3-dev/modules/foo/dev
```

## Upload the module to GiLab

You should upload your module to the proper subgroup under
<https://gitlab.esss.lu.se/epics-modules>

To distribute your module, you need to package it with conda. See [e3_recipe_creation](recipe_creation.md).

[conda]: https://docs.conda.io/en/latest/
[cookiecutter]: https://cookiecutter.readthedocs.io
