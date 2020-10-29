# ESS EPICS Environment (e3)

```{admonition} Under Construction
:class: warning

Please note that this portal currently is being set-up, and that content is evolving fairly rapidly. This warning will be removed once the site is in a fairly stable state.
```

ESS' EPICS Environment, also known as e3, is a design concept and a toolkit intended to a) facilitate development by abstracting away some of the low-level complexities intrinsic to large EPICS implementations (primarily dependency management), and b) allow for more manageable quality control of released modules. It allows for easily building EPICS modules directly from source and automagically resolves module dependencies, and allows for site specific modifications to EPICS modules without needing to directly modify source trees. It is initially based off of the module *require* which allows for dynamic loading of EPICS modules. Thus, e3 aims to simplify the work for primarily two groups: EPICS integrators, and a central core group that oversees module interdependencies.

---

```{toctree}
---
maxdepth: 1
caption: Usage
---
usage/quickstart.md
usage/sample_ioc.md
```

---

```{toctree}
---
maxdepth: 1
caption: Design
---
design/require.md
design/wrappers.md
design/build_process.md
```

---

```{toctree}
---
maxdepth: 1
caption: Knowledge-base
---
training/index.md
howto/index.md
```

---

```{toctree}
---
maxdepth: 1
caption: References
---
references/repos.md
references/comms.md
```
