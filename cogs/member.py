import discord, json, asyncio, time, datetime
from discord.ext import commands
from settings import *
from helpers import Helpers
from objects.user import User

with open("texts/help.json") as f:
    help_str = json.load(f)

init_time = time.time()

class Member:
    """
    General member functions for bot-to-user interaction functionality and helper functions.
    """
    def __init__(self, bot):
        self.bot = bot
        self.errors = ErrorString()
        self.configs = Configs()
        self.msg = Messages() 
        self.themes = Themes()
        self.helpers = Helpers()
    
    @commands.command(pass_context=True, aliases=['h'])
    async def help(self, ctx, option: str = None):
        msg = self.errors.CMD_NOT_EXIST.format(option)
        author = ctx.message.author

        embed = discord.Embed(
                description=self.msg.HELP_DESC.format(self.configs.PREFIX, self.configs.PREFIX),
                color = self.themes.MAIN_COL
                )
        embed.set_author(
                name=self.msg.HELP_TITLE,
                icon_url=self.configs.ICON_URL
                )
        embed.set_thumbnail(
            url=self.configs.THUMB_URL
        )

        if option == None:
            for heading in help_str:
                msg = ""
                for cmd in help_str[heading]:
                    cmd_name = cmd['cmd']
                    msg += f"`{cmd_name}`**,** "
                msg = msg[:-6]
                embed.add_field(
                        name=heading,
                        value=msg
                    )
                    
            await self.bot.say(embed=embed)
            return
        else:
            for heading in help_str:
                for cmd in help_str[heading]:
                    cmd_name = cmd['cmd']
                    cmd_usage = cmd['usage'].format(self.configs.PREFIX)
                    cmd_desc = cmd['desc']
                    cmd_args = cmd['args']
                    if option == cmd_name:
                        msg = self.msg.HELP_OPT.format(cmd_name, cmd_desc, cmd_usage, cmd_args)
                        break
            
            embed.add_field(
                name="Specific Help",
                value=msg,
                inline=False)
            
            await self.bot.say(embed=embed)
            return
    
    @commands.command(pass_context=True)
    async def about(self):
        initial = int(round(time.time() - init_time))
        time_disp = str(datetime.timedelta(seconds=initial))

        embed = discord.Embed(
            description=self.msg.ABT_DESC,
            color=self.themes.MAIN_COL
        )
        embed.set_author(
            name=self.configs.BOT_NAME,
            icon_url=self.configs.ICON_URL
        )
        embed.set_thumbnail(
            url=self.configs.THUMB_URL
        )
        embed.add_field(
            name="Author",
            value=self.configs.AUTHOR,
        )
        embed.add_field(
            name="Version",
            value=self.configs.BOT_VERSION,
        )
        embed.add_field(
            name="Contributor(s)",
            value="Flame#6999",
        )
        embed.add_field(
            name="Uptime",
            value=time_disp,
        )

        await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    async def avatar(self, ctx, user: discord.Member = None):
        author = ctx.message.author

        if user is None:
            target = author
        else:
            target = user 
        
        embed = discord.Embed(
            title=f"Avatar of {target.name}",
            color=self.themes.MAIN_COL
        )
        embed.set_image(
            url=target.avatar_url
        )
        embed.set_footer(
            text=f"Requested by {author.name}",
            icon_url=author.avatar_url
        )
            
        await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        embed = discord.Embed(
            title=self.msg.PING_STR,
            description=self.msg.PING_EMJ,
            color=self.themes.MAIN_COL
        )

        subj = await self.bot.say(embed=embed)
        interval = subj.timestamp - ctx.message.timestamp
        calc = 1000 * interval.total_seconds()

        error = discord.Embed(
            title="Error fetching data",
            description=self.errors.ERR_PING,
            color=self.themes.MAIN_COL
        )

        success = discord.Embed(
            title="Ping successful",
            description=self.msg.PING_SUCC.format(calc),
            color=self.themes.MAIN_COL
        )

        await asyncio.sleep(2)

        if calc <= 0:
            await self.bot.edit_message(subj, embed=error)
        else:
            await self.bot.edit_message(subj, embed=success)

    @commands.command(pass_context=True)
    async def setabout(self, ctx, *, string):
        _user = User(ctx.message.author.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return
        
        if len(string) > 140:
            await self.bot.say(self.errors.ABOUT_LIMIT)
            return

        _user.set_about(string)

        await self.bot.say(self.msg.OPERATION_SUCCESSFUL)

    
    @commands.command(pass_context=True)
    async def profile(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
            _user = User(user.id)
        else:
            _user = User(user.id) 

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return
        
        if len(user.avatar_url) == 0:
            avatar_url = user.default_avatar_url
        else:
            avatar_url = user.avatar_url

        if _user.equipped_background is None:
            bg = "default"
        else:
            bg = _user.equipped_background
        
        self.helpers.profile_generate(
            avatar_url,
            user.name,
            user.discriminator,
            _user.money,
            _user.reputation,
            _user.about,
            _user.level,
            bg,
            _user.equipped_badge
        )
        
        await self.bot.send_file(
            ctx.message.channel, 
            'externals/img/temp/outcome.png')
    
    @commands.command(pass_context=True, aliases=['rep'])
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def giverep(self, ctx, user: discord.Member):
        if user == ctx.message.author:
            await self.bot.say(self.errors.REP_SELF)
            return

        _user = User(user.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return
        
        _user.increment_rep

        await self.bot.say(self.msg.REP_ADD.format(user.mention))
        
def setup(bot):
    bot.add_cog(Member(bot))