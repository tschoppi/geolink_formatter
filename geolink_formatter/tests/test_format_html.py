# -*- coding: utf-8 -*-
from geolink_formatter.format import HTML


def test_format(documents):
    formatter = HTML()
    html = formatter.format(documents)
    assert html == '<ul class="geolink-formatter">' \
                   '<li class="geolink-formatter-document">Document with file (15.01.2017)' \
                   '<ul class="geolink-formatter">' \
                   '<li class="geolink-formatter-file">' \
                   '<a href="http://www.example.com/test.pdf" target="_blank">Test file</a>' \
                   '</li>' \
                   '</ul>' \
                   '</li>' \
                   '</ul>'
