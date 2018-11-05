asciigraf
=========

.. image:: https://travis-ci.org/opusonesolutions/asciigraf.svg?branch=master
    :target: https://travis-ci.org/opusonesolutions/asciigraf

.. image:: https://coveralls.io/repos/github/opusonesolutions/asciigraf/badge.svg?branch=master
    :target: https://coveralls.io/github/opusonesolutions/asciigraf?branch=master

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT

.. image:: https://badge.fury.io/py/asciigraf.svg
    :target: https://pypi.python.org/pypi/asciigraf

.. image:: https://img.shields.io/pypi/pyversions/asciigraf.svg
    :target: https://pypi.python.org/pypi/asciigraf

.. image:: https://api.codeclimate.com/v1/badges/e7e872f6832da6cf6ab6/maintainability
   :target: https://codeclimate.com/github/opusonesolutions/asciigraf/maintainability
   :alt: Maintainability

Asciigraf is a python library that turns ascii diagrams of networks into
network objects. It returns a `networkx <https://networkx.github.io/>`__
graph of nodes for each alpha-numeric element in the input text; nodes
are connected in the graph to match the edges represented in the diagram
by ``-``, ``/``, ``\`` and ``|``.

Installation
------------

Asciigraf can be installed from pypi using pip:

.. code::

    ~/$ pip install asciigraf

Usage
-----

Asciigraf expects a string containg a 2-d ascii diagram. Nodes can be an
alphanumeric string composed of characters in ``A-Z``, ``a-z``, ``0-9``,
and ``_, {, }``. Edges can be composed of ``-``, ``/``, ``\`` and ``|``.

.. code:: python


    import asciigraf

    network = asciigraf.graph_from_ascii("""
              NodeA-----
                       |
                       |---NodeB
                                         """)

    print(network)
    >>> <networkx.classes.graph.Graph at 0x7f24c3a8b470>

    print(network.edges())
    >>> [('NodeA', 'NodeB')]

    print(network.nodes())
    >>> ['NodeA', 'NodeB']


Networkx provides tools to attach data to nodes and edges, and asciigraf
leverages these in a number of ways; in the example below you can see that
asciigraf uses this to attach a ``x, y`` position tuple to each node
indicating where on the *(x, y)* plane each node
starts ( *0,0* is at the top-left). It also attaches a ``length`` attribute
to each edge which matches the number of characters in that edge, as well
as a list of positions for each character an edge

.. code:: python

    print(network.nodes(data=True))
    >>> [('NodeA', {'position': (10, 1)}), ('NodeB', {'position': (23, 3)})]

    print(network.edges(data=True))
    >>> [('NodeA', 'NodeB', OrderedDict([('length', 10), 'points', [...]))]
    
    print(network.edge['NodeA']['NodeB']['points'])
    >>> [(15, 1), (16, 1), (17, 1), (18, 1),
         (19, 1), (19, 2), (19, 3), (20, 3), (21, 3), (22, 3)]


Asciigraf also lets you annotate the edges of graphs using in-line labels ---
denoted by parentheses. The contents of the label will be attached to the edge
on which it is drawn with the attribute name ``label``.

.. code:: python

    network = asciigraf.graph_from_ascii("""

        A---(nuts)----B----(string)---C
                      |
                      |
                      |
                      D---(string)----E

    """)

    print(network.get_edge_data("A", "B")["label"])
    >>> nuts

    print(network.get_edge_data("B", "C")["label"])
    >>> string

    print(network.get_edge_data("D", "E")["label"])
    >>> string

    print(hasattr(network.get_edge_data("B", "D"), "label"))
    >>> False


Have fun!

.. code:: python

    import asciigraf


    network = asciigraf.graph_from_ascii("""
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
