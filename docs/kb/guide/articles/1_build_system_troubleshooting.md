# Build system troubleshooting 

## Case 1

### Problem

When we run any of the e3 `make` instructions (e.g. `make vars`, `make build`), we may see the following message:

```console
configure/CONFIG:19: /epics/base-7.0.5/require/3.4.1/configure/CONFIG: No such file or directory
/epics/base-7.0.5/require/3.4.1/configure/RULES_SITEAPPS: No such file or directory
make: *** No rule to make target '/epics/base-7.0.5/require/3.4.1/configure/RULES_SITEMODS'.  Stop.
```

### Solution

Look up the definition of the `EPICS_BASE` and `E3_REQUIRE_VERSION` variables in `configure/RELEASE` or `configure/RELEASE_DEV` file, and check that the physical location of `EPICS_BASE\require/E3_REQUIRE_VERSION` exists on your system:

```console
[iocuser@host:~]$ ls -lta /epics/base-7.0.5/require/3.4.1/
```

In most cases when you have the above error, your system does not have the specified version of EPICS base and the _require_ module. These are, as we know, defined in `configure/RELEASE` or `configure/RELEASE_DEV`.

A quick-fix to this is to use e3 in local mode and specify the versions there:

```console
[iocuser@host:~]$ echo "EPICS_BASE=/home/iocuser/epics/base-7.0.5" > configure/RELEASE.local
[iocuser@host:~]$ echo "E3_REQUIRE_VERSION=3.4.1" >> configure/RELEASE.local
```

Of course modify the path above to where you have EPICS installed.

---

## Case 2

### Problem

When we run `make install` or `make devinstall`, we may see the following message:

```console
Error: /home/waynelewis/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0+0/lib/linux-x86_64 already exists.
Note: If you really want to overwrite then uninstall first.
make[3]: *** [install] Error 1
```

### Solution

_require_ will not overwrite a module where the version matches the `major.minor.patch+build` format. To reinstall a module version, you need to do the following:

```console
$ make uninstall
$ make install
```

