import datetime

import pkg_resources
import sphinx_material

html_theme = 'sphinx_material'
html_theme_path = sphinx_material.html_theme_path()
html_context = sphinx_material.get_html_context()
html_sidebars = {
    "**": ["globaltoc.html", "searchbox.html"]
}
html_theme_options = {
    'base_url': 'http://email-normalize.readthedocs.io',
    'repo_url': 'https://github.com/gmr/email-normalize/',
    'repo_name': 'email-normalize',
    'html_minify': True,
    'css_minify': True,
    'nav_title': 'email-normalize',
    'globaltoc_depth': 2,
    'theme_color': '0000aa',
    'logo_icon': '&#x2286',
    'color_primary': 'grey',
    'color_accent': 'blue',
    'version_dropdown': False
}
html_static_path = ['_static']
html_css_files = [
    'css/custom.css'
]

master_doc = 'index'
project = 'email-normalize'
release = version = pkg_resources.get_distribution(project).version
copyright = '2015-{}, Gavin M. Roy'.format(datetime.date.today().year)

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx_material'
]

set_type_checking_flag = True
typehints_fully_qualified = True
always_document_param_types = True
typehints_document_rtype = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

autodoc_default_options = {'autodoc_typehints': 'description'}

