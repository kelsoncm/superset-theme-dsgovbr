# Configuration file for the Sphinx documentation builder.
# Cuidado: Não quebrar upstream. Leia AGENTS.md antes de mexer.

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'SupersetBR'
copyright = '2026, SupersetBR'
author = 'SupersetBR Team'
version = '1.0'
release = '1.0.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'pt_BR'

# -- Options for HTML output -------------------------------------------------

html_theme = 'furo'
html_static_path = ['_static']

# Customizações de cores do tema Furo baseadas no DSGovBR
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#1351b4",  # Azul Principal do DSGovBR
        "color-brand-content": "#0c326f",  # Azul Escuro do DSGovBR
        "color-api-keyword": "#e52207",
    },
    "dark_css_variables": {
        "color-brand-primary": "#2670e8",  # Azul Claro do DSGovBR
        "color-brand-content": "#2670e8",
    },
}

