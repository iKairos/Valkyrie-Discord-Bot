import discord, json, asyncio
from discord.ext import commands
from settings import *
from objects.user import User
from objects.server import Server

configs = Configs()
errors = ErrorString()
themes = Themes()

bot = commands.Bot(command_prefix=configs.PREFIX)
bot.remove_command('help')


with open('configs/configs.json') as f:
    cnf = json.load(f)

extensions = ["cogs.member",
              "cogs.server_configs",
              "cogs.channels",
              "cogs.mod",
              "cogs.userconfig",
              "cogs.transaction",
              "cogs.chatutils",
              "cogs.errors",
              "cogs.level",
              "cogs.gambling",
              "cogs.logger",
              "cogs.owner",
              "cogs.lottery",
              "cogs.register",
              "cogs.snr",
              "cogs.noreply",
              "cogs.leaderboards",
              "cogs.fun",
              "cogs.roles",
              "cogs.quiz"]

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='some tests...'))
    print(f"Running {configs.BOT_NAME}...")
    print(f"{configs.BOT_NAME} online on version {configs.BOT_VERSION}")
    print("EVERYTHING BELOW THIS WILL BE THE LOG INSTANCES")
    print("===============================================")

@bot.event
async def on_member_join(member):
    _server = Server(member.server.id)

    if _server.is_Registered is False:
        return

    welcome = discord.Embed(
        title=f"Welcome to {member.server}!",
        description="This bot is created by Friendly Tagalogchatting.",
        color = themes.MAIN_COL,
    )
    welcome.add_field(
        name="Welcome Message",
        value=_server.welcome_message
    )
    welcome.set_author(name=member.server, icon_url=member.server.icon_url)
    welcome.set_footer(text=f"Need help with this bot? Use {configs.PREFIX}help.")

    await bot.send_message(member, embed=welcome)


@bot.command()
@commands.has_permissions(administrator=True)
async def load(extension):
    try:
        bot.load_extension(extension)
        await bot.say(f"`{extension}` module was loaded.") #
        print(f"{extension} was loaded.")                  #
    except Exception as e:
        await bot.say(errors.ERR_LOAD.format(extension, e))

@bot.command()
@commands.has_permissions(administrator=True)
async def unload(extension):
    try:
        bot.unload_extension(extension)
        await bot.say(f"`{extension}` module was unloaded.") #
        print(f"{extension} was unloaded.")                  #
    except Exception as e:
        await bot.say(errors.ERR_LOAD.format(extension, e))

if __name__ == '__main__':
    for ext in extensions:
        try:
            bot.load_extension(ext)
        except Exception as e:
            print(errors.ERR_LOAD.format(ext, e))

@bot.event
async def on_message(message):
    author = message.author
    _user = User(author.id)

    if message.server is None and not author.bot:
        print(f"DM | {author.name} | {message.content}")
        return

    if _user.inter_toggled is False:
        return

    if author.bot:
        return

    await bot.process_commands(message)

bot.run(cnf["GENERAL"]["RUNNER"])
