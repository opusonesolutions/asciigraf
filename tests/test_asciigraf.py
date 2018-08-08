#############################################################################
# Copyright (c) 2017-present, Opus One Energy Solutions Corporation
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#############################################################################

from collections import OrderedDict
import pytest

from asciigraf import graph_from_ascii
from asciigraf.asciigraf import node_iter, Point, BadEdgeException


def test_ascii_positions():
    graph = graph_from_ascii(
        """
                Node_1---Node2-----
                                 /
                               Nald33
        """)
    assert graph.node["Node_1"]["position"] == Point(x=16, y=1)
    assert graph.node["Node2"]["position"] == Point(x=25, y=1)
    assert graph.node["Nald33"]["position"] == Point(x=31, y=3)


def test_node_iter_returns_label_and_position_of_feeder_nodes():
    network = """
    Sa---1
        /
       |---L_245
    """

    nodes = {node_label: pos for node_label, pos in node_iter(network)}

    assert len(nodes) == 3
    assert nodes["Sa"] == Point(4, 1)
    assert nodes["L_245"] == Point(11, 3)
    assert nodes["1"] == Point(9, 1)


def test_point_class():
    p1, p2 = Point(1, 2), Point(3, 4)

    p3 = p1 + p2
    assert p3.x == 4
    assert p3.y == 6
    assert p1 == Point(1, 2)
    assert p1 in {p1, p2, p3}

    x, y = p1
    assert x == 1
    assert y == 2


def test_converts_linear_network():
    graph = graph_from_ascii(" A---B----C----D")

    assert set(graph.nodes()) == {"A", "B", "C", "D"}
    assert set(graph.edges()) == {("A", "B"), ("B", "C"), ("C", "D")}


def test_converts_down_right_angle():
    graph = graph_from_ascii("""
           1--------
                   |
                   2         """)
    assert set(graph.nodes()) == {"1", "2"}
    assert set(graph.edges()) == {("1", "2")}


def test_converts_escaped_down_obtuse_angle():
    graph = graph_from_ascii("""
            1--------
                     \\
                      2      """)
    assert set(graph.nodes()) == {"1", "2"}
    assert set(graph.edges()) == {("1", "2")}


def test_converts_down_acute_angle():
    graph = graph_from_ascii("""
                1--------
                       /
                      2         """)
    assert set(graph.nodes()) == {"1", "2"}
    assert set(graph.edges()) == {("1", "2")}


def test_converts_meshed_network():
    graph = graph_from_ascii("""
          0----1-------2
                \     /
                 3---4       """)
    assert set(graph.nodes()) == {"0", "1", "2", "3", "4"}
    assert set(graph.edges()) == {
        ("0", "1"),
        ("1", "2"),
        ("1", "3"),
        ("2", "4"),
        ("3", "4")
    }


def test_node_ordering():
    graph = graph_from_ascii("""
          0----3-------2
                \     /
                 1---4
                             """)
    assert set(graph.nodes()) == {"0", "1", "2", "3", "4"}
    assert set(graph.edges()) == {
        ("0", "3"),
        ("3", "2"),
        ("3", "1"),
        ("2", "4"),
        ("1", "4")
    }


def test_S_bend():
    graph = graph_from_ascii("""
          0-----
               |
               |---2
                             """)
    assert set(graph.nodes()) == {"0", "2"}
    assert set(graph.edges()) == {("0", "2")}


def test_some_more_node_names():
    graph = graph_from_ascii("""
          s---p----1---nx
         /    |        |
        /     |        0---f
       6l-a   c--
      /   |      \--k
     /   ua         |  9e
    q      \        | /
            \-r7z   jud
                \    |
                 m   y
                  \  |
                   v-ow
                             """)
    assert len(graph.nodes()) == 19
    assert len(graph.edges()) == 19


def test_line_lengths():
    edge_data = graph_from_ascii("""
            <13>           <10>
        n0-------------n1----------n2
                       |
                       |  <3>
                       |
                       n4
    """).edges(data=True)

    assert list(edge_data) == [
        ("n0", "n1", OrderedDict([("length", 13)])),
        ("n1", "n2", OrderedDict([("length", 10)])),
        ("n1", "n4", OrderedDict([("length", 3)])),
    ]


def test_line_labels():
    graph = graph_from_ascii("""
        A---(nuts)----B----(string)---C
                      |
                      |
                      |
                      D---(string)----E
    """)

    assert set(graph.nodes()) == {
        "A", "B", "C", "D", "E"
    }

    assert set(graph.edges()) == {
        ("A", "B"), ("B", "C"), ("B", "D"), ("D", "E")
    }

    assert graph.get_edge_data("A", "B")["label"] == "nuts"
    assert graph.get_edge_data("A", "B")["length"] == 13

    assert graph.get_edge_data("B", "C")["label"] == "string"
    assert graph.get_edge_data("B", "C")["length"] == 15

    with pytest.raises(KeyError):
        assert graph.get_edge_data("B", "D")["label"] == ""
    assert graph.get_edge_data("B", "D")["length"] == 3

    assert graph.get_edge_data("D", "E")["label"] == "string"
    assert graph.get_edge_data("D", "E")["length"] == 15
