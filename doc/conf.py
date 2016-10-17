
# -*- coding: utf-8 -*-

import os
import sys
import imp

BASEDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

os.environ['DJANGO_SETTINGS_MODULE'] = 'project.development'
imp.load_source('django_binary', os.path.join(BASEDIR, 'bin', 'django'))

extensions = ['sphinx.ext.autodoc']
#templates_path = ['_templates']
#html_theme_path = ['_themes']
#html_static_path = ['_static']
source_suffix = '.rst'
master_doc = 'index'
project = u'Foo'
copyright = u'2014'
version = '1.0'
release = '1.0'
language = 'en'
html_title = "Foo"
unused_docs = []
exclude_trees = []
pygments_style = 'colorful'
html_theme = 'nature'
html_theme_options = {}
html_use_modindex = False
html_use_index = True
html_show_sourcelink = False
html_copy_source = False
html_file_suffix = '.html'
html_last_updated_fmt = '%b %d, %Y'
html_add_permalinks = False
#html_use_smartypants = True
html_additional_pages = {
#  'index': 'index.html',
  }

