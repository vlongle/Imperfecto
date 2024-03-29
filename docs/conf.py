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
import sys
sys.path.insert(0, os.path.abspath('../imperfecto'))


# -- Project information -----------------------------------------------------

project = 'Imperfect Information Games'
copyright = '2022, Long Le'
author = 'Long Le'

# The full version, including alpha/beta/rc tags
release = '1.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.napoleon",  # for Google-style Python docstrings support (https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
              "sphinx.ext.intersphinx",  # allow to link external docs
              "sphinx_click.ext",
              "sphinx.ext.autodoc",
              # https://sphinx-toolbox.readthedocs.io/en/latest/extensions/more_autodoc/typehints.html
              # make typing pretty
              'sphinx_toolbox.more_autodoc.typehints',
              "sphinx_autodoc_typehints",
              "sphinx.ext.autosummary",
              "sphinx.ext.mathjax",
              "sphinx.ext.ifconfig",
              "sphinx.ext.viewcode",
              ]
# list of external docs
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/stable/", None),
    "pytest": ("https://docs.pytest.org/en/stable", None),
    "pytest-regressions": ("https://pytest-regressions.readthedocs.io/en/latest/", None),
    "coincidence": ("https://coincidence.readthedocs.io/en/latest", None),
    "autodocsumm": ("https://autodocsumm.readthedocs.io/en/latest", None),
    'numpy': ('http://docs.scipy.org/doc/numpy/', None),
    'enlighten': ('https://python-enlighten.readthedocs.io/en/stable/', None),
}

autosummary_generate = True
autodoc_member_order = 'bysource'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'setup.py']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
#html_theme = 'renku'


# adding open baselines_theme
def setup(app):
    app.add_css_file("css/baselines_theme.css")
    return {}


html_logo = "_static/poker_meme.jpeg"


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
