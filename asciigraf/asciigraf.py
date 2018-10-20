#############################################################################
# Copyright (c) 2017-present, Opus One Energy Solutions Corporation
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#############################################################################

from collections import OrderedDict
import re

import networkx


def graph_from_ascii(network_string):
    """ Produces a networkx graph, based on an ascii drawing
        of a network
    """
    EDGE_CHAR_NEIGHBOURS = {  # first point in tuple is the point parsed first
        "-":  [Point(-1, 0), Point(1, 0)],
        "\\": [Point(-1, -1),  Point(1, 1)],
        "/":  [Point(1, -1), Point(-1, 1)],
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

    # First pass to put edge chars in the map
    edge_chars = OrderedDict(
        (pos, (char if char in EDGE_CHARS else "-"))
        for pos, char in char_iter(network_string)
        if char in EDGE_CHARS or pos in line_label_char_positions
    )

    # Second pass to correct vertical labels. This needs to be
    # a correction so that the OrderedDict is correctly setup
    for root_position, label in list(line_labels.items()):
        is_vertical_label = any(
            above in edge_chars and edge_chars[above] == '|'
            for above in (
                root_position + Point(i + 1, -1)
                for i, char in enumerate(label)
            )
        )

        if is_vertical_label:
            for i in range(len(label) + 2):  # + 2 for the parentheses
                pos = root_position + Point(i, 0)
                above = pos + Point(0, -1)

                try:
                    if edge_chars[above] == '|':
                        edge_chars[pos] = '|'
                        del line_labels[root_position]
                        line_labels[pos] = label
                    else:
                        del edge_chars[pos]
                except KeyError:
                    # pass
                    del edge_chars[pos]

    edge_char_to_edge_map = {}
    edges = []

    for pos, char in edge_chars.items():
        trailing_offset, leading_offset = EDGE_CHAR_NEIGHBOURS[char]
        neighbor = pos + trailing_offset
        neighbor_2 = pos + leading_offset

        # we can skip this position if a previous iteration already
        # mapped the character to an edge
        if pos not in edge_char_to_edge_map:
            if neighbor in edge_char_to_edge_map:  # Add this node to the edge
                edge_char_to_edge_map[pos] = edge_char_to_edge_map[neighbor]
                edge_char_to_edge_map[pos]["points"].append(pos)
            else:  # Make a new edge
                edge_char_to_edge_map[pos] = dict(points=[pos], nodes=[])
                edges.append(edge_char_to_edge_map[pos])

            # we can look ahead at other neighbor and add it too -- this
            # step allows us to solve a few extra corner types
            if (
                neighbor_2 not in edge_char_to_edge_map
                and neighbor_2 in edge_chars
            ):
                edge_char_to_edge_map[neighbor_2] = edge_char_to_edge_map[pos]
                edge_char_to_edge_map[pos]["points"].append(neighbor_2)

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
    for edge in edges:
        if len(edge['nodes']) > 2:
            raise TooManyNodesOnEdge(edge)
        elif len(edge['nodes']) < 2:
            raise TooFewNodesOnEdge(edge)
        else:
            ascii_graph.add_edge(*edge['nodes'])
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


class TooManyNodesOnEdge(Exception):
    def __init__(self, edge):
        super(TooManyNodesOnEdge, self).__init__(
            'Too many nodes ({}) found on edge starting at {!r}'.format(
                len(edge['nodes']), edge['points'][0]))


class TooFewNodesOnEdge(Exception):
    def __init__(self, edge):
        super(TooFewNodesOnEdge, self).__init__(
            'Too few nodes ({}) found on edge starting at {!r}'.format(
                len(edge['nodes']), edge['points'][0]))
