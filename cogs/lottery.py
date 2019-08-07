import discord, time, asyncio, random
from discord.ext import commands
from settings import *
from objects.user import User
from objects.server import Server
from helpers import Helpers

server_bets = {}
current_pool = {}
draw = {}

class Lottery:
    def __init__(self, bot):
        self.bot = bot
        self.errors = ErrorString()
        self.configs = Configs()
        self.msg = Messages()
        self.themes = Themes()
        self.helpers = Helpers()
        self.draw = False
    
    @commands.command(pass_context=True, aliases=['drawlotto'])
    @commands.has_permissions(administrator=True)
    async def drawlottery(self, ctx):
        global draw
        draw[ctx.message.server.id] = True

    @commands.command(pass_context=True, aliases=['tixbuy'])
    async def ticketbuy(self, ctx, first: int, second: int, bet: int = 50):
        global current_pool
        author_id = ctx.message.author.id
        server_id = ctx.message.server.id
        _user = User(author_id)
        _server = Server(server_id)
        
        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return
        
        if _user.money < bet:
            await self.bot.say(self.errors.INSUF_MONEY)
            return
        
        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return
        
        if _server.cmd_channel is None:
            await self.bot.say("❌ | Please register a commands spam channel.")
            return
        
        if bet < 50:
            await self.bot.say("❌ | Minimum bet is 50 coins!")
            return
        
        if first > 30 or second > 30:
            await self.bot.say("❌ | Numbers allowed are only in the range 1-30.")
            return

        user_draw = []
        user_draw.append(first)
        user_draw.append(second)

        try:
            _checker = server_bets[server_id]
        except:
            server_bets[server_id] = {}
        
        _user.add_money(-bet)

        if len(server_bets[server_id]) == 0:
            server_bets[server_id] = {author_id: user_draw}
            await self.bot.say(f"🎰 | You bought a ticket to the lottery with the numbers `{first}` and `{second}` respectively.")
            await self.startlottery(ctx, bet * 3)
        else:
            if author_id in server_bets[server_id]:
                await self.bot.say(self.errors.TICKET_DUPLICATE)
                return
            else:
                await self.bot.say(f"🎰 | You bought a ticket to the lottery with the numbers `{first}` and `{second}` respectively.")
                server_bets[server_id][author_id] = user_draw
                current_pool[ctx.message.server.id] += bet
        
    @commands.command(pass_context=True)
    async def tickets(self, ctx):
        try:
            tickets = server_bets[ctx.message.server.id]
        except:
            tickets = None
        
        try:
            pool = current_pool[ctx.message.server.id]
        except:
            pool = 0

        embed = discord.Embed(
            title="🎟 Lotto Tickets",
            description=f"View all submitted lotto tickets!\nPrize Pool: `{pool}` coins",
            color=self.themes.MAIN_COL
        )
        embed.set_footer(text="Buy tickets using f!ticketbuy.", icon_url=ctx.message.author.avatar_url)

        if tickets is not None:
            for user_id in tickets:
                user = discord.utils.get(ctx.message.server.members, id=user_id)
                embed.add_field(
                    name=f"{user.name}'s ticket",
                    value=f"`{tickets[user_id][0]}` `{tickets[user_id][1]}`",
                    inline=False
                )
        else:
            embed.add_field(
                name="No Tickets Submitted",
                value=f"Submit tickets using `{self.configs.PREFIX}ticketbuy`."
            )
        
        await self.bot.say(embed=embed)
    
    async def startlottery(self, ctx, pool: int):
        global current_pool
        global draw
        _server = Server(ctx.message.server.id)
        cmd_channel = discord.utils.get(ctx.message.server.channels, id=_server.cmd_channel)

        current_pool[ctx.message.server.id] = pool

        second = 0

        await self.bot.send_message(cmd_channel, f"🎰 | Lottery started with a prize pool of **{pool}** coins plus the accumulated bets.")

        while second != 900:
            await asyncio.sleep(1)
            if second == 300:
                await self.bot.send_message(cmd_channel, "🎰 | **10 minutes** left until the draw of lottery results.")
            elif second == 600:
                await self.bot.send_message(cmd_channel, "🎰 | **5 minutes** left until the draw of lottery results.")
            elif second == 840:
                await self.bot.send_message(cmd_channel, "🎰 | **1 minute** left until the draw of lottery results.")
            elif second == 890:
                await self.bot.send_message(cmd_channel, "🎰 | **10 seconds** left until the draw of lottery results.")
            elif second == 895:
                await self.bot.send_message(cmd_channel, "🎰 | **5 seconds** left until the draw of lottery results.")
            second += 1
            try:
                if draw[ctx.message.server.id] is True:
                    break
            except:
                pass
        
        await self.drawresults(ctx, cmd_channel)

    async def drawresults(self, ctx, cmd_channel):
        global current_pool
        global draw
        global server_bets
        lottery_draw = [random.randint(1,30), random.randint(1,30)]

        if len(server_bets) == 0:
            count = 0
        else:
            user_bets = server_bets[ctx.message.server.id]
            winner = []
            for user in user_bets:
                if lottery_draw == user_bets[user]:
                    winner.append(user)
            count = len(winner)

        if count == 0:
            string = f"No one won the `{current_pool[ctx.message.server.id]}` coins in the lottery!"
        elif count == 1:
            string = f"<@{winner[0]}> is the sole winner of `{current_pool[ctx.message.server.id]}` coins!"
            User(winner[0]).add_money(current_pool[ctx.message.server.id])
        elif count > 1:
            pool = int(current_pool[ctx.message.server.id] / count)
            winners = ""
            for user in winner:
                winners += f"<@{user}> "
                User(user).add_money(pool)
            string = f"{winners} won the lottery and will receive `{pool}` coins each!"
        
        try:
            draw.pop(ctx.message.server.id)
        except:
            pass
        current_pool.pop(ctx.message.server.id)
        server_bets.pop(ctx.message.server.id)

        win = discord.Embed(
            title="🎰 Lotto Draw 🎰",
            description=f"Draw Results: `{lottery_draw[0]}` `{lottery_draw[1]}`",
            color=self.themes.MAIN_COL
        )
        win.add_field(
            name="🎊 Winner(s)",
            value=string,
            inline=False
        )

        await self.bot.send_message(cmd_channel, embed=win)

def setup(bot):
    bot.add_cog(Lottery(bot))