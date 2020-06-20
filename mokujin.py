#!/usr/bin/env python3
import os, sys
import datetime
import asyncio
import json

import discord
from discord.ext import commands

import tkfinder
import config

prefix = config.EXTRA_DATA['prefix']
description = config.EXTRA_DATA['description']

bot = commands.Bot(command_prefix=prefix, description=description)

# Dict for searching special move types
move_types = {  'ra': 'Rage art',
                'rage_art': 'Rage art',
                'rd': 'Rage drive',
                'rage_drive': 'Rage drive',
                'wb': 'Wall bounce',
                'wall_bounce': 'Wall bounce',
                'ts': 'Tail spin',
                'tail_spin': 'Tail spin',
                'screw': 'Tail spin',
                'homing': 'Homing',
                'homari': 'Homing',
                'armor': 'Power crush',
                'armori': 'Power crush',
                'pc': 'Power crush',
                'power': 'Power crush',
                'power_crush': 'Power crush'}

token = os.environ.get('BOT_TOKEN')
dirname = os.getcwd()

def move_embed(character, move):
    '''Returns the embed message for character and move'''
    embed = discord.Embed(title=character['proper_name'],
            colour=0x00EAFF,
            url=character['online_webpage'],
            description='Move: ' + move['Command'])

    embed.set_thumbnail(url=character['portrait'])
    embed.add_field(name='Name', value=move['Name'] + "\n\u200b")
    embed.add_field(name='Property', value=move['Property'] + "\n\u200b")
    embed.add_field(name='Damage', value=move['Damage'] + "\n\u200b")
    embed.add_field(name='Startup', value='i' + move['Startup'] + "\n\u200b")
    embed.add_field(name='Block', value=move['Block'] + "\n\u200b")
    embed.add_field(name='Hit', value=move['Hit'] + "\n\u200b")
    embed.add_field(name='Total', value=move['Total'] + "\n\u200b")
    embed.add_field(name='Counter Hit', value=move['Counter Hit'] + "\n\u200b")
    embed.add_field(name='Notes', value=move['Notes'] + "\n\u200b")

    return embed

def move_list_embed(character, move_list, move_type):
    '''Returns the embed message for a list of moves matching to a special move type'''
    desc_string = ''
    for move in move_list:
        desc_string += move + '\n'

    embed = discord.Embed(title=character['proper_name'] + ' ' + move_type.lower() + ':',
            colour=0x00EAFF,
            description=desc_string)

    return embed

def error_embed(err):
    embed = discord.Embed(title='Error',
            colour=0xFF4500,
            description=err)

    return embed

@bot.event
async def on_ready():
    print(datetime.datetime.utcnow().isoformat())
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def test(ctx):
    print('Testing...')
    embed = discord.Embed(title='Test title', description='A test embed thing.', colour=0x0000FF)
    embed.set_author(name='Test name', icon_url=bot.user.default_avatar_url)
    await ctx.send(embed=embed, delete_after=60)

@bot.command()
async def addalias(ctx, *args):
    if len(args) != 2:
        embed = discord.Embed(title='Error', colour=0x0000FF)
        embed.set_author(name='TekkenFrameBot', icon_url=bot.user.default_avatar_url)
        embed.add_field(name="Message", value="Not enough arguments, or too many arguments.")
        await ctx.send(embed=embed, delete_after=15)
        return
    
    character_name = args[0]
    toAddAlias = args[1]
    alias_file = dirname + '/json/character_alias.json'
    character_aliases = []
    
    with open(alias_file, 'r') as characterAliases:
        character_aliases = json.load(characterAliases)

    for alias in character_aliases:
        if alias['name'] == character_name:
            if toAddAlias not in alias['alias']:
                alias['alias'].append(toAddAlias)
                break

    with open(alias_file, 'w') as characterAliases:
        json.dump(character_aliases, characterAliases, indent=4)

    embed=discord.Embed(title="Success", description="Added the alias: %s to character: %s!" % (toAddAlias, character_name), color=0x2dd280)
    embed.set_author(name='TekkenFrameBot', icon_url=bot.user.default_avatar_url)
    await ctx.send(embed=embed, delete_after=15)

