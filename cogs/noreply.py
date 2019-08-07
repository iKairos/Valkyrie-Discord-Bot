import discord, asyncio
from discord.ext import commands
from settings import *
from objects.server import Server
from helpers import Helpers

nrt_state = {}

class NoReply:
    def __init__(self, bot):
        self.bot = bot
        self.msg = Messages() 
        self.themes = Themes()
        self.helpers = Helpers()
    
    def is_mod(ctx):
        _server = Server(ctx.message.server.id)

        mod_role = discord.utils.get(ctx.message.server.roles, id=_server.mod_role)

        return mod_role in ctx.message.author.roles or ctx.message.author.server_permissions.administrator

    async def on_message(self, message):
        if message.server is None:
            return
            
        _server = Server(message.server.id)

        try:
            nrt = nrt_state[message.server.id]

            if _server.is_strict_nrt:
                if nrt[1]:
                    if message.author.id != nrt[0] and message.author.bot is False and nrt[2] == message.channel.id:
                        await self.bot.delete_message(message)
                    else:
                        if message.content.lower() == "end":
                            nrt_state.pop(message.server.id)
                            await self.bot.send_message(message.channel, "🚫 No Reply Thread ended. 🚫")
        except:
            pass

    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def noreply(self, ctx, user: discord.Member, duration = None):
        global nrt_state
        if duration is not None:
            dur = self.helpers.time_convert(duration)[0]
            string = self.helpers.time_convert(duration)[1]
            
        starter = discord.Embed(
            title="⛔🛑NO REPLY THREAD🛑⛔",
            description=self.msg.NRT_DESC,
            color=self.themes.MAIN_COL,
            timestamp=ctx.message.timestamp
        )
        starter_user = discord.Embed(
            title="⛔🛑NO REPLY THREAD🛑⛔",
            description=self.msg.NRT_TAKER.format(user.mention),
            color=self.themes.MAIN_COL
        )
        thirty_seconds = discord.Embed(
            title="No Reply Thread",
            description=self.msg.NRT_THIRTY,
            color=self.themes.MAIN_COL
        )
        five_seconds = discord.Embed(
            title="No Reply Thread",
            description="No Reply Thread will start in **five seconds**.",
            color=self.themes.MAIN_COL
        )
        three_seconds = discord.Embed(
            title="No Reply Thread",
            description="No Reply Thread will start in **three seconds**.",
            color=self.themes.MAIN_COL
        )

        if duration is not None:
            dur = self.helpers.time_convert(duration)[0]
            string = self.helpers.time_convert(duration)[1]

            declare_timed = discord.Embed(
                title="No Reply Thread Invoker",
                description=self.msg.NRT_TAKE.format(user.mention, string),
                color=self.themes.MAIN_COL,
                timestamp=ctx.message.timestamp
            )
            await self.bot.say(embed=declare_timed)
            await asyncio.sleep(dur - 60)
            await asyncio.sleep(30)
            await self.bot.say(embed=thirty_seconds)
            await asyncio.sleep(25)
            await self.bot.say(embed=five_seconds)
            await asyncio.sleep(2)
            await self.bot.say(embed=three_seconds)
            await asyncio.sleep(3)
            await self.bot.say(embed=starter_user)

        else:
            await self.bot.say(embed=starter_user)
        
        nrt_state[ctx.message.server.id] = [user.id, True, ctx.message.channel.id]

def setup(bot):
    bot.add_cog(NoReply(bot))