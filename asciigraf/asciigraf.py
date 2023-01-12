#############################################################################
# Copyright (c) 2017-present, Opus One Energy Solutions Corporation
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#############################################################################

import re
import sys
from collections import OrderedDict
from itertools import chain
from typing import List, Tuple

import colorama
from colorama import Style, Fore
import networkx

from .point import Point

if sys.version_info >= (3, 7):
    networkx_Graph = networkx.Graph
else:
    networkx_Graph = networkx.OrderedGraph

LEFT, RIGHT = Point(-1, 0), Point(1, 0)
ABOVE, BELOW = Point(0, -1), Point(0, 1)
TOP_LEFT, BOTTOM_RIGHT = Point(-1, -1), Point(1, 1)
BOTTOM_LEFT, TOP_RIGHT = Point(1, -1), Point(-1, 1)


EDGE_CHARS = {"\\", "-", "/", "|"}
EDGE_CHAR_NEIGHBOURS = {  # first point in tuple is the point parsed first
    "-":  [LEFT, RIGHT],
    "\\": [TOP_LEFT, BOTTOM_RIGHT],
    "/":  [BOTTOM_LEFT, TOP_RIGHT],
    "|":  [ABOVE, BELOW]
}

ABUTTING = {
    TOP_LEFT:   "\\",  ABOVE: "|",    TOP_RIGHT: "/",
    LEFT:        "-",                     RIGHT: "-",
    BOTTOM_LEFT: "/",  BELOW: "|", BOTTOM_RIGHT: "\\",
}


def graph_from_ascii(network_string):
    """ Produces a networkx graph, based on an ascii drawing
        of a network
    """
    nodes, labels = get_nodes_and_labels(network_string)
    edges = get_edges(network_string, nodes, labels)
    return build_networkx_graph(nodes, edges)


def get_edges(network_string, nodes, labels):
    """ Traverses all adjacent edge characters to identify
        edges in the network.

        returns a set of dictionaries, each represeting an edge:
        {
            {
                "nodes": ("n1", "n2"),
                "points": [Point(), ...]
                "label": "(label_1)"  #
            },
            ...
        }

    """
    edge_chars = get_edge_chars(network_string)
    edge_chars = patch_edge_chars_over_labels(labels, edge_chars)

    node_chars = {}
    for root_pos, text in nodes.items():
        node_chars.update(char_map(text, root_pos))

    edge_char_to_neighbours = {}
    for pos in edge_chars.keys():
        neighbouring_positions = get_neighbours(pos, edge_chars, node_chars)

        # every edge char should end up with exactly 2 neighbours, or
        # we have a line that doesn't make sense. the neighbours could either
        # be an adjacent edge character or a character in a node label
        n_nodes = len(neighbouring_positions)
        if n_nodes != 2:
            error_map = highlight_bad_edge_characters(
                network_string, [pos, *neighbouring_positions]
            )
            raise InvalidEdgeError(
                "Too {} many neighbors at ln {}, col {}".format(
                    "many" if n_nodes > 2 else "few",
                    pos.y,
                    pos.x,
                )
                + "\n\n{}".format(error_map)
            )

        edge_char_to_neighbours[pos] = neighbouring_positions

    edges = []  # [{"points": [], "nodes": []},... ]
    edge_char_to_edge_map = {}  # {Point -> edge}

    node_char_to_node = map_text_chars_to_text(nodes)
    label_char_to_label = map_text_chars_to_text(labels)
    for pos, char in edge_chars.items():
        if pos in edge_char_to_edge_map:
            # We only expect to get past this continue for one char
            # in each edge -- if the above condition is false, we'll
            # process all the chars in the edge within one loop iteration
            continue

        new_edge = build_edge_from_position(
            pos, edge_char_to_neighbours, node_char_to_node
        )

        for position in new_edge['points']:
            edge_char_to_edge_map[position] = new_edge
            if position in label_char_to_label:
                new_edge["label"] = label_char_to_label[position]
        edges.append(new_edge)

    return edges


