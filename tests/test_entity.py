# -*- coding: utf-8 -*-
import datetime
import pytest
from geolink_formatter.entity import File, Document


def test_file():
    f = File('test.pdf', 'http://my.link.to/file', 'test')
    assert isinstance(f, File)
    assert f.title == 'test.pdf'
    assert f.href == 'http://my.link.to/file'
    assert f.category == 'test'


def test_file_missing_argument():
    with pytest.raises(TypeError):
        File()


def test_document():
    date = datetime.date.today()
    d = Document('1', 'Test', 'test', 'testdoc', [File('test.pdf', 'http://my.link.to/file', 'test')], date,
                 'testlevel', 'Authority', 'http://my.link.to/authority', 'testtype', 'testsubtype',
                 'testcycle', date)
    assert isinstance(d, Document)
    assert d.id == '1'
    assert d.title == 'Test'
    assert d.category == 'test'
    assert d.doctype == 'testdoc'
    assert len(d.files) == 1 and isinstance(d.files[0], File)
    assert d.enactment_date == date
    assert d.federal_level == 'testlevel'
    assert d.authority == 'Authority'
    assert d.authority_url == 'http://my.link.to/authority'
    assert d.type == 'testtype'
    assert d.subtype == 'testsubtype'
    assert d.cycle == 'testcycle'
    assert d.decree_date == date


def test_document_missing_argument():
    with pytest.raises(TypeError):
        Document()


def test_document_invalid_files():
    date = datetime.date.today()
    with pytest.raises(TypeError):
        Document('1', 'Test', 'test', 'testdoc', 'invalid', date, 'testlevel', 'Authority',
                 'http://my.link.to/authority', 'testtype', 'testsubtype', 'testcycle', date)


def test_document_empty_files():
    date = datetime.date.today()
    with pytest.raises(ValueError):
        Document(1, 'Test', 'test', 'testdoc', [], date, 'testlevel', 'Authority',
                 'http://my.link.to/authority', 'testtype', 'testsubtype', 'testcycle', date)


def test_document_invalid_enactment_date():
    date = datetime.date.today()
    with pytest.raises(TypeError):
        Document('1', 'Test', 'test', 'testdoc', [File('test.pdf', 'http://my.link.to/file', 'test')],
                 'invalid', 'testlevel', 'Authority', 'http://my.link.to/authority', 'testtype',
                 'testsubtype', 'testcycle', date)


def test_document_invalid_decree_date():
    date = datetime.date.today()
    with pytest.raises(TypeError):
        Document('1', 'Test', 'test', 'testdoc', [File('test.pdf', 'http://my.link.to/file', 'test')], date,
                 'testlevel', 'Authority', 'http://my.link.to/authority', 'testtype', 'testsubtype',
                 'testcycle', 'invalid')
