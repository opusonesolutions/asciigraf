from collections import OrderedDict
import re

import networkx


def graph_from_ascii(network_string):
    """ Produces a networkx graph, based on an ascii drawing
        of a network
    """
    EDGE_CHAR_NEIGHBOURS = {
        "-":  [Point(-1, 0), Point(1, 0)],
        "\\": [Point(-1, -1),  Point(1, 1)],
        "/":  [Point(-1, 1), Point(1, -1)],
        "|":  [Point(0, -1), Point(0, 1)]
    }
    EDGE_CHARS = {"\\", "-", "/", "|"}
    nodes = list(node_iter(network_string))

    node_chars = OrderedDict()
    line_labels = {}
    line_label_char_positions = set()
    for node_label, root_position in nodes:
        node_label_char_positions = {
            root_position + Point(offset, 0)
            for offset, _ in enumerate(node_label)
        }
        if node_label.startswith("(") and node_label.endswith(")"):
            label_value = node_label[1:-1]
            line_labels[root_position] = label_value
            line_label_char_positions |= node_label_char_positions
        else:
            node_chars.update(
                (pos, node_label) for pos in node_label_char_positions
            )

    # we'll treat edge labels (e.g. "(my_label)") as consecutive "-" edge chars
    edge_chars = OrderedDict(
        (pos, (char if char in EDGE_CHARS else "-"))
        for pos, char in char_iter(network_string)
        if char in EDGE_CHARS or pos in line_label_char_positions
    )

    edge_char_to_edge_map = {}
    edges = []

    for pos, char in edge_chars.items():

        neighbors_in_edges = [
            pos+pos_offset
            for pos_offset in EDGE_CHAR_NEIGHBOURS[char]
            if pos+pos_offset in edge_char_to_edge_map
        ]  # assume for now these are all `-` characters

        if len(neighbors_in_edges) == 1:  # Add this node to the edge
            neighbor = neighbors_in_edges[0]
            edge_char_to_edge_map[pos] = edge_char_to_edge_map[neighbor]
            edge_char_to_edge_map[pos]["points"].append(pos)
        elif len(neighbors_in_edges) == 0:  # Make a new edge
            edge_char_to_edge_map[pos] = dict(points=[pos], nodes=[])
            edges.append(edge_char_to_edge_map[pos])
        else:
            raise BadEdgeException("Edge character '{}' at <{}> has too"
                                   "many neighbors.".format(char, pos))

        neighboring_nodes = [
            node_chars[pos+pos_offset]
            for pos_offset in EDGE_CHAR_NEIGHBOURS[char]
            if pos+pos_offset in node_chars
        ]
        edge_char_to_edge_map[pos]["nodes"] += neighboring_nodes

    ascii_graph = networkx.OrderedGraph()
    ascii_graph.add_nodes_from(
        (node, {"position": position})
        for node, position in nodes
        if position not in line_label_char_positions
    )
    ascii_graph.add_edges_from(
        tuple(edge["nodes"])
        for edge in edges if edge["nodes"]
    )
    networkx.set_edge_attributes(ascii_graph, name="length", values={
        tuple(edge["nodes"]): len(edge["points"])
        for edge in edges if edge["nodes"]
    })
    networkx.set_edge_attributes(
        ascii_graph, name="label",
        values={
            tuple(edge_char_to_edge_map[pos]["nodes"]): label
            for pos, label in line_labels.items()
        }
    )
    return ascii_graph


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __iter__(self):
        for el in (self.x, self.y):
            yield el

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        return (type(self) == type(other) and
                self.x == other.x and
                self.y == other.y
                )

    def __hash__(self):
        return hash((self.__class__, self.x, self.y))


def char_iter(network_string):
    return (
        (Point(col, row), char)
        for row, line in enumerate(network_string.split("\n"))
        for col, char in enumerate(line)
        )


def node_iter(network_string):
    for row, line in enumerate(network_string.split("\n")):
        for match in re.finditer('\(?([0-9A-Za-z_{}]+)\)?', line):
            yield (match.group(0), Point(match.start(), row))


class BadEdgeException(Exception):
    pass
