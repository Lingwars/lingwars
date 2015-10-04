#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.stem.snowball import SpanishStemmer

stemmer = SpanishStemmer()


class Word(object):

    def __init__(self, text, do_strip=True):
        self.text = text.strip()

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text

    @property
    def stem(self):
        if not hasattr(self, '_stem'):
            self._stem = stemmer.stem(self.text)
        return self._stem

    @property
    def lemma(self):
        if not hasattr(self, '_lemma'):
            raise NotImplementedError()
        return self._lemma