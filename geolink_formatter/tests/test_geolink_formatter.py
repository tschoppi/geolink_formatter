# -*- coding: utf-8 -*-
from geolink_formatter import GeoLinkFormatter


def test_init():
    assert isinstance(GeoLinkFormatter(), GeoLinkFormatter)
