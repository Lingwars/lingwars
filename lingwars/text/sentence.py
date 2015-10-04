#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.tokenize import word_tokenize
from .word import Word
from lingwars import config
from lingwars.utils.eagles import create_from_code, EaglesCode

apicultur_store = config.get('apicultur_store')


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
            self._words = [Word(w) for w in word_tokenize(self.text, language='spanish')]
        return self._words

    @property
    def pos_words(self):
        if not hasattr(self, '_pos_words'):
            r = apicultur_store.etiqueta(texto=self.text)
            self._pos_words = []
            for tag in r:
                assert len(tag['lemas'])==1
                w = SentenceWord(tag['palabra'], self)
                w.eagles = create_from_code(tag['lemas'][0]['categoria'])

                if w.eagles.code[0] in ['V', 'N', 'A',]:
                    # La llamada a apicultur.etiqueta siempre devuelve una categoría válida,
                    # aunque la palabra no exista; así que no puedo creerme su lema.
                    lemas = apicultur_store.lematiza2(word=w.text)
                    w._lemma = SentenceWord.unknown_lemma
                    if lemas:
                        matches = [EaglesCode.match(w.eagles.code, it['categoria']) for it in lemas['lemas']]
                        if max(matches) > 0:
                            idx = matches.index(max(matches))
                            w._lemma = lemas['lemas'][idx]['lema']
                else:
                    w._lemma = tag['lemas'][0]['lema']
                self._pos_words.append(w)
        return self._pos_words

    """
    def pos_tagger(self):
        r = apicultur_store.etiqueta(texto=self.text)
        for tag, word in zip(r, self.words):
            assert len(tag['lemas'])==1
            word.eagles = create_from_code(tag['lemas'][0]['categoria'])
            word._lemma = tag['lemas'][0]['lema']
    """

class SentenceWord(Word):
    """
        A word inside a sentence
    """
    unknown_lemma = object()
    eagles = None

    def __init__(self, text, sentence, *args, **kwargs):
        super(SentenceWord, self).__init__(text, *args, **kwargs)
        self.sentence = sentence
        #self.index = index

    def __str__(self):
        return "%s/%s" % (self.text, self.eagles)

    def __repr__(self):
        return "%s/%s" % (self.text, self.eagles)

    def print(self, fmt=None):
        fmt = fmt or "%12s|%8s\t%s"
        print(fmt % (self.text, self.eagles, self.lemma if self.lemma != SentenceWord.unknown_lemma else '-'))

    @property
    def lemma(self):
        if not hasattr(self, '_lemma'):
            raise RuntimeError("Invoke sentence.pos_tagger before")
        return self._lemma



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
            print("%d - %s" % (word.index, word.text))
