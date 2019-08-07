import discord
from discord.ext import commands
from settings import *
from objects.channel import Channel
from objects.server import Server

class Logger:
    def __init__(self, bot):
        self.bot = bot
        self.themes = Themes()
    
    async def on_message(self, message):
        try:
            channel = message.channel

            _channel = Channel(channel.id)
            _server = Server(message.server.id)

            if _channel.is_log_blocked:
                return
            
            if _server.logging_allowed is False:
                return
            
            if _server.logs_channel is None:
                return
            
            attach = message.attachments[0]['url']

            embed = discord.Embed(
                title="📷 | Image Sent",
                color=self.themes.MAIN_COL,
                timestamp=message.timestamp
            )
            embed.set_author(
                name=message.author,
                icon_url=message.author.avatar_url
            )
            embed.add_field(
                name="User ID",
                value=message.author.id,
                inline=False
            )
            embed.add_field(
                name="Channel",
                value=message.channel.mention,
                inline=False
            )
            embed.add_field(
                name="Image URL",
                value=attach,
                inline=False
            )
            embed.set_image(url=attach)

            logs = discord.utils.get(message.server.channels, id=_server.logs_channel)

            await self.bot.send_message(logs, embed=embed)
        except:
            pass
    
    async def on_message_delete(self, message):
        _channel = Channel(message.channel.id)
        _server = Server(message.server.id)

        if _channel.is_log_blocked:
            return

        if _server.logging_allowed is False:
            return
        
        if _server.logs_channel is None:
            return
        
        embed = discord.Embed(
            title="❌ | Message DELETED",
            color=self.themes.MAIN_COL,
            timestamp=message.timestamp
        )
        embed.set_author(
            name=message.author,
            icon_url=message.author.avatar_url
        )
        embed.add_field(
            name="User ID",
            value=message.author.id,
            inline=False
        )
        embed.add_field(
            name="Channel",
            value=message.channel.mention,
            inline=False
        )
        embed.add_field(
            name="Message",
            value=f"\u200b{message.content}",
            inline=False
        )

        logs = discord.utils.get(message.server.channels, id=_server.logs_channel)

        await self.bot.send_message(logs, embed=embed)
    
    async def on_message_edit(self, before, after):
        try:
            _channel = Channel(before.channel.id)
            _server = Server(before.server.id)

            if _channel.is_log_blocked:
                return

            if _server.logging_allowed is False:
                return
            
            if _server.logs_channel is None:
                return
            
            embed = discord.Embed(
                title="〽 | Message EDITED",
                color=self.themes.MAIN_COL,
                timestamp=before.timestamp
            )
            embed.set_author(
                name=before.author,
                icon_url=before.author.avatar_url
            )
            embed.add_field(
                name="User ID",
                value=before.author.id,
                inline=False
            )
            embed.add_field(
                name="Channel",
                value=before.channel.mention,
                inline=False
            )
            embed.add_field(
                name="Message Before",
                value=before.content,
                inline=False
            )
            embed.add_field(
                name="Message After",
                value=after.content,
                inline=False
            )

            logs = discord.utils.get(before.server.channels, id=_server.logs_channel)

            await self.bot.send_message(logs, embed=embed)
        except:
            pass

def setup(bot):
    bot.add_cog(Logger(bot))