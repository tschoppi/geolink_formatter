# -*- coding: utf-8 -*-
import datetime
from lxml.etree import XMLParser, XMLSchema, XML, fromstring

from geolink_formatter.entity import Document, File


class XML(XMLParser):
    def __init__(self, dtd_validation=False):
        """Create a new XML parser instance containing the geoLink XSD for validation.

        Args:
            dtd_validation (bool): Enable/disable validation of document type definition (DTD).
                Optional, defaults to False.

        """
        super(XML, self).__init__(dtd_validation=dtd_validation, schema=self.__schema__)

    def __parse_xml__(self, xml):
        """Parses the specified XML string and validates it against the geoLink XSD.

        Args:
            xml (str): The XML to be parsed.

        Returns:
            lxml.etree._Element: The root element of the parsed geoLink XML.

        Raises:
            lxml.etree.XMLSyntaxError: Raised on failed validation.

        """
        return fromstring(xml, self)

    def fromstring(self, xml):
        """Parses XML into internal structure.

        The specified XML string is gets validated against the geoLink XSD on parsing.

        Args:
            xml (str): The XML to be parsed.

        Returns:
            list[geolink_formatter.entity.Document]: A list containing the parsed document elements.

        Raises:
            lxml.etree.XMLSyntaxError: Raised on failed validation.
        """
        root = self.__parse_xml__(xml)
        documents = list()

        for document_el in root.iter('document'):
            doc_id = document_el.attrib.get('id')
            if doc_id and doc_id not in [doc.id for doc in documents]:
                files = list()
                for file_el in document_el.iter('file'):
                    files.append(File(
                        file_el.attrib.get('title'),
                        file_el.attrib.get('href'),
                        file_el.attrib.get('category')
                    ))
                enactment_date = document_el.attrib.get('enactment_date')
                if enactment_date:
                    enactment_date = datetime.datetime.strptime(enactment_date, self.__date_format__).date()
                decree_date = document_el.attrib.get('decree_date')
                if decree_date:
                    decree_date = datetime.datetime.strptime(decree_date, self.__date_format__).date()
                documents.append(Document(
                    doc_id,
                    document_el.attrib.get('title'),
                    document_el.attrib.get('category'),
                    document_el.attrib.get('doctype'),
                    files,
                    enactment_date=enactment_date,
                    federal_level=document_el.attrib.get('federal_level'),
                    authority=document_el.attrib.get('authority'),
                    authority_url=document_el.attrib.get('authority_url'),
                    type=document_el.attrib.get('type'),
                    subtype=document_el.attrib.get('subtype'),
                    cycle=document_el.attrib.get('cycle'),
                    decree_date=decree_date
                ))

        return documents

    __date_format__ = '%Y-%m-%d'
    """str: Format of date values in XML."""

    __schema__ = XMLSchema(XML("""
    <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
      <xs:element name="geolinks">
        <xs:complexType>
          <xs:choice minOccurs="1" maxOccurs="unbounded">
            <xs:element name="document">
              <xs:complexType>
                <xs:sequence>
                  <xs:element name="file" minOccurs="0" maxOccurs="unbounded">
                    <xs:complexType>
                      <xs:attribute name="category">
                          <xs:simpleType>
                              <xs:restriction base="xs:string">
                                  <xs:enumeration value="main" />
                                  <xs:enumeration value="additional" />
                              </xs:restriction>
                          </xs:simpleType>
                      </xs:attribute>
                      <xs:attribute name="href" type="xs:string" />
                      <xs:attribute name="title" type="xs:string" />
                    </xs:complexType>
                  </xs:element>
                </xs:sequence>
                <xs:attribute name="id" type="xs:string" />
                <xs:attribute name="category" >
                    <xs:simpleType>
                        <xs:restriction base="xs:string">
                            <xs:enumeration value="main" />
                            <xs:enumeration value="related" />
                        </xs:restriction>
                    </xs:simpleType>
                </xs:attribute>
                <xs:attribute name="doctype">
                    <xs:simpleType>
                        <xs:restriction base="xs:string">
                            <xs:enumeration value="edict" />
                            <xs:enumeration value="decree" />
                        </xs:restriction>
                    </xs:simpleType>
                </xs:attribute>
                <xs:attribute name="federal_level">
                    <xs:simpleType>
                        <xs:restriction base="xs:string">
                            <xs:enumeration value="Gemeinde" />
                            <xs:enumeration value="Kanton" />
                            <xs:enumeration value="Interkantonal" />
                            <xs:enumeration value="Bund" />
                        </xs:restriction>
                    </xs:simpleType>
                </xs:attribute>
                <xs:attribute name="authority" type="xs:string" />
                <xs:attribute name="authority_url" type="xs:string" />
                <xs:attribute name="cycle" type="xs:string" />
                <xs:attribute name="title" type="xs:string" />
                <xs:attribute name="type" type="xs:string" />
                <xs:attribute name="subtype" type="xs:string" />
                <xs:attribute name="decree_date" type="xs:string" />
                <xs:attribute name="enactment_date" type="xs:string" />
              </xs:complexType>
            </xs:element>
          </xs:choice>
        </xs:complexType>
      </xs:element>
    </xs:schema>
    """))
    """lxml.etree.XMLSchema: geoLink XML schema for validation."""
