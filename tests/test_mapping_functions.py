#############################################################################
# Copyright (c) 2017-present, Opus One Energy Solutions Corporation
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#############################################################################


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


def test_drawing_nodes_and_edge_chars():
    assert draw(
        edge_chars={
            Point(8, 1): "|",
            Point(8, 2): "|",
            Point(8, 4): "|",
            Point(8, 5): "|",
        },
        nodes={
            Point(8, 3): "my_node",
            Point(12, 3): "my_node",
            Point(7, 3): "my_node",
            Point(9, 3): "my_node",
            Point(10, 3): "my_node",
            Point(6, 3): "my_node",
            Point(11, 3): "my_node",
        }
    ) == """
        |
        |
      my_node
        |
        |"""
