import asciigraf.asciigraf


def node_iter(edge_label):
    """ This test module is only concerned with what labels are
        recognized, so we ignore the position yielded by
        asciigraf.asciigraf.node_iter """
    return [
        label
        for label, _ in asciigraf.asciigraf.node_iter(edge_label)
    ]


def test_supports_single_character_nodes():
    assert node_iter("---n--1---") == ["n", '1']


def test_supports_full_sentances():
    assert node_iter("""

            My Best friend Bart!-------My worst `friend` Sarah
              |
              |
              |
            What's his name, "Frank"?

    """) == [
        "My Best friend Bart!",
        "My worst `friend` Sarah",
        'What\'s his name, "Frank"?'
    ]


def test_supports_separators():
    assert node_iter("---n1:35---n2:35;41") == ["n1:35", "n2:35;41"]


def test_supports_decimal_numbers():
    assert node_iter("----3.141625----") == ["3.141625"]


def test_supports_empty_brackets():
    assert node_iter("-----}{---()---)(--[]---][--") == [
        "}{", "()", ")(", "[]", "][",
    ]


def test_minimum_gap_between_nodes():
    assert node_iter("n1  n2") == ["n1", "n2"]


def test_supports_parenthesis():
    assert node_iter(r"""

            ---[n1]---{n2}--}n3{--]n4[-\
                                       |
                      )n6(--(n5)------/
    """) == [
        "[n1]",
        "{n2}",
        "}n3{",
        "]n4[",
        ")n6(",
        "(n5)",
    ]
