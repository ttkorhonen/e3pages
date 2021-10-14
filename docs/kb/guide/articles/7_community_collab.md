# Article: Community collaboration

Although e3 is a custom set of tools designed to facilitate the deployment and
maintenance of EPICS environments, this is still an EPICS environment that uses
tools and functionality built by member of the EPICS community. It is important
to know how to work with that community in order to get help, to troubleshoot,
and to contribute in order to give back to said community.

## EPICS Community resources

The main EPICS [website](https://epics-controls.org/) is the best source for all
things EPICS. There you can find:

* [Frequently Asked
  Questions](https://epics-controls.org/resources-and-support/documents/epics-faq/)
* [Documentation](https://epics-controls.org/resources-and-support/documents/)
  for different versions of EPICS base
* A list of [projects](https://epics-controls.org/epics-users/projects/) that
  use EPICS
* [News and events](https://epics-controls.org/news-and-events/), listing
  upcoming and past events, as well as information about the latest releases of
  EPICS

There is also the Argonne National Labs EPICS
[website](https://epics.anl.gov/index.php), which has a lot of documentation for
previous versions of EPICS.

Note that e3 is designed to work with the EPICS base 7 series, and we have
dropped support for base 3.x.

## Asking for help

If you cannot find the information that you are looking for within the links
above, then one can look to the
[tech-talk](https://epics.anl.gov/tech-talk/index.php) mailing list. This is an
active mailing list which allows you to ask the broader EPICS community for help
and information. For example, if you are struggling to build or install a custom
EPICS module, then this can be a good place to look for help. If you are looking
to see if anyone has already developed support for a piece of hardware, then
this again is a good place to look.

Of course, as a part of a community, it is also a good place to offer your help
and experience in return!

## Working with community modules

As stated in {ref}`wrappers`, one of the key design features of e3 is the idea
of using a _wrapper_ to allow for the import of EPICS modules into an e3
environment. In particular, it allows for Site-specific modifications, patches,
and configuration in a manner that allows for ease of re-use within multiple
dynamically or statically generated IOCs.

### Working with an existing community module

If you are working with a module that already exists within the community and
would like to be able to work with it in e3 as well as contribute to the
community at large, then {ref}`development_mode` is the ideal way to work. This
allows you to have a cloned version of the module that you can commit to as well
as push your changes to the remote, as well as install your latest versions for
testing purposes.

If your changes are of interest to the broader community (instead of being
purely site-specific), then you can try to merge them into the parent repository
with a pull/merge request. If not, you will have to create appropriate patch
files and add them into the wrapper. Please see {ref}`patch_files` for more
information.

One your changes have been merged in to the main branch and tagged, then you can
update `configure/CONFIG_MODULE` in order to update `EPICS_MODULE_TAG` and
release a new version of the module into your e3 environment.

### Working with a new module

If you are designing a new module for your site, then you do not strictly
speaking need to separate the module and wrapper repositories: you can simply
work with {ref}`local_modules`.

It is still recommended, however, to separate the two repositories other than in
certain exceptional cases. This facilitates working with the broader EPICS
community in terms of sharing resources and skills: if you create some
functionality that can only be used in an e3 context, then there is extra work
that needs to be done in order to allow users at sites which do not use e3 to
allow them to use your module.

EPICS is a large community-driven open source project, and so the best practice
is to always make sure to give back to that community wherever possible.
