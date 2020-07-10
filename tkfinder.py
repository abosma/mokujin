# -*- coding: utf-8 -*-
import os
import json
import collections

dirname = os.path.dirname(__file__)

def get_character(chara_name: str) -> dict:
    '''Gets character details from character_misc.json, if character exists
    returns character details as dict if exists, else None
    '''

    filepath = dirname + '/json/character_misc.json'
    with open(filepath) as chara_misc_file:
        contents = chara_misc_file.read()

    chara_misc_json = json.loads(contents)
    chara_details = list(filter(lambda x: (x['name'] == chara_name), chara_misc_json))

    if chara_details:
        return chara_details[0]
    else:
        return None

def get_move(character: dict, move_command: str) -> dict:
    '''Gets move from local_json, if exists
    returns move if exists, else None
    '''

    move_file_name = '/json/' + character.get('local_json')
    
    filepath = dirname + move_file_name
    
    with open(filepath, encoding="utf-8") as move_file:
        move_file_contents = move_file.read()
    
    move_json = json.loads(move_file_contents)

    move = get_move_by_input(move_command.lower(), move_json)

    return move

def get_move_by_input(move_input: str, move_json: json):
    move_strings = []
    moves = []

    for word in move_input.split():
        move_strings.append(word)

    for move in move_json:
        if all(move_simplifier(move_string) in move_simplifier(move['Command'].lower()) for move_string in move_strings):
            moves.append(move)
    
    if moves:
        move = list(filter(lambda x: (move_simplifier(x['Command'].lower()) == move_simplifier(move_input.lower())), move_json))
        
        if move:
            return move[0]
        else:
            return moves[0]
    else:
        return None

def get_by_move_type(character: dict, move_type: str) -> list:
    '''Gets a list of moves that match move_type from local_json
    returns a list of move Commands if finds match(es), else empty list'''

    move_file_name = '/json/' + character.get('local_json')
    filepath = dirname + move_file_name
    with open(filepath) as move_file:
        move_file_contents = move_file.read()
    move_json = json.loads(move_file_contents)

    moves = list(filter(lambda x: (move_type.lower() in x['Notes'].lower()), move_json))

    if moves:
        move_list = []
        for move in moves:
            move_list.append(move['Command'])
        return list(set(move_list))
    else:
        return []

def move_simplifier(move_input) -> str:
    '''Removes bells and whistles from the move_input'''

    move_replacements = {
        'fff': 'f,f,f',
        'ff': 'f,f',
        'bf': 'b,f',
        'fb': 'f,b',
        'ddf': 'd,df',
        'cd': 'f,n,d,df',
        'wr': 'f,f,f',
        'ewgf': 'f,n,d,df+2',
        '☆': 'n',
        'bdbddff': 'hcf',
        'fdfddbb': 'hcb',
        'ddff': 'qcf',
        'd, df, f': 'qcf',
        'd,df,f': 'qcf',
        'ddbb': 'qcb',
        'd, db, b': 'qcb',
        'd,db,b': 'qcb',
        '11': '1,1',
        '22': '2,2',
        '33': '3,3',
        '44': '4,4'
    }

    for move in move_replacements:
        if move in move_input:
            move_input = move_input.replace(move, move_replacements[move])

    move_input = move_input.replace(' ', '')
    move_input = move_input.replace('/', '')
    move_input = move_input.replace('+', '')

    return move_input
