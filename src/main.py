#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
from config import Configuration
from bot import Bot

if __name__ == "__main__":
    cfg = Configuration('config.json')
    bot = Bot(cfg)
    bot.connect()
