#!/bin/sh

arecord -f S16_LE -c 1 -r 48000 -D hw:CARD=Device,DEV=0 - |sox -t raw -esigned-integer -b16 -r 48000 - -esigned-integer -b16 -r 22050 -t raw - | multimon-ng -q -a EAS -t raw  - i

#| python aprs_parser.py
