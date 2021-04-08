import discord; print(discord.__version__)
import asyncio
import os
import sys

sys.path.append(os.path.abspath('settings'))
from global_sets import * # Импорт основных настроек
from config import *

sys.path.append(os.path.abspath('tools'))
from information import *
from moderation import * 
#
from prefix import *
from random_tools import *
from temp_rooms import *
from rps import *
#
from popcommands import *

sys.path.append(os.path.abspath('tools/fun'))
from fakescreen import *


import youtube_dl
import requests
import json
import datetime
from typing import Optional
import config
from dotenv import load_dotenv
from discord import FFmpegPCMAudio
from discord import utils
from config import settings
from SimpleQIWI import *
from colorama import Fore, Style, init
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from discord.ext import commands
from time import sleep
from discord.ext.commands import Bot
from discord.utils import get

@bot.event
async def on_ready():
    song_name='.help'  #Status name
    activity_type=discord.ActivityType.listening #Status type
    await bot.change_presence(activity=discord.Activity(type=activity_type,name=song_name))
    print(bot.user.name + " | Active!")

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send(embed = discord.Embed(description = f':x: Ошибка, {ctx.author.name}, аргументы в команде не верные!', colour = discord.Color.red()))
#	elif isinstance(error, commands.CommandInvokeError):
#		await ctx.send(embed = discord.Embed(description = f'Упс!.. {ctx.author.name}, команда неисправна! :x:', colour = discord.Color.red()))
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send(embed = discord.Embed(description = f':x: Ошибка, {ctx.author.name}, недостаточно прав!', colour = discord.Color.red()))
	elif isinstance(error, commands.CommandNotFound):
		await ctx.send(embed = discord.Embed(description = f':x: Ошибка, {ctx.author.name}, команда не найдена!', colour = discord.Color.red()))
	elif isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(embed = discord.Embed(description = f':x: Ошибка, {ctx.author.name}, не хватает аргументов!', colour = discord.Color.red()))
	else:
		raise error



@bot.command(aliases= ['pay', 'buy', 'br'])
async def __buy(ctx):
	api=QApi(token=settings['qtoken'], phone=settings['number'])
	price=99 # Минимальное значение при котором счет будет считаться закрытым
	comment=api.bill(price) # Создаем счет. Комментарий с которым должен быть платеж генерируется автоматически, но его можно задать # параметром comment. Валютой по умолчанию считаются рубли, но ее можно изменить параметром currency
	await ctx.send("Переведите %i рублей на счет %s с комментарием %s" % (price, settings['number'], comment))
	api.start() # Начинаем прием платежей
	while True:
		if api.check(comment): # Проверяем статус
			await ctx.send("Платёж получен!")

			author = ctx.author
			guild = bot.get_guild(813475764901117962) # получаем объект сервера*
			role = guild.get_role(823583017205235752) # получаем объект роли*
			await author.add_roles(role) # выдаем автору роль
			await message.channel.send(f"{author.mention}, роль выдана!")
			break
	time.sleep(1)
	api.stop()

@bot.command()
async def help_old(ctx):
	embed=discord.Embed(title="Команды бота.", color = 0x5938ff)
	embed.set_author(name="Pyro")
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/820056583911243856/827952668399108177/pfp.png")
	embed.add_field(name=".screen", value="Фальшивый скриншот с текcтом(пример .screen @popCat 1). Работает только английский текст!", inline=False)
	embed.add_field(name=".clear, .ban", value="Команды для администрации", inline=False)
	embed.add_field(name=".play, .join", value="Команды музыки", inline=True)
	embed.add_field(name=".info", value="Информация о сервере(on update).", inline=False)
	await ctx.send(embed=embed)


@bot.command()
async def presence(ctx):
	if ctx.author.id == 296242244619599873:
		await ctx.send("presence changed!")
		await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"Rust!~", url='https://www.twitch.tv/unknowpage'))
	else:
		await ctx.send("net prav!")


for i in exts:
	bot.load_extension(i)

bot.run(settings['token'])
