#!/bin/bash

nc -l -u localhost 7355 | sox -t raw -esigned-integer -b16 -r 48000 - -esigned-integer -b16 -r 22050 -t raw - | multimon-ng -q -v 10 -t raw -A - | python aprs_parser.py

