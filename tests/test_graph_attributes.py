#############################################################################
# Copyright (c) 2017-present, Opus One Energy Solutions Corporation
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#############################################################################

import networkx

from asciigraf import graph_from_ascii


def test_line_lengths():
    graph = graph_from_ascii("""
            <13>           <10>
        n0-------------n1----------n2
                       |
                       |  <3>
                       |
                       n4
    """)

    lengths = networkx.get_edge_attributes(graph, "length")
    assert lengths == {
        ("n0", "n1"): 13, ("n1", "n2"): 10,
        ("n1", "n4"): 3,
    }


def test_node_positions():
    graph = graph_from_ascii(
        """
                Node_1---Node2-----
                                 /
                               Nald33
        """)
    assert graph.node["Node_1"]["position"] == (16, 1)
    assert graph.node["Node2"]["position"] == (25, 1)
    assert graph.node["Nald33"]["position"] == (31, 3)


def test_node_position_attributes():
    graph = graph_from_ascii("""

        n0-------------n1----------n2
                       |
                       |
                       |
                       n4
    """)

    node_positions = networkx.get_node_attributes(graph, "position")
    assert node_positions == {
        "n0": (8, 2), "n1": (23, 2), "n2": (35, 2),
                      "n4": (23, 6),
    }


def test_line_positions():
    graph = graph_from_ascii("""

        n1------
               |
               |
               |
               n2 """)

    points = networkx.get_edge_attributes(graph, 'points')

    assert points == {
        ("n1", "n2"): [
            (10, 2), (11, 2), (12, 2), (13, 2), (14, 2), (15, 2),
                                                         (15, 3),
                                                         (15, 4),
                                                         (15, 5),
        ]
    }


def test_line_positions_when_line_is_split():
    graph = graph_from_ascii("""

               -------n1
               |
               |
               |
               n2 """)

    points = networkx.get_edge_attributes(graph, 'points')

    assert points == {
        ("n1", "n2"): [
            (21, 2), (20, 2), (19, 2), (18, 2), (17, 2), (16, 2), (15, 2),
            (15, 3),
            (15, 4),
            (15, 5),
        ]
    }


def test_line_positions_when_order_is_reversed():
    graph = graph_from_ascii("""

               -----
               |   |
               n2  n1""")

    points = networkx.get_edge_attributes(graph, 'points')

    assert points == {
        ("n2", "n1"): [
            (15, 3),
            (15, 2),
            (16, 2),
            (17, 2),
            (18, 2),
            (19, 2),
            (19, 3),
        ]
    }


def test_line_positions_with_horizontal_label():
    graph = graph_from_ascii("  n1---(label)--n2  ")

    points = networkx.get_edge_attributes(graph, 'points')
    assert points == {
        ("n1", "n2"): [
            # positions of the first three dashes right of `n1`
            (4, 0), (5, 0), (6, 0),

            # positions of the characters in `(label)`
            (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0),

            # positions of the last 2 dashes left of `n2`
            (14, 0), (15, 0)
        ]
    }


def test_line_positions_with_vertical_label():
    graph = graph_from_ascii("""

            n1
            |
         (label)
            |
           n2

    """)

    assert networkx.get_edge_attributes(graph, 'points') == {
        ("n1", "n2"): [
            (12, 3),  # position of the '|' under `n1`
            (12, 4),  # position of the 'b' in `label`
            (12, 5),  # position of the '|' above `n2`
        ]
    }
