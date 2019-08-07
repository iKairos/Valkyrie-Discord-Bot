import discord, random, json
from discord.ext import commands
from settings import *
from objects.user import User
from helpers import Helpers
from db import db_inventory

with open("configs/crates.json") as f:
    crates = json.load(f)

class Gambling:
    def __init__(self, bot):
        self.bot = bot
        self.errors = ErrorString()
        self.configs = Configs()
        self.msg = Messages()
        self.themes = Themes()
        self.helpers = Helpers()
        self.inventory = db_inventory.DB_Inventory()

    @commands.command(pass_context=True)
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def slots(self, ctx, bet: int = 50):
        if bet < 50:
            await self.bot.say(self.errors.BET_INSUF.format("50"))
            return

        user = ctx.message.author

        _user = User(user.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return

        if _user.money < bet:
            await self.bot.say(self.errors.INSUF_MONEY)
            return

        if bet <= 100 and bet > 0:
            bet_win_ratio = 0.5
        elif bet <=500 and bet > 100:
            bet_win_ratio = 1.25
        elif bet <= 1000 and bet > 500:
            bet_win_ratio = 1.5
        else:
            bet_win_ratio = 2.25

        event = self.helpers.getSlotsScreen()

        await self.bot.say(event[0])

        if event[1] == 3:
            win_value = int(1000000 * bet_win_ratio)
            await self.bot.say(f"🎇🎉🎊 | YOU WON **{win_value}** coins from the slot!")
        elif event[1] == 2:
            win_value = int(bet * bet_win_ratio)
            await self.bot.say(f"👏👌 | You won **{win_value}** coins from the slot!")
        elif event[1] == 1:
            win_value = bet
            await self.bot.say(f"👍 | You won back your bet.")
        else:
            win_value = -bet
            await self.bot.say(f"\n 😢 | You lost your bet.")

        _user.add_money(win_value)
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def coinflip(self, ctx, guess: str, bet: int = 50):
        guess = guess.lower()

        author = ctx.message.author

        options = ["heads", "tails"]

        if guess not in options:
            await self.bot.say(self.errors.OPTION_ERR.format("heads or tails"))
            return
        
        _user = User(author.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return

        if _user.money < bet:
            await self.bot.say(self.errors.INSUF_MONEY)
            return
        
        if bet <= 100 and bet > 0:
            bet_win_ratio = 0.25
        elif bet <=500 and bet > 100:
            bet_win_ratio = 0.5
        elif bet <= 1000 and bet > 500:
            bet_win_ratio = 0.75
        else:
            bet_win_ratio = 1.25

        draw = random.choice(options)

        win_value = int(bet * bet_win_ratio)

        if guess == draw:
            await self.bot.say(self.msg.COIN_WIN.format(draw, guess, win_value))
            _user.add_money(win_value)
        else:
            await self.bot.say(self.msg.COIN_LOSE.format(draw, guess, bet))
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def gamble(self, ctx, bet: int = 50):
        author = ctx.message.author

        _user = User(author.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return

        if _user.money < bet:
            await self.bot.say(self.errors.INSUF_MONEY)
            return
        
        if bet < 50:
            await self.bot.say(self.errors.BET_INSUF.format("50"))
            return

        probabilities = [True, False]

        draw = random.choice(probabilities)

        ratio = [0.25, 0.5, 0.75]

        rate = random.choice(ratio)

        if draw:
            value = random.randint(1, int(bet * rate))

            await self.bot.say(self.msg.GAMBLE_WON.format(bet, value))
        else:
            value = -bet
            await self.bot.say(self.msg.GAMBLE_LOSE.format(bet))
        
        _user.add_money(value)
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def opencrate(self, ctx, crate_id: str):
        author = ctx.message.author
        _user = User(author.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return
        
        item = self.inventory.get_item(crate_id)
        
        if len(item) == 0:
            await self.bot.say(self.errors.ITEM_NOT_EXIST)
            return

        item_name = item[0][0]
        item_type = item[0][1]
        crate_key = item[0][4]

        if len(_user.get_user_item(item_name)) == 0:
            await self.bot.say(self.errors.ITEM_DONT_OWN)
            return
        
        if item_type is not 2:
            await self.bot.say(self.errors.NOT_CRATE)
            return
        
        if len(_user.get_user_item(crate_key)) == 0:
            await self.bot.say(self.errors.NO_KEY)
            return

        pool = []

        for heading in crates:
            if heading == crate_id:
                for given in crates[heading]:
                    pool = list(given['pool'])
                    string = given['str']
        
        draw = random.choice(pool)
        draw_str = str(draw) + string
        if draw is None:
            await self.bot.say(self.msg.CRATE_NONE)
            _user.delete_user_item(crate_key)
            _user.delete_user_item(item_name)
        else:
            await self.bot.say(self.msg.CRATE_WON.format(draw_str))
            _user.add_money(draw)
            _user.delete_user_item(crate_key)
            _user.delete_user_item(item_name)
        
    @commands.command(pass_context=True)
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def fish(self, ctx):
        author = ctx.message.author
        _user = User(author.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return
        
        win = [True, False]

        if random.choice(win):
            pool = ['🦈', '🐡', '🐠', '🐟']
            draw = random.choice(pool)

            if draw == pool[0]:
                prize = random.randint(50, 75)
                fish = pool[0]
            elif draw == pool[1]:
                prize = random.randint(10, 30)
                fish = pool[1]
            elif draw == pool[2]:
                prize = random.randint(50, 100)
                fish = pool[2]
            elif draw == pool[3]:
                prize = random.randint(1, 60)
                fish = pool[3]
            
            _user.add_money(prize)

            await self.bot.say(f"🎣 | You caught a fish `{fish}` and sold it for `{prize}` coins!")
        else:
            await self.bot.say("😢 | You only caught some piece of shi- junks in the ocean.")

def setup(bot):
    bot.add_cog(Gambling(bot))
