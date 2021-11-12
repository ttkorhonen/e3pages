
# How to: Build Dynamic Kernel Module Support Module (DKMS)

## 1. ) Background information

We have simplified the standard e3 wrapper template to remove the boilerplate
`RULES_DKMS_L` file, and associated DKMS build stuffs from the e3
wrapper(e3 cookie-cutter).

DKMS (Dynamic Kernel Module Support) is a framework for third party kernel
modules which are automatically rebuilt when new kernels are installed.

This section provides some information about the DKMS contents removed from
the e3 build system, and informations about how to build a DKMS after this
contents have been removed.

## 2. ) Removed DKMS(Dynamic Kernel Module Support) in e3 wrapper

The removed `RULES_DKMS_L` file in e3 wrapper defines makefile rules to
prepare and install a DKMS module's configure and source files into
system's file system. It also provides rules to make the user space
device driver deamon to reload its rule so that the newly built and
installed DKMS module can work properly.

The contents of RUELS_DKMS_L file, which will be deleted, are as following:

```console
# KMOD_NAME := mrf

# .PHONY: dkms_add

# dkms_add: conf
#       $(MSI) -M name="$(E3_MODULE_NAME)" -M  version="$(E3_MODULE_VERSION)" -M kmod_name="$(KMOD_NAME)" $(TOP)/dkms/dkms_with_msi.conf.in > $(TOP)/dkms/dkms_with_msi.conf
#       $(QUIET) cat $(TOP)/dkms/dkms_with_msi.conf $(TOP)/dkms/dkms_without_msi.conf > $(TOP)/dkms/dkms.conf
#       $(QUIET) install -m 644 $(TOP)/dkms/dkms.conf  $(E3_KMOD_SRC_PATH)/
#       $(SUDO) install -d /usr/src/$(E3_MODULE_NAME)-$(E3_MODULE_VERSION)
#       $(SUDO) cp -r $(TOP)/$(E3_KMOD_SRC_PATH)/* /usr/src/$(E3_MODULE_NAME)-$(E3_MODULE_VERSION)/
#       $(SUDO) $(DKMS) add $(DKMS_ARGS)

# setup:
#       $(QUIET) $(SUDO2) 'echo KERNEL==\"uio*\", ATTR{name}==\"mrf-pci\", MODE=\"0666\" | tee  /etc/udev/rules.d/99-$(KMOD_NAME).rules'
#       $(QUIET) $(SUDO) /bin/udevadm control --reload-rules
#       $(QUIET) $(SUDO) /bin/udevadm trigger
#       $(QUIET) $(SUDO2) 'echo $(KMOD_NAME) | tee /etc/modules-load.d/$(KMOD_NAME).conf'
#       $(QUIET) $(SUDO) depmod --quick
#       $(QUIET) $(SUDO) modprobe -rv $(KMOD_NAME)
#       $(QUIET) $(SUDO) modprobe -v $(KMOD_NAME)
#       $(QUIET) echo ""
#       $(QUIET) echo ""
#       $(QUIET) echo "It is OK to see \"E3/RULES_DKMS:37: recipe for target 'setup' failed\""
#       $(QUIET) echo "---------------------------------------------------------------------"
#       $(QUIET) -ls -l /dev/uio* 2>/dev/null
#       $(QUIET) echo "---------------------------------------------------------------------"

# setup_clean:
#       $(QUIET) $(SUDO) modprobe -rv $(KMOD_NAME)
#       $(SUDO) rm -f /etc/modules-load.d/$(KMOD_NAME).conf
#       $(SUDO) rm -f /etc/udev/rules.d/99-$(KMOD_NAME).rules

# .PHONY: setup setup_clean
```

This file(`RULES_DKMS_L`) is part of the cookie-cutter for e3 wrapper. That
means that each e3 wrapper module created with the cookie-cutter will have
this file included as part of the wrapper. However, these rules seems not a
general rules which can be used by all e3 wrappers. Probably, this is one
reason that why it never be used(commented out).

The rule `dkms_add` uses macro substitution tool to process a template DKMS
configure file with macro substitutions, to generate a `dkms.conf` file and
install it together with other kernel source files of the DKMS module into
the host system. The generated `dkms.conf` file includes `E3_MODULE_NAME`,
`E3_MODULE_VERSION` and kernel module name.

The rule `setup` seems try to setup user space input output driver deamon
to reload its rules so that the newly installed DKMS module can work properly.
The make rule which does `dkms build` is not included in this file. The
original design seems intending to use the `dkms_add` rule defined in
this file to prepare and install the DKMS source and configure files into
the system's DKMS source location. And then use the `dkms_build` rule
defined in e3 `require` module to build and install the DKMS model into
system's DKMS tree. And then use the `setup` rule defined in this file
to make the user space input output driver deamon to reload its rules
so that the newly built DKMS module can work properly.

However, this file seems not a general file which can be used for all e3
wrappers. And it sees that it has never been used.

## 3.) Build and install a third-party kernel module as a DKMS module

### 3.1) Build and install DKMS module with dkms tool

DKMS is usually for kernel device driver. DKMS tool comes with systems
provide convenient way to build and install a third party kernel module as DKMS module.

To build and install a third-party kernel module as a DKMS module, one must
have the kernel module source to be built. If the kernel module does not exist,
one need to get it or write your own.

