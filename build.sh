#!/bin/sh
py scrape.py && py process.py && py model.py
