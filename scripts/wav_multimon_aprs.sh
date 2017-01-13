#!/bin/sh

sox -t wav $1 -esigned-integer -b16 -r 22050 -t raw - | multimon-ng -v 10 -t raw -A -
