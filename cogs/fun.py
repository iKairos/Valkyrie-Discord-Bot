import discord, json, spotipy
from discord.ext import commands
from settings import *
from objects.server import Server
from gtts import gTTS
from helpers import Helpers

class Fun:
    def __init__(self, bot):
        self.bot = bot
        self.errors = ErrorString()
        self.configs = Configs()
        self.msg = Messages() 
        self.themes = Themes()
        self.helpers = Helpers()
    
    @commands.command(pass_context=True)
    async def tts(self, ctx, language: str, *, string: str):
        try:
            tts = gTTS(text=string, lang=language)
            tts.save("externals/audio/temp/audio.mp3")

            await self.bot.send_file(ctx.message.channel, "externals/audio/temp/audio.mp3")
        except ValueError:
            await self.bot.say(
            "❌ | The language that you set is not supported. Please try languages like `en = english`, " + 
            "`tl = Filipino`, `ja = japanese`, and others."
            )
    
    @commands.command(pass_context=True)
    async def artist(self, ctx, *, name: str):
        author = ctx.message.author
        sp = self.helpers.spotify_authenticate()

        results = sp.search(q=f'artist:{name}', type='artist')

        artists = results['artists']['items']

        if len(artists) == 0:
            await self.bot.say("❌ | Cannot find the artist on spotify.")
            return

        
        try:
            artist = artists[0]

            e = discord.Embed(title=artist['name'],
                            color=self.themes.MAIN_COL,
                            url=artist['external_urls']['spotify'])
            #e.set_author(name=artist['name'], icon_url=author.avatar_url)
            e.add_field(name="Follower Count",
                        value=artist['followers']['total'])
            e.add_field(name="Popularity Score",
                        value=artist['popularity'])
            if len(artist['genres']) == 0:
                genres = "Nothing indicated"
            else:
                genres = ""
                for i in artist['genres']:
                    genres += f"{i}, "
                
                genres = genres[:-2]

            e.add_field(name="Genres",
                        value=genres)

            albums = sp.artist_albums(artist['uri'])
            albums = albums['items']
            albs = ""
            eps = ""
            apps = ""
            for album in albums:
                if album['album_group'] == 'single':
                    if album['name'] in eps:
                        pass
                    else:
                        eps += f"{album['name']}\n"
                elif album['album_group'] == 'album':
                    if album['name'] in albs:
                        pass
                    else:
                        albs += f"{album['name']}\n"
                elif album['album_group'] == 'appears_on':
                    apps += f"{album['name']} by {album['artists'][0]['name']}\n"
            
            albs = albs if len(albs) is not 0 else None
            eps = eps if len(eps) is not 0 else None
            apps = apps if len(apps) is not 0 else None

            e.add_field(name="Singles/EPs",
                        value=eps)
            e.add_field(name="Albums",
                        value=albs)
            e.add_field(name="Appears On",
                        value=apps)

            e.set_thumbnail(url=artist['images'][0]['url'])

            await self.bot.say(embed=e)
        except Exception as er:
            await self.bot.say("❌ | Artist details are faulty.")
            print("Error on command artist: ")
            print(er)

def setup(bot):
    bot.add_cog(Fun(bot))