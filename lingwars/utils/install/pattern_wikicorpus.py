#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
## Using Wikicorpus & NLTK to build a Spanish part-of speech tagger
http://www.clips.ua.ac.be/pages/using-wikicorpus-nltk-to-build-a-spanish-part-of-speech-tagger

Upgrade with changes in NLTK3 as stated here:
    http://streamhacker.com/2014/12/02/nltk-3/
    http://stackoverflow.com/questions/30323409/python-nltk-brill-tagger-does-not-have-symmetricproximatetokenstemplate-proxima
"""

import os
from glob import glob
from codecs import open, BOM_UTF8
from collections import defaultdict

from nltk.tag import UnigramTagger
from nltk.tag.brill_trainer import BrillTaggerTrainer

from nltk.tag.brill import fntbl37

"""
from nltk.tag.brill import SymmetricProximateTokensTemplate
from nltk.tag.brill import ProximateTokensTemplate
from nltk.tag.brill import ProximateTagsRule
from nltk.tag.brill import ProximateWordsRule
"""
from .utils import download, extract


def install(dirname = os.path.join(os.path.expanduser("~"), 'lingwars'), tmp_dir=None):
    # TODO: Check if it is already downloaded and extracted

    tmp_dir = tmp_dir or os.path.join(dirname, 'tmp')
    wikicorpus_dir = os.path.join(dirname, 'wikicorpus')
    print("Installing Wikicorpus")
    download_wikicorpus(wikicorpus_dir, tmp_dir)

    brill_dir = os.path.join(dirname, 'brill')
    if not os.path.exists(brill_dir):
        os.makedirs(brill_dir)

    print("Extracting a lexicon of known words")
    lexicon_file = os.path.join(brill_dir, 'es-lexicon.txt')
    if (not os.path.isfile(lexicon_file)) or os.stat(lexicon_file).st_size == 0:
        build_lexicon(wikicorpus_dir, lexicon_file)

    print("Extracting contextual rules with NLTK")
    context_file = os.path.join(brill_dir, 'es-context.txt')
    if (not os.path.isfile(context_file)) or os.stat(context_file).st_size == 0:
        contextual_rules(wikicorpus_dir, context_file)

    print("Rules for unknown words based on word suffixes")
    morpho_file = os.path.join(brill_dir, 'es-morphology.txt')
    if (not os.path.isfile(morpho_file)) or os.stat(morpho_file).st_size == 0:
        unknown_words(wikicorpus_dir, morpho_file)


def download_wikicorpus(wikicorpus_dir, tmp_dir):
    # Check if it is already downloaded and extracted
    # TODO: This check is a little bit naïve
    if os.path.exists(wikicorpus_dir):
        return

    # Download to tmp file
    url = 'http://www.cs.upc.edu/~nlp/wikicorpus/tagged.es.tgz'
    local_filename = os.path.join(tmp_dir, 'wikicorpus_' + url.split('/')[-1])
    if os.path.exists(local_filename):
        print("Wikicorpus tagged.es.tgz is already on the system.")
    else:
        download(url, local_filename)

    # Extract
    print("Extracting Wikicorpus files to %s" % wikicorpus_dir)
    extract(local_filename, wikicorpus_dir)
    return wikicorpus_dir


def wikicorpus(wikicorpus_dir, words=1000000, start=0):
    s = [[]]
    i = 0
    for f in glob(os.path.join(wikicorpus_dir, "*"))[start:]:
        for line in open(f, encoding="latin-1"):
            if line == "\n" or line.startswith((
              "<doc", "</doc>", "ENDOFARTICLE", "REDIRECT",
              "Acontecimientos",
              "Fallecimientos",
              "Nacimientos")):
                continue
            w, lemma, tag, x = line.split(" ")
            if tag.startswith("Fp"):
                tag = tag[:3]
            elif tag.startswith("V"):  # VMIP3P0 => VMI
                tag = tag[:3]
            elif tag.startswith("NC"): # NCMS000 => NCS
                tag = tag[:2] + tag[3]
            else:
                tag = tag[:2]
            for w in w.split("_"): # Puerto_Rico
                s[-1].append((w, tag)); i+=1
            if tag == "Fp" and w == ".":
                s.append([])
            if i >= words:
                return s[:-1]


def build_lexicon(wikicorpus_dir, lexicon_file):
    # "el" => {"DA": 3741, "NP": 243, "CS": 13, "RG": 7})
    lexicon = defaultdict(lambda: defaultdict(int))

    for sentence in wikicorpus(wikicorpus_dir, 1000000):
        for w, tag in sentence:
            lexicon[w][tag] += 1

    top = []
    for w, tags in lexicon.items():
        freq = sum(tags.values())      # 3741 + 243 + ...
        tag  = max(tags, key=tags.get) # DA
        top.append((freq, w, tag))

    top = sorted(top, reverse=True)[:100000] # top 100,000
    top = ["%s %s" % (w, tag) for freq, w, tag in top if w]

    open(lexicon_file, "w").write("\n".join(top))


def contextual_rules(wikicorpus_dir, context_file):
    sentences = wikicorpus(wikicorpus_dir, words=1000000)

    ANONYMOUS = "anonymous"
    for s in sentences:
        for i, (w, tag) in enumerate(s):
            if tag == "NP": # NP = proper noun in Parole tagset.
                s[i] = (ANONYMOUS, "NP")

    ctx = fntbl37()

    tagger = UnigramTagger(sentences)
    tagger = BrillTaggerTrainer(tagger, ctx, trace=0)
    tagger = tagger.train(sentences, max_rules=100)

    #print tagger.evaluate(wikicorpus(10000, start=1))

    with open(context_file, "w") as f:
        for rule in tagger.rules():
            f.write("%s\n" % rule)


def unknown_words(wikicorpus_dir, morpho_file):
    # {"mente": {"RG": 4860, "SP": 8, "VMS": 7}}
    suffix = defaultdict(lambda: defaultdict(int))

    for sentence in wikicorpus(wikicorpus_dir, 1000000):
        for w, tag in sentence:
            x = w[-5:] # Last 5 characters.
            if len(x) < len(w) and tag != "NP":
                suffix[x][tag] += 1

    top = []
    for x, tags in suffix.items():
        tag = max(tags, key=tags.get) # RG
        f1  = sum(tags.values())      # 4860 + 8 + 7
        f2  = tags[tag] / float(f1)   # 4860 / 4875
        top.append((f1, f2, x, tag))

    top = sorted(top, reverse=True)
    top = list(filter(lambda item: item[0] >= 10 and item[1] > 0.8, top))
    top = list(filter(lambda item: item[3] != "NCS", top))
    top = top[:100]
    top = ["%s %s fhassuf %s %s" % ("NCS", x, len(x), tag) for f1, f2, x, tag in top]

    open(morpho_file, "w").write("\n".join(top))