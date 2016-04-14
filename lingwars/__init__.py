#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from apicultur.utils import ApiculturRateLimitSafe

def load_config():
    data = {}
    try:
        from secret import ACCESS_TOKEN_STORE, ACCESS_TOKEN_IO
        apicultur_store = ApiculturRateLimitSafe(ACCESS_TOKEN_STORE)
        apicultur_io = ApiculturRateLimitSafe(ACCESS_TOKEN_IO, cfg_data='apicultur.io')
        data['apicultur_store'] = apicultur_store
        data['apicultur_io'] = apicultur_io
    except ImportError:
        raise RuntimeError("Cannot load 'ACCESS_TOKEN_STORE', 'ACCESS_TOKEN_IO' from 'secret.py' file")
    return data


# Installing packages
import nltk
from .utils.install import pattern_wikicorpus


def download():
    # Create directory for data (and cache)
    lingwars_dir = os.path.join(os.path.expanduser("~"), 'lingwars')
    tmp_dir = os.path.join(lingwars_dir, 'tmp')
    if not os.path.exists(lingwars_dir):
        os.makedirs(lingwars_dir)
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    print("Installing NLTK")
    print("---------------")
    nltk.download('punkt')

    print("\nInstalling Pattern/Wikicorpus")
    print("-----------------------------")
    pattern_wikicorpus.install(lingwars_dir, tmp_dir)

config = load_config()
