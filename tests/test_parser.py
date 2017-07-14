# -*- coding: utf-8 -*-
import pytest
import requests_mock
from lxml.etree import XMLSyntaxError, _Element
from requests import RequestException

from geolink_formatter.parser import XML


def test_xml_init():
    parser = XML(host_url='http://oereblex.test.com')
    assert isinstance(parser, XML)
    assert parser.host_url == 'http://oereblex.test.com'


@pytest.mark.parametrize('as_bytes', [False, True])
def test_xml_parse(as_bytes):
    xml = u"""<?xml version="1.0" encoding="utf-8"?>
    <geolinks>
        <document authority='Example Authority' authority_url='http://www.example.com'
                  category='main' cycle='Example Cycle' doctype='decree' enactment_date='1999-10-18'
                  federal_level='Gemeinde' id='1' subtype='Example Subtype' title='Example'
                  type='Example Type'>
            <file category='main' href='/api/attachments/1' title='example1.pdf'></file>
            <file category='additional' href='/api/attachments/2' title='example2.pdf'></file>
            <file category='additional' href='/api/attachments/3' title='example3.pdf'></file>
        </document>
        <document authority='Another authority' authority_url='http://www.example.com' category='related'
                  doctype='edict' enactment_date='2016-01-01' federal_level='Bund' id='2'
                  title='Another example'>
            <file category='main' href='http://www.example.com/example' title='example.pdf'></file>
        </document>
    </geolinks>
    """
    if as_bytes:
        xml = xml.encode('utf-16be')
    parser = XML()
    root = parser.__parse_xml__(xml)
    assert isinstance(root, _Element)
    assert root.tag == 'geolinks'
    assert len(root.findall('document')) == 2
    document = root.find('document')
    assert isinstance(document, _Element)
    assert document.attrib.get('category') == 'main'
    assert len(document.findall('file')) == 3


def test_xml_from_string_invalid():
    xml = """<?xml version="1.0" encoding="utf-8"?>
    <invalidTag></invalidTag>
    """
    with pytest.raises(XMLSyntaxError):
        parser = XML()
        parser.from_string(xml)


@pytest.mark.parametrize('host_url', [None, 'http://oereblex.test.com'])
def test_xml_from_string(host_url):
    xml = """<?xml version="1.0" encoding="utf-8"?>
    <geolinks>
        <document authority='Example Authority' authority_url='http://www.example.com'
                  category='main' cycle='Example Cycle' doctype='decree' enactment_date='1999-10-18'
                  federal_level='Gemeinde' id='1' subtype='Example Subtype' title='Example'
                  type='Example Type' decree_date='1999-11-01'>
            <file category='main' href='/api/attachments/1' title='example1.pdf'></file>
            <file category='additional' href='/api/attachments/2' title='example2.pdf'></file>
            <file category='additional' href='/api/attachments/3' title='example3.pdf'></file>
        </document>
        <document authority='Another authority' authority_url='http://www.example.com' category='related'
                  doctype='edict' enactment_date='2016-01-01' federal_level='Bund' id='2'
                  title='Another example'>
            <file category='main' href='http://www.example.com/example' title='example.pdf'></file>
        </document>
    </geolinks>
    """
    parser = XML(host_url=host_url)
    documents = parser.from_string(xml)
    assert len(documents) == 2
    assert documents[0].authority == 'Example Authority'
    assert documents[0].authority_url == 'http://www.example.com'
    assert documents[0].category == 'main'
    assert documents[0].cycle == 'Example Cycle'
    assert documents[0].doctype == 'decree'
    assert documents[0].enactment_date.year == 1999
    assert documents[0].enactment_date.month == 10
    assert documents[0].enactment_date.day == 18
    assert documents[0].federal_level == 'Gemeinde'
    assert documents[0].id == '1'
    assert documents[0].subtype == 'Example Subtype'
    assert documents[0].title == 'Example'
    assert documents[0].type == 'Example Type'
    assert documents[0].decree_date.year == 1999
    assert documents[0].decree_date.month == 11
    assert documents[0].decree_date.day == 1
    assert len(documents[0].files) == 3
    assert documents[0].files[1].title == 'example2.pdf'
    if host_url:
        assert documents[0].files[1].href == 'http://oereblex.test.com/api/attachments/2'
    else:
        assert documents[0].files[1].href == '/api/attachments/2'
    assert documents[0].files[1].category == 'additional'


def test_xml_duplicate_document():
    xml = """<?xml version="1.0" encoding="utf-8"?>
    <geolinks>
        <document authority='Example Authority' authority_url='http://www.example.com'
                  category='main' cycle='Example Cycle' doctype='decree' enactment_date='1999-10-18'
                  federal_level='Gemeinde' id='1' subtype='Example Subtype' title='Example'
                  type='Example Type' decree_date='1999-11-01'>
            <file category='main' href='/api/attachments/1' title='example1.pdf'></file>
            <file category='additional' href='/api/attachments/2' title='example2.pdf'></file>
            <file category='additional' href='/api/attachments/3' title='example3.pdf'></file>
        </document>
        <document authority='Example Authority' authority_url='http://www.example.com'
                  category='main' cycle='Example Cycle' doctype='decree' enactment_date='1999-10-18'
                  federal_level='Gemeinde' id='1' subtype='Example Subtype' title='Example'
                  type='Example Type' decree_date='1999-11-01'>
            <file category='main' href='/api/attachments/1' title='example1.pdf'></file>
            <file category='additional' href='/api/attachments/2' title='example2.pdf'></file>
            <file category='additional' href='/api/attachments/3' title='example3.pdf'></file>
        </document>
    </geolinks>
    """
    parser = XML()
    documents = parser.from_string(xml)
    assert len(documents) == 1


def test_xml_from_url_invalid():
    with pytest.raises(RequestException):
        XML().from_url('http://invalid.url.bl.ch/')


def test_xml_from_url_error():
    with requests_mock.mock() as m:
        m.get('http://oereblex.test.com/api/geolinks/1501.xml', text='error', status_code=500)
        with pytest.raises(RequestException):
            XML().from_url('http://oereblex.test.com/api/geolinks/1501.xml')


def test_xml_from_url(mock_request):
    with mock_request():
        documents = XML().from_url('http://oereblex.test.com/api/geolinks/1500.xml')
        assert len(documents) == 4
        assert len(documents[0].files) == 5
