import discord
from discord.ext import commands
from objects.user import User
from objects.item import Item
from objects.server import Server
from settings import *

class Owner:
    def __init__(self, bot):
        self.bot = bot
        self.errors = ErrorString()
        self.msg = Messages()
    
    def is_owner(ctx):
        return ctx.message.author.id == "231782718352916480"
    
    @commands.command(pass_context=True)
    @commands.check(is_owner)
    async def grantcoins(self, ctx, user: discord.Member, coins: int):
        _user = User(user.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return
        
        _user.add_money(coins)

        await self.bot.say(f"You have given **{user.name}** `{coins}` coins.")
    
    @commands.command(pass_context=True)
    @commands.check(is_owner)
    async def grantexp(self, ctx, user: discord.Member, exp: int):
        _user = User(user.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return
        
        _user.add_experience(exp)

        await self.bot.say(f"You have given **{user.name}** `{exp}` experience points.")
    
    @commands.command(pass_context=True)
    @commands.check(is_owner)
    async def changepresence(self, ctx, *, string: str):
        await self.bot.change_presence(game=discord.Game(name=string))
        await self.bot.say(f"🤖 | Bot presence changed to `{string}`.")
    
    @commands.command(pass_context=True)
    @commands.check(is_owner)
    async def eval(self, ctx, operation: str):
        try:
            await self.bot.say(eval(operation))
        except Exception as e:
            await self.bot.say(e)
    
    @commands.command(pass_context=True)
    @commands.check(is_owner)
    async def grantbadge(self, ctx, user: discord.Member, badge):
        _user = User(user.id)
        _item = Item(badge)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return

        if _item.exists is False:
            await self.bot.say(self.errors.ITEM_NOT_EXIST)
            return
        
        if _item.kind != 3:
            await self.bot.say("❌ | Item is not a badge.")
            return
        
        try:
            if badge == _user.get_user_badge(badge)[0][1]:
                await self.bot.say(self.errors.ALREADY_OWNED)
                return
        except:
            pass

        _user.store_badge(badge)

        await self.bot.say(f"You gave {user.mention} the badge **{_item.name}**.")
    
    @commands.command(pass_context=True)
    @commands.check(is_owner)
    async def purgebadge(self, ctx, user: discord.Member, badge):
        _user = User(user.id)
        _item = Item(badge)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return

        if _item.exists is False:
            await self.bot.say(self.errors.ITEM_NOT_EXIST)
            return
        
        if _item.kind != 3:
            await self.bot.say("❌ | Item is not a badge.")
            return
        
        try:
            if len(_user.get_user_badge(badge)) == 0:
                await self.bot.say(self.errors.ITEM_DONT_OWN)
                return
        except:
            pass

        _user.purge_user_badge(badge)

        await self.bot.say(f"You purged **{_item.name}** from {user.mention}.")
    
    @commands.command(pass_context=True)
    @commands.check(is_owner)
    async def setlevel(self, ctx, user: discord.Member, level: int):
        _user = User(user.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return
        
        _user.set_level(level)

        await self.bot.say(f"You set {user.mention}'s level to **{level}**.")
    
    @commands.command(pass_context=True)
    @commands.check(is_owner)
    async def setexp(self, ctx, user: discord.Member, exp: int):
        _user = User(user.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return
        
        _user.set_experience(exp)

        await self.bot.say(f"You set {user.mention}'s experience to **{exp}**.")
    
    @commands.command(pass_context=True)
    @commands.check(is_owner)
    async def setwarnings(self, ctx, user: discord.Member, warnings: int):
        _user = User(user.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return
        
        _user.set_warnings(warnings)

        await self.bot.say(f"You set {user.mention}'s warnings to **{warnings}**.")

def setup(bot):
    bot.add_cog(Owner(bot))