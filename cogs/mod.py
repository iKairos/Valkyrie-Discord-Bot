import discord, asyncio
from discord.ext import commands
from settings import *
from objects.user import User
from objects.server import Server
from helpers import Helpers

class Mod:
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
    @commands.has_permissions(administrator=True)
    async def registerall(self, ctx):
        await self.bot.say(self.msg.REG_WAIT)
        count = 0
        for member in ctx.message.server.members:
            if member.bot:
                continue
                
            _member = User(member.id)

            if _member.is_Registered:
                continue

            _member.append_user
            count += 1
        
        if count == 0:
            await self.bot.say(self.msg.NO_USER_REG)
            return
        
        await self.bot.say(self.msg.REG_SUCC.format(count))
    
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def registeruser(self, ctx, user: discord.Member):
        _member = User(user.id)

        if _member.is_Registered:
            await self.bot.say(self.errors.USER_IN_DB)
            return
        
        _member.append_user

        await self.bot.say(self.msg.OPERATION_SUCCESSFUL)
        
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def mute(self, ctx, user: discord.Member, duration = None):
        _server = Server(ctx.message.server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return

        if _server.mute_role is None:
            await self.bot.say(self.errors.MUTE_ROLE_NOT)
            return
        
        if user == ctx.message.author:
            await self.bot.say(self.errors.MUTE_SELF_NOT)
            return

        mute_role = discord.utils.get(ctx.message.server.roles, id=_server.mute_role)

        if mute_role in user.roles:
            await self.bot.say(self.msg.ALREADY_MUTED)
            return

        await self.bot.add_roles(user, mute_role)

        if _server.sanction_logs_allowed:
            if len(_server.logs_channel) == 0:
                await self.bot.say(self.errors.NO_LOGS_CHAN)
                return
            else:
                log = discord.Embed(
                    title="🔇 | User Muted",
                    description=user.mention,
                    color=self.themes.MAIN_COL,
                    timestamp=ctx.message.timestamp
                )
                log.add_field(
                    name="Duration",
                    value=duration
                )
                log.add_field(
                    name="Muted By",
                    value=ctx.message.author.mention
                )

                logs = discord.utils.get(ctx.message.server.channels, id=_server.logs_channel)

                await self.bot.send_message(logs, embed=log)

        try:
            dur = self.helpers.time_convert(duration)[0]
            string = self.helpers.time_convert(duration)[1]

            embed1 = discord.Embed(
                title=self.msg.MUTED,
                description=self.msg.MUTED_DESC_DUR.format(user.mention, string),
                color=self.themes.MAIN_COL,
                timestamp=ctx.message.timestamp
            )
            embed3 = discord.Embed(
                title=self.msg.TITLE_UNMUTED,
                description=self.msg.UNMUTED.format(user.mention, string),
                color=self.themes.MAIN_COL,
                timestamp=ctx.message.timestamp
            )
        except:
            pass

        embed = discord.Embed(
            title=self.msg.MUTED,
            description=self.msg.MUTED_DESC.format(user.mention),
            color=self.themes.MAIN_COL,
            timestamp=ctx.message.timestamp
        )

        if duration is not None:
            await self.bot.say(embed=embed1)
            await asyncio.sleep(dur)
            await self.bot.remove_roles(user, mute_role)
            await self.bot.say(embed=embed3)
        else:
            await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def unmute(self, ctx, user: discord.Member):
        _server = Server(ctx.message.server.id)

        if _server.mute_role is None:
            await self.bot.say(self.errors.MUTE_ROLE_NOT)
            return
        
        mute_role = discord.utils.get(ctx.message.server.roles, id=_server.mute_role)

        if mute_role not in user.roles:
            await self.bot.say(self.msg.NOT_MUTED)
            return
        
        embed = discord.Embed(
            title=self.msg.TITLE_UNMUTED,
            description=self.msg.EM_UNMUTED.format(user.mention),
            color=self.themes.MAIN_COL,
            timestamp=ctx.message.timestamp
        )

        await self.bot.remove_roles(user, mute_role)

        await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def warn(self, ctx, user: discord.Member, *, reason: str):
        _user = User(user.id)
        _server = Server(ctx.message.server.id)
        _author = ctx.message.author

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return
        
        warn = discord.Embed(
            title=self.msg.WARN_TITLE,
            description=self.msg.WARN_STR,
            color=self.themes.MAIN_COL,
            timestamp=ctx.message.timestamp
        )
        warn.add_field(
            name="Server:",
            value=ctx.message.server.name,
            inline=False
        )
        warn.add_field(
            name="Reason:",
            value=reason,
            inline=False
        )

        _user.increment_warning

        await self.bot.send_message(user, embed=warn)
        await self.bot.say(self.msg.WARN_SUCCESS.format(user.mention))

        if _server.sanction_logs_allowed:
            if len(_server.logs_channel) == 0:
                await self.bot.say(self.errors.NO_LOGS_CHAN)
                return
            else:
                logger=discord.Embed(
                    title=self.msg.LOG_WARN,
                    description=self.msg.LOG_WARN_DESC,
                    color=self.themes.MAIN_COL,
                    timestamp=ctx.message.timestamp
                )
                logger.add_field(
                    name=self.msg.LOG_WARNER,
                    value=_author.mention,
                    inline=False
                )
                logger.add_field(
                    name=self.msg.LOG_WARNED,
                    value=user.mention,
                    inline=False
                )
                logger.add_field(
                    name=self.msg.LOG_WARN_REASON,
                    value=reason,
                    inline=False
                )
                logger.add_field(
                    name=self.msg.LOG_WARN_USER_TOT,
                    value=_user.warnings,
                    inline=False
                )

                logs = discord.utils.get(ctx.message.server.channels, id=_server.logs_channel)

                await self.bot.send_message(logs, embed=logger)

    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def userinter(self, ctx, user: discord.Member):
        if ctx.message.author == user:
            await self.bot.say(self.errors.SELF_CMD)
            return

        _user = User(user.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return
        
        if _user.inter_toggled:
            _user.toggle_inter(False)
            await self.bot.say(self.msg.INT_TOGGLE_OFF)
        else:
            _user.toggle_inter(True)
            await self.bot.say(self.msg.INT_TOGGLE)
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def poll(self, ctx, question, *options: str):
        if len(options) <= 1:
            await self.bot.say("You need more than 1 option to start a poll")
        if len(options) >= 10:
            await self.bot.say("You cannot create a poll for more than 10 options.")

        if len(options) == 2 and options[0] == 'yes' or options[0] == 'Yes' and options[1] == 'no' or options[1] == 'No':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []

        for x, option in enumerate(options):
            description += '\n {} | {}'.format(reactions[x], option)
        embed = discord.Embed(title=question, description=''.join(description), color=self.themes.MAIN_COL, timestamp=ctx.message.timestamp)
        react_message = await self.bot.say(embed=embed)
        for reaction in reactions[:len(options)]:
            await self.bot.add_reaction(react_message, reaction)
        embed.set_footer(text = "Poll ID: {}".format(react_message.id))
        await self.bot.edit_message(react_message, embed=embed)
        await self.bot.delete_message(ctx.message)

def setup(bot):
    bot.add_cog(Mod(bot))