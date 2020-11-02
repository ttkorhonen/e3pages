# ESS EPICS Environment (e3)

```{admonition} Under Construction
:class: warning

Please note that this portal currently is being set-up, and that content is evolving fairly rapidly. This warning will be removed once the site is in a fairly stable state.
```

ESS' EPICS Environment (e3) is a design concept and a toolkit intended to a) facilitate development by abstracting away some of the low-level complexities intrinsic to large EPICS implementations (primarily dependency management), and b) allow for more manageable quality control of released modules. It allows for easily building EPICS modules directly from source and automagically resolves module dependencies, and allows for site specific modifications to EPICS modules without needing to directly modify source trees.

e3 was initially based off of the module *require* which allows for dynamic loading of EPICS modules. Thus, e3 aims to simplify the work for primarily two groups: EPICS integrators, and a central core group that oversees module interdependencies.

---

```{toctree}
:maxdepth: 2
:caption: Usage
:glob:
usage/1*
usage/2*
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
kb/howto/index.md
```

```{toctree}
:maxdepth: 2
:caption: References
:glob:
references/1*
references/2*
references/3*
```
