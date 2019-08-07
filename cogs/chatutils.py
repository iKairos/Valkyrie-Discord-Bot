import discord, asyncio, requests
from discord.ext import commands
from settings import *
from io import BytesIO
from objects.user import User
from objects.server import Server
from helpers import Helpers
from PIL import Image

class ChatUtils:
    def __init__(self, bot):
        self.bot = bot
        self.errors = ErrorString()
        self.configs = Configs()
        self.msg = Messages() 
        self.themes = Themes()
        self.helpers = Helpers()
    
    def is_mod(ctx):
        _server = Server(ctx.message.server.id)

        mod_role = discord.utils.get(ctx.message.server.roles, id=_server.mod_role)

        return mod_role in ctx.message.author.roles or ctx.message.author.server_permissions.administrator
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def purge(self, ctx, number: int, user: discord.Member = None):
        if number < 2:
            await self.bot.say(self.errors.PURGE_TWO)
            return
        
        msg = []
        count = 0

        async for x in self.bot.logs_from(ctx.message.channel, limit=number):
            if user is not None:
                if x.author == user:
                    count += 1
                    msg.append(x)
            else:
                count += 1
                msg.append(x)
        
        await self.bot.delete_messages(msg)
        
        if user is None:
            await self.bot.say(self.msg.DELETED_MSG.format(count), delete_after=2)
        else:
            await self.bot.say(self.msg.USER_DELETED_MSG.format(count, user.mention), delete_after=2)
    
    @commands.command(pass_context=True, aliases=['ann'])
    @commands.check(is_mod)
    async def announce(self, ctx, channel: discord.Channel, *, string):
        embed = discord.Embed(
            description=string,
            color=self.themes.MAIN_COL,
            timestamp=ctx.message.timestamp
        )

        await self.bot.send_message(channel, embed=embed)
        await self.bot.delete_message(ctx.message)
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def say(self, ctx, channel: discord.Channel, *, string):
        await self.bot.send_message(channel, string)


        try:
            e = discord.Embed(color=self.themes.MAIN_COL)
            attach = ctx.message.attachments[0]['url']
            e.set_image(url=attach)
            await self.bot.send_message(channel, embed=e)
        except:
            pass
        
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def dm(self, ctx, user: discord.Member, *, string):
        msg = f"Message from **{ctx.message.server.name}** | {string}"
        await self.bot.send_message(user, msg)
        await self.bot.delete_message(ctx.message)

        await self.bot.say(f"📩 | A message is sent to {user.mention}.")

def setup(bot):
    bot.add_cog(ChatUtils(bot))