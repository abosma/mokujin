#!/usr/bin/env python3
import discord

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
    embed.add_field(name='Startup', value=move['Startup'] + "\n\u200b")
    embed.add_field(name='Block', value=move['Block'] + "\n\u200b")
    embed.add_field(name='Hit', value=move['Hit'] + "\n\u200b")
    embed.add_field(name='Total', value=move['Total'] + "\n\u200b")
    embed.add_field(name='Counter Hit', value=move['Counter Hit'] + "\n\u200b")
    embed.add_field(name='Notes', value=move['Notes'] + "\n\u200b")

    return embed

def info_embed():
    embed = discord.Embed(title="Extra Information",
            colour=0x00EAFF,
            description="Extra information explaining the move data")

    embed.add_field(name='Suffix G', value="Character can still block")
    embed.add_field(name='C', value="Character is forced to crouch")
    embed.add_field(name='B', value="Character is forced back towards you")
    embed.add_field(name='SD', value="Character is forced side towards you")
    embed.add_field(name='A', value="Character is half launched")
    embed.add_field(name='KND', value="Character is knocked down to the ground")
    embed.add_field(name='LNC', value="Character is launched")
    embed.add_field(name='H', value="Move is homing")
    embed.add_field(name='TS', value="Move is a tail spin (corkscrew)")
    embed.add_field(name='PC', value="Move is a power crush (armor)")
    embed.add_field(name='WB', value="Move is a wall bounce (wallbound)")
    embed.add_field(name='C', value="Move is cancelable with a special move")
    embed.add_field(name='TC', value="Move causes tech crouching state")
    embed.add_field(name='TJ', value="Move causes tech jumping state")

    return embed

def guess_embed(guess_message):
    embed = discord.Embed(title="Guess", description="")
    embed.add_field(name="Guessed Character", value=guess_message)

    return embed

def error_embed(error_message):
    embed = discord.Embed(title='Error', colour=0x0000FF)
    embed.set_author(name='TekkenFrameBot')
    embed.add_field(name="\n\u200b", value=error_message)

    return embed