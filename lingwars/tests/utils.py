#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from ..utils.file import guess_encoding

me = os.path.dirname(__file__)

class TestText(unittest.TestCase):
    def setUp(self):
        self.utf8_file =os.path.join(me, 'data/file_utf8.txt')
        self.us_ascii_file = os.path.join(me, 'data/file_us-ascii.txt')
        self.iso_8859_1_file = os.path.join(me, 'data/file_iso-8859-1.txt')

    def test_guess_encoding(self):
        self.assertEqual(guess_encoding(self.utf8_file), 'utf-8')
        self.assertEqual(guess_encoding(self.us_ascii_file), 'us-ascii-file')
        self.assertEqual(guess_encoding(self.iso_8859_1_file), 'iso-8859-1')


if __name__ == '__main__':
    unittest.main()