import discord
from discord.ext import commands
from settings import *
from objects.user import User

class UserConfig:
    def __init__(self, bot):
        self.bot = bot
        self.errors = ErrorString()
        self.configs = Configs()
        self.msg = Messages() 
        self.themes = Themes()
    
    @commands.command(pass_context=True)
    async def toggleexp(self, ctx):
        _user = User(ctx.message.author.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return
        
        if _user.exp_toggled:
            _user.toggle_exp(False)
            await self.bot.say(self.msg.EXP_TOGGLE_OFF)
        else:
            _user.toggle_exp(True)
            await self.bot.say(self.msg.EXP_TOGGLE)
    
    @commands.command(pass_context=True)
    async def toggleinter(self, ctx):
        _user = User(ctx.message.author.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return
        
        if _user.inter_toggled:
            _user.toggle_inter(False)
            await self.bot.say(self.msg.INT_TOGGLE_OFF)
        else:
            _user.toggle_inter(True)
            await self.bot.say(self.msg.INT_TOGGLE)
    
def setup(bot):
    bot.add_cog(UserConfig(bot))