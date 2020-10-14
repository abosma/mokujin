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

shortcuts = {
    'cd' : 'fnddf',
    'wr' : 'fff',
    'hcf' : 'bdbddff',
    'hcb' : 'fdfddbb',
    'qcf' : 'ddff',
    'qcb' : 'ddbb'
}

def get_character(char_name):
    contents = None

    with open(misc_file) as char_misc_file:
        contents = char_misc_file.read()
        contents = json.loads(contents)

    if contents != None:
        char_details = filter_dictionary('name', char_name, contents)

        if char_details:
            return char_details
        else:
            names = dict_key_to_list('name', contents)

            guessed_char = difflib.get_close_matches(char_name, names, n=2, cutoff=0.4)

            if guessed_char:
                guessed_char = guessed_char[0]

                to_return_char = filter_dictionary('name', guessed_char, contents)

                if to_return_char:
                    return to_return_char
                else:
                    return None
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
        if char_move == "ra":
            to_return_move = filter_dictionary('Name', 'Rage Art', char_move_list)
            return to_return_move

        if char_move == "rd":
            to_return_move = filter_dictionary('Name', 'Rage Drive', char_move_list)
            return to_return_move

        char_move = replace_shortcuts(char_move)

        to_return_move = filter_dictionary('Command', char_move, char_move_list)

        if to_return_move:
            return to_return_move
        else:
            move_inputs = dict_key_to_list('Command', char_move_list)

            guessed_move = difflib.get_close_matches(char_move, move_inputs, n=2, cutoff=0.4)

            if guessed_move:
                guessed_move = guessed_move[0]

                to_return_move = filter_dictionary('Command', guessed_move, char_move_list)

                if to_return_move:
                    return to_return_move
                else:
                    return None
            else:
                return None

def filter_dictionary(to_compare_key, to_compare_value, dictionary):
    to_return_item = None
    value_split = to_compare_value.split(' ')

    # First check if move is equal to move list item, then if move is contained in move list item
    for item in dictionary:
        item_clean = item[to_compare_key].lower().strip().replace(' ', '')
        
        if len(value_split) == 1:
            value_clean = to_compare_value.lower().strip().replace(' ', '')

            if item_clean == value_clean:
                to_return_item = item
                break
        else:
            value_clean = [value.lower().strip().replace(' ','') for value in value_split]

            if all(value in item_clean for value in value_clean):
                to_return_item = item
                break

    if to_return_item != None:
        return to_return_item
    else:
        for item in dictionary:
            item_clean = item[to_compare_key].lower().strip().replace(' ', '')

            if len(value_split) == 1:
                value_clean = to_compare_value.lower().strip().replace(' ', '')

                if value_clean in item_clean:
                    to_return_item = item
                    break
            else:
                value_clean = [value.lower().strip().replace(' ','') for value in value_split]

                if all(value in item_clean for value in value_clean):
                    to_return_item = item
                    break
        
        return to_return_item

def replace_shortcuts(char_move):
    for key, item in shortcuts.items():
        if char_move == key or char_move.__contains__(key):
            return char_move.replace(key, item)
    return char_move

def dict_key_to_list(key, dictionary):
    to_return_list = []
    for item in dictionary:
        to_add_item = item[key].lower().strip().replace(' ', '')
        to_return_list.append(to_add_item)

    return to_return_list