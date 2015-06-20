'''OrgOnPy Pelican Plugin

This is heavily cribbed from the Org Reader Pelican plugin.

This plugin lets you write content in Emacs org-mode.  

It uses Emacs and org-exporter (v8) itself to export a content
document to HTML.  Some metadata is extracted from the org-element
tree and passed to Pelican.  

#+TITLE: The title.
#+DATE: 1970-01-01
#+CATEGORY: tag1, tag2
#+SLUG: a-short-name-for-the-url

If no slug given, the file name will be used unless it is index.org
then its directory will be used.

'''
import os
import sys
import logging

from pelican import readers
from pelican import signals

import orgmode.util as orgutil

LOG = logging.getLogger(__name__)

class OrgOnPelican(readers.BaseReader):
    enabled = True

    file_extensions = ['org']

    def read(self, filename):

        html, top = orgutil.htmltree(filename)

        first = top[0]

        justfname = os.path.basename(filename)
        fullpath = os.path.realpath(filename)
        fileslug, _ = os.path.splitext(os.path.basename(fullpath))
        if fileslug == 'index':
            fileslug = os.path.basename(os.path.dirname(fullpath))

        sys.stderr.write('Default slug: %s\n' % fileslug)

        metadata = dict(
            title = first.get('title',""),
            author = first.get('author',""),
            date = str(orgutil.date(first.get('date',"1970-01-01"))),
            category = first.get('category',"misc"),
            slug = first.get('slug',fileslug),
            tags = first.get('tags',''),
            url = fileslug,
            save_as = os.path.join(fileslug, justfname.replace('.org','.html'))
        )
        #sys.stderr.write('Metadata: %s\n' % str(metadata))

        parsed = {}
        for key, value in metadata.items():
            parsed[key] = self.process_metadata(key, value)

        #sys.stderr.write('Parsed: %s\n' % str(parsed))
        #sys.stderr.write('HTML: %s\n' % html)
        return html, parsed

def add_reader(readers):
    readers.reader_classes['org'] = OrgOnPelican

def register():
    signals.readers_init.connect(add_reader)


