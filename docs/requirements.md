# Requirements

All requirements are already installed in the ESS Development Machine (4.x and upward).

**E3 is only supported on Linux.**

## conda

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
Artifactory includes mirrors for `anaconda-main` and `conda-forge` channels.
To work with E3, you should use the `conda-e3-virtual` channel:

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
cat ~/.condarc
channel_alias: https://artifactory.esss.lu.se/artifactory/api/conda
channels:
  - conda-e3-virtual
use_only_tar_bz2: true
```

You can modify the configuration by editing directly this file or using the `conda config` command.
