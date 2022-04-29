"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Copyright (c) 2019-2022 Todd LaWall, aka Bitreaper
"""

import pytest
from modelBase import ModelBase


class ModelA(ModelBase):
    modelStrings = ["A", "a"]


class ModelB(ModelA):
    modelStrings = ["B", "b"]


class ModelC(ModelB):
    modelStrings = ["C", "c"]


def test_findModel_firstItem():
    obj = ModelA.findModel("C")
    assert obj.__name__ == "ModelC"


def test_findModel_secondItem():
    obj = ModelA.findModel("c")
    assert obj.__name__ == "ModelC"


def test_dont_findModel():
    with pytest.raises(NotImplementedError):
        obj = ModelA.findModel("IDontExist")


def test_dont_have_subclasses():
    with pytest.raises(NotImplementedError):
        obj = ModelC.findModel("NonExistent")


def test_findBase():
    obj = ModelA.findModel("D", returnBase=True)
    assert obj.__name__ == "ModelA"
