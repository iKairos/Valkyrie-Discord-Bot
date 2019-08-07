import discord
from discord.ext import commands
from objects.server import Server

class Roles:
    def __init__(self, bot):
        self.bot = bot
    
    def is_mod(ctx):
        _server = Server(ctx.message.server.id)

        mod_role = discord.utils.get(ctx.message.server.roles, id=_server.mod_role)

        return mod_role in ctx.message.author.roles or ctx.message.author.server_permissions.administrator
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def assignable(self, ctx, *, role: discord.Role):
        _server = Server(ctx.message.server.id)

        if role.id in _server.assignable_roles:
            await self.bot.say("❌ | The role is already self-assignable.")
            return
        
        _server.add_assignable_role(role.id)

        await self.bot.say(f"✅ | You made **{role.name}** a self-assignable role.")
    
    @commands.command(pass_context=True, aliases=['rass'])
    @commands.check(is_mod)
    async def removeassignable(self, ctx, *, role: discord.Role):
        _server = Server(ctx.message.server.id)

        if role.id not in _server.assignable_roles:
            await self.bot.say("❌ | The role is not self-assignable.")
            return
        
        _server.remove_assignable_role(role.id)

        await self.bot.say(f"✅ | You revoked **{role.name}**'s self assignable state.")
    
    @commands.command(pass_context=True, aliases=['iam'])
    async def join(self, ctx, *, role: discord.Role):
        _server = Server(ctx.message.server.id)
        author = ctx.message.author

        if role.id not in _server.assignable_roles:
            await self.bot.say("❌ | The role is not self-assignable.")
            return
        
        if role in author.roles:
            await self.bot.say("❌ | You already have this role.")
            return
        
        await self.bot.add_roles(author, role)

        await self.bot.say(f"✅ | {author.mention} joined **{role.name}**!")
    
    @commands.command(pass_context=True, aliases=['iamn'])
    async def leave(self, ctx, *, role: discord.Role):
        _server = Server(ctx.message.server.id)
        author = ctx.message.author

        if role.id not in _server.assignable_roles:
            await self.bot.say("❌ | The role is not self-assignable.")
            return
        
        if role not in author.roles:
            await self.bot.say("❌ | don't have this role.")
            return
        
        await self.bot.remove_roles(author, role)

        await self.bot.say(f"✅ | {author.mention} left **{role.name}**!")

def setup(bot):
    bot.add_cog(Roles(bot))