def build_networkx_graph(nodes, edges):
    # Build networkx datastructure
    ascii_graph = networkx_Graph()
    ascii_graph.add_nodes_from(
        (node, {"position": tuple(pos)}) for pos, node in nodes.items()
    )
    ascii_graph.add_edges_from(
        (edge['nodes'][0], edge['nodes'][1], {
            "length": len(edge["points"]),
            "points": [tuple(el) for el in edge["points"]]
        })
        for edge in edges
    )
    networkx.set_edge_attributes(
        ascii_graph, name="label",
        values={
            edge["nodes"]: edge["label"][1:-1]
            for edge in edges
            if "label" in edge
        }
    )
    return ascii_graph


def get_nodes_and_labels(network_string):
    """ Map the root position of nodes and labels
        to the node / label text.

        e.g. map_nodes_and_labels("  n1--(label1)--n2  ") -> {
            Point(2, 0): "n1",
            Point(6, 0): "(label1)",
            Point(16, 0): "n2",
        }
    """
    nodes = OrderedDict()  # of the form {Point -> 'node_name'}
    labels = OrderedDict()  # of the form {Point -> 'label'}
    for ascii_label, root_position in node_iter(network_string):
        if ascii_label.startswith("(") and ascii_label.endswith(")"):
            labels[root_position] = ascii_label
        else:
            nodes[root_position] = ascii_label
    return nodes, labels


def get_edge_chars(network_string):
    """ Map positions in the string to edge chars

        e.g. get_edge_chars("   --|   ") -> {
            Point(3,0): "-",
            Point(4,0): "-",
            Point(5,0): "|",
        }
    """
    return OrderedDict(
        (Point(col, row), char)
        for row, line in enumerate(network_string.split("\n"))
        for col, char in enumerate(line)
        if char in EDGE_CHARS
    )


def get_neighbours(pos, edge_chars, node_chars):
    """ Return the edge/node positions that neighbour the given position.

        e.g. let `pos` equal Point(2,2):
         ___
        |  /|
        | *-|    -> Point(3, 1), Point(3, 2) are neighbours
        |___|
         ___
        |  /|
        |-* |    -> Point(3, 1), Point(1, 2) are neighbours
        |___|
         ______
        |      |
        |--Node| -> Point(1, 2), Point(3, 2) are neighbours
        |______|
         ___
        |  -|
        |---|    -> Point(1, 2), Point(3, 2) are neighbours, Point(0,3) is not
        |___|

    """
    neighbouring_positions = set()

    # first, consider neighbours of our char (e.g. if our char
    # is '-' then any node or edge char to the left or right
    # is neighbouring to the char at `pos`)
    for offset in EDGE_CHAR_NEIGHBOURS[edge_chars[pos]]:
        neighbour = pos + offset
        if neighbour in edge_chars or neighbour in node_chars:
            neighbouring_positions |= {neighbour}

    # second, consider chars to which this char could be a neighbour
    # (e.g. if the char below is a |, our char neighbours it)
    for offset, valid_char in ABUTTING.items():
        if edge_chars.get(pos + offset) == valid_char:
            neighbouring_positions |= {pos + offset}

    return tuple(neighbouring_positions)


