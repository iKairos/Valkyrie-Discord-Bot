import discord
from discord.ext import commands
from settings import *
from objects.user import User

class Register:
    def __init__(self, bot):
        self.bot = bot
        self.errors = ErrorString()
        self.configs = Configs()
        self.msg = Messages() 
        self.themes = Themes()
    
    async def on_message(self, message):
        author = message.author

        if author.bot:
            return
            
        _user = User(author.id)

        if _user.is_Registered:
            return
        
        
        _user.append_user

def setup(bot):
    bot.add_cog(Register(bot))