To build and install a third-party kernel module as a DKMS module, a `dkms.conf`
file which describes the module source to the DKMS system is required. It usually
looks like the following:

```console
    PACKAGE_NAME="myModuleName"
    PACKAGE_VERSION="myModuleVersion"
    BUILT_MODULE_NAME[0]="myModuleName"
    AUTOINSTALL="yes"
```

Add this `dkms.conf` file to your kernel module source, and copy the DKMS source
which contains the kernel module and this `dkms.conf` file into the following directory:

```console
    /usr/src/myModuleName-myModuleVersion/
```

After this is done, launch DKMS tool to build and install the built DKMS module as:

```console
    dkms build -m myModuleName -v myModuleVersion
```

This will, first, copy the DKMS source from the above location to the system's DKMS
build location, and then, build the DKMS module in DKMS build location of the system.
After a successful build, install it into the DKMS tree with the following command:

```console
    dkms install -m myModuleName -v myModuleVersion
```

This will install the built module into the system's DKMS tree.

## 4. ) DKMS build in e3

### 4.1) CONFIG_DKMS file

Following is the contents of the CONFIG_DKMS file in e3 require module:

```console
    DKMS := /usr/sbin/dkms
    DKMS_ARGS := -m $(E3_MODULE_NAME) -v $(E3_MODULE_VERSION)

    VARS_EXCLUDES+=DKMS_ARGS
    VARS_EXCLUDES+=DKMS
```

This file defines makefile variables for the DKMS tool.

### 4.2) RULES_DKMS

Following is the contents of the RULES_DKMS file in e3 require module:

```console
    .PHONY: dkms_build dkms_remove dkms_install dkms_uninstall

    dkms_build:
        $(DKMS) build $(DKMS_ARGS)

    dkms_remove:
	    $(DKMS) remove $(E3_MODULE_NAME)/$(E3_MODULE_VERSION) --all
	    rm -rf /usr/src/$(E3_MODULE_NAME)-$(E3_MODULE_VERSION)

    dkms_install:
	    $(DKMS) install $(DKMS_ARGS)
	    $(QUIET) depmod

    dkms_uninstall:
        $(DKMS) uninstall $(DKMS_ARGS)
        $(QUIET) depmod

    .PHONY: dkms_build dkms_install dkms_remove dkms_uninstall
```

This file defines the makefile rules for building a DKMS module with e3.

So, the e3 RULES_DKMS provides the following makefile rules:

```console
    a.) “make dkms_build”
    b.) “make dkms_install”
    c.) “make dkms_remove”
    d.) “make dems_uninstall”
```

Following are detail explanation of each of the rule.

#### 4.2.1.) make dkms_build

The DKMS build in original e3 will invoke the system's DKMS tool to take
the module source from `/usr/src/<module_name>-<module_version>/` directory.
According to the DKMS tool's manual, by default, all builds occur in the
directory `/var/lib/dkms/<module_name>/<module_version>/build/`.

After the DKMS tool is invoked, if the `<module_name>` and `<module_version>`
have not been added to the `/var/lib/dkms/` build directory, the tool will copy
them from `/usr/src/<module_name>-<moudle_version>/`. So, just as a normal build,
copy the DKMS source in the system DKMS's source directory is a prerequisite
before launch the `make dkms_build` make command.

#### 4.2.2.) make dkms_remove

This makefile rule invoke DKMS tool to remove the source in the
`/usr/src/<module_name>-<module_version>/` directory and do a `dkms remove`
of the installed DKMS module from the DKMS tree

#### 4.2.3.) make dkms_install

Call DKMS tool from the system to install the module specified by the module
name and module version into the DKMS tree. If the kernel option is not specified,
it assumes the currently running kernel.

#### 4.2.4.) make dkms_uninstall

Call DKMS tool from the system to uninstall the DKMS module specified by the
module name and module version

### 4.3.)  build DKMS kernel module with e3

Although the `RULES_DKMS_L` rule has be removed from e3 wrapper modules, one
still can build a DKMS kernel module with e3 build system.
The build and install processes are similar as normal DKMS build and install process.
E3 try to associate the DKMS module and the e3 wrapper module which depends on it
together(From this point of view, it might be good to modify the cookie-cutter to
let it create a `dkms` directory in e3 wrapper module).

To build a DKMS module with e3, do the same preparation described in section 3.1. 
That is to get the kernel module source or write your own kernel module, and add a
`dkms.conf` file to the kernel module source. A typical simple dkms.conf file looks
like the following:

```console
    PACKAGE_NAME="myModuleName"
    PACKAGE_VERSION="myModuleVersion"
    BUILT_MODULE_NAME[0]="myModuleName"
    AUTOINSTALL="yes"
```

When the DKMS source is ready, copy the DKMS source which contains the kernel
module files and the dkms.conf file into:

```console
    /usr/src/myModuleName-myModuleVerson/
```

After the source has been copied, at the top of the e3 wrapper directory, do:

```console
    make dkms_build
```

This will build the DKMS module in the default DKMS build location of the system.
After a successful build, launch the following command to install the built DKMS
module into the DKMS tree:

```console
    make dkms_install
```

Note, when use e3 build rules, `myMoudleName` should be the same as the corresponding
e3 wrapper module name. And `myModuleVersion` should be the same as the corresponding
e3 wrapper module's version.
