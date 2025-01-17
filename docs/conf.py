# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os

# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "ESS EPICS Environment (e3)"
copyright = "2022, European Spallation Source ERIC"
author = "European Spallation Source ERIC"

# The full version, including alpha/beta/rc tags
try:
    # CI_COMMIT_REF_NAME is defined by GitLab Runner
    # The branch or tag name for which project is built
    release = os.environ["CI_COMMIT_REF_NAME"]
except KeyError:
    # dev mode
    release = os.popen("git describe").read().strip()


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["myst_parser"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "_legacy",
    "CONTRIBUTING.md",
    "MAINTAINING.md"
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# Enable special syntax for admonitions (:::{directive})
myst_admonition_enable = True

# Enable definition lists (Term\n: Definition)
myst_deflist_enable = True

# Allow colon fencing of directives
myst_enable_extensions = ["colon_fence",]
