#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Códigos EAGLES, +info: http://nlp.lsi.upc.edu/freeling/doc/tagsets/tagset-es.html


class EaglesCode(object):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return self.code

    def __repr__(self):
        return self.code

    @classmethod
    def match(cls, lhs, rhs):
        i = 0
        length = min(len(lhs), len(rhs))
        while i<length and lhs[i] == rhs[i]:
            i += 1
        return i

# TODO: Create class hierarchy, and useful methods for each class


def create_from_code(code):
    # TODO: Build proper EAGLE class
    return EaglesCode(code)

"""
ADJETIVOS
ADVERBIOS
DETERMINANTES
NOMBRES
VERBOS
PRONOMBRES
CONJUNCIONES
INTERJECCIONES
PREPOSICIONES
PUNTUACIÓN
NUMERALES
FECHAS Y HORAS
"""