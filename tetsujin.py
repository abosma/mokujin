#!/usr/bin/env python3
import os
import datetime

import discord
from discord.ext import commands
from discord.message import Message

import infofinder
import config

import aliashandler
import embedhandler

from dotenv import load_dotenv
load_dotenv()

bot_prefix = config.EXTRA_DATA['prefix']
bot_description = config.EXTRA_DATA['description']
bot_token = os.getenv("BOT_TOKEN")
bot = commands.Bot(command_prefix=bot_prefix, description=bot_description)

cwd = os.getcwd()
alias_file = cwd + '/json/character_alias.json'

@bot.event
async def on_ready():
    print(datetime.datetime.utcnow().isoformat())
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def addalias(ctx : commands.Context, *args):
    embed = None
    
    if len(args) != 2:
        embed = embedhandler.error_embed("Too many, or not enough arguments.")
        await ctx.send(embed=embed, delete_after=15)
        return
    
    if(aliashandler.add_alias(args)):
        embed = discord.Embed(title="Success", description="Added the alias: %s to character: %s!" % (args[1], args[0]), color=0x2dd280)
        embed.set_author(name='TekkenFrameBot')
    else:
        embed = embedhandler.error_embed("Something went wrong adding the alias, please try again.")
    
    await ctx.send(embed=embed, delete_after=15)

@bot.command()
async def removealias(ctx : commands.Context, *args):
    embed = None
    
    if len(args) != 2:
        embed = embedhandler.error_embed("Too many, or not enough arguments.")
        await ctx.send(embed=embed, delete_after=15)
        return

    if(aliashandler.remove_alias(args)):
        embed = discord.Embed(title="Success", description="Removed the alias: %s from character: %s!" % (args[0], args[1]), color=0x2dd280)
        embed.set_author(name='TekkenFrameBot')
    else:
        embed = embedhandler.error_embed("Something went wrong removing the alias, please try again.")
    
    await ctx.send(embed=embed, delete_after=15)

@bot.command()
async def info(ctx : commands.Context):
    embed = embedhandler.info_embed()

    await ctx.send(embed=embed, delete_after=60)

@bot.event
async def on_message(message : Message):
    channel = message.channel
    
    if message.content.startswith('!') and ((isinstance(channel, discord.channel.DMChannel)) or (channel.name in config.CHANNELS)):
        user_message = message.content
        user_message = user_message.replace('!', '')
        user_message_list = user_message.split(' ', 1)

        if len(user_message_list) <= 1:
            return

        char_name = user_message_list[0].lower()
        char_move = user_message_list[1]

        potential_name = aliashandler.get_alias(char_name)
        if(potential_name != None):
            char_name = potential_name

        character = infofinder.get_character(char_name)
        
        if character != None:
            move = infofinder.get_move(character['local_json'], char_move)
            if(move != None):
                to_return_embed = None
                
                if 'BreakThrow' in move:
                    to_return_embed = embedhandler.throw_embed(character, move)
                else:
                    to_return_embed = embedhandler.move_embed(character, move)

                await channel.send(embed=to_return_embed, delete_after=config.EXTRA_DATA['timeout_normal'])
            else:
                to_return_error = embedhandler.error_embed("Could not find move input, or any like it. Please check geppopotamus for the move data.")
                await channel.send(embed=to_return_error, delete_after=config.EXTRA_DATA['timeout_error'])
        else:
            to_return_error = embedhandler.error_embed("Could not find character, or any like it. Please check geppopotamus for the move data.")
            await channel.send(embed=to_return_error, delete_after=config.EXTRA_DATA['timeout_error'])

    await bot.process_commands(message)

bot.run(bot_token)