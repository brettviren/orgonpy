# -*- coding: utf-8 -*-
"""
Extract Table of Content
========================

A Pelican plugin to extract table of contents (ToC) from `article.content` and
place it in its own `article.toc` variable for use in templates.
"""

from os import path
from bs4 import BeautifulSoup
from pelican import signals, readers, contents


def extract_toc(content):
    if isinstance(content, contents.Static):
        return

    soup = BeautifulSoup(content._content,'html.parser')
    filename = content.source_path
    extension = path.splitext(filename)[1][1:]
    toc = None

    # if it is a Markdown file
    if extension in readers.MarkdownReader.file_extensions:
        toc = soup.find('div', class_='toc')
        if toc: toc.extract()
    # else if it is a reST file
    elif extension in readers.RstReader.file_extensions:
        toc = soup.find('div', class_='contents topic')
        if toc: toc.extract()
        if toc:
            tag=BeautifulSoup(str(toc))
            tag.div['class']='toc'
            tag.div['id']=''
            p=tag.find('p', class_='topic-title first')
            if p:p.extract()
            toc=tag
    elif extension in ['org']:
        toc = soup.find('div', id="table-of-contents")
        if toc:
            toc.extract()
            tag=BeautifulSoup(str(toc))
            tag.div['class']='toc'
            tag.div['id']=''
            p=tag.find('p', class_='topic-title first')
            if p:p.extract()
            h2=tag.find('h2')   # 'Table of Contents'
            if h2: h2.extract()
            orgfile = path.basename(content.source_path)
            tag.append(BeautifulSoup('<a href="%s">Org source</a>'%orgfile))
            toc=tag

    elif not toc:  # Pandoc reader
        toc = soup.find('nav', id='TOC')
    if toc:
        toc.extract()
        content._content = soup.decode()
        content.toc = toc.decode()
        if content.toc.startswith('<html>'):
            content.toc = content.toc[12:-14]


def register():
    signals.content_object_init.connect(extract_toc)
