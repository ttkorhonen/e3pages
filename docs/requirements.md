(e3_requirements)=

# Requirements

All requirements are already installed in the ESS Development Machine (4.x and upward).

**E3 is only supported on Linux.**

## Conda

[Conda](https://docs.conda.io/en/latest/) is a Package, dependency and environment management for any language — Python, R, Ruby, Lua, Scala, Java, JavaScript, C/ C++, FORTRAN.

Conda is open-source and runs on Linux, MacOS and Windows. It allows to easily install packages and their dependencies in isolated environment.
You can read more about conda concepts in the official [user-guide](https://conda.io/projects/conda/en/latest/user-guide/concepts.html).

### Installation

To install conda, we'll use the [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installer.
The only requirements to run the installation are `bzip2` and `curl`.

```bash
curl -LO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -bp $HOME/miniconda
rm -f Miniconda3-latest-Linux-x86_64.sh
# Let conda update your ~/.bashrc
source $HOME/miniconda/bin/activate
conda init
```

You can refer to the [official documentation](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) for more detailed information.

### Update

The installer might not come with the latest available version of conda. After installation you should update conda:

```bash
conda update -y -c conda-forge -n base conda
```

To check the version of conda installed, run:

```bash
$ conda -V
conda 4.8.3
```

You need at least conda 4.7 to work with E3. Conda 4.8 is recommended.

### Configuration

If you don't want conda to activate the base environment by default (and modify your PATH),
you should run:

```bash
conda config --set auto_activate_base false
```

All E3 packages are available on [ESS Artifactory](https://artifactory.esss.lu.se).
Artifactory includes mirrors for `anaconda-main` and `conda-forge` channels. You should set artifactory as the the default channel_alias.
To work with E3, you have to use the `conda-e3-virtual` channel:

```bash
conda config --set channel_alias https://artifactory.esss.lu.se/artifactory/api/conda
conda config --add channels conda-e3-virtual
conda config --remove channels defaults
```

conda 4.7 introduced a new [.conda package format](https://conda.io/projects/conda/en/latest/user-guide/concepts/packages.html#conda-file-format). Artifactory 6.11.3 doesn't support that format and it creates issues with remote conda repository. See [RTFACT-19267](https://www.jfrog.com/jira/browse/RTFACT-19267). To use conda >= 4.7 with Artifactory you should force conda to only download .tar.bz2 packages by setting the `use_only_tar_bz2` boolean.

```bash
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

You can modify the configuration by editing directly this file or using the `conda config` command.

## conda-build

[conda-build](https://docs.conda.io/projects/conda-build/en/latest/index.html) is only required if you want to build conda packages locally. It's not directly needed to work with E3.

Install conda-build in the base environment:

```bash
conda install -y -n base -c conda-forge conda-build
```

## Cookiecutter

[Cookiecutter](https://cookiecutter.readthedocs.io) creates projects from templates. It's used to easily create new E3 modules, recipes or IOCs for development. It's not required to run E3.

### Installation

Cookiecutter is a Python tool. It can be installed with `pip`.
Note that you should **never run** `sudo pip install`. This can override system packages.

Cookiecutter can be installed in different ways (`pip install --user` or using [pipx](https://pipxproject.github.io/pipx/)).
As conda is installed, let's use it.

```bash
conda create -y -c conda-forge -n cookiecutter python=3 cookiecutter
```

Add an alias to your `.bashrc`:

```bash
echo "alias cookiecutter='~/miniconda/envs/cookiecutter/bin/cookiecutter'" >> ~/.bashrc
```

Close and re-open your current shell. You should be able to run `cookiecutter`:

```bash
cookiecutter --version
Cookiecutter 1.7.2 from /home/csi/miniconda/envs/cookiecutter/lib/python3.8/site-packages (Python 3.8)
```

### Configuration

Add the following aliases to your `.bashrc`:

```bash
echo "alias e3-module='cookiecutter git+https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-module.git'" >> ~/.bashrc
echo "alias e3-recipe='cookiecutter git+https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-recipe.git'" >> ~/.bashrc
echo "alias e3-ioc='cookiecutter git+https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-ioc.git'" >> ~/.bashrc
```

To create a new E3 module, recipe or IOC, just run `e3-module`, `e3-recipe` or `e3-ioc`.
