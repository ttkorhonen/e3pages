# Sample IOC

The following assumes that you already have EPICS base, *require*, and *iocStats* installed.

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
