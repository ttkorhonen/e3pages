# Sample IOC

```{admonition} Under Construction
:class: warning

Please note that this portal currently is being set-up, and that content is evolving fairly rapidly. This specific warning will be removed once this page is in a reasonable state. 
```

The following assumes that you already have EPICS base, *require*, and *iocStats* installed.

An IOC in e3 is typically (minimally) just a startup script, preferably also with an `env.sh` file to set environment variables.

## Create the startup script

A very minimal startup script to illustrate what "a typical" IOC in e3 looks like:

```bash
$ touch st.cmd
$ echo "require iocstats" >> st.cmd  # iocInit() is called implicitly
```

## Start the IOC

```bash
$ ./opt/epics/base-7.0.4/require/3.3.0/bin/iocsh.bash st.cmd
```

## Other

You should preferably add a `README.md` documenting the controlled hardware, the host machine (if the IOC is running in a lab), etc., and version control in the proper subgroup under <https://gitlab.esss.lu.se/iocs>
