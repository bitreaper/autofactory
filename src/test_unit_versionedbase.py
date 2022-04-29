"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Copyright (c) 2019-2022 Todd LaWall, aka Bitreaper
"""

import pytest
from versionedBase import VersionedBase


class Ver1(VersionedBase):
    versionString = "1.0"


class Ver2(Ver1):
    versionString = "2.0"


class Ver3(Ver2):
    versionString = "3.0"


def test_findVersion_BaseIsReturned():
    obj = Ver1.findVersion("1.0")
    assert obj.__name__ == "Ver1"


def test_findVersion_middleIsReturned():
    obj = Ver1.findVersion("2.0")
    assert obj.__name__ == "Ver2"


def test_findVersion_endIsReturned():
    obj = Ver1.findVersion("3.0")
    assert obj.__name__ == "Ver3"


def test_dont_find_version():
    with pytest.raises(NotImplementedError):
        obj = Ver1.findVersion("4.0")


def test_dont_have_subclasses():
    with pytest.raises(NotImplementedError):
        obj = Ver3.findVersion("4.0")


def test_return_latest():
    obj = Ver1.findVersion("4.0", returnLatest=True)
    assert obj.__name__ == "Ver3"


def test_return_base():
    obj = Ver1.findVersion("4.0", returnBase=True)
    assert obj.__name__ == "Ver1"


def test_find_prev():
    obj = Ver3.findPreviousVersion("2.0")
    assert obj.__name__ == "Ver2"
