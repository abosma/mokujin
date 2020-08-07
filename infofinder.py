#!/usr/bin/env python3
import os
import json
import collections
import re
import difflib
import embedhandler

cwd = os.getcwd()
misc_file = cwd + '/json/character_misc.json'

def get_character(char_name):
    contents = None

    with open(misc_file) as char_misc_file:
        contents = char_misc_file.read()
        contents = json.loads(contents)

    if contents != None:
        char_details = list(filter(lambda character: (character['name'] == char_name), contents))

        if char_details:
            return char_details[0]
        else:
            names = []
            list(filter(lambda character: names.append(character['name']), contents))
            guessed_char = difflib.get_close_matches(char_name, names, n=2, cutoff=0.6)
            
            if guessed_char:
                embed = embedhandler.guess_embed("Did you mean character: %s?" % guessed_char[0])
                return embed
            else:
                return None

    return None

def get_move(char_name, char_move):
    print("test")
