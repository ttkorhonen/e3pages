# How to: Investigate a segmentation fault

## Case 1

### Problem

Segmentation fault when iocsh.bash starts:

```console
[iocuser@host:~]$ iocsh.bash st.cmd
...
/epics/base-7.0.5/require/3.4.1/bin/iocsh.bash: line 131: 18208 Segmentation fault      (core dumped) softIoc${_PVA_} -D ${EPICS_BASE}/dbd/softIoc${_PVA_}.dbd "${IOC_STARTUP}" 2>&1
```

### Solution

Run the IOC using `gdb` to try to identify the source of the problem.

:::{note}
The following two paragraphs and the command block need to be updated
when the next e3 environment after `base-7.0.5/require-3.4.1` is built, as it
will natively include the `linux-x86_64-debug` architecture.
:::

Some ESS e3 environments have been built with `debug` architectures. At the
moment, the `/epics-test/base-7.0.5-debug` ESS e3 environment has the
`linux-x86_64-debug` architecture available.[^esse3envs] After
`base-7.0.5/require-3.4.1` the `linux-x86_64-debug` architecture will be
available in all e3 environments.[^adddebugarch]

Execute the following commands (assuming you have the `/epics-test` e3
environment mounted from the shared file system). If you do not have the
`/epics-test` environment available, skip to the third command. You will still
be able to use the `gdb` debugger, but will not have all the symbol names
available to you.

```console
[iocuser@host:~]$ source /epics-test/base-7.0.5-debug/require/3.4.1/bin/setE3Env.bash
[iocuser@host:~]$ export EPICS_HOST_ARCH=linux-x86_64-debug
[iocuser@host:~]$ iocsh.bash -dg st.cmd
```

The IOC will still segmentation fault, and will return you to the `(gdb)`
prompt, meaning that you are now in the `gdb` environment, and can start to
investigate the cause of the problem.

:::{note}
The following example shows a segmentation fault that occurred in an older
version of EPICS base. Your exact output will be different to this.
:::

```console
Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0x7fffcfdfe700 (LWP 18940)]
epicsMutexLock (pmutexNode=0x0) at ../../../src/libCom/osi/epicsMutex.cpp:143
143             epicsMutexOsdLock(pmutexNode->id);
Missing separate debuginfos, use: debuginfo-install glibc-2.17-260.el7.x86_64 libgcc-4.8.5-36.el7.x86_64 libstdc++-4.8.5-36.el7.x86_64 ncurses-libs-5.9-14.20130511.el7_4.x86_64 readline-6.2-10.el7.x86_64
(gdb)
```

Check the backtrace (`(gdb) bt`) to identify the source code file and line that
caused the problem, and the sequence of function calls that lead to it.

```console
(gdb) bt
#0  epicsMutexLock (pmutexNode=0x0) at ../../../src/libCom/osi/epicsMutex.cpp:143
#1  0x00007ffff796c9d9 in casStatsFetch (pChanCount=0x7fffcfdfdd10, pCircuitCount=0x7fffcfdfdce0) at ../../../src/ioc/rsrv/caservertask.c:1466
#2  0x00007ffff4cf2d08 in scan_time (type=3) at ../devIocStats/devIocStatsAnalog.c:355
#3  0x00007ffff7485bae in epicsTimerForC::expire (this=<optimized out>) at ../../../src/libCom/timer/epicsTimer.cpp:61
#4  0x00007ffff7486ffe in timerQueue::process (this=this@entry=0x2524090, currentTime=...) at ../../../src/libCom/timer/timerQueue.cpp:139
#5  0x00007ffff7487663 in timerQueueActive::run (this=0x2524060) at ../../../src/libCom/timer/timerQueueActive.cpp:93
#6  0x00007ffff7476a19 in epicsThreadCallEntryPoint (pPvt=0x2524130) at ../../../src/libCom/osi/epicsThread.cpp:83
#7  0x00007ffff747c77c in start_routine (arg=0x2524580) at ../../../src/libCom/osi/os/posix/osdThread.c:403
#8  0x00007ffff6639dd5 in start_thread () from /lib64/libpthread.so.0
#9  0x00007ffff694bead in clone () from /lib64/libc.so.6
```

