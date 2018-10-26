#############################################################################
# Copyright (c) 2017-present, Opus One Energy Solutions Corporation
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#############################################################################


class Point(object):

    def __setattr__(self, attr, val):
        raise TypeError("Can't set '{}' on Point object".format(attr))

    def __delattr__(self, attr):
        raise TypeError("Can't delete '{}' on Point object".format(attr))

    def __init__(self, x, y):
        super(Point, self).__setattr__('x', x)
        super(Point, self).__setattr__('y', y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

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

    def __lt__(self, other):
        """Point instances are ordered by row and
           then column.

           e.g. in the following diagram,
                        b
                   a----|

            if the points are ordered by position then we
            can expect this edge to always be (b, a)
            and not (a, b) based on reading the diagram like
            a paragraph, left-to-right and then top-to-bottom.
        """
        return self.y < other.y or (
            not self.y > other.y and
            self.x < other.x
        )

    def __hash__(self):
        return hash((self.__class__, self.x, self.y))
