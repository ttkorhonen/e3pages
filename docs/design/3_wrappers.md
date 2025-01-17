(wrappers)=

# Module wrappers

A key feature of e3 is the module wrapper. It is named as such
since it "wraps" the underlying EPICS module/extension. This allows us
to apply site-specific changes to modules from any source without
needing to modify that source directly. Site-specific changes include
code changes in the form of patches, separate database and substitution
files to enable ESS-compliant Process Variable (PV) naming structure,
and custom GUIs.

The e3 environment has two different management solution, see {ref}`build_process`.
The first and primary one, which uses custom tooling, relies on something we
will refer to as just "e3 wrappers", while the second one, which uses `conda` for
package management, uses a different wrapper that we refer to as "recipes".

## e3 wrappers

The build system of e3 will build according to configuration
spread between the main `${MODULE}.Makefile` and other GNU Make
files under `./configure`.

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

* `configure/CONFIG_MODULE`: The file that defines project
  name, version, and that lists dependencies.

* `configure/RELEASE`: Where the build environment and installation
  target is defined.

* `{MODULE}.Makefile`: The build project definitions; source
  files, includes, database files, etc.

In the above output, `${MODULE}` is the name of the EPICS
module(/application/library). For community modules that are version controlled
with git, this would be a *git submodule*. For ESS-specific modules, it can be a
embedded file tree (i.e. both the wrapper and the wrapped module are controlled
in the same repository).

:::{note}
We generally prefer "decoupled" modules---where the wrapper and the module are
in separate repositories---as that allows for more flexibility (e.g. allowing
the standard EPICS module to be made available for community
usage, or for the module to be used with both conda and without).
:::

It should be noted that non-used directories in the above structure should be
removed; e.g. if there are no patch-files, `patch/*` should be deleted.

To create a wrapper, see {ref}`cookiecutter_wrapper` and {ref}`wrapper_config`.
You may also want to go through the {ref}`training_series`.

## Conda recipes

The build system of conda will create a contained build environment,
and it will then copy the source code into this environment and build
according to a `recipe` given in a `meta.yaml` file.

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

Just as with the e3 wrapper, it is possible to add files "on top" of the
source's repository in the conda recipe. As example below we have the
file structure for `iocstats-recipe`.

``` console
[iocuser@host:iocstats-recipe]$ tree
.
├── LICENSE
├── README.md
├── recipe
│   ├── build.sh
│   └── meta.yaml
└── src
    ├── cmds                # example, template, or test startup scripts
    │   └── iocStats.cmd
    ├── iocsh               # snippets
    │   └── iocStats.iocsh
    ├── Makefile
    └── template            # template, substitution, and database files
        ├── iocAdminSoft-ess.substitutions
        └── iocE3EnvVar-ess.template
```

To create a conda recipe, see {ref}`cookiecutter_recipe` and {ref}`recipe_config`.
You may also want to go through the {ref}`training_series`.
