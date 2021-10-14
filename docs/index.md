# ESS EPICS Environment (e3)

ESS' EPICS Environment (e3) is a design concept and a toolkit intended to

1. facilitate development by abstracting away some of the low-level complexities
   intrinsic to large EPICS implementations (primarily dependency management),
   and to
2. allow for more manageable quality control of released modules as well as
   IOCs.

It allows for easily building EPICS modules directly from source and
automagically resolves module dependencies, and allows for site-specific
modifications to EPICS modules without needing to directly modify source trees.

---

```{toctree}
:maxdepth: 2
:caption: Quickstart
:glob:
quickstart/1*
quickstart/2*
```

```{toctree}
:maxdepth: 2
:caption: Design
:glob:
design/1*
design/2*
design/3*
design/4*
```

```{toctree}
:maxdepth: 2
:caption: Knowledge-base
kb/training/index.md
kb/guide/index.md
```

```{toctree}
:maxdepth: 2
:caption: References
:glob:
references/1*
references/2*
references/3*
```
