#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from nltk.tokenize import sent_tokenize
from ..utils.file import guess_encoding
from .sentence import Sentence

class Text(object):

    def __init__(self, text=None, filename=None):
        assert bool(text) ^ bool(filename), "You can only provide 'filename' or 'text'"
        self.raw = text if text else self._read_filename(filename)

    def _read_filename(self, filename):
        if not isinstance(filename, str):
            filename, encoding = filename
        else:
            encoding = guess_encoding(filename)

        with open(filename, 'rb') as f:
            return f.read().decode(encoding)

    @property
    def sentences(self):
        if not hasattr(self, '_sentences'):
            self._sentences = [Sentence(it) for it in sent_tokenize(self.raw, language='spanish')]
        return self._sentences

    def count_words(self, filters = []):
        counter = Counter()
        for sentence in self.sentences:
            for word in sentence.words:
                if all(filter(word) for filter in filters):
                    counter[word.text] += 1
        return counter

    def count_stems(self, filters = []):
        counter = Counter()
        for sentence in self.sentences:
            for word in sentence.words:
                if all(filter(word) for filter in filters):
                    counter[word.stem] += 1
        return counter


if __name__ == '__main__':
    print("="*20)
    print("= lingwars.text.text")
    print("-"*20)
    data = """
Muchos años después, frente al pelotón de fusilamiento, el coronel Aureliano Buendía había de
recordar aquella tarde remota en que su padre lo llevó a conocer el hielo. Macondo era entonces
una aldea de veinte casas de barro y cañabrava construidas a la orilla de un río de aguas diáfanas
que se precipitaban por un lecho de piedras pulidas, blancas y enormes como huevos
prehistóricos. El mundo era tan reciente, que muchas cosas carecían de nombre, y para
mencionarlas había que señalarlas con el dedo.
"""
    text = Text(data)
    print("Sentences:")
    print('\n-----\n'.join([str(s) for s in text.sentences]))

    print("Count words:")
    cnt = text.count_words()
    print(cnt.most_common(3))

    print("Count words (filtering stop-words and punctuation):")
    from .word.filters import RemoveStopWords, RemovePunctuation
    filters = [RemoveStopWords(), RemovePunctuation()]
    cnt = text.count_words(filters)
    print(cnt.most_common(3))

    print("Count stems (filtering stop-words and punctuation):")
    from .word.filters import RemoveStopWords, RemovePunctuation
    filters = [RemoveStopWords(), RemovePunctuation()]
    cnt = text.count_stems(filters)
    print(cnt.most_common(3))

