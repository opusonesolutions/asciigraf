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


def test_points_subtract(p12, p34):
    p = p12 - p34
    assert p.x == -2
    assert p.y == -2


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
