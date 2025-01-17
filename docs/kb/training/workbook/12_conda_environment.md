# 12. Conda Environment

In this lesson, you'll learn how to do the following:

* Install and configure conda.
* Create an environment in conda.
* Handle environments in conda.
* Work with cookiecutter

:::{note}
This chapter contains detailed information to work with conda and e3.
If you intend to work only with e3 environment, then this chapter can be skipped.
:::

## Conda

[Conda] is a Package, dependency and environment management for any language —
Python, R, Ruby, Lua, Scala, Java, JavaScript, C/ C++, FORTRAN.

[Conda] is open-source and runs on Linux, MacOS and Windows. It allows to easily
install packages and their dependencies in isolated environment.  You can read
more about conda concepts in the official
[user-guide](https://conda.io/projects/conda/en/latest/user-guide/concepts.html).

### Conda installation

To install conda, we'll use the
[Miniconda](https://docs.conda.io/en/latest/miniconda.html) installer.  The only
requirements to run the installation are `bzip2` and `wget`.

```console
$ mkdir -p ~/miniconda3
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
$ bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
$ rm -rf ~/miniconda3/miniconda.sh
$ ~/miniconda3/bin/conda init bash
```

You can refer to the [official
documentation](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
for more detailed information.

### Conda update

The installer might not come with the latest available version of conda. After
installation you should update conda:

```console
$ conda update -y -c conda-forge -n base conda
```

To check the version of conda installed, run:

```console
$ conda -V
conda 4.12.0
```

You need at least conda 4.7 to work with e3. Conda >=4.8 is recommended.

### Conda configuration

If you don't want conda to activate the base environment by default (and modify
your `PATH`), you should run:

```console
$ conda config --set auto_activate_base false
```

All e3 packages are available on [ESS
Artifactory](https://artifactory.esss.lu.se).  Artifactory includes mirrors for
`anaconda-main` and `conda-forge` channels. You should set artifactory as the
the default `channel_alias`.  To work with e3, you have to use the
`conda-e3-virtual` channel:

```console
$ conda config --set channel_alias https://artifactory.esss.lu.se/artifactory/api/conda
$ conda config --add channels conda-e3-virtual
$ conda config --remove channels defaults
```

Conda 4.7 introduced a new [.conda package
format](https://conda.io/projects/conda/en/latest/user-guide/concepts/packages.html#conda-file-format).
Artifactory 6.11.3 doesn't support that format and it creates issues with remote
conda repository. See
[RTFACT-19267](https://www.jfrog.com/jira/browse/RTFACT-19267). To use conda >=
4.7 with Artifactory you should force conda to only download .tar.bz2 packages
by setting the `use_only_tar_bz2` boolean.

```console
conda config --set use_only_tar_bz2 true
```

The previous commands created the following `~/.condarc` file:

```bash
auto_activate_base: false
channel_alias: https://artifactory.esss.lu.se/artifactory/api/conda
channels:
  - conda-e3-virtual
use_only_tar_bz2: true
```

You can modify the configuration by editing directly this file or using the
`conda config` command.

## conda-build

[conda-build] is only required if you want to build conda packages locally. It's
not directly needed to work with e3.

Install conda-build in the base environment:

```console
conda install -y -n base -c conda-forge conda-build
```

```{note}
The base environment shall be writeable by the current user to run this command.
```

## Conda usage

### How to create a new environment

To create an environment named "epics-7" with epics-base 7, run:

```console
[iocuser@host:~]$ conda create -n epics-7 epics-base=7
```

### How to activate an environment

Use the `conda activate` command followed by the environment name:

```console
[iocuser@host:~]$ conda activate epics-7
```

### How to deactivate an environment

Use `conda deactivate`:

```console
(epics-7) [iocuser@host:~]$ conda deactivate
```

### How to delete an environment

Use the `conda env remove` command:

```console
[iocuser@host:~]$ conda env remove -n epics-7
```

### How to export an environment

Use the `conda env export` command:

```console
[iocuser@host:~]$ conda env export -n epics-7 > environment.yml
```

### How to create an environment based on an environment file

Use the `conda env create` command:

```console
[iocuser@host:~]$ conda env create -n epics-7 -f environment.yml
```

If you omit the `-n` parameter, the environment name will be taken from the
`environment.yml` file.  The command will fail if the environment already
exists. You can to destroy it first by using `--force`.

## Cookiecutter

[Cookiecutter](https://cookiecutter.readthedocs.io) creates projects from
templates. It's used to easily create new e3 wrappers, recipes or IOCs for
development. It's not required to run e3.

### Cookiecutter installation

[Cookiecutter] is a Python tool. It can be installed with `pip`.  Note that you
should **never run** `sudo pip install`. This can override system packages.

[Cookiecutter] can be installed in different ways (`pip install --user` or using
[pipx](https://pipxproject.github.io/pipx/)).  As conda is installed, let's use
it.

```console
[iocuser@host:~]$ conda create -y -c conda-forge -n cookiecutter python=3 cookiecutter
```

Add an alias to your `.bashrc`:

```console
[iocuser@host:~]$ echo "alias cookiecutter='~/miniconda/envs/cookiecutter/bin/cookiecutter'" >> ~/.bashrc
```

Reload the `.bashrc` file

```console
[iocuser@host:~] source ~/.bashrc
```

You should be able to run `cookiecutter`:

```console
[iocuser@host:~]$ cookiecutter --version
Cookiecutter 1.7.2 from /home/iocuser/miniconda/envs/cookiecutter/lib/python3.8/site-packages (Python 3.8)
```

### Cookiecutter configuration

Create the file `~/.cookiecutterrc` with your name:

```bash
default_context:
    full_name: "Your Name"
```

This will override the variable `full_name` from any cookiecutter template with
your name.  It will become the default value and avoid you having to enter it
every time you create a new project.  Note that you could add to that file other
variables.

Add the following aliases to your `.bashrc`:

```console
[iocuser@host:~]$ echo "alias e3-wrapper='cookiecutter git+https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-wrapper.git'" >> ~/.bashrc
[iocuser@host:~]$ echo "alias e3-recipe='cookiecutter git+https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-recipe.git'" >> ~/.bashrc
[iocuser@host:~]$ echo "alias e3-ioc='cookiecutter git+https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-ioc.git'" >> ~/.bashrc
```

To create a new e3 wrapper, recipe or IOC, just run `e3-wrapper`, `e3-recipe` or
`e3-ioc`.

[conda]: https://docs.conda.io/en/latest/
[conda-build]: https://docs.conda.io/projects/conda-build/en/latest/index.html
[cookiecutter]: https://cookiecutter.readthedocs.io