def build_edge_from_position(
        starting_char_position, neighbour_map, node_char_to_node):
    """ Given the position of any one character on an edge, traverses the
        neighbour_map to build an ordered list of all the points on the edge

        Arguments:
          * starting_char_position: The position from which to start traversing
                                    the edge.
          * neighbour_map: For each character in the network_string, contains
                           the positions of its two neighbours, which could
                           be characters in a node or other edge characters
          * node_char_to_node: a map of {node character position -> node}
                               {
                                    Point(0,0): "n1",
                                    Point(1,0): "n1",
                                    Point(2,2): "n2",
                                    Point(3,2): "n2",
                               }
    """
    def follow_edge(starting_position, neighbour):
        if neighbour in node_char_to_node:
            return (neighbour,)
        else:
            a, b = neighbour_map[neighbour]
            next_neighbour = a if b == starting_position else b
            return (neighbour, ) + follow_edge(neighbour, next_neighbour)

    neighbour_1, neighbour_2 = sorted(neighbour_map[starting_char_position])
    positions = list(chain(
        reversed(follow_edge(starting_char_position, neighbour_1)),
        (starting_char_position, ),
        follow_edge(starting_char_position, neighbour_2)
    ))

    if positions[0] > positions[-1]:
        positions = list(reversed(positions))

    new_edge = dict(
        points=positions[1:-1],
        nodes=(
            node_char_to_node[positions[0]],
            node_char_to_node[positions[-1]]
        ),
    )
    return new_edge


def patch_edge_chars_over_labels(labels, edge_chars):
    """ Adds in edge chars where labels crossed an edge

        e.g.

        ---(horizontal_label)---

                becomes

        ------------------------

        e.g.
                |                         |
          (vertical_label)   becomes      |
                |                         |
    """

    edge_chars = dict(edge_chars)  # so we don't mutate
    label_chars = OrderedDict(
        (root_position + Point(i, 0), char)
        for root_position, label in labels.items()
        for i, char in enumerate(label)
    )
    for position, label_character in label_chars.items():
        def neighbour(offset):
            return edge_chars.get(position + offset)

        if label_character == "(":
            if neighbour(LEFT) == "-":
                edge_chars[position] = "-"
        elif label_character == ")":
            if neighbour(RIGHT) == "-":
                edge_chars[position] = "-"
        elif neighbour(ABOVE) == "|" and neighbour(BELOW) == "|":
            edge_chars[position] = "|"
        else:
            # since we process each label left->right, we'll have already
            # patched characters to the left of our position during previous
            # iterations of the loop
            if neighbour(LEFT) == '-':
                edge_chars[position] = '-'

    return OrderedDict(sorted(edge_chars.items()))


def char_map(text, root_position):
    """ Maps the position of each character in 'text'

        e.g.

        char_map("foo", root_position=Point(20, 2)) -> {
            Point(20, 2) -> 'f',
            Point(21, 2) -> 'o',
            Point(22, 2) -> 'o',
        }
    """
    return OrderedDict(
        (Point(root_position.x+x, root_position.y), char)
        for x, char in enumerate(text)
    )


def map_text_chars_to_text(text_map):
    """ Maps characters in text elements to the text elements

        e.g.

        text_map = {
            Point(1, 2): 'foo',
            Point(3, 4):  'bar',
        }

        map_text_chars_to_text(text_map) -> {
            Point(1, 2): 'foo',
            Point(2, 2): 'foo',
            Point(3, 2): 'foo',
            Point(3, 4): 'bar',
            Point(4, 4): 'bar',
            Point(5, 4): 'bar',
        }
    """
    return OrderedDict(
        (position, text)
        for root_position, text in text_map.items()
        for position, _ in char_map(text, root_position).items()
    )


def node_iter(network_string):
    """ Yields the starting position and value of any nodes in
        the ascii network string

        e.g. node_iter("node1----(label1)") -> (
            (Point(0,0), node1), (Point(9,0), (label1))
        )
    """
    NODE_MATCH = re.compile(
        r'('
          r'[^ \-\\\/|]+[ ^ ]'  # any of non-edge chars, followed by  1 space # noqa
        r')*'  # as many of ^ as are repeated (including zero)
        r'([^ \\\/\-|]+)'  # ... followed by a group of non-edge characters
    )
    for row, line in enumerate(network_string.split("\n")):
        for match in NODE_MATCH.finditer(line):
            yield (match.group(0), Point(match.start(), row))


class InvalidEdgeError(Exception):
    """ Raise this when an edge is wrongly drawn """


