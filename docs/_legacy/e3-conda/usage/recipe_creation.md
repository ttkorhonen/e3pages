(e3_recipe_creation)=

# E3 recipe creation

The following assumes you already installed [conda], [conda-build] and
[cookiecutter].  Please refer to the {ref}`e3_requirements`.

To package a module with conda, you have to create a conda recipe.

## Create the recipe

Use the `e3-recipe` alias to create a new recipe (refer to
{ref}`cookiecutter_configuration` to create this alias).  You'll be prompted to
enter some values. Press enter to keep the default.

```bash
[csi@8ef3d5671aef Dev]$ e3-recipe
company [European Spallation Source ERIC]:
module_name [mymodule]: foo
summary [EPICS foo module]:
Select module_kind:
1 - ESS
2 - Community
Choose from 1, 2 [1]:
module_home [https://gitlab.esss.lu.se/epics-modules]: https://gitlab.esss.lu.se/epics-modules/test-group
module_version [1.0.0]: 0.1.0
```

The `module_home` variable shall point to the group in GitLab where your module
is stored.

This will create the following project:

```bash
[csi@8ef3d5671aef Dev]$ tree foo-recipe/
foo-recipe/
|-- LICENSE
|-- README.md
`-- recipe
    |-- build.sh
    |-- meta.yaml
    `-- test.cmd
```

## Update the recipe

You should only have to update the `recipe/meta.yaml` and `recipe/test.cmd`
files.

### meta.yaml

The `meta.yaml` file is the file that defines the recipe.  It describes where to
get the source of the module and the dependencies to build and run the modules.
The file contains many hints in comments. Follow them and remove them when
you've finalized your recipe.

```{note}
The final recipe shouldn't contain any comments!
```

### test.cmd

The file `recipe/test.cmd` is for testing purpose.  It will be used by
[conda-build] to check the created package by running `iocsh.bash
recipe/test.cmd`.  You can add extra commands to it if you want.

## Build the recipe

To build the recipe, run:

```bash
[csi@8ef3d5671aef foo-recipe]$ conda build recipe
```

In case of failure, check the error message and update your `meta.yaml` file.

If the build was successful, you should see something like that:

````bash
...
TEST END: /home/csi/miniconda/conda-bld/linux-64/foo-0.8.0-0.tar.bz2
Renaming work directory,  /home/csi/miniconda/conda-bld/foo_1591215967088/work  to  /home/csi/miniconda/conda-bld/foo_1591215967088/work_moved_foo-0.8.0-0_linux-64_main_build_loop
# Automatic uploading is disabled
# If you want to upload package(s) to anaconda.org later, type:

anaconda upload /home/csi/miniconda/conda-bld/linux-64/foo-0.8.0-0.tar.bz2

# To have conda build upload to anaconda.org automatically, use
# $ conda config --set anaconda_upload yes

anaconda_upload is not set.  Not uploading wheels: []
####################################################################################
Resource usage summary:

Total time: 0:00:07.2
CPU usage: sys=0:00:00.0, user=0:00:00.0
Maximum memory usage observed: 2.4M
Total disk usage observed (not including envs): 52B


####################################################################################
Source and build intermediates have been left in /home/csi/miniconda/conda-bld.
There are currently 2 accumulated.
To remove them, you can run the ```conda build purge``` command
````

## Test the built package

You can install the package you built locally by using the `-c local` argument
(to use the local channel).

```bash
[csi@8ef3d5671aef foo-recipe]$ conda create -y -n test -c local foo
...
The following NEW packages will be INSTALLED:

  foo                home/csi/miniconda/conda-bld/linux-64::foo-0.8.0-0
...
```

Activate your test environment and test your package.

## Upload the recipe to GitLab

You should upload your recipe to <https://gitlab.esss.lu.se/e3-recipes/staging>.
GitLab-ci will automatically build it and upload the package to Artifactory
`conda-e3-test` channel.

[conda]: https://docs.conda.io/en/latest/
[conda-build]: https://docs.conda.io/projects/conda-build/en/latest/index.html
[cookiecutter]: https://cookiecutter.readthedocs.io
