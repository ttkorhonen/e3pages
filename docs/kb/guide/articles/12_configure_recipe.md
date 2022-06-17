(recipe_config)=

# Article: Configuring your conda recipe

To create a conda recipe, you should use
`cookiecutter`, see{ref}`cookiecutter_recipe`.

## The `src/` directory

If you used the cookiecutter [e3-recipe](https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-recipe),
it will create the directory file `Makefile.E3` on src directory.

This file is very similar to module [Makefile](6_configure_wrapper.md#the-module-makefile)
created for an e3 wrapper. We only make sure that in the Makefile on recipe
is necessary to remove the line:

``` make
include $(E3_REQUIRE_CONFIG)/DECOUPLE_FLAGS
```

## The `recipe/` directory Makefile

Also created automatically by cookiecutter, there are two files in the recipe directory:

* `build.sh`: This is just a set of bash instructions that will build and install
  the e3 module. They should be the same for every e3 module.

  ``` bash
  #!/bin/bash

  LIBVERSION=${PKG_VERSION}

  # Clean between variants builds
  make -f Makefile.E3 clean

  make -f Makefile.E3 MODULE=${PKG_NAME} LIBVERSION=${LIBVERSION}
  make -f Makefile.E3 MODULE=${PKG_NAME} LIBVERSION=${LIBVERSION} db
  make -f Makefile.E3 MODULE=${PKG_NAME} LIBVERSION=${LIBVERSION} install
  ```

* `meta.yaml`: A file that contains all the metadata in the recipe.
  This file contains information about the package like its name,
  its version, its dependencies, etc.

  For concreteness’ sake, let us focus on a specific recipe: [julabof25hl-recipe](https://gitlab.esss.lu.se/e3-recipes/julabof25hl-recipe/-/blob/87e49dfa/recipe/meta.yaml).
  To be explicit, we are currently looking at the recipe for version `0.1.18`.

  At the top of the meta.yaml file there are some macro definitions.

  ``` yaml
  {% set version = "0.1.18" %}
  {% set name = "julabof25hl" %}
  ```

  The package sections specifies the package information

  ``` yaml
  package:
    name: "{{name}}"
    version: "{{ version }}"
  ```

  :::{note}
  The name should be lower case and may contain `-`, but not spaces.
  For the version number we should use the [PEP-386](https://peps.python.org/pep-0386/)
  verlib conventions and cannot contain `-`. The YAML interprets version
  numbers such as 1.0 as floats, meaning that 0.10 will be the same as 0.1.
  To avoid this, put the version number in quotes so that it is interpreted
  as a string.
  :::

  The source section specifies where the source code of the package is
  coming from. For the ESS recipes, we used source from git and from a
  local path `../src`.

  ``` yaml
  source:
    - git_url: https://gitlab.esss.lu.se/epics-modules/julabof25hl.git
      git_rev: {{ version }}
    - path: ../src
  ```

  The build section defines the build number that should be incremented
  for new builds of the same version. The number defaults to 0.
  No change is necessary for the  keys `run_export` and `skip`. For more
  details about what means each key see [conda website](https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html).

  ``` yaml
  build:
    number: 0
    run_exports:
      - {{ pin_subpackage(name, max_pin='x.x.x.x') }}
    skip: True
  ```

  The requirements section specifies the build and runtime requirements.
  Dependencies of these requirements are included automatically.
  In the `build` key, will be used always those same values.
  In the case of `host` key, it specifies the dependencies necessary
  to build and run the module.

  ``` yaml
  requirements:
    build:
      - make
      - perl
      - tclx
      - {{ compiler('c') }}
      - {{ compiler('cxx') }}
    host:
      - epics-base 7
      - require
      - stream
  ```

  The test section defines the test that are run after the build is finished.

  ``` yaml
  test:
    requires:
      - run-iocsh
    commands:
      - run-iocsh -r {{name}}
  ```