class AnsiColours:
    PURPLE = "\033[35;1m"
    FAIL = "\033[91;1m"
    RESET = "\033[0m"


def highlight_bad_edge_characters(
    network_string: str, relevant_char_positions: List[Point]
) -> str:
    """Highlights all the characters specified in `relevant_char_positions`
    using ANSI colour codes"""
    try:
        colorama.init()
        lines = network_string.splitlines(keepends=True)

        quote_char = "\'" if "\"" in network_string else "\""
        quote_val = (
            3 * quote_char
            if len(network_string.splitlines()) > 1
            else quote_char
        )
        quotes = Style.DIM + quote_val + Style.RESET_ALL

        # first we calculate the index in `network_string` of each character
        # we want to highlight
        char_indexes = sorted(
            sum(len(el) for el in lines[0:char_pos.y])
            + char_pos.x  # depth into relevant line
            for char_pos in relevant_char_positions
        )

        # next we split apart `network_string` into consecutive segments that
        # surround the characters we are interested in
        #
        # e.g. given indexes for the stars in '----*====*----', we would get
        # ['----;, '====', '----' ]
        def keep_ranges(
            char_indexes: List[int], network_string: str
        ) -> List[Tuple[int, int]]:
            yield (0, char_indexes[0])
            for a, b in zip(char_indexes[:-1], char_indexes[1:]):
                yield (a + 1, b)
            yield (b + 1, len(network_string))

        segments = [
            network_string[start:end]
            for start, end in keep_ranges(char_indexes, network_string)
        ]

        # next, we extract just the characters we want to highlight
        replaced_characters = [
            network_string[char_index] for char_index in char_indexes
        ]

        # next, we wrap the target characters in ansi colours, and sandwich
        # them back in between the segments
        highlighted_segments = [
            (
                f"{preceeding_segment}"
                f"{Fore.RED + Style.BRIGHT}{char}{Style.RESET_ALL}"
            )
            for preceeding_segment, char in zip(
                segments[:-1], replaced_characters
            )
        ]
        error_text = (
            f"network_string = {quotes}"
            f"{''.join(highlighted_segments)}{segments[-1]}"
            f"{quotes}"
        )

        # here we resplit the text as lines, and do some cleanup formatting
        error_lines = ''.join(error_text).splitlines(keepends=True)
        if error_lines[-1].lstrip() == quotes:
            # this gets rid of the indent if the last line of `network_string`
            # is just indented closing quotes, i.e. the underscored part here:
            #
            #    def some_func():
            #        graph_from_ascii('''
            #
            #            all---ur---base
            #
            #    ____''')
            error_lines[-1] = error_lines[-1].lstrip()

        # lastly, we add a reset to each line in the map, to override anything
        # added by tools that try to add colouring to error outputs (e.g.
        # pytest)
        return (
            Style.RESET_ALL
            + Style.RESET_ALL.join(error_lines)
        )
    except Exception:
        # it'd be embarassing to fail while trying to describe why we failed
        return ""


def draw(edge_chars, nodes=None):
    """ Redraws a char_map and node_char map """
    nodes = nodes or {}
    node_start_map = OrderedDict()
    for position, node_label in nodes.items():
        if node_label not in node_start_map:
            node_start_map[node_label] = position
        else:
            if position < node_start_map[node_label]:
                node_start_map[node_label] = position

    all_chars = sorted(chain(
        ((val, key) for key, val in node_start_map.items()),
        edge_chars.items()),
        key=lambda x: x[0]
    )

    string = ""
    cursor = Point(0, 0)
    for position, label in all_chars:
        if cursor.y < position.y:
            string += '\n' * (position.y - cursor.y)
            cursor = Point(0, position.y+1)
        if cursor.x < position.x:
            string += ' ' * (position.x - cursor.x)
            cursor = position
        string += label
        cursor = Point(position.x + len(label), position.y)
    return string
