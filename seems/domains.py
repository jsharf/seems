"""A list of default test domains."""
import numpy
from typing import List

INTEGERS = range(-10, 10)
FLOATS = [float(i) for i in INTEGERS] + [float(i) / 10 for i in INTEGERS]
STRINGS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
JSON_STRINGS = ['{"a": 1}', '{"b": 2}', '{"c": 3}', '{"d": 4}', '{"e": 5}']
VECTORS = [numpy.array([i, i + 1, i + 2]) for i in INTEGERS]
UNIT_VECTORS = [v / numpy.linalg.norm(v) for v in VECTORS]
MATRICES = [numpy.array([[i, i + 1, i + 2], [i + 3, i + 4, i + 5]]) for i in INTEGERS]
UNIT_MATRICES = [m / numpy.linalg.norm(m) for m in MATRICES]