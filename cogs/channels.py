import discord, random
from discord.ext import commands
from settings import *
from objects.channel import Channel

class Channels:
    def __init__(self, bot):
        self.bot = bot
        self.errors = ErrorString()
        self.configs = Configs()
        self.msg = Messages() 
        self.themes = Themes()
    
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def registerchannel(self, ctx, channel: discord.Channel = None):
        if channel is None:
            channel = ctx.message.channel
        
        _channel = Channel(channel.id)

        if _channel.is_Registered:
            await self.bot.say(self.errors.CHANNEL_ALREADY_IN_DB)
            return
        else:
            _channel.append_channel()
        
        await self.bot.say(self.msg.CHANNEL_REGISTERED.format(channel.name))
    
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def registerallchannels(self, ctx, persistence: int):
        await self.bot.say(self.msg.REG_WAIT)
        count = 0
        for channel in ctx.message.server.channels:
            _channel = Channel(channel.id)

            if _channel.is_Registered:
                continue
            
            _channel.append_channel()
            _channel.set_persistence(persistence)
            count += 1
        
        if count == 0:
            await self.bot.say(self.msg.NO_CHANNEL_REG)
            return
        
        await self.bot.say(self.msg.REG_CHAN_SUCC.format(count))
    
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def revokechannel(self, ctx, channel: discord.Channel = None):
        if channel is None:
            channel = ctx.message.channel

        _channel = Channel(channel.id)

        if _channel.is_Registered:
            _channel.remove_channel()
            await self.bot.say(self.msg.CHANNEL_REVOKED.format(channel.name))
        else:
            await self.bot.say(self.errors.CHANNEL_NOT_IN_DB)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def togglensfw(self, ctx, channel: discord.Channel = None):
        if channel is None:
            channel = ctx.message.channel
        
        _channel = Channel(channel.id)

        if _channel.is_Registered is False:
            await self.bot.say(self.errors.CHANNEL_NOT_IN_DB)
            return

        if _channel.is_NSFW:
            _channel.toggle_nsfw(False)
            await self.bot.say(self.msg.CHANNEL_REVOKED_NSFW.format(channel.name))
        else:
            _channel.toggle_nsfw(True)
            await self.bot.say(self.msg.CHANNEL_IS_NSFW.format(channel.name))
    
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def setpersistence(self, ctx, value: int, channel: discord.Channel = None):
        if channel is None:
            channel = ctx.message.channel
        
        _channel = Channel(channel.id)

        if _channel.is_Registered is False:
            await self.bot.say(self.errors.CHANNEL_NOT_IN_DB)
            return

        rng = random.randint(100, 999)

        embed = discord.Embed(
            title=self.msg.E_VERIFY_TITLE,
            description=self.msg.E_VERIFY_DESC.format(rng),
            color=self.themes.MAIN_COL
        )
        embed.add_field(
            name=self.msg.E_VERIFY_BEFORE,
            value=_channel.persistence,
            inline=False
        )
        embed.add_field(
            name=self.msg.E_VERIFY_PERSIST,
            value=value,
            inline=False
        )
        embed.add_field(
            name=self.msg.E_VERIFY_CHANGING,
            value=channel.name,
            inline=False
        )

        await self.bot.say(embed=embed)

        msg = await self.bot.wait_for_message(author=ctx.message.author, 
            content=str(rng),
            timeout=20.00)
        
        if msg is None:
            await self.bot.say("Confirmation timed out, please try again.")
            return
        
        _channel.set_persistence(value)

        await self.bot.say(self.msg.OPERATION_SUCCESSFUL)

    @commands.command(pass_context=True, aliases=['cinfo'])
    async def channelinfo(self, ctx, channel: discord.Channel = None):
        if channel is None:
            channel = ctx.message.channel

        _channel = Channel(channel.id)

        if _channel.is_Registered is False:
            await self.bot.say(self.errors.CHANNEL_NOT_IN_DB)
            return

        _data = _channel.info

        target = channel.mention
        is_nsfw = _data[0][1]
        if is_nsfw == 0:
            is_nsfw = "False"
        else:
            is_nsfw = "True"
        persistence = _data[0][2]

        embed = discord.Embed(
            title=self.msg.E_CINFO_TITLE,
            description=self.msg.E_CINFO_DESC,
            color=self.themes.MAIN_COL
        )
        embed.add_field(
            name=self.msg.E_CINFO_CHAN,
            value=target,
            inline=False
        )
        embed.add_field(
            name=self.msg.E_CINFO_ID,
            value=channel.id,
            inline=False
        )
        embed.add_field(
            name=self.msg.E_CINFO_NSFW,
            value=is_nsfw,
            inline=False
        )
        embed.add_field(
            name=self.msg.E_CINFO_PERSIST,
            value=persistence,
            inline=False
        )

        await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def togglelogblock(self, ctx, channel: discord.Channel = None):
        if channel is None:
            channel = ctx.message.channel

        _channel = Channel(channel.id)

        if _channel.is_Registered is False:
            await self.bot.say(self.errors.CHANNEL_NOT_IN_DB)
            return
        
        if _channel.is_log_blocked:
            _channel.toggle_log_block(False)
            await self.bot.say(self.msg.LOG_UNBLOCKED.format(channel.name))
        else:
            _channel.toggle_log_block(True)
            await self.bot.say(self.msg.LOG_BLOCKED.format(channel.name))

def setup(bot):
    bot.add_cog(Channels(bot))