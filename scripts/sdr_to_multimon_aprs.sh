#!/bin/sh

rtl_fm -f 144.390M -s 22050 - | multimon-ng -q -v 10 -t raw -A - | python aprs_parser.py
