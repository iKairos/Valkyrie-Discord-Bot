import discord
from discord.ext import commands
from settings import *
from objects.server import Server

class SuggestReport:
    def __init__(self, bot):
        self.bot = bot
        self.errors = ErrorString()
        self.configs = Configs()
        self.msg = Messages() 
        self.themes = Themes()
    
    def is_mod(ctx):
        _server = Server(ctx.message.server.id)

        mod_role = discord.utils.get(ctx.message.server.roles, id=_server.mod_role)

        return mod_role in ctx.message.author.roles or ctx.message.author.server_permissions.administrator
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def setsuggestchannel(self, ctx, channel: discord.Channel = None):
        if channel is None:
            channel = ctx.message.channel

        _server = Server(ctx.message.server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return
        
        if _server.suggest_channel == channel.id:
            await self.bot.say("❌ | Channel already registered as your suggestions and reports channel.")
            return
        
        _server.set_suggest_channel(channel.id)

        await self.bot.say(f"✅ | You set **{channel.name}** as your suggestions and reports channel.")
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def removesuggestchannel(self, ctx, channel: discord.Channel = None):
        if channel is None:
            channel = ctx.message.channel

        _server = Server(ctx.message.server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return
        
        if _server.suggest_channel is None:
            await self.bot.say("❌ | You don't have a suggestions and reports channel.")
            return
        
        _server.remove_suggest_channel()

        await self.bot.say("✅ | You removed your server's suggestions and reports channel.")
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def setpublicsuggestchannel(self, ctx, channel: discord.Channel = None):
        if channel is None:
            channel = ctx.message.channel

        _server = Server(ctx.message.server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return
        
        if _server.public_suggest_channel == channel.id:
            await self.bot.say("❌ | Channel already registered as your suggestions and reports channel.")
            return
        
        _server.set_public_suggest(channel.id)

        await self.bot.say(f"✅ | You set **{channel.name}** as your public suggestionschannel.")
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def removepublicsuggestchannel(self, ctx, channel: discord.Channel = None):
        if channel is None:
            channel = ctx.message.channel

        _server = Server(ctx.message.server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return
        
        if _server.public_suggest_channel is None:
            await self.bot.say("❌ | You don't have a suggestions and reports channel.")
            return
        
        _server.remove_public_suggest()

        await self.bot.say("✅ | You removed your server's public suggestions channel.")
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def togglepublicsuggest(self, ctx):
        _server = Server(ctx.message.server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return
        
        if _server.is_public_suggest:
            await self.bot.say("📴 | You turned public suggestions off.")
            _server.toggle_public_suggest(False)
        else:
            await self.bot.say("✅ | You turned public suggestions on.")
            _server.toggle_public_suggest(True)
    
    @commands.command(pass_context=True)
    async def suggest(self, ctx, *, string: str):
        suggest_user = discord.Embed(
            title="💹🔵Suggestions🔴💹",
            description="Thank you for submitting your suggestion! Abusing this feature can lead to sanctions from the moderators. Thank you for contributing in making this server better!",
            color=self.themes.MAIN_COL,
            timestamp=ctx.message.timestamp
        )

        _server = Server(ctx.message.server.id)

        if _server.suggest_channel is None:
            await self.bot.say("❌ | You don't have a suggestions and reports channel.")
            return

        await self.bot.delete_message(ctx.message)

        await self.bot.say(embed=suggest_user)

        ticket_id = ctx.message.id

        await self.bot.send_message(
            ctx.message.author, 
            f"🔵 | You submitted a suggestion on **{ctx.message.server.name}** and your ticket id is `{ticket_id}`.")

        suggest_admin = discord.Embed(
            title="User ID",
            description=ctx.message.author.id,
            color=self.themes.MAIN_COL,
            timestamp=ctx.message.timestamp
        )
        suggest_admin.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        suggest_admin.add_field(
            name="Suggestion",
            value=string
        )
        suggest_admin.add_field(
            name="Ticket ID",
            value=ticket_id
        )

        channel = discord.utils.get(ctx.message.server.channels, id=_server.suggest_channel)

        msg = await self.bot.send_message(channel, embed=suggest_admin)

        await self.bot.add_reaction(msg, '👍')
        await self.bot.add_reaction(msg, '👎')

        if _server.is_public_suggest:
            suggest_public = discord.Embed(
                title="Suggestion",
                description=string,
                color=self.themes.MAIN_COL,
                timestamp=ctx.message.timestamp
            )
            suggest_public.set_author(
                name=ctx.message.author.name,
                icon_url=ctx.message.author.avatar_url
            )

            public_channel = discord.utils.get(ctx.message.server.channels, id=_server.public_suggest_channel)

            pub = await self.bot.send_message(public_channel, embed=suggest_public)
            await self.bot.add_reaction(pub, '👍')
            await self.bot.add_reaction(pub, '👎')
            
    @commands.command(pass_context=True)
    async def report(self, ctx, *, string: str):
        report_user = discord.Embed(
            title="🔴Report🔴",
            description="Thank you for submitting a report ticket! Abusing this feature can lead to sanctions. Thank you for contributing in making this server better!",
            color=0xfc1235,
            timestamp=ctx.message.timestamp
        )

        _server = Server(ctx.message.server.id)

        if _server.suggest_channel is None:
            await self.bot.say("❌ | You don't have a suggestions and reports channel.")
            return

        await self.bot.delete_message(ctx.message)

        await self.bot.say(embed=report_user)

        ticket_id = ctx.message.id

        await self.bot.send_message(
            ctx.message.author, 
            f"🔴 | You submitted a report on **{ctx.message.server.name}** and your ticket id is `{ticket_id}`.")

        report_admin = discord.Embed(
            title="User ID",
            description=ctx.message.author.id,
            color=0xfc1235,
            timestamp=ctx.message.timestamp
        )
        report_admin.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        report_admin.add_field(
            name="Report",
            value=string
        )
        report_admin.add_field(
            name="Ticket ID",
            value=ticket_id
        )

        channel = discord.utils.get(ctx.message.server.channels, id=_server.suggest_channel)

        await self.bot.send_message(channel, embed=report_admin)

def setup(bot):
    bot.add_cog(SuggestReport(bot))
