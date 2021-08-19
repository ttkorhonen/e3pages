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
None

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





