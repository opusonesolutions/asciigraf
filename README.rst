asciigraf
=========

.. image:: https://travis-ci.org/AnjoMan/asciigraf.svg?branch=master
    :target: https://travis-ci.org/AnjoMan/asciigraf

.. image:: https://coveralls.io/repos/github/AnjoMan/asciigraf/badge.svg?branch=master
    :target: https://coveralls.io/github/AnjoMan/asciigraf?branch=master

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT

.. image:: https://badge.fury.io/py/asciigraf.svg
    :target: https://pypi.python.org/pypi/asciigraf

.. image:: https://img.shields.io/pypi/pyversions/asciigraf.svg
    :target: https://pypi.python.org/pypi/asciigraf

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
and ``_, {, }``. Edges can be composed of ``-``, ``/``, ``\`` and ``|``
(with some restrictions on how corners work --- see the tests).

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

    print(network.nodes(data=True))
    >>> [('NodeA', {'position': Point(1, 10)}), ('NodeB', {'position': Point(3, 23)})]

Networkx provides tools to attach data to nodes and edges; in the above
example you can see that asciigraf uses this to attach a ``Point``
object to each node indicating where on the *(x, y)* plane each node
starts ( *0,0* is at the top-left).

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
