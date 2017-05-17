# -*- coding: utf-8 -*-
import datetime
import pytest

from geolink_formatter.entity import Document, File


@pytest.fixture()
def documents():
    return [
        Document(
            '1',
            'Document with file',
            'main',
            'decree',
            [File('Test file', 'http://www.example.com/test.pdf', 'main')],
            enactment_date=datetime.date(2017, 1, 15)
        )
    ]
