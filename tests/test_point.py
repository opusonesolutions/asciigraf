#############################################################################
# Copyright (c) 2017-present, Opus One Energy Solutions Corporation
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#############################################################################


import pytest

from asciigraf.point import Point


@pytest.fixture
def p12():
    return Point(1, 2)


@pytest.fixture
def p34():
    return Point(3, 4)


def test_points_add_together(p12, p34):
    p = p12 + p34
    assert p.x == 4
    assert p.y == 6

    assert p is not p12
    assert p is not p34


def test_points_subtract(p12, p34):
    p = p12 - p34
    assert p.x == -2
    assert p.y == -2

    assert p is not p12
    assert p is not p34


def test_points_compare():
    assert Point(1, 1) < Point(1, 2)
    assert Point(1, 1) < Point(2, 1)


def test_points_are_sortable():
    starting_list = [Point(1, 2), Point(2, 1), Point(1, 1)]
    sorted_list = sorted(starting_list)
    assert sorted_list == [
        Point(1, 1), Point(2, 1), Point(1, 2)
    ]


def test_sorting_commutes():
    assert Point(33, 2) > Point(34, 1)
    assert Point(34, 1) < Point(33, 2)
    assert not Point(33, 2) < Point(34, 1)
    assert not Point(34, 1) > Point(33, 2)


def test_points_with_same_coords_are_equal(p12):
    assert p12 == Point(1, 2)


def test_points_can_be_in_sets(p12, p34):
    assert p12 in {p12, p34}


def test_points_iter_out_their_coords(p12):
    x, y = p12
    assert x == 1
    assert y == 2


def test_points_repr_their_coords(p12):
    assert repr(p12) == 'Point(1, 2)'


def test_point_attributes_cant_be_set(p12):
    with pytest.raises(TypeError):
        p12.x = 100

    with pytest.raises(TypeError):
        p12.y = 200

    with pytest.raises(TypeError):
        p12.z = 100


def test_point_attributes_cant_be_deleted(p12):
    with pytest.raises(TypeError):
        del p12.x

    with pytest.raises(TypeError):
        del p12.y

    with pytest.raises(TypeError):
        del p12.z