```console
(gdb) bt full
#0  epicsMutexLock (pmutexNode=0x0) at ../../../src/libCom/osi/epicsMutex.cpp:143
No locals.
#1  0x00007ffff796c9d9 in casStatsFetch (pChanCount=0x7fffcfdfdd10, pCircuitCount=0x7fffcfdfdce0) at ../../../src/ioc/rsrv/caservertask.c:1466
        status = <optimized out>
#2  0x00007ffff4cf2d08 in scan_time (type=3) at ../devIocStats/devIocStatsAnalog.c:355
        cainfo_clients_local = 0
        cainfo_connex_local = 0
#3  0x00007ffff7485bae in epicsTimerForC::expire (this=<optimized out>) at ../../../src/libCom/timer/epicsTimer.cpp:61
No locals.
#4  0x00007ffff7486ffe in timerQueue::process (this=this@entry=0x2524090, currentTime=...) at ../../../src/libCom/timer/timerQueue.cpp:139
        unguard = {_guard = <synthetic pointer>, _pTargetMutex = 0x25240c8}
        pTmpNotify = 0x25249f8
        expStat = {delay = -1.7976931348623157e+308}
        guard = {_pTargetMutex = 0x0}
        delay = 1.7976931348623157e+308
#5  0x00007ffff7487663 in timerQueueActive::run (this=0x2524060) at ../../../src/libCom/timer/timerQueueActive.cpp:93
        delay = <optimized out>
#6  0x00007ffff7476a19 in epicsThreadCallEntryPoint (pPvt=0x2524130) at ../../../src/libCom/osi/epicsThread.cpp:83
        pThread = 0x2524130
        threadDestroyed = false
#7  0x00007ffff747c77c in start_routine (arg=0x2524580) at ../../../src/libCom/osi/os/posix/osdThread.c:403
        pthreadInfo = 0x2524580
        status = <optimized out>
        blockAllSig = {__val = {18446744067267100671, 18446744073709551615 <repeats 15 times>}}
#8  0x00007ffff6639dd5 in start_thread () from /lib64/libpthread.so.0
No symbol table info available.
#9  0x00007ffff694bead in clone () from /lib64/libc.so.6
No symbol table info available.
```

Check the current thread:

```console
(gdb) info threads
  Id   Target Id         Frame
  26   Thread 0x7fffceef6700 (LWP 18948) "scan-0.1" 0x00007ffff663dd12 in pthread_cond_timedwait@@GLIBC_2.3.2 () from /lib64/libpthread.so.0
  25   Thread 0x7fffcf0f7700 (LWP 18947) "scan-0.2" 0x00007ffff663dd12 in pthread_cond_timedwait@@GLIBC_2.3.2 () from /lib64/libpthread.so.0
  24   Thread 0x7fffcf2f8700 (LWP 18946) "scan-0.5" 0x00007ffff663dd12 in pthread_cond_timedwait@@GLIBC_2.3.2 () from /lib64/libpthread.so.0
  23   Thread 0x7fffcf4f9700 (LWP 18945) "scan-1" 0x00007ffff663dd12 in pthread_cond_timedwait@@GLIBC_2.3.2 () from /lib64/libpthread.so.0
  22   Thread 0x7fffcf6fa700 (LWP 18944) "scan-2" 0x00007ffff663dd12 in pthread_cond_timedwait@@GLIBC_2.3.2 () from /lib64/libpthread.so.0
  21   Thread 0x7fffcf8fb700 (LWP 18943) "scan-5" 0x00007ffff663dd12 in pthread_cond_timedwait@@GLIBC_2.3.2 () from /lib64/libpthread.so.0
  20   Thread 0x7fffcfafc700 (LWP 18942) "scan-10" 0x00007ffff663dd12 in pthread_cond_timedwait@@GLIBC_2.3.2 () from /lib64/libpthread.so.0
  19   Thread 0x7fffcfcfd700 (LWP 18941) "scanOnce" 0x00007ffff663d965 in pthread_cond_wait@@GLIBC_2.3.2 () from /lib64/libpthread.so.0
* 18   Thread 0x7fffcfdfe700 (LWP 18940) "timerQueue" epicsMutexLock (pmutexNode=0x0) at ../../../src/libCom/osi/epicsMutex.cpp:143
```

Quit gdb.

```console
(gdb) quit
A debugging session is active.

        Inferior 1 [process 18904] will be killed.

Quit anyway? (y or n) y
```

[^esse3envs]: The `/epics-test` e3 environment is specific to the ESS site e3
  installation. It is provided as a location for testing new e3 environments.

[^adddebugarch]: To add the `linux-x86_64-debug` architecture to a local build
    of e3, add the following line to `e3-base/configure/CONFIG_BASE`:

    ```makefile
    E3_CROSS_COMPILER_TARGET_ARCHS+=linux-x86_64-debug
    ```
