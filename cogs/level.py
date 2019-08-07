import discord, asyncio
from discord.ext import commands
from settings import *
from settings import *
from helpers import Helpers
from objects.user import User
from objects.channel import Channel

class Level():
    def __init__(self, bot):
        self.bot = bot
        self.errors = ErrorString()
        self.configs = Configs()
        self.msg = Messages() 
        self.themes = Themes()
        self.helpers = Helpers()
    
    async def on_message(self, message):
        _user = User(message.author.id)
        _channel = Channel(message.channel.id)

        if message.author.bot is True:
            return

        if _user.is_Registered is False:
            return
        
        if _user.exp_toggled is False:
            return
        
        if _channel.is_Registered is False:
            return
        
        _user.add_experience(_channel.persistence)

        level = _user.level

        next_lvl_exp = 25 * level * level - 25 * level

        if _user.experience > next_lvl_exp:
            _user.level_up
            if level == 1:
                return
            else:
                self.helpers.level_up_img(message.author.avatar_url, _user.level)
                msg = await self.bot.send_file(message.channel, 'externals/img/temp/leveltemp.png', content=self.msg.LEVEL_UP.format(message.author.mention, level + 1))
                await asyncio.sleep(20)
                await self.bot.delete_message(msg)
    
    @commands.command(pass_context=True)
    async def stats(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
        
        _user = User(user.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return

        level = _user.level
        experience = _user.experience
        next_lvl_exp = 25 * level * level - 25 * level

        embed = discord.Embed(
            title="User Stats 👨‍💼",
            description=f"Statistics of **{user.name}**",
            color=self.themes.MAIN_COL
        )
        embed.add_field(
            name="Level",
            value=level,
            inline=False
        )
        embed.add_field(
            name="Experience",
            value=f"{experience} / {next_lvl_exp}",
            inline=False
        )
        embed.add_field(
            name="Exp To Next Level",
            value=next_lvl_exp - experience,
            inline=False
        )
        embed.add_field(
            name="Total Warnings",
            value=_user.warnings,
            inline=False
        )
        embed.set_author(
            name=user.name,
            icon_url=user.avatar_url
        )

        await self.bot.say(embed=embed)
    
def setup(bot):
    bot.add_cog(Level(bot))