import discord
from discord.ext import commands
from db import db_hfuncts
from settings import *

class Leaderboards:
    def __init__(self, bot):
        self.bot = bot
        self.db = db_hfuncts.DB_Helpers("db/data/users.db")
        self.themes = Themes()
        self.configs = Configs()
    
    @commands.command(pass_context=True, aliases=['top', 'lead'])
    async def leaderboards(self, ctx, num: int = 1):
        fetched = self.db.fetch_row("users")

        sort = sorted(fetched, key=lambda k: k[2], reverse=True)

        count = 1
        string = ""

        server = ctx.message.server
        _user = ctx.message.author

        embed = discord.Embed(
            title="🥇 Valkyrie Leaderboards",
            description="Global Valkyrie Ranks",
            color=self.themes.MAIN_COL,
            timestamp=ctx.message.timestamp
        )
        embed.set_thumbnail(url=self.configs.THUMB_URL)

        temp = 1

        for x in sort:
            user_id = x[0]
            score = x[2]
            if _user.id == user_id:
                place = temp
                break

            temp += 1
        
        pos = 1

        for tups in sort:
            id_1 = tups[0]
            exp = tups[2]
            user = discord.utils.get(self.bot.get_all_members(), id=id_1)
            try:
                name = user.name
            except:
                name = "User Left Valkyrie's Servers"
            string += f"**[**`{count}`**]**  {name}  | `{exp} points`\n\n"
            
            count += 1
            
            if count % 11 == 0:
                if num == pos:
                    break
                string = ""
                pos += 1
                
        
        string += f"==================================\nYour Place: Rank `{place}` | Total Score: `{score}`"

        embed.add_field(name="Leaderboards", value=string, inline=False)
        
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Leaderboards(bot))