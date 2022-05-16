(module_tests)=

# Article: How to automate tests for your module

It is important to test that your module builds and works correctly. To that
effect, *require* includes a build target `make test` which runs a basic tollbooth
test, as well as any developer-specified module specific tests.

## Tollbooth test with `run-iocsh`

### *run-iocsh*

The most minimal test that an e3 module must be able to pass is that it should

* be able to be built
* be able to be loaded into an IOC

This does not mean that any functionality is tested, but simply that you can build
and load the module into memory. This is equivalent to running

```console
[iocuser@host:~]$ make cellinstall
[iocuser@host:~]$ iocsh -l cellMods -r mymodule

# --- snip snip ---

require mymodule
Module mymodule version $VERSION found in /path/to/module/cellMods/base-7.0.6.1/require-4.0.0/mymodule/$VERSION
Loading library /path/to/module/cellMods/base-7.0.6.1/require-4.0.0/mymodule/$VERSION/lib/linux-x86_64/libmymodule.so
Loaded mymodule version $VERSION

# --- snip snip ---

iocInit
Starting iocInit
############################################################################
## EPICS R7.0.6.1-E3-7.0.6.1-patch
## Rev. 2022-02-14T09:46+0100
############################################################################
iocRun: All initialization complete
localhost-6695 > exit
```

or, more succinctly:

```console
[iocuser@host:~]$ echo exit | iocsh -l cellMods -r mymodule
```

In order to automate this and to provide better testing information, we use a utility
called [*run-iocsh*](https://gitlab.esss.lu.se/ics-infrastructure/run-iocsh). This
can be installed via

```console
[iocuser@host:~]$ pip install run-iocsh -i https://artifactory.esss.lu.se/artifactory/api/pypi/pypi-virtual/simple
```

To run the above test, you would run

```console
[iocuser@host:~]$ make cellinstall
[iocuser@host:~]$ run-iocsh -l cellMods -r mymodule
```

This will also check the output of the IOC for a few common error messages

### `make test`

In essence, the first part of `make test` performs all of the above. It generates
a temporary cell (called `testMods-$TIMESTAMP`), runs `make cellinstall` into that
location, and then runs `run-iocsh` to load the module.

If the above passes, then *require* will look for any module-specific tests to run.
If all of the above pass, then *require* will clean up the temporary directly. If
any tests fail, then the temporary cell will be left there for a post-mortem of the
failing test.

## Developer-specific tests

As stated above, the above test is the _bare minimum_ that a module should be able
to pass in order to be a candidate for use; if you cannot build it, or cannot load
it into an IOC then it is by definition not useable.

However, it is very good practice to write further tests that will actually probe
the module's functionality. The exact language of the tests is up to a module
developer, and e3 simply provides a "hook" that can be used to trigger specific
tests. This is the *make* target `make module_tests`.

This target should be specified in `configure/module/RULES_MODULE`. A prototypical
example would be the following:

```make
module_tests: passing_test failing_test

.PHONY: passing_test
passing_test:
    true

.PHONY: failing_test
failing_test:
    false
```

A good example is from the e3 module [*e3-opcua*](https://gitlab.esss.lu.se/e3/wrappers/communication/e3-opcua/-/blob/master/configure/module/RULES_MODULE#L24).
This test compiles a test server and then uses [*pytest*](https://docs.pytest.org/en/7.1.x/)
to run a number of module-specific tests.
