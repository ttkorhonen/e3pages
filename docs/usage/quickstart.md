# Quickstart

```{admonition} Under Construction
:class: warning

Please note that this portal currently is being set-up, and that content is evolving fairly rapidly. This specific warning will be removed once this page is in a reasonable state. 
```

Building e3 locally is fairly easy:

```bash
$ git clone https://gitlab.esss.lu.se/e3/e3.git
$ cd e3
$ ./e3_building_config.bash -b 7.04 -r 3.3.0 -t /opt/epics
$ ./e3.bash base
$ ./e3.bash req
$ ./e3.bash -c mod
$ source tools/setenv
```
