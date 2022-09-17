import discord
import typing
from discord.ext import commands # Bot Commands Framework (Important apparently lolololol)

bot = commands.Bot(intents = discord.Intents.all(), command_prefix = ".") # command_prefix is the character(s) that will be used to call a command

@bot.event
async def on_ready(): # When the bot is ready
    print("Bot is ready.")

@bot.event
async def on_command_error(ctx, error): # When an error occurs
    if isinstance(error, commands.CommandNotFound): # If the error is a command not found error
        async with ctx.typing():
            await ctx.send("INVALID COMMAND! Use .help for more information on usable commands!") # Send a message to the channel
    elif isinstance(error, commands.MissingRequiredArgument):
        async with ctx.typing():
            await ctx.send("You are missing a required argument!")

@bot.command() # This is a command decorator
async def ping(ctx): # When the command "ping" is called (ctx = context)
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms") # Send "Pong!" in the same channel

@bot.command()
async def stats(ctx, scope, text_limit : typing.Optional[int]): # gets number of messages sent by user in the channel
    print(text_limit)
    counter = 0
    total = 0
    async with ctx.typing():

        if(scope == "channel"):
            async for message in ctx.channel.history(limit=text_limit): # search through all messages
                if message.author == ctx.author: # if the message author is the user who called the command
                    counter += 1
                total += 1
            if(text_limit != None):
                await ctx.send(f"You have sent {counter} messages in the last {text_limit} messages in {ctx.channel}.")
                
            else:
                await ctx.send(f"You have sent {counter} / {total} messages in this channel.")
                print(f"You have sent {counter} messages in this channel.")

        elif(scope == "server"):
            for channel in ctx.guild.text_channels: # search through all channels
                async for message in channel.history(limit=text_limit): # search through all messages
                    if message.author == ctx.author: # if the message author is the user who called the command
                        counter += 1
                    total += 1
            if(text_limit == None):
                await ctx.send(f"You have sent {counter} / {total} messages in this server.")
            else:
                await ctx.send(f"You have sent {counter} of the last {text_limit} messages from each channel.")

        elif(scope == "global"):
            for guild in bot.guilds: # search through all servers
                for channel in guild.text_channels: # search through all channels
                    async for message in channel.history(limit=text_limit): # search through all messages
                        if message.author == ctx.author: # if the message author is the user who called the command
                            counter += 1
                        total += 1
            if(text_limit == None):
                await ctx.send(f"You have sent {counter} / {total} messages in all servers that use Distats.")
            else:
                await ctx.send(f"You have sent {counter} of the last {text_limit} messages from each channel in each server that uses Distats.")

        else:
            await ctx.send("Invalid argument. Use 'channel', 'server', or 'global'.")

bot.run(TOKEN)