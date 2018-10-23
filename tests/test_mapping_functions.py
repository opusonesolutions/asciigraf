from asciigraf.asciigraf import (
    draw,
    get_edge_chars,
    patch_edge_chars_over_labels
)
from asciigraf.point import Point


def test_get_edge_chars():
    assert get_edge_chars("   --|   ") == {
        Point(3, 0): "-",
        Point(4, 0): "-",
        Point(5, 0): "|",
    }


def test_get_edge_chars_with_horizontal_label():
    assert get_edge_chars("---(label)---") == {
        Point(0, 0): "-",
        Point(1, 0): "-",
        Point(2, 0): "-",
        Point(10, 0): "-",
        Point(11, 0): "-",
        Point(12, 0): "-",
    }


def test_get_edge_chars_with_vertical_label():
    assert get_edge_chars("""
        |
        |
      (label)
        |
        |
    """) == {
        Point(8, 1): "|",
        Point(8, 2): "|",
        Point(8, 4): "|",
        Point(8, 5): "|",
    }


def test_patching_edge_chars_over_horizontal_label():
    edge_chars = get_edge_chars("---(label)---")
    labels = {Point(3, 0): "(label)"}
    edge_chars = patch_edge_chars_over_labels(labels, edge_chars)

    assert draw(edge_chars) == "-------------"


def test_patching_edge_chars_over_vertical_label():
    edge_chars = get_edge_chars("""
        |
        |
      (label)
        |
        |""")
    labels = {Point(6, 3): "(label)"}
    edge_chars = patch_edge_chars_over_labels(labels, edge_chars)

    assert draw(edge_chars) == """
        |
        |
        |
        |
        |"""
