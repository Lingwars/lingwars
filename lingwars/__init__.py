#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import nltk
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

def download():
    nltk.download('punkt')

config = load_config()
