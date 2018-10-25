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

               --------n1
               |
               |
               |
               n2 """)

    points = networkx.get_edge_attributes(graph, 'points')

    assert points == {
        ("n1", "n2"): [
            (22, 2), (21, 2), (20, 2), (19, 2),
            (18, 2), (17, 2), (16, 2), (15, 2),
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
