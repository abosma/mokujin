#!/usr/bin/env python3
import os
import json
import collections
import re
import difflib
import embedhandler
import random

cwd = os.getcwd()
misc_file = cwd + '/json/character_misc.json'

def get_character(char_name):
    contents = None

    with open(misc_file) as char_misc_file:
        contents = char_misc_file.read()
        contents = json.loads(contents)

    if contents != None:
        #TODO put filter into function to reduce copy paste code
        char_details = list(filter(lambda character: (character['name'] == char_name) or (character['name'].__contains__(char_name)), contents))

        if char_details:
            return char_details[0]
        else:
            names = []
            list(filter(lambda character: names.append(character['name']), contents))

            guessed_char = difflib.get_close_matches(char_name, names, n=2, cutoff=0.6)
            guessed_char = random.choice(guessed_char)

            to_return_char = list(filter(lambda character: (character['name'] == guessed_char) or (character['name'].__contains__(char_name)), contents))

            if to_return_char:
                return to_return_char[0]
            else:
                return None

    return None

def get_move(character_json, char_move):
    char_move_list = None
    char_json = cwd + '/json/' + character_json
    
    with open(char_json, 'r', encoding="utf8") as char_json_file:
        char_move_list = char_json_file.read()
        char_move_list = json.loads(char_move_list)

    if char_move_list != None:
        to_return_move = list(filter(lambda move: (move['Command'] == char_move) or (move['Command'].__contains__(char_move)), char_move_list))

        if to_return_move:
            return to_return_move[0]
        else:
            move_inputs = []
            list(filter(lambda move: move_inputs.append(move['Command']), char_move_list))

            guessed_move = difflib.get_close_matches(char_move, move_inputs, n=2, cutoff=0.6)
            guessed_move = random.choice(guessed_move)

            to_return_move = list(filter(lambda move: (move['Command'] == guessed_move) or (move['Command'].__contains__(guessed_move)), char_move_list))

            if to_return_move:
                return to_return_move[0]
            else:
                return None
