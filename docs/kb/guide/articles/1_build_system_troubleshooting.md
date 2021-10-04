---
orphan: true
---
% Remove this orphan definition when this document is added back into the
% toctree

# Build system troubleshooting 

```{admonition} Under Construction
:class: warning

Please note that this portal currently is being set-up, and that content is evolving fairly rapidly. This specific warning will be removed once this page is in a reasonable state. 
```

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

In most cases when you have the above error, your system does not have the specified version of EPICS base and the require module. These are, as we know, defined in `configure/RELEASE` or `configure/RELEASE_DEV`.

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

`require` will not overwrite a module where the version matches the `major.minor.patch+build` format. To reinstall a module version, you need to do the following:

```console
$ make uninstall
$ make install
```

## Case 3

### Problem

When we run `make init`, we may see the following sort of conflict with the git submodule:

```console
# --- snip snip ---

git submodule update --remote --merge opcua/
X11 forwarding request failed on channel 0
Auto-merging devOpcuaSup/linkParser.cpp
Auto-merging devOpcuaSup/devOpcua.cpp
CONFLICT (content): Merge conflict in devOpcuaSup/devOpcua.cpp
Auto-merging devOpcuaSup/UaSdk/SessionUaSdk.cpp
CONFLICT (content): Merge conflict in devOpcuaSup/UaSdk/SessionUaSdk.cpp
Auto-merging devOpcuaSup/UaSdk/ItemUaSdk.cpp
Auto-merging devOpcuaSup/UaSdk/DataElementUaSdk.cpp
CONFLICT (content): Merge conflict in devOpcuaSup/UaSdk/DataElementUaSdk.cpp
Auto-merging devOpcuaSup/RecordConnector.cpp
Auto-merging configure/CONFIG_OPCUA_VERSION
CONFLICT (content): Merge conflict in configure/CONFIG_OPCUA_VERSION
Automatic merge failed; fix conflicts and then commit the result.
Unable to merge 'a52002c31e6d5d32a21c130af42e579ae17b5b6f' in submodule path 'opcua'
make: *** [/epics/base-7.0.3/require/3.1.1/configure/RULES_E3:88: opcua] Error 2
```

This happens because the main module source repository `opcua` uses complicated branch and release rules. The `master` branch that e3 uses doesn't have enough information about release `v0.5.2` which exists in in branch `release/0.5`.

### Solution

Change the default branch in `.gitmodules` from `master` (undefined) to `release/0.5`: 

```yaml
[submodule "opcua"]
  path = opcua
  url = https://github.com/ralphlange/opcua
  branch = release/0.5
```

