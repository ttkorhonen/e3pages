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

(warnings)=
- You may see a warning like
  ```console
  Warning: environment file /home/waynelewis/git/e3-training-material/4_startup_scripts_in_e3/env.sh does not exist.
  ```
  `iocsh.bash` is looking for an `env.sh` file to define a custom environment
  for the IOC. This warning can be ignored if you are not needing to define any
  custom environment variables. Note that this warning only will turn up if you are using a version of require < 4.0.0; otherwise the corresponding check will be for whether the variable `IOCNAME` has been defined.

  The second warning is:
  ```
  drvStreamInit: Warning! STREAM_PROTOCOL_PATH not set. Defaults to "."
  ```

  This is referring to a specific streamdevice requirement for the
  `STREAM_PROTOCOL_PATH` environment variable so that it knows where to search
  for protocol files. This will cause run-time issues with the IOC if there are
  protocol files that the IOC cannot find.

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

- There are two warnings in this IOC. They are described {ref}`above <warnings>`.

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
  ```console
  [iocuser@host:~]$ ls /epics/base-7.0.5/require/3.4.1/siteMods/iocstats/3.1.16+0/db/iocAdminSoft.db
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

## Anatomy of an e3 module
### Exercises
None

### Assignments
1. e3 make targets are defined a number of locations, including:
   - `/epics/base-7.0.5/require/3.4.1/configure/RULES_*`
   - `/epics/base-7.0.5/require/3.4.1/tools/driver.makefile`

   Running `make help` gives a list of the commonly used targets.

(dot_local_file)=
2. Create a `CONFIG_MODULE.local` file in the `e3-<module>/configure` directory,
   and set the new `EPICS_MODULE_TAG` value in this file. This will override the
   value in `CONFIG_MODULE`.

   It is possible for the `git status` to not show a completely clean response,
   as it may identify two potential changes, one to the submodule contents, and
   one identifying the new `CONFIG_MODULE.local` file as being untracked. This
   is OK.

   ```console
   [iocuser@localhost:e3-iocStats]$ git st
   # HEAD detached at 7.0.5-3.4.1/3.1.16-2fd5f31-20210426T180403
   # Changes not staged for commit:
   #   (use "git add <file>..." to update what will be committed)
   #   (use "git checkout -- <file>..." to discard changes in working directory)
   #
   #	modified:   iocStats (new commits)
   #
   # Untracked files:
   #   (use "git add <file>..." to include in what will be committed)
   #
   #	configure/CONFIG_MODULE.local
   no changes added to commit (use "git add" and/or "git commit -a")
   [iocuser@localhost:e3-iocStats]$ cat configure/CONFIG_MODULE.local
   EPICS_MODULE_TAG:=tags/3.1.15
   [iocuser@localhost:e3-iocStats]$
   ```

	Another method of changing the reference is to define it on the command line
	when issuing the `make init` command:
	```console
   [iocuser@localhost:e3-iocStats]$ make init EPICS_MODULE_TAG:=tags/3.1.15
   ```

3. A `p0` patch uses the paths exactly as defined in the patch file, while the
   `p1` patch strips any leading slash from the paths in the patch file, making
   it a relative path. Run the `man patch` command and look for the
   documentation for the `-p` option.

   For details of what happens behind the scenes, see the `RULES_PATCH` and
   `DEFINES_FT` in `/epics/base-7.0.5/require/3.4.1/configure` for the actual
   commands being executed.





## Variables within e3
### Exercises
#### Variables created by `require`
- Add the following to the top of the IOC startup script:
  ```
  require stream
  ```

  There will be a few new \<module\>\_DIR environment variables:
  ```
  <snip>
  localhost-1593 > epicsEnvShow
  <snip>
  asyn_DIR=/epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.41.0+0/
  pcre_DIR=/epics/base-7.0.5/require/3.4.1/siteMods/pcre/8.44.0+0/
  stream_DIR=/epics/base-7.0.5/require/3.4.1/siteMods/stream/2.8.18+0/
  sequencer_DIR=/epics/base-7.0.5/require/3.4.1/siteMods/sequencer/2.2.8+0/
  sscan_DIR=/epics/base-7.0.5/require/3.4.1/siteMods/sscan/2.11.4+0/
  calc_DIR=/epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4+0/
  <snip>
  ```
  
  `asyn`, `pcre`, and `calc` are all dependencies of `stream`, while `sscan` and `sequencer` are dependencies of `calc`.
  All of these modules must then be loaded, and *require* will then specify the respective paths.

#### EPICS variables, parameters, and environment variables
- Single variables can be printed by passing the variable name to
  `epicsEnvShow`:
  ```
  localhost-1593 > epicsEnvShow("stream_DIR")
  stream_DIR=/epics/base-7.0.5/require/3.4.1/siteMods/stream/2.8.18+0/
  localhost-1593 >
  ```

- From the IOC's perspective, the parentheses `()` and braces `{}` are
  considered to be equivalent. See
  [here](https://epics.anl.gov/base/R3-15/6-docs/AppDevGuide/IOCShell.html#x19-73600018.2.1)
  for more information.

  Unix shells do not require the parentheses or braces when referencing an
  environment variable. The name is prefixed with the `$` symbol only. Braces
  can also be used around the variable name in a Unix shell. See the 'Brace
  Expansion' section on the [bash man
  page](https://man7.org/linux/man-pages/man1/bash.1.html).

  The `$(command)` form in Bash creates a subshell and executes the `command`
  part, so has a completely different effect to the EPICS usage.  See the
  'Command Substitution' section in the [bash man
  page](https://man7.org/linux/man-pages/man1/bash.1.html).

- Apart from the fact that the startup script includes some `epicsEnvShow`
  commands, the main difference is that the version using the `ch6.cmd` file
  sets the `E3_CMD_TOP` variable to the path for the startup script file.

- The `stream` module has the `streamDebug` variable.

### Assignments
1. The `asyn_DB` EPICS environment variable defines the location for asyn
   databases.

   The `system` command can be used to access shell commands.
   ```
   localhost-1593 > system "ls $(asyn_DB)"
   asynFloat64TimeSeries.db  asynInt32TimeSeries.db  asynRecord.db
   localhost-1593 >
   ```

2. Use the `--debug` flag to `make`:
   ```console
   [iocuser@localhost:e3-asyn]$ make --debug vars
   <snip>
   Reading makefiles...
   Updating goal targets....
   File `vars' does not exist.
   File `header' does not exist.
   Must remake target `header'.
   Invoking recipe from /epics/base-7.0.5/require/3.4.1/configure/RULES_VARS:34 to update target `header'.
   <snip>
   ```
   The `Invoking recipe` line provides a clue to the location of the `vars` make
   rule.

   In the `/epics/base-7.0.5/require/3.4.1/configure/RULES_VARS` file, the
   `vars` rule is as follows:

   ```make
   ## Print relevant environment variables
   .PHONY: vars
   vars: header
   		$(foreach v, $(E3_MODULES_VARIABLES), $(info $(v) = $($(v)))) @#noop
   ```

## Understanding module dependence
### Exercises

#### Dependent environment variables

There are several possible reasons to use a `CONFIG_MODULE.local` file instead of directly modifying `CONFIG_MODULE`. One is that it keeps the git status clean, which can make one feel better.

Another reason is to allow for temporary site-specific changes while preserving the community wrapper.

Finally, another possible reason is to synchronise between multiple modules: if you store your wrappers in a common location:
```console
[iocuser@host:e3]$ tree -L 1 modules/
modules/
|-- area
|-- bi
|-- CONFIG_MODULE.local
|-- communication
|-- core
|-- devices
|-- ecat
|-- ifc
|-- mps
|-- ps
|-- psi
|-- rf
|-- ts
`-- vac
```
then you can modify a single file in order to update the dependency versions of every module.

