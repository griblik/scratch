# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:04:19 2017

@author: ntelford
"""

import pytest
from e1 import tips


def test_tips():
    assert tips(100,.15) == 115
    assert tips(10.0,.15) == 11.50
    assert tips(1.5,.15) == 1.72

    with pytest.raises(TypeError):
        tips('a', .1)