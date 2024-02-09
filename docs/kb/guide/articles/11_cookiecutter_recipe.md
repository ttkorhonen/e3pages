(cookiecutter_recipe)=

# How to: Create a conda recipe with cookiecutter

*[Cookiecutter](https://github.com/cookiecutter/cookiecutter)* is a templating
utility built in Python. Cookiecutter is already extensively used within ICS to
help standardize the creation of multiple projects, see
<https://gitlab.esss.lu.se/ics-cookiecutter>. To create a conda-recipe, we will
be using [a template designed for
that](https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-recipe).

## Prerequisites

### Installing cookiecutter

Cookiecutter requires Python to be installed, but does not require any knowledge
of Python to use. From the terminal, run the following:

```console
$ pip3 install cookiecutter --user
```

:::{note}
Be aware that you will need to have Python 3 as well as `pip` installed on your machine.
:::

:::{tip}
It is highly recommended to use virtual environments (using, for example, the
`venv` module or *conda*) when dealing with Python environments.
:::

### Building an EPICS module

Assuming that you have an existing EPICS module, and you would like to create a
recipe for that is publicly available via git. Note that the configuration
and *make* files that are used to build this EPICS module will not be used in the
conda package process, and that you will have to configure the recipe separately.

## Creating the conda recipe

Run the following command in the terminal to create a conda recipe
using cookiecutter:

```console
$ cookiecutter git+https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-recipe.git
```

:::{note}
If you have run it before, it will ask if you want to re-download the template;
you should answer the default of 'yes', which ensures that you will use an
up-to-date template.
:::

Cookiecutter then provides a list of prompts:

```console
company [European Spallation Source ERIC]:
module_name [mymodule]: fakemodule
summary [EPICS fakemodule module]:
module_home [https://gitlab.esss.lu.se/epics-modules]: https://gitlab.esss.lu.se/epics-modules/training
module_version [1.0.0]:
```

Above, I have chosen the defaults for some of the responses other than the
module name, and the repository path.

This will create the following:

```console
[iocuser@host:~]$ tree fakemodule-recipe/
fakemodule-recipe/
├── .gitignore
├── .gitlab-ci.yml
├── LICENSE
├── README.md
├── recipe
│   ├── build.sh
│   └── meta.yaml
└── src
    └── fakemodule.Makefile
```

### Creating a remote project on GitLab and deploying the package

When you have created a conda recipe as above, it is only a local folder
on your machine. If you want to share it on the ESS GitLab (or otherwise), you
will need to init a local git repository and add a remote to the repository.
Assuming you are using the ESS GitLab, then the steps are as follows:

1. Create the remote repository by choosing 'New project' from the menu on
   <https://gitlab.esss.lu.se>.

2. The repository should be named *fakemodule-recipe*, and (although not necessary)
   should be public, at least if you want to share it with anyone else. However,
   you can change this at a later date.

   :::{warning}
   It is best to leave the box 'Initialize repository with a README' unchecked.
   :::

3. As the repository has already been initialised, you do not need to do all of
   the steps, but only the following (from 'Push an existing folder'). You will
   want to, of course, change the name `username` to your account or to the
   target group where you have created your repository, and change the name
   `fakemodule-recipe` to the name you have chosen:

   ``` console
   $ # You do not need to switch into the directory if you are already there
   [iocuser@host:~]$ cd fakemodule-recipe
   [iocuser@host:fakemodule-recipe]$ git init
   $ # There are two possibilities, depending on whether or not you have uploaded an SSH key to GitLab:
   $ # If you have not uploaded an ssh key (or do not know what that is), do the following:
   [iocuser@host:fakemodule-recipe]$ git remote add origin https://gitlab.esss.lu.se/username/fakemodule-recipe.git
   $ # Otherwise, you can do this:
   $ # git remote add origin git@gitlab.esss.lu.se:username/fakemodule-recipe.git
   $ # Add all of the files and commit them
   [iocuser@host:fakemodule-recipe]$ git add .
   [iocuser@host:fakemodule-recipe]$ git commit -m "Initial commit"
   $ # Push to the remote repository
   [iocuser@host:fakemodule-recipe]$ git push -u origin main
   ```

   If you use https and not ssh, then you will have to enter your username and password.

4. If all has gone well, you can see your new recipe on GitLab.

5. If you put the conda-recipe repository in the group e3-recipes
   <https://gitlab.esss.lu.se/e3-recipes> this will trigger a build
   with `.gitlab-ci` and make the release job button available to
   release a new or a first version of the module in the Artifactory
   conda-e3 channel