#### Updating a dependency

- The expression `require stream` in your startup script will load the *highest numerical version* available. So if you have the following versions installed
  ```console
  [iocuser@host:e3-stream]$ make existent LEVEL=1
  /epics/base-7.0.5/require/3.4.1/siteMods/stream
  |-- 2.8.18+0
  `-- e3training
  ```
  then `require stream` will load 2.8.18+0.
- In the first and third cases, where you load *stream* 2.8.18, then the version of *asyn* that is loaded is 4.41.0. This can be seen in the output of the IOC upon startup, or by looking at the following PVs that are generated by require:
  ```console
  localhost-25251 > dbgrep *_VER
  REQMOD:localhost-25251:MOD_VER
  REQMOD:localhost-25251:require_VER
  REQMOD:localhost-25251:asyn_VER
  REQMOD:localhost-25251:sequencer_VER
  REQMOD:localhost-25251:sscan_VER
  REQMOD:localhost-25251:calc_VER
  REQMOD:localhost-25251:pcre_VER
  REQMOD:localhost-25251:stream_VER
  ```
  In the middle case, it is *asyn* 4.42.0 that is loaded, as specified in `CONFIG_MODULE.local` during the build and install of that version.
- If you run `iocsh.bash -r stream -r asyn`, then it should load fine. However, if you run `iocsh.bash -r asyn -r stream` (with the versions installed as in this chapter), then the IOC will fail to start up:
  ```console
  [iocuser@host:~]$ iocsh.bash -r asyn -r stream
  # --- snip snip ---
  equire asyn
  Module asyn version 4.42.0+0 found in /epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.42.0+0/
  Loading library /epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.42.0+0/lib/linux-x86_64/libasyn.so
  Loaded asyn version 4.42.0+0
  Loading dbd file /epics/base-7.0.5/require/3.4.1/siteMods/asyn/4.42.0+0/dbd/asyn.dbd
  Calling function asyn_registerRecordDeviceDriver
  Loading module info records for asyn
  require stream
  Module stream version 2.8.18+0 found in /epics/base-7.0.5/require/3.4.1/siteMods/stream/2.8.18+0/
  Module stream depends on asyn 4.41.0+0
  Conflict between requested asyn version 4.41.0+0 and already loaded version 4.42.0+0.
  Aborting startup script
  ```
  This is due to the order in which the modules are loaded. First, we load the latest numeric version of *asyn* (4.42.0), followed by the latest numeric version of *stream* (2.8.18). However, that version of *stream* depends on a different version of *asyn* than is loaded, and due to this incompatibility, the IOC shuts down.

  Note that this is one example of what is meant by the fact that *require* can only perform rudimentary dependency resolution.
- The dependency information is stored in the file `$module.dep`:
  ```console
  [iocuser@host:~]$ cat /epics/base-7.0.5/require/3.4.1/siteMods/stream/2.8.18+0/lib/linux-x86_64/stream.dep 
  # Generated file. Do not edit.
  asyn 4.41.0+0
  calc 3.7.4+0
  pcre 8.44.0+0
  [iocuser@host:~]$ cat /epics/base-7.0.5/require/3.4.1/siteMods/stream/e3training/lib/linux-x86_64/stream.dep 
  # Generated file. Do not edit.
  asyn 4.42.0+0
  calc 3.7.4+0
  pcre 8.44.0+0
  ```

#### Dependency resolution limitations

- If you were to release a new version of asyn after the IOC has been developed then as in the example above, you will have an inconsistency in loaded and dependent versions of *asyn*, causing the IOC to fail to start up.
  
  This is a challenge for a maintainer of a shared environment because this means that a functional IOC can fail due to changes in the environment that seem unrelated to the IOC.

  In this case, the fix is simple. An IOC should only load top-level modules (i.e. *stream*, but not *asyn*). However, this does not address all cases

#### Whence cometh the dependencies

- *calc* is referenced in the file `devscalcoutStream.c`, and *pcre* is referenced in `RegexpConverter.cc`.

### Assignments
1. `e3-fug` is contained in the group `ps` (loaded with `-s`):
   ```console
   [iocuser@host:e3]$ ./e3.bash -so vars
   >> Vertical display for the selected modules :

    Modules List 
       0 : ps/e3-caenelsmagnetps
       1 : ps/e3-fug      # Here it is! 
       2 : ps/e3-sairem
       3 : ps/e3-sorensen
       4 : ps/e3-tdklambdagenesys
       5 : ps/e3-magnetps
       6 : ps/e3-caenelfastps
       7 : ps/e3-caensyproxy
   ```
   If you install it as a part of a group, you are certain to get all of the necessary dependencies installed as well - both from the dependent groups, but also from any modules within that group that may be necessary.
2. The only place that it is referenced in the temporary build files is in `fug.dep`:
   ```console
   [iocuser@host:e3-fug]$ grep -nr stream fug/O.7.0.5_linux-x86_64/
   fug/O.7.0.5_linux-x86_64/fug.dep:2:stream 2.8.18+0
   ```
3. `e3-fug` knows that stream is a dependency due to the variable `REQUIRED` used in `fug.Makefile`:
   ```make
   [iocuser@host:e3-fug]$ grep  stream fug.Makefile 
   REQUIRED += stream
   stream_VERSION=$(STREAM_DEP_VERSION)
   ```
   This allows *require* to keep track of run-time dependencies.




## Building an e3 module
### Exercises

#### IOCs

- As seen in [An e3 IOC](2_e3_ioc.md), you can use the variable `$(E3_CMD_TOP)` to refer to the directory which holds `st.cmd`.

#### External modules

- `make init patch` should always be run before building a new module. This will do two things:
  1. Make sure that the submodule is initialised correctly 
  2. Make sure that all of the correct patches have been applied
  Without these two steps, it is possible that the module you are trying to build might not build as expected, or could even fail to build at all.

### Assignments
1. There is an `st.cmd` included with the repository that we can use as a basis for our e3 startup script. One possibility is
   ```sh
   require stream
   require fimscb
   epicsEnvSet("STREAM_PROTOCOL_PATH", "$(fimscb_DB)")

   epicsEnvSet(P, FIMSCB)
   epicsEnvSet(R, KAM)

   epicsEnvSet("PORT", "FIMSCB")

   drvAsynIPPortConfigure($(PORT), "127.0.0.1:9999", 0, 0, 0)
   asynOctetSetInputEos($(PORT), 0, "\r\n")
   asynOctetSetOutputEos($(PORT), 0, "\r")

   dbLoadRecords("db/fimscb.db",     "P=$(P)-$(R):FimSCB:,PORT=FIMSCB")

   iocInit

   dbl > "$(TOP)/PVs.list"
   ```
   Note that the *fimscb* module defined in this chapter does *not* add *stream* as a dependency, and so for the IOC to run correctly we need to include `require stream` in the startup script. A better solution, of course, is to add *stream* as a run-time dependency.
2. One should use the cookiecutter for this, same as for `e3-fimscb`.
3. One possible startup script could be the following.
   ```sh
   require ch8

   epicsEnvSet("IOCNAME", "test_ioc")

   dbLoadRecords("$(ch8_DB)/dbExample1.db", "user=$(IOCNAME)")
   dbLoadRecords("$(ch8_DB)/dbExample2.db", "user=$(IOCNAME),no=1,scan=1 Second")
   dbLoadRecords("$(ch8_DB)/dbSubExample.db", "user=$(IOCNAME)")

   iocInit

   seq sncExample "user=$(IOCNAME)"
   ```
   If you run this IOC, you should see output like this after a few seconds.
   ```console
   [iocuser@host:e3-ch8]$ make cellinstall
   [iocuser@host:e3-ch8]$ iocsh.bash -l cellMods st.cmd
   # --- snip snip ---
   iocRun: All initialization complete
   seq sncExample "user=test_ioc"
   sevr=info Sequencer release 2.2.8+0, compiled Fri May  7 14:04:03 2021
   sevr=info Spawning sequencer program "sncExample", thread 0x189bc90: "sncExample"
   # Set the IOC Prompt String One 
   epicsEnvSet IOCSH_PS1 "localhost-5721 > "
   #
   sevr=info sncExample[0]: all channels connected & received 1st monitor
   localhost-5721 > sncExample: Startup delay over
   sncExample: Changing to high
   sncExample: Changing to low
   ```




## Other dependencies
### Exercises

#### Fixing the dependency

- We do not need to run `make init` or `make patch` since there is no embedded git submodule; `make init` does nothing in this case, and it would be extremely weird to apply patches from your own repository to the same repository.

### Assignments
1. If you look at the output from an IOC trying to load `pid.db`, you should see the following.
   ```
   dbLoadRecords("/home/simonrose/data/git/e3.pages.esss.lu.se/e3-mypid/cellMods/base-7.0.5/require-3.4.1/mypid/master/db/pid.db")
   Record "mypid:PID1_limits" is of unknown type "transform"
   Error at or before ")" in file "/home/simonrose/data/git/e3.pages.esss.lu.se/e3-mypid/cellMods/base-7.0.5/require-3.4.1/mypid/master/db/pid.db" line 22
   Error: syntax error
   dbLoadRecords: failed to load '/home/simonrose/data/git/e3.pages.esss.lu.se/e3-mypid/cellMods/base-7.0.5/require-3.4.1/mypid/master/db/pid.db'
   ```
   The database file uses the `transform` record type, which is not a part of EPICS base. How can we determine which module contains this? Consider
   ```console
   [iocuser@host:e3-mypid]$ grep -nr "\btransform\b" /epics/base-7.0.5/require/3.4.1/siteMods/ --include=*.dbd
   /epics/base-7.0.5/require/3.4.1/siteMods/calc/3.7.4+0/dbd/calc.dbd:15:recordtype(transform) {
   ```
   Note that this pinpoints that the record type `transform` is defined in `calc.dbd`. This means that we need to also include the *calc* module.
2. `FETCH_BUILD_NUMBER` is a macro defined in `driver.makefile`, which is the main build engine in *require*
3. EPICS base also include the function `dbLoadTemplate` which can be used to load `.substitution` files instead of just `.db` files (and which does so at run-time). Hence the line
   ```sh
   dbLoadTemplate("$(mypid_DB)/pid.substitutions")
   ```
   will produce the same output.
4. If you have the `ps` modules cloned in a common directory (as would be done by running `e3.bash -s mod`), then the following will display all of the run-time dependencies.
   ```console
   [iocuser@host:e3]$ grep -nr "^REQUIRED\b" ps --include=*.Makefile
   ps/e3-magnetps/magnetps.Makefile:33:REQUIRED += iocshutils
   ps/e3-sorensen/sorensen.Makefile:39:REQUIRED += stream
   ps/e3-caenelfastps/caenelfastps.Makefile:39:REQUIRED += stream
   ps/e3-fug/fug/fug.Makefile:39:REQUIRED += stream
   ps/e3-fug/fug.Makefile:39:REQUIRED += stream
   ps/e3-caenelsmagnetps/caenelsmagnetps.Makefile:39:REQUIRED += stream
   ps/e3-sairem/sairem.Makefile:39:REQUIRED += modbus
   ps/e3-tdklambdagenesys/tdklambdagenesys.Makefile:39:REQUIRED += stream
   ```
   We can see that the only dependent modules are *stream*, *modbus*, and *iocshutils*. *stream* and *modbus* are pretty common dependencies, but what is *iocshutils*? It turns out that it includes a utility to update database definitions after the IOC has started (but before it has run `iocInit`), which is what is used in that case. See the file [magnetps.iocsh](https://gitlab.esss.lu.se/epics-modules/magnetps/-/blob/master/iocsh/magnetps.iocsh).




## Additional working modes
### Exercises

#### Development mode

- `make existent` and `make devexistent` both run the command `tree` in the directory `${EPICS_BASE}/require/${E3_REQUIRE_VERSION}/siteMods/${E3_MODULE_NAME}`. So these will only differ if any of those variables differ between the regular and `_DEV` configure files.

### Assignments
1. In order to change the install path used in *cell mode*, you need to redefine `E3_CELL_PATH`. This is best done in a `CONFIG_CELL.local` file either in the configure directory, or in the parent directory of the wrapper.
   
   Alternatively, you can also just export the variable into the environment via e.g.
   ```console
   [iocuser@host:e3-module]$ export E3_CELL_PATH=/absolute/path/to/cellMods
   [iocuser@host:e3-module]$ make cellinstall
   ```
2. Assuming the modules are in different locations, then it is simply a matter of running
   ```console
   [iocuser@host:~]$ iocsh.bash -l <path/to/cellMods_1> -l <path/to/cellMods_2> st.cmd
   ```
   Note that the module search will prioritise the last specified path.
3. As seen {ref}`before <dot_local_file>`, one should create a `CONFIG_MODULE_DEV.local` file with an updated `E3_MODULE_DEV_GITURL`, which git will ignore.
4. Technically, `make devdistclean` does two things: it runs `make devclean` and then deletes the dev source directory. However, that first step is not relevant as deleting the source tree also gets rid of the temporary files.
   
   This is not really a necessary make target, but there is some value in having a common interface for building, cleaning, installing, etc. a module.
5. Like all development mode tasks, there is a target for this: if you have patch files in `e3-module/patch/Site`, then running `make devpatch` will apply them to the development source files.




## Supplementary tools
### Exercises

### Assignments
1.
2.
3.
4.
5.
6.





