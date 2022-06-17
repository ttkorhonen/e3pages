(wrappers)=

# Module wrappers

The e3 has two different management solution, see {ref}`build_process`.
In the first one that uses a custom tooling, the e3 build process
uses the feature e3 wrapper.
The second one uses the `conda` to build and distribute the modules
as packages. This approach uses a separate wrapper
(making it decoupled from the non-conda ones) which are referred
to as recipes.

## e3 wrappers

Another key feature of e3 is the module wrapper. This allows us to apply
site-specific changes to modules from any source without needing to modify that
source directly. Site-specific changes include code changes in the form of
patches, separate database and substitution files to enable ESS-compliant
Process Variable (PV) naming structure, and custom GUIs.

The template structure for an e3 wrapper is as follows:

```console
[iocuser@host:~]$ tree e3-${MODULE}
e3-${MODULE}
├── Makefile
├── README.md
├── cmds                        # example or template startup scripts
├── configure
├── docs                        # additional documentation (e.g. design docs)
├── iocsh                       # 'snippets' - common functions that are used by several IOCs
├── patch                       # ESS-specific modifications (in the shape of patch-files)
├── opi                         # example or template graphical user interfaces
├── template                    # ESS-specific database/template/substitution files
├── ${MODULE}
├── ${MODULE}.Makefile
└── tools                       # additional tools or utilities
```

In the above output, `${MODULE}` is the name of the EPICS
module(/application/library). For community modules that are version controlled
with git, this would be a *git submodule*. For ESS-specific modules, it can be a
embedded file tree (i.e. both the wrapper and the wrapped module are controlled
in the same repository).

:::{note}
We generally prefer 'decoupled' modules---where the wrapper and the module are
in separate repositories---as that allows for more flexibility (e.g. allowing
the standard EPICS module to be made available for community usage).
:::

It should be noted that non-used directories in the above structure should be
removed; e.g. if there are no patch-files, `patch/*` should be deleted.

:::{tip}
Embedded file-trees are recommended for ESS-developed modules that the community
would have no use of.
:::

To create a wrapper, see {ref}`cookiecutter_wrapper` and {ref}`wrapper_config`.
You may also want to go through the {ref}`training_series`.

## Conda recipes

If `conda` is the management system, the wrappers are referred to as
*conda recipes*.

Conda will create a contained build environment, and it will then
copy the source code into this environment and build according to a
`recipe` given in a `meta.yaml` file.

The template structure for a conda recipe is as follows:

``` console
[iocuser@host:~]$ tree ${MODULE}-recipe
.
├── LICENSE
├── README.md
├── recipe
│   ├── build.sh
│   └── meta.yaml
└── src
    └── Makefile.E3
```

* `meta.yaml`: A file that contains all the metadata in the recipe.
  Only package name and package version are required.

* `build.sh`: The build script for building and installing the package.

* `Makefile.E3`: This is essentially just a copy of the `${MODULE}.Makefile`
  used in the e3-wrapper, but with minor modifications.

In the conda recipe it is possible to add files on top of the
sources repository, from separate repository or in the recipe
itself. As example below we have the file structure for `iocstats-recipe`.

``` console
[iocuser@host:iocstats-recipe]$ tree
.
├── LICENSE
├── README.md
├── recipe
│   ├── build.sh
│   └── meta.yaml
└── src
    ├── cmds
    │   └── iocStats.cmd
    ├── iocsh
    │   └── iocStats.iocsh
    ├── Makefile
    └── template
        ├── iocAdminSoft-ess.substitutions
        └── iocE3EnvVar-ess.template
```

To create a conda recipe, see {ref}`cookiecutter_recipe` and {ref}`recipe_config`.
You may also want to go through the {ref}`training_series`.