@bot.command()
async def removealias(ctx, *args):
    if len(args) != 2:
        embed = discord.Embed(title='Error', colour=0x0000FF)
        embed.set_author(name='TekkenFrameBot', icon_url=bot.user.default_avatar_url)
        embed.add_field(name="Message", value="Not enough arguments, or too many arguments.")
        await ctx.send(embed=embed, delete_after=15)
        return
    
    toRemoveAlias = args[0]
    character_name = args[1]
    alias_file = dirname + '/json/character_alias.json'
    character_aliases = []
    
    with open(alias_file, 'r') as characterAliases:
        character_aliases = json.load(characterAliases)

    for alias in character_aliases:
        if alias['name'] == character_name:
            if toRemoveAlias in alias['alias']:
                alias['alias'].remove(toRemoveAlias)
                break

    with open(alias_file, 'w') as characterAliases:
        json.dump(character_aliases, characterAliases, indent=4)

    embed=discord.Embed(title="Success", description="Removed the alias: %s from character: %s!" % (toRemoveAlias, character_name), color=0x2dd280)
    embed.set_author(name='TekkenFrameBot', icon_url=bot.user.default_avatar_url)
    await ctx.send(embed=embed, delete_after=15)

@bot.event
async def on_message(message):
    '''This has the main functionality of the bot. It has a lot of
    things that would be better suited elsewhere but I don't know
    if I'm going to change it.
    '''
    channel = message.channel
    if message.content.startswith('!') and ((isinstance(channel, discord.channel.DMChannel)) or (channel.name in config.CHANNELS)):

        user_message = message.content
        user_message = user_message.replace('!', '')
        user_message_list = user_message.split(' ', 1)

        if len(user_message_list) <= 1:
            # malformed command
            return

        chara_name = user_message_list[0].lower()
        chara_move = user_message_list[1]

        # iterate through character aliases in config for matching value
        character_aliases = []
        with open(alias_file, 'r') as characterAliases:
            character_aliases = json.load(characterAliases)

        chara_alias = list(filter(lambda x: (chara_name in x['alias']), character_aliases))
        if chara_alias:
            chara_name = chara_alias[0]['name']

        character = tkfinder.get_character(chara_name)
        if character is not None:
            if chara_move.lower() in move_types:
                chara_move = chara_move.lower()
                move_list = tkfinder.get_by_move_type(character, move_types[chara_move])
                if  len(move_list) < 1:
                    embed = error_embed('No ' + move_types[chara_move].lower() + ' for ' + character['proper_name'])
                    msg = await channel.send(embed=embed, delete_after=config.EXTRA_DATA['timeout_error'])
                elif len(move_list) == 1:
                    move = tkfinder.get_move(character, move_list[0], False)
                    embed = move_embed(character, move)
                    msg = await channel.send(embed=embed, delete_after=config.EXTRA_DATA['timeout_normal'])
                elif len(move_list) > 1:
                    embed = move_list_embed(character, move_list, move_types[chara_move])
                    msg = await channel.send(embed=embed, delete_after=config.EXTRA_DATA['timeout_normal'])

            else:
                move = tkfinder.get_move(character, chara_move, True)

                #First checks the move as case sensitive, if it doesn't find it
                #it checks it case unsensitive

                if move is not None:
                    embed = move_embed(character, move)
                    msg = await channel.send(embed=embed, delete_after=config.EXTRA_DATA['timeout_normal'])
                else:
                    move = tkfinder.get_move(character, chara_move, False)
                    if move is not None:
                        embed = move_embed(character, move)
                        msg = await channel.send(embed=embed, delete_after=config.EXTRA_DATA['timeout_normal'])
                    else:
                        embed = error_embed('Move not found: ' + chara_move)
                        msg = await channel.send(embed=embed, delete_after=config.EXTRA_DATA['timeout_error'])
        else:
            bot_msg = 'Character ' + chara_name + ' does not exist.'
            embed = error_embed(bot_msg)
            msg = await message.channel.send(embed=embed, delete_after=config.EXTRA_DATA['timeout_error'])

            return
    await bot.process_commands(message)

bot.run(token)