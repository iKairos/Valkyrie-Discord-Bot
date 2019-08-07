import urllib, random, discord, json, asyncio
from discord.ext import commands
from objects.user import User
from settings import *

quizzes = {} # {"253423": [s,s,s,s]}

class Quiz:
    def __init__(self, bot):
        self.bot = bot
        self.themes = Themes()
    
    async def on_message(self, message):
        if self.taking_quiz(message.author.id):
            answer = quizzes[message.author.id][0]
            channel = discord.utils.get(self.bot.get_all_channels(), id=quizzes[message.author.id][2])
            if self.answer_correct(message.author.id, message.content):
                await self.reward_user(self.bot, message.author.id)
                quizzes.pop(message.author.id)
            else:
                attempts = quizzes[message.author.id][3]
                if attempts == 2:
                    quizzes[message.author.id][3] -= 1
                    attempts = quizzes[message.author.id][3]
                    await self.bot.send_message(channel, f"❌ | Your answer is wrong! You still have **{attempts}** attempt(s).")
                else:
                    await self.bot.send_message(channel, f"❌ | Your answer is wrong, the answer is **{quizzes[message.author.id][0]}**!")
                    quizzes.pop(message.author.id)

    def get_question(self):
        with urllib.request.urlopen("https://opentdb.com/api.php?amount=50") as url:
            data = json.loads(url.read().decode())
            ques = random.randint(1, 49)
            data = data["results"][ques]
        
        return data

    def taking_quiz(self, user_id):
        if user_id in quizzes:
            return True
        else:
            return False
    
    def answer_correct(self, user_id, choice: int):
        choices = quizzes[user_id][4]
        answer = quizzes[user_id][0].lower()
        
        try:
            choice = int(choice)
        except ValueError:
            return False

        choice -= 1

        try:
            if choices[choice].lower() == answer:
                return True
            else:
                return False
        except IndexError:
            return False
    
    async def reward_user(self, bot, user_id):
        _user = User(user_id)

        if quizzes[user_id][1] == "easy":
            prize = 50
        elif quizzes[user_id][1] == "medium":
            prize = 125
        elif quizzes[user_id][1] == "hard":
            prize = 200

        _user.add_money(prize)

        channel = discord.utils.get(self.bot.get_all_channels(), id=quizzes[user_id][2])

        await bot.send_message(channel, f"✅ | You answered the question correctly! You received **{prize}** coins.")

    @commands.command(pass_context=True, aliases=['trivia'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def quiz(self, ctx):
        if self.taking_quiz(ctx.message.author.id):
            await self.bot.say("❌ | You're still taking a previous quiz, calm down!")
            return

        data = self.get_question()
            
        category = data["category"]
        game_type = data["type"]
        difficulty = data["difficulty"]
        question = data["question"]
        correct = data["correct_answer"]
        channel = ctx.message.channel.id

        try:
            question = question.replace("&quot;", "\"")
        except:
            pass
        
        try:
            question = question.replace("&amp;", "&")
        except:
            pass
        
        try:
            question = question.replace("&#039;", "'")
        except:
            pass
        
        try:
            question = question.replace("&Aacute;", "Á")
        except:
            pass

        choices = []

        for que in data["incorrect_answers"]:
            try:
                que = que.replace("&quot;", "\"")
            except:
                pass
        
            try:
                que = que.replace("&amp;", "&")
            except:
                pass
            
            try:
                que = que.replace("&#039;", "'")
            except:
                pass

            choices.append(que)
        
        choices.append(correct)

        random.shuffle(choices)
        
        str_choice = ""
        count = 1
        for ch in choices:
            str_choice += f"`{count}.` **{ch}**\n"
            count += 1

        q = discord.Embed(
            description=f"__{question}__",
            color=self.themes.MAIN_COL
        )
        q.add_field(
            name="Choices (Use it's number to answer)",
            value=str_choice,
            inline=False
        )
        q.add_field(
            name="Difficulty",
            value=difficulty,
            inline=True
        )
        q.add_field(
            name="Category",
            value=category,
            inline=True
        )
        q.set_author(name="Quiz / Trivia", icon_url=ctx.message.author.avatar_url)
        q.set_footer(text="You only have 25 seconds to answer the question.")

        await self.bot.say(embed=q)

        if game_type == "boolean":
            attempts = 1
        else:
            attempts = 2

        quizzes[ctx.message.author.id] = [correct, difficulty, channel, attempts, choices]

        await asyncio.sleep(25)

        try:
            quizzes.pop(ctx.message.author.id)
            await self.bot.say(f"❌ | You did not answered the question in time, the answer is **{correct}**!")
        except:
            pass

def setup(bot):
    bot.add_cog(Quiz(bot))