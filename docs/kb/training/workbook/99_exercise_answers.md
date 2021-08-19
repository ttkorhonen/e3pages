# Answers to exercises, assignments, and questions

## Installing e3

### Exercises
None

### Assignments

1. Understanding makefiles and git submodules.

   1. [makefile documentation](https://www.gnu.org/software/make/manual/html_node/index.html)
   2. [git submodule documentation](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
   3. git submodules are used to link from an e3 wrapper to the module source
   code repository. The `make init` step performs the following `git submodule`
   commands:
   ```console
   git submodule init fug/
   git submodule update --init --recursive fug/
   ```

2. You should end up with the following directories in your e3 installation
   location. Your host name will be different and the installation location may be
   different from the example below.
   ```console
   [test-vm-wl02] 19:03 $ ls -1 /epics
   base-7.0.3.1
   base-7.0.5
   ```

3. Clone the [e3 repository](https://gitlab.esss.lu.se/e3/e3.git).

   The groups and the contents of each group are defined in the
   `tools/e3-inventory.yaml` file.

   References to the group names defined in `tools/e3-inventory.yaml` exist in the following files:
   * `e3.bash`
   * `tools/e3_modules_list.sh`

   Adding a module to a group is done by editing the `tools/e3-inventory.yaml`
   file.

   Adding a new group involves editing all three files:
   * `e3.bash`
   * `tools/e3_modules_list.sh`
   * `tools/e3-inventory.yaml`

## An e3 IOC
### Exercises
None

### Assignments
1. A brief description of each expression meaning, function, and/or action
   follows, along with references for more details.
   - `require` is the keyword used by the require module to indicate that a
	 module needs to be loaded into this IOC. When the IOC starts, the require
	 module will load all modules identified in the startup script, along with
	 any dependencies.
   - `E3_CMD_TOP` is the path to the directory holding the startup script used
	 to launch the IOC.
   - `system` is an IOC function used to execute an operating system command.
	 [EPICS system utility
	 command](https://epics.anl.gov/base/R3-15/6-docs/AppDevGuide/IOCShell.html#x19-74000018.2.5)
   - `iocshLoad` loads a startup script snippet. This allows each module to
	 define the required IOC startup script commands for the module in a file
	 which is loaded by the IOC. [EPICS iocshLoad
	 description](https://epics.anl.gov/base/R3-15/6-docs/AppDevGuide/IOCShell.html#x19-74400018.3.1)
   - `iocInit` tells the IOC to perform all initialisation tasks, including
	 driver and database initialisation. All database files must be loaded prior
	 to calling `iocInit`.
	 [iocInit](https://docs.epics-controls.org/en/latest/specs/IOCInit.html)

	 `iocInit` must be executed to start the IOC. `iocsh.bash` adds `iocInit` to
	 the generated startup script if it is not present in the user-provided
	 startup script.
   - `>` is the output redirect command. It will send any `stdout` output to the
	 location following the `>`. If it is writing to a file, it will overwrite
	 any existing contents of the file. Use `>>` to append to any existing
	 contents in a file. [Redirection
	 commands](https://epics.anl.gov/base/R3-15/6-docs/AppDevGuide/IOCShell.html#x19-73900018.2.4)
   - `<` is the input redirect command. In an IOC, this is used to read in the
	 contents of another file and execute those commands in the IOC shell. We
	 recommend using `iocshLoad` instead of `<`. [Redirection
	 commands](https://epics.anl.gov/base/R3-15/6-docs/AppDevGuide/IOCShell.html#x19-73900018.2.4)
	 
2. The short answer to this question is "It depends.".

   In some cases, placing commands in a different order in the startup script
   makes no difference. This is true for commands that don't have any dependence
   on previous commands, including loading of database files. It also applies to
   the `iocshLoad` commands for startup script snippets, assuming the snippets
   are all independent of each other (e.g., referencing different devices). 

   Any commands that call driver functions directly and depend on previous calls
   having been made (e.g., to create a named asyn port) need to be called in a
   specific order so that the required code has been executed and objects
   created and/or memory allocated in the correct order. 

   `iocInit` must not be called until all databases and database definitions
   have been loaded, as no new records can be added after `iocInit` has run.




## Installing other versions of modules
### Exercises

### Assignments
1. The command is:
   ```console
   $ make existent LEVEL=4
   ```
   The output should look something like the following, with the `LEVEL=4`
   selection additionally (compared with `LEVEL=3`) showing the installed files
   for each architecture in the `lib` directory.

   ```console
    [iocuser@host:e3-stream]$ make existent LEVEL=4
	/epics/base-7.0.5/require/3.4.1/siteMods/stream
	└── 2.8.18+0
		├── dbd
		│   └── stream.dbd
		├── include
		│   ├── devStream.h
		│   ├── MacroMagic.h
		│   ├── StreamBuffer.h
		│   ├── StreamBusInterface.h
		│   ├── StreamCore.h
		│   ├── StreamError.h
		│   ├── StreamFormatConverter.h
		│   ├── StreamFormat.h
		│   └── StreamProtocol.h
		├── lib
		│   ├── linux-corei7-poky
		│   │   ├── libstream.so
		│   │   └── stream.dep
		│   ├── linux-ppc64e6500
		│   │   ├── libstream.so
		│   │   └── stream.dep
		│   └── linux-x86_64
		│       ├── libstream.so
		│       └── stream.dep
		├── SetSerialPort.iocsh
		└── stream_meta.yaml

	7 directories, 18 files
    [iocuser@host:e3-stream]$
   ```

2. `make init` performs the following functions to set up the e3 wrapper and
   submodule for the subsequent steps:
   - de-initialise and remove any stored data for the submodule
   - re-initialise the submodule
   - clone the submodule
   - update the submodule to the required reference
   - enter the submodule directory and clones the reference provided in the
	 wrapper configuration file (`CONFIG_MODULE` or `CONFIG_MODULE_DEV`)

   :::{Note}
   The current use of submodules (as of require-3.4.1) in the e3 wrappers is not
   consistent with normal submodule usage. The submodule reference update is
   overridden by the subsequent `git checkout` command, which makes the step
   where the submodule is updated (step 4 above) redundant. The use of
   submodules may change in a future release of e3, which will change the
   behaviour of the `make init` command.
   :::

3. e3 installed module names must consist only of:
   - lower-case characters in the a-z range (no accents or Unicode characters)
   - numbers
   - the underscore `_` character

   The module name must begin with a character between 'a' and 'z'.

   :::{Note}
   There are no restrictions on the repository or wrapper names. However, e3
   best practice is to make the wrapper name, and the repository names/URLs,
   consistent with the installed module name where possible. This is not always
   possible for community-sourced modules, where upper-case characters are often
   used.
   :::

4. `make uninstall`

5. The commands can be combined as:
   ```console
   $ make build install
   ```

   Alternatively, the `make rebuild` command will call the following targets in
   order:
   - `clean`
   - `build`
   - `install`

6. `require` will default to loading the latest version that matches the
   `major.minor.patch` format, as these are considered the production releases
   of the module. To load a version that does not match this format, specify the
   version name explicitly when starting the IOC:

   ```console
   [iocuser@host:e3-stream]$ iocsh.bash -r stream,e3training
   ```




## Startup scripts in e3
### Exercises

### Assignments
1.
2.
3.
4.
5.
6.




## Anatomy of an e3 module
### Exercises

### Assignments
1.
2.
3.
4.
5.
6.




## Variables within e3
### Exercises

### Assignments
1.
2.
3.
4.
5.
6.




## Understanding module dependence
### Exercises

### Assignments
1.
2.
3.
4.
5.
6.




## Building an e3 module
### Exercises

### Assignments
1.
2.
3.
4.
5.
6.




## Other dependencies
### Exercises

### Assignments
1.
2.
3.
4.
5.
6.




## Additional working modes
### Exercises

### Assignments
1.
2.
3.
4.
5.
6.




## Supplementary tools
### Exercises

### Assignments
1.
2.
3.
4.
5.
6.





