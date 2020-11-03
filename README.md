# E3 documentation

Source for E3 documentation hosted on GitLab pages: http://e3.pages.esss.lu.se

The documentation is built using [Sphinx](http://www.sphinx-doc.org/en/master/index.html) and [MyST](https://myst-parser.readthedocs.io/en/latest/index.html), stylized with the [Read the Docs](https://readthedocs.org/) theme. All files are written in Markdown, none in reStructuredText.

It is updated only on tag.

## Build locally

From the root dir: `sphinx-build -b html docs/ docs/_build/html`

## MyST

Supports all the syntax of the CommonMark Markdown but also several extensions to CommonMark (often called [MyST Markdown syntax](https://myst-parser.readthedocs.io/en/latest/using/syntax.html)). The syntax highlighting parser is Ruby Rogue.
