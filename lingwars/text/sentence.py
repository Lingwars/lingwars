#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.tokenize import word_tokenize
from .word import Word

class Sentence(object):

    def __init__(self, text, remove_newlines=True):
        self.text = text.replace('\n', ' ').replace('\r', ' ').replace('  ', ' ').strip()

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text

    @property
    def words(self):
        if not hasattr(self, '_words'):
            self._words = [Word(it) for it in word_tokenize(self.text, language='spanish')]
        return self._words


if __name__ == '__main__':
    print("="*20)
    print("= lingwars.text.sentence")
    print("-"*20)
    data = """
Muchos años después, frente al pelotón de fusilamiento, el coronel Aureliano Buendía había de
recordar aquella tarde remota en que su padre lo llevó a conocer el hielo.
"""
    sentence = Sentence(data)
    print("Words:")
    print('\n'.join([str(w) for w in sentence.words]))

    from .word.filters import RemoveStopWords, RemovePunctuation
    print("Apply filters: stop-words and punctuation")
    filters = [RemoveStopWords(), RemovePunctuation()]
    for word in sentence.words:
        if all(filter(word) for filter in filters):
            print(word)
