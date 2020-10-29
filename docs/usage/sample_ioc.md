# Sample IOC

```{admonition} Under Construction
:class: warning

Please note that this portal currently is being set-up, and that content is evolving fairly rapidly. This specific warning will be removed once this page is in a reasonable state. 
```

The following assumes that you already have EPICS base, *require*, and *iocStats* installed.

An IOC in e3 is typically (minimally) just a startup script, preferably also with an `env.sh` file to set environment variables.

## Create the startup script

```bash
$ touch st.cmd
$ echo "require iocstats" >> st.cmd
$ ./opt/epics/base-7.0.4/require/3.3.0/bin/iocsh.bash st.cmd
```

## Populate the directory

Add `README.md`.

## Upload the directory to GiLab

You should upload your IOC to the proper subgroup under <https://gitlab.esss.lu.se/iocs>
