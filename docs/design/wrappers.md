# Module wrappers

```{admonition} Under Construction
:class: warning

Please note that this portal currently is being set-up, and that content is evolving fairly rapidly. This specific warning will be removed once this page is in a reasonable state. 
```

At the core of e3 is the module wrapper. This allows us to apply site specific changes - whether those are source code changes in the form of patches, different PV naming structure, or custom GUIs - to modules of any source without needing to modify that source directly.

```bash
$ tree
.
├── Makefile
├── README.md
├── cmds
├── configure
├── docs
├── patch
├── opi
├── <module>
├── <module>.Makefile
└── tools
```

In the above output, `<module>` is the name of the EPICS module/application/library. For community modules, this would be a git submodule. For ESS-specific application, it can be a normal directory (i.e. both the wrapper and the wrapped module are controlled in the same repository).
