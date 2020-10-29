# Quickstart

```{admonition} Under Construction
:class: warning

Please note that this portal currently is being set-up, and that content is evolving fairly rapidly. This specific warning will be removed once this page is in a reasonable state. 
```

Building EPICS with "common modules" using e3 is fairly easy. Note, however, that the workflow (and tools) listed below typically isn't what you would do for a production build.

# Building a local e3 environment

```bash
$ git clone https://gitlab.esss.lu.se/e3/e3.git
$ cd e3
$ ./e3_building_config.bash -b 7.04 -r 3.3.0 -t /opt/epics
$ ./e3.bash base
$ ./e3.bash req
$ ./e3.bash -c mod
```

# Sourcing a specific e3 environment

```bash
$ source /path/to/epics/<EPICS_VERSION>/require/<REQUIRE_VERSION>/bin/setE3Env.bash
```

or, alternatively:

```bash
$ source /path/to/e3/repository/tools/setenv
```
