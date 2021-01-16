#!/usr/bin/env python3
import os
import json

cwd = os.getcwd()
alias_file = cwd + '/json/character_alias.json'

def add_alias(*args):
    character_alias = args[0]
    character_name = character_alias[0]
    to_add_alias = character_alias[1]
    character_aliases = []
    
    with open(alias_file, 'r') as characterAliases:
        character_aliases = json.load(characterAliases)

    for alias in character_aliases:
        if alias['name'] == character_name:
            if to_add_alias not in alias['alias']:
                alias['alias'].append(to_add_alias)
                break

    with open(alias_file, 'w') as characterAliases:
        json.dump(character_aliases, characterAliases, indent=4)

    return True

def remove_alias(*args):
    character_alias = args[0]
    to_remove_alias = character_alias[0]
    character_name = character_alias[1]
    character_aliases = []
    
    with open(alias_file, 'r') as characterAliases:
        character_aliases = json.load(characterAliases)

    for alias in character_aliases:
        if alias['name'] == character_name:
            if to_remove_alias in alias['alias']:
                alias['alias'].remove(to_remove_alias)
                break

    with open(alias_file, 'w') as characterAliases:
        json.dump(character_aliases, characterAliases, indent=4)

    return True

def get_alias(potential_alias):
    char_name = None

    character_aliases = []
    with open(alias_file, 'r') as characterAliases:
        character_aliases = json.load(characterAliases)

    char_alias = list(filter(lambda character: (potential_alias == character['alias']) or (potential_alias in character['alias']), character_aliases))
    if char_alias:
        char_name = char_alias[0]['name']

    return char_name