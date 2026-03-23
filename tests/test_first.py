# Tests para el calculo de FIRST

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from parser import parse_grammar, EPSILON
from first_follow import compute_first

GRAMMARS_DIR = os.path.join(os.path.dirname(__file__), 'grammars')


# Gramatica simple sin epsilon: S -> A B, A -> a, B -> b c
class TestFirstSimple(unittest.TestCase):

    def setUp(self):
        path = os.path.join(GRAMMARS_DIR, 'simple.txt')
        _, nts, terms, prods = parse_grammar(path)
        self.first = compute_first(nts, terms, prods, verbose=False)

    def test_first_A(self):
        self.assertEqual(self.first['A'], {'a'})

    def test_first_B(self):
        self.assertEqual(self.first['B'], {'b'})

    def test_first_S(self):
        self.assertEqual(self.first['S'], {'a'})


# Gramatica con epsilon: S -> A B, A -> a | ε, B -> b A
class TestFirstEpsilon(unittest.TestCase):

    def setUp(self):
        path = os.path.join(GRAMMARS_DIR, 'epsilon.txt')
        _, nts, terms, prods = parse_grammar(path)
        self.first = compute_first(nts, terms, prods, verbose=False)

    def test_first_A(self):
        self.assertEqual(self.first['A'], {'a', EPSILON})

    def test_first_B(self):
        self.assertEqual(self.first['B'], {'b'})

    def test_first_S(self):
        # A puede ser ε, asi que FIRST(S) incluye FIRST(B)
        self.assertEqual(self.first['S'], {'a', 'b'})


# Gramatica de expresiones con EP, TP
class TestFirstIndirect(unittest.TestCase):

    def setUp(self):
        path = os.path.join(GRAMMARS_DIR, 'indirect.txt')
        _, nts, terms, prods = parse_grammar(path)
        self.first = compute_first(nts, terms, prods, verbose=False)

    def test_first_F(self):
        self.assertEqual(self.first['F'], {'(', 'id'})

    def test_first_T(self):
        self.assertEqual(self.first['T'], {'(', 'id'})

    def test_first_TP(self):
        self.assertEqual(self.first['TP'], {'*', EPSILON})

    def test_first_E(self):
        self.assertEqual(self.first['E'], {'(', 'id'})

    def test_first_EP(self):
        self.assertEqual(self.first['EP'], {'+', EPSILON})


# Gramatica obligatoria del curso con notacion E', T'
class TestFirstCourse(unittest.TestCase):

    def setUp(self):
        path = os.path.join(GRAMMARS_DIR, 'course.txt')
        _, nts, terms, prods = parse_grammar(path)
        self.first = compute_first(nts, terms, prods, verbose=False)

    def test_first_E(self):
        self.assertEqual(self.first['E'], {'(', 'id'})

    def test_first_EP(self):
        self.assertEqual(self.first["E'"], {'+', EPSILON})

    def test_first_T(self):
        self.assertEqual(self.first['T'], {'(', 'id'})

    def test_first_TP(self):
        self.assertEqual(self.first["T'"], {'*', EPSILON})

    def test_first_F(self):
        self.assertEqual(self.first['F'], {'(', 'id'})


if __name__ == '__main__':
    unittest.main()
