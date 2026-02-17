# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
from pathlib import Path
import sys
import os

project = 'EnsgSearch'
copyright = '2026, Jean-François Lecomte'
author = 'Jean-François Lecomte'
release = '0.2.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

extensions = [
    "sphinx.ext.napoleon",
    'sphinx_rtd_theme',
    'myst_parser',
    "sphinx.ext.mathjax"
]

myst_enable_extensions = [
    "dollarmath",
]

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
sys.path.insert(0, Path(__file__).parents[2].resolve().as_posix())
