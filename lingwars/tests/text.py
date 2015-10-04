#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from ..text.text import Text

me = os.path.dirname(__file__)

class TestText(unittest.TestCase):
    def setUp(self):
        self.raw = "Muchos años después, frente al pelotón de fusilamiento, el coronel Aureliano..."
        self.utf8_file =os.path.join(me, 'data/file_utf8.txt')
        self.us_ascii_file = os.path.join(me, 'data/file_us-ascii.txt')
        self.iso_8859_1_file = os.path.join(me, 'data/file_iso-8859-1.txt')

    def test_raw(self):
        text = Text(text=self.raw)
        self.assertEqual(text.raw, self.raw)

    def test_def_file(self):
        text = Text(filename=self.utf8_file)
        self.assertEqual(text.raw, self.raw)

    def test_utf8_file(self):
        text = Text(filename=(self.utf8_file, 'utf-8'))
        self.assertEqual(text.raw, self.raw)

    def test_us_ascii_file(self):
        text = Text(filename=(self.us_ascii_file, 'US-ASCII'))
        self.assertEqual(text.raw, self.raw)

    def test_iso_8859_1_file(self):
        text = Text(filename=(self.iso_8859_1_file, 'iso-8859-1'))
        self.assertEqual(text.raw, self.raw)

if __name__ == '__main__':
    unittest.main()