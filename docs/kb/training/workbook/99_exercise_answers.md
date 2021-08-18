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
1.
2.
3.
4.
5.
6.




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





