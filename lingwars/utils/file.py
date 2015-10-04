#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import cchardet as chardet
except ImportError:
    import chardet


def guess_encoding(filename_or_bytes):
    if isinstance(filename_or_bytes, bytes):
        result = chardet.detect(filename_or_bytes)
        return result['encoding']
    else:
        # TODO: Use UniversalDetector to detect encoding incrementally (for large files)
        # http://chardet.readthedocs.org/en/latest/usage.html#example-using-the-detect-function
        with open(filename_or_bytes, 'rb') as f:
            return guess_encoding(f.read())
