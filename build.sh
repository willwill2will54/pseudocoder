#!/bin/zsh

tatsu ./grammar.tatsu > ./pseudocoder/tatsu_gen.py
tatsu ./grammar.tatsu -d --outfile image.jpg
python ./pseudocoder/tatsu_gen.py -c ./code.pseudo