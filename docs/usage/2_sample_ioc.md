# Sample IOC

The following assumes that you already have EPICS base, *require* (`3.3.0` or later as the module version has been left out), and *iocStats* installed.

An IOC in e3 is typically (minimally) just a startup script---passed to `softIoc` or `softIocPVA`---preferably also with an `env.sh` file to define environment variables (such as `$IOCNAME`, and/or the architecture and versions to be used when calling `iocsh.bash` using macros[^1]).

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


[^1]: With macros, you could run `./epics/${BASE_VERSION}/require/{REQUIRE_VERSION}/bin/iocsh.bash`.
