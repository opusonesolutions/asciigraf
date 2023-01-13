#############################################################################
# Copyright (c) 2017-present, Opus One Energy Solutions Corporation
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#############################################################################

from .asciigraf import graph_from_ascii # noqa F401


def get_version():
    import sys

    # TODO: if 3.8 support is dropped, we can standardize on
    # importlib.resources.files
    if sys.version_info < (3, 9):
        from importlib.resources import read_text

        return read_text(__name__, "VERSION").strip()
    else:
        from importlib.resources import files

        return files(__name__).joinpath("VERSION").open("r").read().strip()


__version__ = get_version()
