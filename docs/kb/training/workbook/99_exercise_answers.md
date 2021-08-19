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
#### First IOC
- You should see lines like the following in the output of your IOC that show
  the variables being defined. These are created by `iocsh.bash`, not by the
  startup script.
  ```console
  [iocuser@host:cmds]$ iocsh.bash 1.cmd
  <snip>
  # Set E3_IOCSH_TOP for the absolute path where iocsh.bash is executed.
  epicsEnvSet E3_IOCSH_TOP "/home/waynelewis/git/e3-training-material/4_startup_scripts_in_e3/cmds"
  <snip>
  # Set E3_CMD_TOP for the absolute path where 1.cmd exists
  epicsEnvSet E3_CMD_TOP "/home/waynelewis/git/e3-training-material/4_startup_scripts_in_e3/cmds"
  <snip>
  ```

- The definition of `E3_IOCSH_TOP` will change to the directory from which you
  call `iocsh.bash`.

  The definition of `E3_CMD_TOP` will not change, as it is the path to the
  startup script file.

- The following additional modules will be loaded as direct dependencies of
  `stream`:
  - `asyn`
  - `calc`
  - `pcre`

  Additional modules that are indirect dependencies (via the direct
  dependencies) are also loaded:
  - `sscan`
  - `sequencer`

(env_sh_warning)=
- You may see a warning like
  ```console
  Warning: environment file /home/waynelewis/git/e3-training-material/4_startup_scripts_in_e3/env.sh does not exist.
  ```
  `iocsh.bash` is looking for an `env.sh` file to define a custom environment
  for the IOC. This warning can be ignored if you are not needing to define any
  custom environment variables.

  It is good practice to check the IOC startup messages for any warnings, and
  make sure that you understand the implications of any warnings. Some, like the
  one above, can be safely ignored, but others may have an impact on the
  operation of the IOC.

#### Second IOC
- The official description of the IOC initialisation process is
  [here](https://docs.epics-controls.org/en/latest/specs/IOCInit.html).

- If you delete the `iocInit()` line from the startup script, `iocsh.bash` will
  add it in to the generated startup script used to start the IOC.

  If you comment out the `iocInit()` line:
  ```
  #iocInit()
  ```
  then `iocsh.bash` will not add the iocInit command, and the IOC will be only
  partially started, as `iocInit()` will not be executed. You can run
  `iocInit()` yourself from the IOC shell prompt to complete the IOC startup.

- There are two warnings in this IOC. The first is the one listed
  {ref}`above <env_sh_warning>`.

  The second warning is:
  ```
  drvStreamInit: Warning! STREAM_PROTOCOL_PATH not set. Defaults to "."
  ```
  This is referring to a specific streamdevice requirement for the
  `STREAM_PROTOCOL_PATH` environment variable so that it knows where to search
  for protocol files. This will cause run-time issues with the IOC if there are
  protocol files that the IOC cannot find.

- The second script establishes a communications link to the simulator, so you
  should expect to see some information printed to the simulator console
  indicating that the connection has occurred.

#### IOC the three
- `E3_CMD_TOP` is used to define the value of the `TOP` environment variable.
  ```
  epicsEnvSet("TOP","$(E3_CMD_TOP)/..")
  ```
  `TOP` is then used as the location for a number of other files in other
  commands in the startup script.

- `random.bash` generates a random number and stores it in `random.cmd`.

  `random.cmd` is an IOC startup script snippet that sets an environment
  variable to the generated random number.

- The stream protocol file is `db/example_motor.proto`. This is listed in the
  INP or OUT field each of the records in `db/example_motor.db`:
  ```
  field( INP, "@example_motor.proto read_position $(PORT)")
  ```

- There should be some diagnostic printouts in the simulator reflecting the
  communications from the IOC.

#### For the fourth
- You can locate the PV using
  ```
  localhost-1593 > dbgrep *HEART*
  ```

  This PV value increments once per second while the IOC is running. It can be
  used by other applications to confirm that the IOC is executing by monitoring
  for continuous changes in the value.

- `iocAdminSoft.db` is located in the `db` directory in the `iocstats` module in
  your e3 environment. On the shared file system, the location is:
  ```
  [iocuser@host]$ ls /epics/base-7.0.5/require/3.4.1/siteMods/iocstats/3.1.16+0/db/iocAdminSoft.db
  /epics/base-7.0.5/require/3.4.1/siteMods/iocstats/3.1.16+0/db/iocAdminSoft.db
  ```

  `require` generates a database search path variable, `EPICS_DB_INCLUDE_PATH`,
  which is used by the `dbLoadRecords` command as the list of paths to search
  for database files.

  ```
  localhost-1593 > epicsEnvShow("EPICS_DB_INCLUDE_PATH")
  EPICS_DB_INCLUDE_PATH=.:/epics/base-7.0.5/require/3.4.1/siteMods/iocstats/3.1.16+0/db:/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4+0/db:/epics/base-7.0.5/require/3.4.1/siteMods/sscan/2.11.4+0/db:/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0+0/db
  localhost-1593 >
  ```

### Assignments
1. The list of parameters that can be passed to each module is usually defined
   in the startup script snippet associated with each module. Refer to:
   - `iocStats.iocsh`
   - `autosave.iocsh`
   - `recsync.iocsh`

   from each module.

   Most module startup script snippets expect something like an IOCNAME
   variable, as this is used to create the fully expanded PV names.

   Some variables can have defaults defined in the startup script snippet, which
   can be overridden. See the `recsync.iocsh` snippet for examples of this, such
   as:
   ```
   var(reccastTimeout, "$(TIMEOUT=5.0)")
   ```

   The `autosave.iocsh` file has a long list of variables that can be defined.
   Most are optional. Refer to the documentation at the top of the
   `autosave.iocsh` file for the list of variables and their functions.

2. Potential improvements include:
   - commenting.
   - a production IOC would not use random numbers for PV names, as clients
	 would need to be updated each time the IOC is restarted.
   - using the `essioc` module to load the standard set of IOC modules (for ESS
     IOCs), which includes:
	 - `iocstats`
	 - `autosave`
	 - `recsync`
	 - `auth`
	 - `caputlog`

3. Add the following lines before the `iocInit` line:
   ```
   epicsEnvSet("IOCNAME2", "$(P)-2")
   epicsEnvSet("PORT2", "MOTOR2")

   drvAsynIPPortConfigure("$(PORT2)", "127.0.0.1:9998", 0, 0, 0)

   dbLoadRecords("$(TOP)/db/example_motor.db", "P=$(IOCNAME2),S=:,PORT=$(PORT2)")
   ```

   Note how the same commands are used, the only changes are in the values of
   the variables so that the port name and PV names are unique.

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





