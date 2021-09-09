(cookiecutter_wrapper)=

# How to: Create an e3 wrapper with cookiecutter

*[Cookiecutter](https://github.com/cookiecutter/cookiecutter)* is a templating utility built in Python. Cookiecutter is already extensively used within ICS to help standardize the creation of multiple projects, see <https://gitlab.esss.lu.se/ics-cookiecutter>. To create an e3 wrapper, we will be using [a template designed for that](https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-wrapper).

## Prerequisites

### Installing cookiecutter

Cookiecutter requires Python to be installed, but does not require any knowledge of Python to use. From the terminal, run the following:

```console
$ pip3 install cookiecutter --user
```

:::{warning}
Beware that you will need to have Python 3 as well as *pip* installed on your machine.
:::

:::{tip}
It is highly recommended to use virtual environments (using, for example, the `venv` module or *conda*) when dealing with Python environments.
:::

### Building an EPICS module

This step is not technically a prerequisite; if you do not have an EPICS module built already, then the steps below will construct a template EPICS module which you can modify to suit your needs. This uses a cookiecutter that is based on `makeBaseApp.pl` from EPICS base: <https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-module>.

Assuming that you have an existing EPICS module you would like to create a wrapper for, it should be made publicly available on the ESS GitLab, although both GitHub and GitLab will work. Note that the configuration and *make* files that are used to build this EPICS module will not be used in the e3 build process.

## Creating the e3 wrapper

Run the following command in the terminal to create a cookiecutter:

```console
$ cookiecutter git+https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-wrapper.git
```

If you have run it before, it will ask if you want to re-download the template; you should answer the default of "yes", which ensures that you will use an up-to-date template.

Cookiecutter then provides a list of prompts:

```console
$ cookiecutter git+https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-wrapper.git
You've downloaded /Users/simonrose/.cookiecutters/cookiecutter-e3-wrapper before. Is it okay to delete and re-download it? [yes]:
company [European Spallation Source ERIC]:
module_name [mymodule]: testmodule
summary [EPICS testmodule module]:
full_name [Simon Rose]:
email [simon.rose@ess.eu]:
epics_base_version [7.0.4]:
epics_base_location [/epics/base-7.0.4]:
require_version [3.2.0]:
git_repository [https://gitlab.esss.lu.se/epics-modules/testmodule.git]:
```

Above, I have chosen the defaults for most of the responses other than the module name. In the last step, there are two possibilities:

1. The git repository that you provide exists and is public.
2. The git repository does not exist, or is not public.

In the first case, you will see the following:

```
git_repository [https://gitlab.esss.lu.se/epics-modules/testmodule.git]: https://gitlab.esss.lu.se/simonrose/http
Initialized empty Git repository in /Users/simonrose/git/e3-testmodule/.git/
>>>> git repository has been initialized.
Cloning into '/Users/simonrose/git/e3-testmodule/http'...
warning: redirecting to https://gitlab.esss.lu.se/simonrose/http.git/
remote: Enumerating objects: 237, done.
remote: Counting objects: 100% (237/237), done.
remote: Compressing objects: 100% (167/167), done.
remote: Total 237 (delta 129), reused 107 (delta 52), pack-reused 0
Receiving objects: 100% (237/237), 46.63 KiB | 2.74 MiB/s, done.
Resolving deltas: 100% (129/129), done.
```

This means that the e3 wrapper has successfully added the EPICS module as a submodule, and is ready to work with.

In the second case, you will see something like the following.

```
git_repository [https://gitlab.esss.lu.se/epics-modules/testmodule.git]:
Initialized empty Git repository in /Users/simonrose/git/e3-testmodule/.git/
>>>> git repository has been initialized.
>>>> The repository 'https://gitlab.esss.lu.se/epics-modules/testmodule.git' was not found.
>>>> Please check that the repository is public, and then re-run 'git submodule add https://gitlab.esss.lu.se/epics-modules/testmodule.git'.
>>>> A template module has been included in the meantime.
```

In this case, either the EPICS modules you are looking for was not found (it may be private), or it does not exist. A temporary module has been added which displays the expected structure of an EPICS module. This is created using the cookiecutter template for EPICS modules found at <https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-module>. If this was not what you intended, you can delete the local directory, confirm that your EPICS module is available, and run:

```console
$ git submodule add https://gitlab.esss.lu.se/epics-modules/testmodule.git
```

### Adding a remote

When you have created an e3-wrapper as above, it is only a local git repository on your machine. If you want to share it on the ESS GitLab (or otherwise), you will need to add a remote to the repository. Assuming you are using the ESS GitLab, then the steps are as follows:

1. Create the remote repository by choosing "New project" from the menu on <https://gitlab.esss.lu.se>.
2. The repository should be named *e3-testmodule*, and (although not necessary) should be public, at least if you want to share it with anyone else. However, you can change this at a later date. 

   :::{warning}
   It is best to leave the box "Initialise repository with a README" unchecked.
   :::

3. As the repository has already been initialised, you do not need to do all of the steps, but only the following (from "Push an existing folder"). You will want to, of course, change the name `simonrose` to your account or to the target group where you have created your repository, and change the name `e3-testmodule` to the name you have chosen:

   ```bash
   $ # You do not need to switch into the directory if you are already there
   $ cd existing_folder
   $
   $ # You do not need to initialize the git repo; this has already been done
   $ # git init
   $
   $ # There are two possibilities, depending on whether or not you have uploaded an SSH key to GitLab:
   $ # If you have not uploaded an ssh key (or do not know what that is), do the following:
   $ git remote add origin https://gitlab.esss.lu.se/simonrose/e3-testmodule.git
   $ # Otherwise, you can do this:
   $ git remote add origin git@gitlab.esss.lu.se:simonrose/e3-testmodule.git
   $
   $ # Add all of the files and commit them
   $ git add .
   $ git commit -m "Initial commit"
   $
   $ # Push to the remote repository
   $ git push -u origin master
   ```
   If you use https and not ssh, then you will have to enter your username and password.
4. If all has gone well, you can see your new module on GitLab, and share it with others.

## Next steps

Once you have created your template, you will want to customise it. For this, please see the e3 training, as well as {ref}`wrappers`, {ref}`require_build`, and {ref}`wrapper_config`.
