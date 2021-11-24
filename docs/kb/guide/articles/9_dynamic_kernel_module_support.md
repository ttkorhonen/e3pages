# How to: Build dynamic kernel module support (DKMS)

## Background information

DKMS (Dynamic Kernel Module Support) is a framework that enables
generating Linux kernel modules whose source generally reside
outside the kernel source tree. The concept is to have DKMS
modules automatically rebuilt when a new kernel is installed.

This article describes two alternative ways to build and install a
DKMS module:

* using DKMS tool directly
* using e3

(with_dkms_tool)=

## Build and install DKMS module with DKMS tool

### Prepare a DKMS configure file

To build and install a third-party kernel module as a DKMS module, a
`dkms.conf` file which describes the module source to the DKMS system
is required. It usually looks like the following:

```bash
PACKAGE_NAME=myModuleName
PACKAGE_VERSION=myModuleVersion
BUILT_MODULE_NAME[0]=myModuleName
AUTOINSTALL=yes
```

Add this `dkms.conf` file to your kernel module source, and copy the
DKMS source which contains the kernel module and this `dkms.conf` file
into `/usr/src/myModuleName-myModuleVersion/`

### Build and install the module

When the DKMS source and configuration file is ready, launch the DKMS
tool to build and install the built DKMS module as:

```bash
$ dkms build -m myModuleName -v myModuleVersion
```

This will, first, copy the DKMS source from the above location to the system's DKMS
build location, and then, build the DKMS module in DKMS build location of the system.
After a successful build, install it into the DKMS tree with the following command:

```bash
$ dkms install -m myModuleName -v myModuleVersion
```

This will install the built module into the system's DKMS tree.

## Build and install DKMS module with e3

### Create a DKMS configure file

Please see {ref}`with_dkms_tool` about how to create DKMS configuration file.
The `dkms_add` rule in the following file generates DKMS configuration file
from a template file with macro substitution.

```makefile
KMOD_NAME := mrf

.PHONY: dkms_add

dkms_add: conf
    $(MSI) -M name="$(E3_MODULE_NAME)" -M  version="$(E3_MODULE_VERSION)" -M kmod_name="$(KMOD_NAME)" $(TOP)/dkms/dkms_with_msi.conf.in > $(TOP)/dkms/dkms_with_msi.conf
    $(QUIET) cat $(TOP)/dkms/dkms_with_msi.conf $(TOP)/dkms/dkms_without_msi.conf > $(TOP)/dkms/dkms.conf
    $(QUIET) install -m 644 $(TOP)/dkms/dkms.conf  $(E3_KMOD_SRC_PATH)
    $(SUDO) install -d /usr/src/$(E3_MODULE_NAME)-$(E3_MODULE_VERSION)
    $(SUDO) cp -r $(TOP)/$(E3_KMOD_SRC_PATH)/* /usr/src/$(E3_MODULE_NAME)-$(E3_MODULE_VERSION)/
    $(SUDO) $(DKMS) add $(DKMS_ARGS)

.PHONY: setup
setup:
    $(QUIET) echo "KERNEL==uio*, ATTR{name}==mrf-pci, MODE=0666" | $(SUDO) tee  /etc/udev/rules.d/99-$(KMOD_NAME).rules
    $(QUIET) $(SUDO) /bin/udevadm control --reload-rules
    $(QUIET) $(SUDO) /bin/udevadm trigger
    $(QUIET) echo $(KMOD_NAME) | $(SUDO) tee /etc/modules-load.d/$(KMOD_NAME).conf
    $(QUIET) $(SUDO) depmod --quick
    $(QUIET) $(SUDO) modprobe -rv $(KMOD_NAME)
    $(QUIET) $(SUDO) modprobe -v $(KMOD_NAME)
    $(QUIET) echo ""
    $(QUIET) echo ""
    $(QUIET) echo "It is OK to see \"E3/RULES_DKMS:37: recipe for target 'setup' failed\""
    $(QUIET) echo "---------------------------------------------------------------------"
    $(QUIET) -ls -l /dev/uio* 2>/dev/null
    $(QUIET) echo "---------------------------------------------------------------------"

.PHONY: setup_clean
setup_clean:
    $(QUIET) $(SUDO) modprobe -rv $(KMOD_NAME)
    $(SUDO) rm -f /etc/modules-load.d/$(KMOD_NAME).conf
    $(SUDO) rm -f /etc/udev/rules.d/99-$(KMOD_NAME).rules

```

The rule `dkms_add` processes template DKMS configure file with
macro substitutions, and generates `dkms.conf` file.
It will install the generated file together with the source into
the host file system. The generated `dkms.conf` file includes
`E3_MODULE_NAME`, `E3_MODULE_VERSION` and kernel module name.

### DKMS related makefile rules provided by e3

e3 provides the following makefile rules to build and install
DKMS modules:

* `make dkms_add`
* `make dkms_build`
* `make dkms_install`
* `make setup`
* `make dkms_remove`
* `make dkms_uninstall`

Following explains the rules in detail.

#### make dkms_build

The DKMS build in e3 will invoke the system's DKMS tool to take
the module source from `/usr/src/<module_name>-<module_version>/` directory.
By default, all builds occur in the directory
`/var/lib/dkms/<module_name>/<module_version>/build/`.

After the DKMS tool is invoked, if the `<module_name>` and `<module_version>`
have not been added to the `/var/lib/dkms/` build directory, the tool will copy
them from `/usr/src/<module_name>-<moudle_version>/`. So, just as a normal build,
copy the DKMS source in the system DKMS's source directory is a prerequisite
before launch the `make dkms_build` make command.

#### make dkms_remove

This makefile rule invokes DKMS tool to remove the source in the
`/usr/src/<module_name>-<module_version>/` directory and does a `dkms remove`
of the installed DKMS module from the DKMS tree.

#### make dkms_install

Call DKMS tool from the system to install the module specified by the module
name and module version into the DKMS tree. If the kernel option is not
specified, it assumes the currently running kernel.

#### make dkms_uninstall

Call DKMS tool from the system to uninstall the DKMS module specified by the
module name and module version

### Steps to build and install a DKMS module with e3

```console
  prepare module source and DKMS configuration file
$ cd /wrapper/top/directory
$ make dkms_build
$ make dkms_install
$ make setup
```

Note, when use e3 to build and install DKMS module, `myMoudleName`
must be the same as the corresponding e3 wrapper module's name.
And `myModuleVersion` must be the same as the corresponding
e3 wrapper module's version.
[EOF]
