#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from . import Word
from ..sentence import SentenceWord
from ...utils.eagles import create_from_code, EaglesCode

root = os.path.dirname(__file__)

stop_words_filename = os.path.join(root, '../../data/stop_words.txt')


class BaseFilter(object):
    def __call__(self, word):
        assert isinstance(word, Word)
        return self.filter_pass(word)


class RemoveFromList(BaseFilter):
    filtered = None

    def __init__(self):
        if not self.filtered:
            self.filtered = self.get_filter_list()

    def get_filter_list(self):
        raise "Provide a 'filtered' list attribute or implement 'get_filter_list'"

    def filter_pass(self, word):
        return word.text not in self.filtered


class RemoveStopWords(RemoveFromList):
    def __init__(self, filename=stop_words_filename):
        self.filename = filename
        super(RemoveStopWords, self).__init__()

    def get_filter_list(self):
        return set(self._read_filename(self.filename))

    def _read_filename(self, filename):
        with open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                if not line.startswith("#"):
                    yield line.strip()


class RemovePunctuation(RemoveFromList):
    filtered = ['.', ',',]


class RemoveByEAGLES(BaseFilter):
    def __init__(self, codes):
        self.eagles = [create_from_code(code) for code in codes]

    def __call__(self, word):
        assert isinstance(word, SentenceWord)
        return not any([EaglesCode.match(word.eagles.code, it.code)>0 for it in self.eagles])
