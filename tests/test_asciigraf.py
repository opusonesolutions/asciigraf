#############################################################################
# Copyright (c) 2017-present, Opus One Energy Solutions Corporation
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#############################################################################

import pytest

from asciigraf import graph_from_ascii
from asciigraf.asciigraf import (
    node_iter,
    InvalidEdgeError,
)
from asciigraf.point import Point


def test_node_iter_returns_label_and_position_of_nodes():
    network = """
    Sa---1
        /
       |---L_245
    """

    nodes = dict(node_iter(network))

    assert len(nodes) == 3
    assert nodes["Sa"] == Point(4, 1)
    assert nodes["L_245"] == Point(11, 3)
    assert nodes["1"] == Point(9, 1)


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


def test_converts_the_other_kind_down_right_angle():
    graph = graph_from_ascii("""
            1-|
              |
              2         """)

    assert set(graph.nodes()) == {"1", "2"}
    assert set(graph.edges()) == {("1", "2")}


def test_converts_down_left_angle():
    graph = graph_from_ascii("""
        1
        |
        |--2 """)

    assert set(graph.nodes()) == {"1", "2"}
    assert set(graph.edges()) == {("1", "2")}


def test_converts_other_kind_of_down_left_angle():
    graph = graph_from_ascii("""
        1
        |
        ---2 """)
    assert set(graph.nodes()) == {"1", "2"}
    assert set(graph.edges()) == {("1", "2")}


def test_converts_escaped_down_obtuse_angle():
    graph = graph_from_ascii(r"""
            1--------
                     \
                      2      """)
    assert set(graph.nodes()) == {"1", "2"}
    assert set(graph.edges()) == {("1", "2")}


def test_converts_other_kind_of_escaped_down_obtuse_angle():
    graph = graph_from_ascii(r"""
            1-------\
                     \
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


def test_converts_other_kind_of_down_acute_angle():
    graph = graph_from_ascii("""
                1-------/
                       /
                      2         """)
    assert set(graph.nodes()) == {"1", "2"}
    assert set(graph.edges()) == {("1", "2")}


def test_converts_up_right_angle():
    graph = graph_from_ascii("""
                1
                |
         2------|            """)
    assert set(graph.nodes()) == {"1", "2"}
    assert set(graph.edges()) == {("1", "2")}


def test_converts_the_other_kind_of_up_right_angle():
    graph = graph_from_ascii("""
                1
                |
         2-------            """)
    assert set(graph.nodes()) == {"1", "2"}
    assert set(graph.edges()) == {("1", "2")}


def test_converts_left_down_angle():
    graph = graph_from_ascii("""
         ------2
         |
         1
    """)

    assert set(graph.nodes()) == {"2", "1"}
    assert set(graph.edges()) == {("2", "1")}


def test_u_bend():
    graph = graph_from_ascii("""
         ------|
         |     |
         1     |
        2------|
    """)

    assert set(graph.nodes()) == {"1", "2"}
    assert set(graph.edges()) == {("1", "2")}


def test_doubl_down_left_angle():
    graph = graph_from_ascii("""
         ------2
         |
         |
        --
    1---|
    """)

    assert set(graph.nodes()) == {"2", "1"}
    assert set(graph.edges()) == {("2", "1")}


def test_converts_meshed_network():
    graph = graph_from_ascii(r"""
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
    graph = graph_from_ascii(r"""
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


def test_adjacent_edges():
    graph = graph_from_ascii("""
        a------b
        c----------d
    """)

    assert set(graph.nodes()) == {
        "a", "b", "c", "d"
    }
    assert set(graph.edges()) == {
        ("a", "b"),
        ("c", "d"),
    }


def test_some_more_node_names():
    graph = graph_from_ascii(r"""
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


@pytest.mark.parametrize("label", [
    'longlonglabel', 'short', 'l',
])
def test_vertical_line_labels(label):
    graph = graph_from_ascii("""
        A
        |
       ({label})
        |
        B
    """.format(label=label))

    assert set(graph.nodes()) == {
        "A", "B"
    }

    assert set(graph.edges()) == {
        ("A", "B")
    }

    assert graph.get_edge_data("A", "B")["label"] == label
    assert graph.get_edge_data("A", "B")["length"] == 3


def test_vertical_line_adjacent_labels():
    graph = graph_from_ascii("""
                C
        A---D   |
          (Vertical)
                |
                B
    """)

    assert set(graph.nodes()) == {
        "A", "B", "C", "D"
    }

    assert set(graph.edges()) == {
        ("A", "D"),
        ("C", "B")
    }

    assert graph.get_edge_data("C", "B")["label"] == "Vertical"
    assert graph.get_edge_data("C", "B")["length"] == 3


def test_too_many_neighbours_triggers_bad_edge_exception(caplog):
    with pytest.raises(InvalidEdgeError) as e:
        graph_from_ascii("""
               1---------------3
                       |
                       2""")

    assert str(e.value) == '''\
Too many many neighbors at ln 1, col 23

\x1b[0mnetwork_string = \x1b[2m"""\x1b[0m
\x1b[0m               1------\x1b[31m\x1b[1m-\x1b[0m\x1b[31m\x1b[1m-\x1b[0m\x1b[31m\x1b[1m-\x1b[0m------3
\x1b[0m                       \x1b[31m\x1b[1m|\x1b[0m
\x1b[0m                       2\x1b[2m"""\x1b[0m''' # noqa


def test_missing_end_node_raises_missing_end_node_exception():
    with pytest.raises(InvalidEdgeError) as e:
        graph_from_ascii('1---')

    assert str(e.value) == """\
Too few many neighbors at ln 0, col 3

\x1b[0mnetwork_string = \x1b[2m"\x1b[0m1-\x1b[31m\x1b[1m-\x1b[0m\x1b[31m\x1b[1m-\x1b[0m\x1b[2m"\x1b[0m"""  # noqa


def test_bad_label_triggers_exception(caplog):
    with pytest.raises(InvalidEdgeError) as e:
        graph_from_ascii("""
                n1
                |
           n2--(label)
                |
                n3
        """)
    assert str(e.value) == '''\
Too many many neighbors at ln 3, col 16

\x1b[0mnetwork_string = \x1b[2m"""\x1b[0m
\x1b[0m                n1
\x1b[0m                \x1b[31m\x1b[1m|\x1b[0m
\x1b[0m           n2--\x1b[31m\x1b[1m(\x1b[0m\x1b[31m\x1b[1ml\x1b[0mabel)
\x1b[0m                \x1b[31m\x1b[1m|\x1b[0m
\x1b[0m                n3
\x1b[0m\x1b[2m"""\x1b[0m'''  # noqa
