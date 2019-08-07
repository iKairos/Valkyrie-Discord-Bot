import discord, helpers
from discord.ext import commands
from settings import *

class Errors:
    def __init__(self, bot):
        self.bot = bot
        self.errors = ErrorString()
        self.configs = Configs()
        self.helpers = helpers.Helpers()
    
    async def on_command_error(self, error, ctx):
        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == "avatar":
                await self.bot.send_message(ctx.message.channel, self.errors.ERR_NOT_MEMBER)
            else:
                await self.bot.send_message(ctx.message.channel, self.errors.WRONGFUL_INP.format(ctx.command, self.configs.PREFIX, ctx.command))
        elif isinstance(error, commands.MissingRequiredArgument):
            await self.bot.send_message(ctx.message.channel, self.errors.MISSING_ARGS.format(self.configs.PREFIX, ctx.command))
        elif isinstance(error, commands.CheckFailure):
            await self.bot.send_message(ctx.message.channel, self.errors.USER_NO_PERMS)
        elif isinstance(error, commands.CommandOnCooldown):
            await self.bot.send_message(ctx.message.channel, self.errors.CMD_COOLDOWN.format(self.helpers.return_time_str(error.retry_after)[0], self.helpers.return_time_str(error.retry_after)[1]))
        elif isinstance(error, discord.errors.Forbidden):
            await self.bot.send_message(ctx.message.channel, self.errors.BOT_NO_PERMS)
        else:
            pass

        print(f"Error Logs | {ctx.message.author.name} | {ctx.message.server.name} | Command: {ctx.command} | Error: {error}")

def setup(bot):
    bot.add_cog(Errors(bot))