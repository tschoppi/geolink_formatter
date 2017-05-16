# -*- coding: utf-8 -*-
import datetime


class Msg(object):

    invalid_argument = 'Invalid argument "{arg}": expected "{expected}", got "{got}"'
    """
    Message for invalid argument type.

    :type: str
    """


class Document(object):
    def __init__(self, id, title, category, doctype, files, enactment_date, federal_level, authority,
                 authority_url, type=None, subtype=None, cycle=None, decree_date=None):
        """
        Creates a new document instance.

        :param id: The document identifier.
        :type id: int
        :param title: The document title.
        :type title: str
        :param category: The document category.
        :type category: str
        :param doctype: The internal type of the document.
        :type doctype: str
        :param files: The files contained by the document.
        :type files: list of geolink_formatter.entity.File
        :param enactment_date: The date of enactment.
        :type enactment_date: datetime.date
        :param federal_level: The federal level of the document.
        :type federal_level: str
        :param authority: The name of the authority responsible for the document.
        :type authority: str
        :param authority_url: The URL of the authority's website.
        :type authority_url: str
        :param type: The official type of the document.
        :type type: str
        :param subtype: The subtype of the document.
        :type subtype: str
        :param cycle: The document cycle.
        :type cycle: str
        :param decree_date: The date of decree.
        :type decree_date: datetime.date
        """
        if not isinstance(files, list):
            raise TypeError(Msg.invalid_argument.format(
                arg='files',
                expected=list,
                got=files.__class__
            ))

        if len(files) < 1:
            raise ValueError('Argument "files" has to contain at least one element')

        if not isinstance(enactment_date, datetime.date):
            raise TypeError(Msg.invalid_argument.format(
                arg='enactment_date',
                expected=datetime.date,
                got=enactment_date.__class__
            ))

        if decree_date and not isinstance(decree_date, datetime.date):
            raise TypeError(Msg.invalid_argument.format(
                arg='decree_date',
                expected=datetime.date,
                got=decree_date.__class__
            ))

        self.__id__ = id
        self.__title__ = title
        self.__category__ = category
        self.__doctype__ = doctype
        self.__files__ = files
        self.__enactment_date__ = enactment_date
        self.__federal_level__ = federal_level
        self.__authority__ = authority
        self.__authority_url__ = authority_url
        self.__type__ = type
        self.__subtype__ = subtype
        self.__cycle__ = cycle
        self.__decree_date__ = decree_date

    @property
    def id(self):
        """

        :ivar id: The document identifier.
        :type id: int
        """
        return self.__id__

    @property
    def title(self):
        """

        :ivar title: The document title.
        :type title: str
        """
        return self.__title__

    @property
    def category(self):
        """

        :ivar category: The document category.
        :type category: str
        """
        return self.__category__

    @property
    def doctype(self):
        """

        :ivar doctype: The internal type of the document.
        :type doctype: str
        """
        return self.__doctype__

    @property
    def files(self):
        """

        :ivar files: The files contained by the document.
        :type files: list of geolink_formatter.entity.File
        """
        return self.__files__

    @property
    def enactment_date(self):
        """

        :ivar enactment_date: The date of enactment.
        :type enactment_date: datetime.date
        """
        return self.__enactment_date__

    @property
    def federal_level(self):
        """

        :ivar federal_level: The federal level of the document.
        :type federal_level: str
        """
        return self.__federal_level__

    @property
    def authority(self):
        """

        :ivar authority: The name of the authority responsible for the document.
        :type authority: str
        """
        return self.__authority__

    @property
    def authority_url(self):
        """

        :ivar authority_url: The URL of the authority's website.
        :type authority_url: str
        """
        return self.__authority_url__

    @property
    def type(self):
        """

        :ivar type: The official type of the document.
        :type type: str
        """
        return self.__type__

    @property
    def subtype(self):
        """

        :ivar subtype: The subtype of the document.
        :type subtype: str
        """
        return self.__subtype__

    @property
    def cycle(self):
        """

        :ivar cycle: The document cycle.
        :type cycle: str
        """
        return self.__cycle__

    @property
    def decree_date(self):
        """

        :ivar decree_date: The date of decree.
        :type decree_date: datetime.date
        """
        return self.__decree_date__


class File(object):
    def __init__(self, title, href, category):
        """
        Creates a new file instance.

        :param title: The file's title.
        :type title: str
        :param href: The URL to access the file.
        :type href: str
        :param category: The file's category.
        :type category: str
        """
        self.__title__ = title
        self.__href__ = href
        self.__category__ = category

    @property
    def title(self):
        """

        :ivar title: The file's title.
        :type title: str
        """
        return self.__title__

    @property
    def href(self):
        """

        :ivar href: The URL to access the file.
        :type href: str
        """
        return self.__href__

    @property
    def category(self):
        """

        :ivar category: The file's category.
        :type category: str
        """
        return self.__category__
