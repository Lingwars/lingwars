#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pattern.text import Parser, Lexicon

PAROLE = {
    "AO": "JJ"  ,   "I": "UH"  , "VAG": "VBG",
    "AQ": "JJ"  ,  "NC": "NN"  , "VAI": "MD",
    "CC": "CC"  , "NCS": "NN"  , "VAN": "MD",
    "CS": "IN"  , "NCP": "NNS" , "VAS": "MD",
    "DA": "DT"  ,  "NP": "NNP" , "VMG": "VBG",
    "DD": "DT"  ,  "P0": "PRP" , "VMI": "VB",
    "DI": "DT"  ,  "PD": "DT"  , "VMM": "VB",
    "DP": "PRP$",  "PI": "DT"  , "VMN": "VB",
    "DT": "DT"  ,  "PP": "PRP" , "VMP": "VBN",
    "Fa": "."   ,  "PR": "WP$" , "VMS": "VB",
    "Fc": ","   ,  "PT": "WP$" , "VSG": "VBG",
    "Fd": ":"   ,  "PX": "PRP$", "VSI": "VB",
    "Fe": "\""  ,  "RG": "RB"  , "VSN": "VB",
    "Fg": "."   ,  "RN": "RB"  , "VSP": "VBN",
    "Fh": "."   ,  "SP": "IN"  , "VSS": "VB",
    "Fi": "."   ,                  "W": "NN",
    "Fp": "."   ,                  "Z": "CD",
    "Fr": "."   ,                 "Zd": "CD",
    "Fs": "."   ,                 "Zm": "CD",
   "Fpa": "("   ,                 "Zp": "CD",
   "Fpt": ")"   ,
    "Fx": "."   ,
    "Fz": "."
}

def parole2penntreebank(token, tag):
    return token, PAROLE.get(tag, tag)

class SpanishParser(Parser):

    def find_tags(self, tokens, **kwargs):
        # Parser.find_tags() can take an optional map(token, tag) function,
        # which returns an updated (token, tag)-tuple for each token.
        kwargs.setdefault("map", parole2penntreebank)
        return Parser.find_tags(self, tokens, **kwargs)

def build_parser(brill_dir):
    lexicon = Lexicon(
            path = os.path.join(brill_dir, "es-lexicon.txt"),
      morphology = os.path.join(brill_dir, "es-morphology.txt"),
         context = os.path.join(brill_dir, "es-context.txt"),
        language = "es"
    )

    parser = SpanishParser(
         lexicon = lexicon,
         default = ("NCS", "NP", "Z"),
        language = "es"
    )
    return parser