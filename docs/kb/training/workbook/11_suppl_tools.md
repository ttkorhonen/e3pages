# Supplementary tools

## Lesson Overview

In this lesson, you'll learn how to do the following:

* Run IOCs in procServ containers.
* Run processes as system daemons.
* Use conserver to manage procServ containers.

---

## Utilities

Typically, IOCs will be running on a dedicated (virtual or physical) machine that you log in remotely to. A single machine may host a number of IOCs, which should be running regardless of if you are attached to a session or not. Thus we want to be able to allow the system to run and take care of the IOC itself. However, we need to be able to easily connect to the IOC if necessary in order to access logs, to check on the status of an IOC, etc. Historically, common user accounts with screen or tmux sessions have been used towards this purpose, but they come with issues.

One solution is to run each IOC in a procServ container as a (possibly templated) system daemon. The system daemons are managed by `systemd`, and the IOC consoles accessed by conserver.

:::{note}
These deployments (including set up of these utilities) are typically automated with configuration management/remote execution utilities like *ansible*, *salt* or *puppet*. It is, however, still useful to understand how they work.
:::

## Starting an IOC in a procServ container

`procServ` is a utility that runs a specified command as a dæmon process in the background while opening up either a`telnet` connection at a specified port or
a Unix Domain Socket in order to allow users to communicate with the process. For more information, see its [documentation](https://linux.die.net/man/1/procserv).

Let us create a `procServ` container for a blank IOC using `iocsh.bash` and listening on port 2000, which we will then connect to via `telnet`. First,
start the `procServ` container:
```console
[iocuser@host:~]$ procServ -n iocsh 2000 $(which iocsh.bash)
```

:::{admonition} Exercise
What do each of the arguments passed to `procServ` mean?
:::

Now, one should be able to connect to the container using telnet.

```console
[iocuser@host:~]$ telnet localhost 2000
Trying ::1...
telnet: connect to address ::1: Connection refused
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
@@@ Welcome to procServ (procServ Process Server 2.7.0)
@@@ Use ^X to kill the child, auto restart is ON, use ^T to toggle auto restart
@@@ procServ server PID: 15539
@@@ Server startup directory: /home/iocuser/data/git
@@@ Child startup directory: /home/iocuser/data/git
@@@ Child "iocsh" started as: /epics/base-7.0.5/require/3.4.1/bin/iocsh.bash
@@@ Child "iocsh" PID: 15549
@@@ procServ server started at: Wed Aug 11 13:38:00 2021
@@@ Child "iocsh" started at: Wed Aug 11 13:38:01 2021
@@@ 0 user(s) and 0 logger(s) connected (plus you)
```
No other text occurs, since the IOC is up and running. If you press enter, or type `dbl` (or any other IOC command)
then you can interact with the IOC.

:::{note}
As in [Chapter 4](4_startup_scripts.md), the command to escape to the `telnet` console is `^]`. 
:::

If you try to exit the IOC by typing `exit` or with `^C`, then the default behaviour of `procServ` is to restart the IOC.
In order to kill the IOC, one should instead first press `^X` and then `^Q`.

The above process starts an blank e3 IOC and opens up TCP port 2000 for communication. In general you will want to do a bit more:
* Use a named Unix Domain Socket (UDS) so that you don't have to separately configure a port for each IOC running on a machine
* Run an actual meaningful startup script
* Keep a log of the output
* Block certain control commands from being sent to the IOC (e.g. `^C` (SIGINT) and `^D` (EOF))

This can be achieved with
```console
[iocuser@host:~]$ procServ -n "Test IOC" -i ^D^C -L procServ.log \
                  unix:/var/run/procServ/my-ioc $(which iocsh.bash) /path/to/st.cmd
```

:::{note}
You will have to have write permission to the path specified by the UDS.
:::

If you want to connect to the UDS, you can use `socat` via
```console
[iocuser@host:~]$ socat - UNIX-CONNECT:/var/run/procServ/my-ioc
```
However, we will discuss another option below to manage connections to IOCs started with `procServ`, namely `conserver`.

## Letting the system manage our processes

One of systemd's primary components is a system and service manager. We want to let our system manage our IOCs as services. We do this by creating *unit files* (more on those [here](https://www.freedesktop.org/software/systemd/man/systemd.unit.html)) that encode information about our service.

We will now set up a simplistic system daemon to run an IOC. Begin by saving the following as `/etc/systemd/system/test-ioc.service`.
```
[Unit]
Description=procServ container for test IOC
After=network.target remote-fs.target

[Service]
User=iocuser
ExecStart=/usr/bin/procServ \
                     --foreground \
                     --name=test-ioc \
                     --logfile=/home/iocuser/test-ioc.log \
                     --ignore=^C^D \
                     --port=2000 \
                     /epics/base-7.0.5/require/3.4.1/bin/iocsh.bash

[Install]
WantedBy=multi-user.target
```

:::{note}
Note that you need to provide the full path to `iocsh.bash` as command substitution doesn't work in unit files. Instead, systemd offers its own minimalistic shell-style command line parsing - if interested, see more [here](https://www.freedesktop.org/software/systemd/man/systemd.service.html#Command%20lines).
:::

Next, start up and inspect your service:

```console
[iocuser@host:~]$ systemctl start test-ioc.service
[iocuser@host:~]$ systemctl status test-ioc.service
```
If you want the system to keep the process alive and start it on boot, enable it: `systemctl enable test-ioc.service`.

Once you have confirmed that your IOC is running properly, you can stop and disable your service with the following.
```console
[iocuser@host:~]$ systemctl stop test-ioc.service
```

As you can see from the unit file, most of the parameters are fairly generic, and can be used for all IOCs. This allows us to use *template* unit files, and to instantiate daemons for our IOCs. We can thus create a single file called `ioc@.service`, and start any number of processes of the format `ioc@<instance_name>.service`. As we will want to be able to have different processes listen at different ports, we can use a few different specifiers supported by systemd.

In order to do so, create a template file called `ioc@.service`:
```
[Unit]
Description=procServ container for IOC %i
Documentation=file:/opt/iocs/e3-ioc-%i/README.md
Before=conserver.service
After=network.target remote-fs.target
AssertPathExists=/opt/iocs/e3-ioc-%i

[Service]
User=iocuser
Group=iocgroup
PermissionsStartOnly=true

ExecStartPre=/bin/mkdir -p /var/log/procServ/%i
ExecStartPre=/bin/chown -R iocuser:iocgroup /var/log/procServ/%i
ExecStartPre=/bin/mkdir -p /var/run/procServ/%i
ExecStartPre=/bin/chown -R iocuser:iocgroup /var/run/procServ/%i

ExecStart=/usr/bin/procServ \
                     --foreground \
                     --name=%i \
                     --logfile=/var/log/procServ/%i/out.log \
                     --info-file=/var/run/procServ/%i/info \
                     --ignore=^C^D \
                     --logoutcmd=^Q \
                     --chdir=/var/run/procServ/%i \
                     --port=unix:/var/run/procServ/%i/control \
                     /epics/base-7.0.5/require/3.4.1/bin/iocsh.bash \
                     /opt/iocs/e3-ioc-%i/st.cmd

[Install]
WantedBy=multi-user.target
```

In the above template file, `%i` is the instance name (character escaped; `%I` is verbatim). You can also see that we've added some requirements for where the startup script shall be located, etc.

:::{note}
As suggested above, we now are using UDS instead of TCP ports, which allows us to name the socket.
:::

With the template created, all that we need to do is create a startup script for the service to load. Create a simple startup script at `/opt/iocs/` with the format `e3-ioc-<iocname>/st.cmd`.

```bash
require stream

iocInit()

dbl > PV.list
```

Finally, start an instantiated system daemon.

```console
[iocuser@host:~]$ systemctl start ioc@test-ioc.service
```
As above, you could also *enable* the service so that it autostarts on boot.

Finally, check the status of the process.
```console
[iocuser@host:~]$ systemctl status ioc@test-ioc.service
● ioc@test-ioc.service - procServ container for IOC test-ioc
   Loaded: loaded (/etc/systemd/system/ioc@.service; disabled; vendor preset: disabled)
   Active: active (running) since Wed 2021-08-11 15:42:46 CEST; 1min 3s ago
     Docs: file:/opt/iocs/e3-ioc-test-ioc/README.md
  Process: 20432 ExecStartPre=/bin/chown -R iocuser /var/run/procServ/%i (code=exited, status=0/SUCCESS)
  Process: 20430 ExecStartPre=/bin/mkdir -p /var/run/procServ/%i (code=exited, status=0/SUCCESS)
  Process: 20428 ExecStartPre=/bin/chown -R iocuser /var/log/procServ/%i (code=exited, status=0/SUCCESS)
  Process: 20427 ExecStartPre=/bin/mkdir -p /var/log/procServ/%i (code=exited, status=0/SUCCESS)
 Main PID: 20435 (procServ)
   CGroup: /system.slice/system-ioc.slice/ioc@test-ioc.service
           ├─20435 /usr/bin/procServ --foreground --name=test-ioc --logfile=/var/log/procServ/test-ioc/out.log --info-file=/var/run/procServ/test-ioc/inf...
           ├─20447 /bin/bash /epics/base-7.0.5/require/3.4.1/bin/iocsh.bash /opt/iocs/e3-ioc-test-ioc/st.cmd
           └─20482 /epics/base-7.0.5/bin/linux-x86_64/softIocPVA -D /epics/base-7.0.5/dbd/softIocPVA.dbd /tmp/systemd-private-e3-iocsh-iocuser/tm...

Aug 11 15:42:46 localhost.localdomain systemd[1]: Starting procServ container for IOC test-ioc...
Aug 11 15:42:46 localhost.localdomain systemd[1]: Started procServ container for IOC test-ioc.
```
We can see from the above that the IOC is up and running. You can do a quick further test without logging in by checking for any of the PVs that should be visible from the IOC with `pvlist`.

```console
[iocuser@host:~]$ pvlist localhost
REQMOD:localhost-20447:MODULES
REQMOD:localhost-20447:VERSIONS
REQMOD:localhost-20447:MOD_VER
REQMOD:localhost-20447:exit
REQMOD:localhost-20447:BaseVersion
REQMOD:localhost-20447:require_VER
REQMOD:localhost-20447:asyn_VER
REQMOD:localhost-20447:sequencer_VER
REQMOD:localhost-20447:sscan_VER
REQMOD:localhost-20447:calc_VER
REQMOD:localhost-20447:pcre_VER
REQMOD:localhost-20447:stream_VER
```

:::{note}
`pvlist` is a utility (installed with EPICS base 7) that allows you to list pvs on a given host as well as what pvs are reachable via PVAccess. For example, running `pvlist` on a network with several running IOCs could yield something like
```console
[iocuser@host:~]$ pvlist
GUID 0x00000000612FF55911A8B7E9 version 2: tcp@[ 172.30.5.209:5075 ]
GUID 0x000000006130B9CD20A10E23 version 2: tcp@[ 172.30.6.131:5075 ]
GUID 0x006F2F6100000000F1893C25 version 2: tcp@[ 172.30.6.131:47078 ]
# --- snip snip ---
```
where you can see that there is at least one IOC running on `172.30.5.209`, and two IOCs running on `172.30.6.131`. You can then query the PVs from those IOCs either using the GUID (`0x00000000612FF55911A8B7E9`) or by specifying the `ip:port`.
:::

As you saw, we added no specifics to our templated unit file, but instead used essentially macros. By having a template, we can instantiate as many IOCs as we want and have them appear and behave consistently.

## Managing your IOCs with conserver

[Conserver](https://www.conserver.com) is an application that allows multiple users to watch and interact with a serial console at the same time. We will thus use conserver instead of telnet or netcat to attach to our consoles. Conserver consists of a server and a client. The server will run as a system daemon on our IOC machine, but the client could be either local to that machine or remote.

Conserver requires a bit of boilerplate code for its setup. We will first have a quick look at the two programs and the main configuration files necessary for setup.

```console
[iocuser@host:~]$ conserver -V
conserver: conserver.com version 8.2.1
conserver: default access type `r'
conserver: default escape sequence `^Ec'
conserver: default configuration in `/etc/conserver.cf'
conserver: default password in `/etc/conserver.passwd'
conserver: default logfile is `/var/log/conserver'
conserver: default pidfile is `/var/run/conserver.pid'
conserver: default limit is 16 members per group
conserver: default primary port referenced as `782'
conserver: default secondary base port referenced as `0'
conserver: options: freeipmi, libwrap, openssl, pam
conserver: freeipmi version: 1.2.2
conserver: openssl version: OpenSSL 1.0.1e-fips 11 Feb 2013
conserver: built with `./configure --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu --program-prefix= --disable-dependency-tracking --prefix=/usr --exec-prefix=/usr --bindir=/usr/bin --sbindir=/usr/sbin --sysconfdir=/etc --datadir=/usr/share --includedir=/usr/include --libdir=/usr/lib64 --libexecdir=/usr/libexec --localstatedir=/var --sharedstatedir=/var/lib --mandir=/usr/share/man --infodir=/usr/share/info --with-libwrap --with-openssl --with-pam --with-freeipmi --with-gssapi --with-striprealm --with-port=782'
```

The main two things to notice above is the location of the default configuration file and the default password file (`/etc/conserver.cf` and `/etc/conserver.passwd` respectively). If you were to look at these two files on your machine, you will find that they already contain some (commented out) example settings.

We will now modify these two files for our setup. As we do not need access control, we will simply allow all users to access conserver without any password. Modify your `conserver.passwd` to look like this:

```cpp
*any*:
```

For the configuration file, we will set up some default values, and then we will use an include directive (`#include`) to be able to inventorize our consoles in a separate file. Modify your `conserver.cf` to look like this:

```cpp
config * {
}

default full { rw *; }
default * {
        timestamp "";
        include full;
        master localhost;
}

#include /etc/conserver/procs.cf

access * {
        trusted 127.0.0.1;
        allowed 127.0.0.1;
}
```

Thus we are allowing only local access, and we are specifying to include the file `/etc/conserver/procs.cf` into this configuration file (we could otherwise just take whatever contents we soon will put in `procs.cf` and instead have them in `conserver.cf` - but we will modularize this a bit).

Now create the above included `procs.cf`, and populate it with data to describe one of our already-running IOCs:

```cpp
console test-ioc {
    type uds;
    uds /var/run/procServ/test-ioc/control;
}
```

:::{note}
We could have inventorized also a console on a TCP port, in which we would set type to `host`, and port to `2000`.
:::

As we are making changes to the configuration of an already-running system daemon (conserver), we will need to do a soft restart of the systemd manager:

```console
[iocuser@host:~]$ systemctl daemon-reload
[iocuser@host:~]$ systemctl status conserver.service
```

If conserver is not already running on your machine, make sure to start and enable it with `systemctl start conserver.service` and `systemctl enable conserver.service`.

We now have conserver running, managing a console on a UDS at `/var/run/procServ/test-ioc/control`. To test, we can attach to this using socat again:

```console
[iocuser@host:~]$ socat - UNIX-CONNET:/var/run/procServ/test-ioc/control
```

As we will want to use conserver client, also known as *console*, to attach to IOCs, we will need to set it up too. Let's first look at its settings:

```console
[iocuser@host:~]$ console -V
console: conserver.com version 8.2.1
console: default initial master server `console'
console: default port referenced as `782'
console: default escape sequence `^Ec'
console: default site-wide configuration in `/etc/console.cf'
console: default per-user configuration in `$HOME/.consolerc'
console: options: libwrap, openssl, gssapi
console: openssl version: OpenSSL 1.0.1e-fips 11 Feb 2013
console: built with `./configure --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu --program-prefix= --disable-dependency-tracking --prefix=/usr --exec-prefix=/usr --bindir=/usr/bin --sbindir=/usr/sbin --sysconfdir=/etc --datadir=/usr/share --includedir=/usr/include --libdir=/usr/lib64 --libexecdir=/usr/libexec --localstatedir=/var --sharedstatedir=/var/lib --mandir=/usr/share/man --infodir=/usr/share/info --with-libwrap --with-openssl --with-pam --with-freeipmi --with-gssapi --with-striprealm --with-port=782'
```

As you can see, site-wide configurations are kept in `/etc/console.cf`. All we will need to do now to use the service is to define where console should look for consoles:

```cpp
config * {
        master localhost;
}
```

And voilá ! If we just do a soft reload of the systemd manager again, we should be able to both see and attach to our IOC.

```console
[iocuser@host:~]$ systemctl daemon-reload
[iocuser@host:~]$ console -u  # to list available consoles
[iocuser@host:~]$ console test-ioc
```

:::{tip}
You can detach from a console by pressing `^E c .` (note the dot at the end).
:::

## How to monitor your IOC and related processes

So, as we've set things up, systemd starts and manages procServ processes that run our IOC(s). A conserver server is also run as a system daemon, and currently we have conserver client (also a daemon) attach to local IOCs. In our templated unit file, we specified that logging from procServ would go to `/var/log/procServ/<iocname>` (which we inspect with e.g. `less` or could monitor like `tail -f /path/to/logfile`), and since we included `dbl > PV.list` in the startup script, we will also print out a database list upon IOC initialization. This will be placed in `/var/run/procServ/<iocname>` since we executed procServ with `--chdir=/var/run/procServ/%i` in the unit file.

As we're now dealing with multiple system daemons, yet another useful troubleshooting utility is *journalctl*, which is used to query the contents of the systemd journal. We will not go in-depth into how to use journalctl, but here are some examples of how we could use it to troubleshoot our services:

```console
[iocuser@host:~]$ sudo journalctl --since yesterday
[iocuser@host:~]$ sudo journalctl -u ioc@test-ioc.service
[iocuser@host:~]$ sudo journalctl conserver.service --since today
[iocuser@host:~]$ sudo journalctl _UID=1001 -n 10 -f
```

> In the above examples, 1001 is the user ID of this author's `iocuser` account.

---

## Assignments

1. Try to set up a unit file to execute procServ to listen to a TCP socket instead of an UDS. Can you also get conserver to work with this?
2. Let's assume you had your e3 installation on a NFS server. Explain to yourself what you would modify to get above examples to work with this.
3. The template unit file we created could be improved in many ways. Can you think of a few?

