import discord
from discord.ext import commands
from settings import *
from objects.server import Server

class ServerConfigs:
    """
    Administrative commands to configure server settings.
    """
    def __init__(self, bot):
        self.bot = bot
        self.errors = ErrorString()
        self.configs = Configs()
        self.msg = Messages() 
        self.themes = Themes()
    
    async def on_voice_state_update(self, before, after):
        _server = Server(before.server.id)

        if _server.vc_role is None:
            return

        try:
            role = discord.utils.get(after.server.roles, id=_server.vc_role)
        except:
            return

        if not before.voice.voice_channel and after.voice.voice_channel and after.voice.voice_channel != before.server.afk_channel:
            await self.bot.add_roles(after, role)
        elif before.voice.voice_channel and not after.voice.voice_channel:
            await self.bot.remove_roles(after, role)
    
    def is_mod(ctx):
        _server = Server(ctx.message.server.id)

        mod_role = discord.utils.get(ctx.message.server.roles, id=_server.mod_role)

        return mod_role in ctx.message.author.roles or ctx.message.author.server_permissions.administrator
    
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def registerserver(self, ctx):
        server = ctx.message.server

        _server = Server(server.id)

        if _server.is_Registered:
            await self.bot.say(self.errors.SRV_ALREADY_IN_DB)
            return
        else:
            _server.append_server()
        
        await self.bot.say(self.msg.SERVER_REGISTERED.format(server.name))

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def revokeserver(self, ctx):
        server = ctx.message.server

        _server = Server(server.id)

        if _server.is_Registered:
            _server.remove_server()
            await self.bot.say(self.msg.SERVER_REVOKED.format(server.name))
        else:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def togglelogging(self, ctx):
        server = ctx.message.server

        _server = Server(server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return

        if _server.logging_allowed:
            _server.toggle_logging(False)
            await self.bot.say(self.msg.TOGGLE_LOGGING_OFF.format(server.name))
        else:
            _server.toggle_logging(True)
            await self.bot.say(self.msg.TOGGLE_LOGGING_ON.format(server.name))
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def togglesanctions(self, ctx):
        server = ctx.message.server

        _server = Server(server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return

        if _server.sanction_logs_allowed:
            _server.toggle_sanctions(False)
            await self.bot.say(self.msg.TOGGLE_SANCTIONS_OFF.format(server.name))
        else:
            _server.toggle_sanctions(True)
            await self.bot.say(self.msg.TOGGLE_SANCTIONS_ON.format(server.name))

    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def togglenrt(self, ctx):
        server = ctx.message.server

        _server = Server(server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return

        if _server.is_strict_nrt:
            _server.toggle_strict_nrt(False)
            await self.bot.say(self.msg.TOGGLE_NRT_OFF.format(server.name))
        else:
            _server.toggle_strict_nrt(True)
            await self.bot.say(self.msg.TOGGLE_NRT_ON.format(server.name))
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def muterole(self, ctx, *, role: discord.Role):
        role_id = role.id
        server = ctx.message.server

        _server = Server(server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return

        if _server.mute_role == role_id:
            await self.bot.say(self.errors.MUTE_ROLE_REG)
            return
        
        _server.set_mute_role(role_id)

        await self.bot.say(self.msg.MUTE_ROLE_SET.format(role.mention))
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def setlogs(self, ctx, channel: discord.Channel):
        channel_id = channel.id
        server = ctx.message.server

        _server = Server(server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return
        
        if _server.logs_channel == channel_id:
            await self.bot.say(self.errors.LOGS_CHAN_REG)
            return
        
        _server.set_logs_channel(channel_id)

        await self.bot.say(self.msg.LOGS_CHAN_SET.format(channel.mention))
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def setvcrole(self, ctx, role: discord.Role):
        role_id = role.id
        server = ctx.message.server

        _server = Server(server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return
        
        if _server.vc_role == role_id:
            await self.bot.say(self.errors.ROLE_SET_ALREADY)
            return
        
        _server.set_vc_role(role_id)

        await self.bot.say(self.msg.ROLE_SET.format(role.name))
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def removevcrole(self, ctx):
        server = ctx.message.server

        _server = Server(server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return
        
        if _server.vc_role is None:
            await self.bot.say(self.errors.ROLE_IS_NONE)
            return

        _server.set_vc_role(None)

        await self.bot.say(self.msg.ROLE_REMOVE)
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def cmdchannel(self, ctx, channel: discord.Channel = None):
        if channel is None:
            channel = ctx.message.channel

        server = ctx.message.server 
        _server = Server(server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return
        
        if _server.cmd_channel == channel.id:
            await self.bot.say(self.errors.CMD_REG)
            return
        
        _server.set_cmd_channel(channel.id)

        await self.bot.say(self.msg.CMD_SUCCESS.format(channel.name))
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def removecmdchannel(self, ctx, channel: discord.Channel = None):
        if channel is None:
            channel = ctx.message.channel

        server = ctx.message.server 
        _server = Server(server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return
        
        if _server.cmd_channel is None:
            await self.bot.say(self.errors.CMD_NONE)
            return
        
        _server.set_cmd_channel(None)

        await self.bot.say(self.msg.CMD_REMOVE.format(channel.name))
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def setmodrole(self, ctx, role: discord.Role):
        server = ctx.message.server 
        _server = Server(server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return
        
        if _server.mod_role == role.id:
            await self.bot.say("❌ | This is already your mod role.")
            return
        
        _server.set_mod_role(role.id)

        await self.bot.say(f"✅ | You set {role.mention} as your server's mod role.")
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def setwelcomemessage(self, ctx, *, msg: str):
        server = ctx.message.server 
        _server = Server(server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return
        
        _server.set_welcome_message(msg)

        await self.bot.say(f"🛠 | You set the server's welcome message to \"**{msg}**\".")
    
    @commands.command(pass_context=True)
    @commands.check(is_mod)
    async def removewelcomemessage(self, ctx):
        server = ctx.message.server 
        _server = Server(server.id)

        if _server.is_Registered is False:
            await self.bot.say(self.errors.SRV_NOT_IN_DB)
            return
        
        _server.remove_welcome_message()

        await self.bot.say("🛠 | You removed the server's welcome message.")
    
    
def setup(bot):
    bot.add_cog(ServerConfigs(bot))
