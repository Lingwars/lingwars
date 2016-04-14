#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.stem.snowball import SpanishStemmer
from apicultur.utils import ApiculturRateLimitSafe
from lingwars import config
from lingwars.utils.eagles import create_from_code

apicultur_store = config.get('apicultur_store')

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
        raise RuntimeError("Non desambiguated words may have more than one lemma")

    """
    def get_lemmas(self):
        if not hasattr(self, '_lemmas'):
            r = apicultur_store.lematiza2(word=self.text)
            assert r['palabra'] == self.text
            self._lemmas = [(lema['lema'], create_from_code(lema['categoria'])) for lema in r['lemas']]
        return self._lemmas
    """