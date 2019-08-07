import requests, random
import spotipy
from io import BytesIO
from discord.ext import commands
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps
from PIL import ImageFilter
from spotipy.oauth2 import SpotifyClientCredentials

class Helpers:
    def time_convert(self, time):
        if "mo" in time:
            convert = time.replace("mo", "")
            cooldown = int(convert) * 2629746
            return cooldown, convert + " month(s)"

        if "s" in time:
            convert = time.replace("s", "")
            cooldown = int(convert)
            return cooldown, convert + " second(s)"
        elif "m" in time:
            convert = time.replace("m", "")
            cooldown = int(convert) * 60
            return cooldown, convert + " minute(s)"
        elif "h" in time:
            convert = time.replace("h", "")
            cooldown = int(convert) * 3600
            return cooldown, convert + " hour(s)"
        elif "d" in time:
            convert = time.replace("d", "")
            cooldown = int(convert) * 86400
            return cooldown, convert + " day(s)"
        elif "y" in time:
            convert = time.replace("y", "")
            cooldown = int(convert) * 31556952
            return cooldown, convert + " year(s)"
    
    def profile_generate(self, 
                        avatar_url, 
                        username, 
                        userdisc,
                        usermoney,
                        userrep,
                        userabout,
                        userlevel,
                        bg,
                        badges):

        avatar_file = requests.get(avatar_url)
        im = Image.open(BytesIO(avatar_file.content))
        if im.format == 'GIF':
            for i, frame in enumerate(self.iter_frames(im)):
                frame.save('externals/img/temp/profile.png')
            im = Image.open('externals/img/temp/profile.png').convert("RGBA")
            
        im = im.resize((175, 175))
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)

        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output.save('externals/img/temp/profile.png')


        background = Image.open(f'externals/img/backgrounds/{bg}.png')

        username = (username[:15] + "...") if len(username) > 17 else username

        #badge code
        if badges is not None:
            #count = 1
            #_x = 216
            #_y = 195
            #for badge in badges:
            #    bd = Image.open(f'externals/img/badges/{badge}.png')
            #    background.paste(bd, (_x, _y), bd)
                
            prem_im = Image.open(f'externals/img/badges/{badges}.png')
            background.paste(prem_im, (485, 26), prem_im)
        else:
            pass

        user_font = ImageFont.truetype("externals/fonts/Montserrat-Medium.ttf", 35)
        user_name = ImageDraw.Draw(background)
        user_name.text((216, 130), username, font=user_font, fill="white")    

        disc_font = ImageFont.truetype("externals/fonts/Montserrat-Light.ttf", 25)
        user_disc = ImageDraw.Draw(background)
        user_disc.text((216, 165), f"#{userdisc}", font=disc_font, fill="white")

        coins_font = ImageFont.truetype("externals/fonts/Montserrat-Light.ttf", 13)
        user_coins = ImageDraw.Draw(background)
        user_coins.text((130, 274), str(usermoney), font=coins_font, fill="white")

        rep_font = ImageFont.truetype("externals/fonts/Montserrat-Light.ttf", 13)
        user_rep = ImageDraw.Draw(background)
        user_rep.text((130, 319), str(userrep), font=rep_font, fill="white")

        about_font = ImageFont.truetype("externals/fonts/ARIALUNI.TTF", 13)
        user_about = ImageDraw.Draw(background)
        user_about.text((262, 270), self.conc_about(userabout,36), font=about_font, fill="white")

        if userlevel < 10:
            _x = 66
        elif userlevel >= 10:
            _x = 60 

        level_font = ImageFont.truetype("externals/fonts/Montserrat-Medium.ttf", 22)
        level_draw = ImageDraw.Draw(background)
        level_draw.text((_x, 293), str(userlevel), font=level_font, fill="white")

        background.paste(im.filter(ImageFilter.DETAIL), (28, 39), im.filter(ImageFilter.DETAIL))
        background.save('externals/img/temp/outcome.png')
    
    def level_up_img(self, avatar_url, level):
        avatar_file = requests.get(avatar_url)
        im = Image.open(BytesIO(avatar_file.content))
        im = im.resize((55, 55))
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)

        background = Image.open("externals/img/backgrounds/levelup.png")
        level_font = level_font = ImageFont.truetype("externals/fonts/Montserrat-Medium.ttf", 20)
        user_level = ImageDraw.Draw(background)

        if level < 10:
            _x = 37
        elif level >= 10 and level < 100:
            _x = 33

        user_level.text((_x, 82), f"LVL {level}", font=level_font, fill="white")

        background.paste(im, (37, 6), im)
        background.save('externals/img/temp/leveltemp.png')
    
    def conc_about(self, text, length):
        if len(text) <= length:
            return text
        else:
            return text[:length] + "\n" + self.conc_about(text[length:], length)
    
    def convert_to_d_h_m_s(self, seconds: float):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        return days, hours, minutes, seconds

    def return_time_str(self, seconds: float):
        count = 1
        for i in self.convert_to_d_h_m_s(seconds):
            if count == 1:
                y = "day(s)"
            elif count == 2:
                y = "hour(s)"
            elif count == 3:
                y = "minute(s)"
            elif count == 4:
                y = "second(s)"

            if i > 0:
                return i, y
            
            count += 1
    
    def getSlotsScreen1(self):
	    slots = ['chocolate_bar', 'apple', 'cherries', 'seven']
	    slot1 = slots[random.randint(0, 3)]
	    slot2 = slots[random.randint(0, 3)]
	    slot3 = slots[random.randint(0, 3)]
	    slot4 = slots[random.randint(0, 3)]

	    slotOutput = '|:{}:|:{}:|:{}:|:{}:|\n'.format(slot1, slot2, slot3, slot4)

	    return slotOutput

    def getSlotsScreen2(self):
	    slots = ['chocolate_bar', 'apple', 'cherries', 'seven']
	    slot1 = slots[random.randint(0, 3)]
	    slot2 = slots[random.randint(0, 3)]
	    slot3 = slots[random.randint(0, 3)]
	    slot4 = slots[random.randint(0, 3)]

	    slotOutput = '|:{}:|:{}:|:{}:|:{}:|\n'.format(slot1, slot2, slot3, slot4)

	    return slotOutput

    def getSlotsScreen(self):
	    slots = ['chocolate_bar', 'apple', 'cherries', 'seven']
	    slot1 = slots[random.randint(0, 3)]
	    slot2 = slots[random.randint(0, 3)]
	    slot3 = slots[random.randint(0, 3)]
	    slot4 = slots[random.randint(0, 3)]
	    slotOutput = '|:{}:|:{}:|:{}:|:{}:| :arrow_backward: \n'.format(slot1, slot2, slot3, slot4)



	    if slot1 == slot2 and slot2 == slot3 and slot3 == slot4 and slot4 != 'seven':
		    return '**[** :slot_machine: | **SLOTS** | :slot_machine: **]**\n' + self.getSlotsScreen1() + slotOutput + self.getSlotsScreen2() + '$$ GREAT $$', 2

	    elif slot1 == 'seven' and slot2 == 'seven' and slot3 == 'seven' and slot4 == 'seven':
		    return '**[** :slot_machine: | **SLOTS** | :slot_machine: **]**\n' + self.getSlotsScreen1() + slotOutput + self.getSlotsScreen2() + '🎉🎉 JACKPOT 🎉🎉', 3

	    elif slot1 == slot2 and slot3 == slot4 or slot1 == slot3 and slot2 == slot4 or slot1 == slot4 and slot2 == slot3:
		    return '**[** :slot_machine: | **SLOTS** | :slot_machine: **]**\n' + self.getSlotsScreen1() + slotOutput + self.getSlotsScreen2() + '$ NICE $', 1

	    else:
		    return '**[** :slot_machine: | **SLOTS** | :slot_machine: **]**\n' + self.getSlotsScreen1() + slotOutput + self.getSlotsScreen2() + ':sob: TRY AGAIN :sob:', 0
    
    def iter_frames(self, im):
        try:
            i= 0
            while 1:
                im.seek(i)
                imframe = im.copy()
                if i == 0: 
                    palette = imframe.getpalette()
                else:
                    imframe.putpalette(palette)
                yield imframe
                i += 1
        except EOFError:
            pass
    
    def spotify_authenticate(self):
        client_credentials_manager = SpotifyClientCredentials(client_id='fd1bd0e52749456ebf6a2b2c5a914387',
                                                      client_secret='987c58b89ecb48d38a3a6cd936b525ba')

        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        return sp

