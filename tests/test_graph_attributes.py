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

