import discord, random, json
from discord.ext import commands
from settings import *
from objects.user import User
from objects.item import Item

left = "⏪"
right = "⏩"

class Transaction:
    """
    Commands class that withholds functions on economy and transactions.
    """
    def __init__(self, bot):
        self.bot = bot
        self.errors = ErrorString()
        self.configs = Configs()
        self.msg = Messages() 
        self.themes = Themes()
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def daily(self, ctx):
        _user = User(ctx.message.author.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return
        
        _user.add_money(200)

        await self.bot.say(self.msg.DAILY_RECEIVED.format(200))
    
    @commands.command(pass_context=True, aliases=['credits', 'money'])
    async def coins(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
        
        _user = User(user.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return

        money = _user.money

        embed = discord.Embed(
            title="Coins 💸🤑",
            description=f"You currently have **{money}** coins!",
            color=self.themes.MAIN_COL
        )
        embed.set_author(
            name=user.name,
            icon_url=user.avatar_url
        )

        await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True, aliases=['reps'])
    async def reputation(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
            string = "You currently have "
        
        _user = User(user.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return

        rep = _user.reputation

        embed = discord.Embed(
            title="Reputation 💪👦",
            description=f"{user.mention} currently have **{rep}** reputation point(s)!",
            color=self.themes.MAIN_COL
        )
        embed.set_author(
            name=user.name,
            icon_url=user.avatar_url
        )

        await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    async def givecoins(self, ctx, user: discord.Member, value: int):
        _giver = User(ctx.message.author.id)
        _receiver = User(user.id)

        if _giver.is_Registered is False or _receiver.is_Registered is False:
            await self.bot.say(self.errors.SPEC_NOT_IN_DB)
            return

        if _giver.money < value:
            await self.bot.say(self.errors.INSUF_MONEY)
            return
        
        if value <= 0:
            await self.bot.say(self.errors.ZERO_GIVE)
            return
        
        if user == ctx.message.author:
            await self.bot.say(self.errors.COIN_GIVE_SELF)
            return

        rng = random.randint(1000, 9999)

        embed = discord.Embed(
            title="Please verify that this is right",
            description=f"Type **{rng}** to confirm. (Expires 20 seconds)",
            color=self.themes.MAIN_COL,
            timestamp=ctx.message.timestamp
        )
        embed.add_field(
            name="Giving Coins Too:",
            value=user.mention
        )
        embed.add_field(
            name="Amount to be Transfered:",
            value=str(value),
            inline=False
        )
        embed.add_field(
            name="Your Current Coins:",
            value=str(_giver.money),
            inline=False
        )
        embed.add_field(
            name="Your Coins After Transaction:",
            value=str(_giver.money - value),
            inline=False
        )

        await self.bot.say(embed=embed)

        msg = await self.bot.wait_for_message(author=ctx.message.author, 
            content=str(rng),
            timeout=20.00)
        
        if msg is None:
            await self.bot.say("❌ | Confirmation timed out, please try again.")
            return
        
        _giver.add_money(-value)
        _receiver.add_money(value)

        await self.bot.say(self.msg.OPERATION_SUCCESSFUL)

    @commands.command(pass_context=True)
    async def shop(self, ctx):
        with open('texts/backgrounds.json') as f:
            bgs = json.load(f)
        
        with open('texts/badges.json') as f:
            badges = json.load(f)

        page_one = discord.Embed(
            title="🛍 SHOP",
            description="Page **1** Profile Backgrounds\nTo view the backgrounds, click `SHOP` above.",
            url="http://valkyriediscord.tk.s3-website-us-east-1.amazonaws.com/backgrounds.html",
            color=self.themes.MAIN_COL
        )
        for i_type in bgs:
            for x in bgs[i_type]:
                i_id = x["id"]
                i_price = x["price"]
                page_one.add_field(
                    name=i_type,
                    value=f"Price: {i_price}\nItem ID: `{i_id}`\n"
                )

        page_one.set_thumbnail(
            url=self.configs.THUMB_URL
        )
        page_one.set_footer(
            text=f"Use {self.configs.PREFIX}buy <Item_ID> to buy an item."
        )

        page_two = discord.Embed(
            title="🛍 SHOP",
            description="Page **2** Crates and Keys",
            color=self.themes.MAIN_COL
        )
        page_two.add_field(
            name="🔑 Default Key:",
            value="Item ID: `key_1`\nPrice: `1000` coins",
            inline=False
        )
        page_two.add_field(
            name="📦 Default Crate:",
            value="Item ID: `crate_1`\nPrice: `130` coins\nKey: Default Key",
            inline=True
        )
        page_two.set_thumbnail(
            url=self.configs.THUMB_URL
        )
        page_two.set_footer(
            text=f"Use {self.configs.PREFIX}buy <Item_ID> to buy an item."
        )

        page_three = discord.Embed(
            title="🛍 SHOP",
            description="Page **3** Badges",
            color=self.themes.MAIN_COL
        )

        for badge in badges:
            for x in badges[badge]:
                bdg_id = x["id"]
                bdg_price = x["price"]
                page_three.add_field(
                    name=badge,
                    value=f"Price: {bdg_price}\nBadge ID: `{bdg_id}`\n"
                )

        page_three.set_thumbnail(
            url=self.configs.THUMB_URL
        )
        page_three.set_footer(
            text=f"Use {self.configs.PREFIX}buy <Item_ID> to buy an item."
        )

        index = 0
        while True:
            if index == 0:
                msg = await self.bot.say(embed=page_one)
            elif index == 1:
                msg = await self.bot.say(embed=page_two)
            elif index == 2:
                msg = await self.bot.say(embed=page_three)
            
            l = index != 0
            r = index != 2

            if l:
                await self.bot.add_reaction(msg, left)
            if r:
                await self.bot.add_reaction(msg, right)
            
            react, user = await self.bot.wait_for_reaction(check=self.predicate(msg, l, r))
            if react.emoji == left:
                index -= 1
            elif react.emoji == right:
                index += 1
                
            await self.bot.delete_message(msg)

    
    @commands.command(pass_context=True)
    async def buy(self, ctx, item_id):
        _user = User(ctx.message.author.id)
        _item = Item(item_id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return

        if _item.exists is False:
            await self.bot.say(self.errors.ITEM_NOT_EXIST)
            return
        
        try:
            if item_id == _user.get_user_item(item_id)[0][1]:
                await self.bot.say(self.errors.ALREADY_OWNED)
                return
        except:
            try:
                if item_id == _user.get_user_badge(item_id)[0][1]:
                    await self.bot.say(self.errors.ALREADY_OWNED)
                    return
            except:
                pass
        
        cost = _item.cost

        if _user.money < cost:
            await self.bot.say(self.errors.INSUF_MONEY)
            return
        
        if _item.kind == 3:
            _user.store_badge(item_id)
        else:
            _user.put_background(item_id)

        _user.add_money(-cost)

        await self.bot.say(self.msg.ITEM_INV)
    
    @commands.command(pass_context=True)
    async def sell(self, ctx, item_id):
        _item = Item(item_id)
        _user = User(ctx.message.author.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return

        if _item.exists is False:
            await self.bot.say(self.errors.ITEM_NOT_EXIST)
            return
        
        if len(_user.get_user_item(item_id)) == 0:
            await self.bot.say(self.errors.ITEM_DONT_OWN)
            return
        
        if _item.kind ==3:
            await self.bot.say("❌ | Badges cannot be sold.")

        cost = _item.cost
        give_back = cost * 0.20
        
        _user.delete_user_item(item_id)
        _user.add_money(int(give_back))

        await self.bot.say(self.msg.SELL_STR.format(int(give_back)))
    
    @commands.command(pass_context=True)
    async def equip(self, ctx, item_id):
        _item = Item(item_id)
        _user = User(ctx.message.author.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return

        if _item.exists is False:
            await self.bot.say(self.errors.ITEM_NOT_EXIST)
            return

        if len(_user.get_user_item(item_id)) == 0 and len(_user.get_user_badge(item_id)) == 0:
            await self.bot.say(self.errors.ITEM_DONT_OWN)
            return
        
        try:
            if _user.get_user_item(item_id)[0][2] == 1:
                await self.bot.say(self.errors.ALREADY_EQUIPPED)
                return
        except:
            if _user.get_user_badge(item_id)[0][2] == 1:
                await self.bot.say(self.errors.ALREADY_EQUIPPED)
                return
        
        if _user.equipped_background is not None and _item.kind == 0: # if background
            _user.unequip_item(_user.equipped_background)
            
        if _user.equipped_badge is not None and _item.kind == 3: #if badge
            _user.unequip_badge(_user.equipped_badge)
        
        if _item.kind == 3:
            _user.equip_badge(item_id)
        else:
            _user.equip_item(item_id)
            

        await self.bot.say(self.msg.ITEM_EQUIPPED)
    
    @commands.command(pass_context=True)
    async def unequip(self, ctx, item_id):
        _item = Item(item_id)
        _user = User(ctx.message.author.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return

        if _item.exists is False:
            await self.bot.say(self.errors.ITEM_NOT_EXIST)
            return
        
        if len(_user.get_user_item(item_id)) == 0 and len(_user.get_user_badge(item_id)) == 0:
            await self.bot.say(self.errors.ITEM_DONT_OWN)
            return
        
        try:
            if _user.get_user_item(item_id)[0][2] == 0:
                await self.bot.say(self.errors.NOT_EQUIPPED)
                return
        except:
            if _user.get_user_badge(item_id)[0][2] == 0:
                await self.bot.say(self.errors.NOT_EQUIPPED)
                return
        
        if _item.kind == 3:
            _user.unequip_badge(item_id)
        else:
            _user.unequip_item(item_id)

        await self.bot.say(self.msg.ITEM_UNEQUIPPED)
    
    @commands.command(pass_context=True, aliases=['inventory'])
    async def myitems(self, ctx):
        _user = User(ctx.message.author.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return


        items = _user.user_items

        user_items = []

        for item_id in items:
            _item = Item(item_id)
            conc = f"`{_item.name}` | ID: `{item_id}`"
            user_items.append(conc)
        
        msg = ""

        for i in user_items:
            msg += f"{i}\n"
        
        if len(msg) == 0:
            msg = f"No items in your inventory. Buy some items at `{self.configs.PREFIX}shop`!"

        embed = discord.Embed(
            description="This is your backpack! 🎒",
            color=self.themes.MAIN_COL
        )
        embed.set_author(
            name=f"{ctx.message.author.name}'s Inventory",
            icon_url=ctx.message.author.avatar_url
        )
        embed.add_field(
            name="Inventory",
            value=msg
        )
        embed.set_footer(
            text=f"Use {self.configs.PREFIX}equip <Item_ID> to equip an item."
        )

        await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def loot(self, ctx):
        _user = User(ctx.message.author.id)

        if _user.is_Registered is False:
            await self.bot.say(self.errors.USER_NOT_IN_DB)
            return

        creds = random.randint(10,99)

        probabilities = [True, False]

        choice = probabilities[random.randint(0,1)]

        if choice:
            _user.add_money(creds)
            await self.bot.say(self.msg.LOOT_SUCCESSFUL.format(creds))
        else:
            await self.bot.say(self.msg.LOOT_FAIL)
    
    @commands.command(pass_context=True)
    async def viewbgs(self, ctx):
        e = discord.Embed(
            title="Valkyrie's Website",
            url="http://valkyriediscord.tk.s3-website-us-east-1.amazonaws.com/index.html",
            description="Click the link above to view Valkyrie's backgrounds.",
            color=self.themes.MAIN_COL
        )
        e.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

        await self.bot.say(embed=e)


    def predicate(self, message, l, r):
        def check(reaction, user):
            if reaction.message.id != message.id or user == self.bot.user:
                return False
            if l and reaction.emoji == left:
                return True
            if r and reaction.emoji == right:
                return True
            return False

        return check

def setup(bot):
    bot.add_cog(Transaction(bot))
