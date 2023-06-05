# bot.py
import os







import gpt4all
modelpath = 'C:/Users/Derek/AppData/Local/nomic.ai/GPT4All/'
modelname = 'ggml-mpt-7b-chat'
# modelname = 'ggml-gpt4all-l13b-snoozy'

gpt = gpt4all.GPT4All(modelname, modelpath)

def generate_line(gpt, prompt, stops={'\n'}, **kwargs):
    words = []
    def callback(token_id, response):
        word = response.decode('utf-8')
        words.append( word )
        print(word)
        return word not in stops or not ''.join(words).strip()
    gpt.model._response_callback = callback
    gpt.model.generate(prompt, streaming=True, **kwargs)
    return ''.join(words).strip()

def luciusreplies(msg, author = 'human', n_predict = 5120, temp = 1.5, intro = 'A cold and callous Roman Dictator'):
    prompt = f'''
{author}:
{msg}

Lucius ({intro}): 
'''
    print(prompt)

    response = generate_line(gpt, prompt, n_predict = n_predict, temp = temp)
    return response













import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


# from discord.ext import commands
# bot = commands.Bot(command_prefix='%',intents=discord.Intents.all())

bot=discord.Bot(command_prefix='%')

@bot.slash_command(name = 'question', description = 'Ask Lucius Bot a question')
async def question(
        ctx,
        query: discord.Option(str, description = 'The question to be asked'),
        mood: discord.Option(str, choices = ['Emo', 'Angry', 'Serious', 'Sad']),
        insanity: discord.Option(float, choices = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]),

        ):
    await ctx.defer()
    if mood == 'Angry':
        response = luciusreplies(query, author=ctx.author.display_name, temp = insanity, intro = 'A furious and angry Roman Dictator')
    elif mood == 'Emo':
        response = luciusreplies(query, author=ctx.author.display_name, temp = insanity, intro = 'An emo and silly Roman Dictator')
    elif mood == 'Sad':
        response = luciusreplies(query, author=ctx.author.display_name, temp = insanity, intro = 'A sad and depressed Roman Dictator')
    elif mood == 'Serious':
        response = luciusreplies(query, author=ctx.author.display_name, temp = insanity, intro = 'A super serious Roman Dictator')
    else:
        response = luciusreplies(query, author=ctx.author.display_name)

    response2 = f'> {query}\n\n{response}'
    # response = 'testing'
    await ctx.followup.send(response2)


@bot.command(name='99', help='Salve Consul, here is my help menu')
async def nine_nine(ctx):
    await ctx.send('99 bottles of beer on the wall!')


@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello master.')

@bot.command()
async def mycommand(ctx):
    async with ctx.typing():
        # do expensive stuff here
        await asyncio.sleep(10)
    await ctx.send('done!')

# @bot.hybrid_command()
# async def test(ctx):
#     await ctx.send("this is a hybrid command!")
    

@bot.command(name='say')
async def hello(ctx, *args):
    arguments = ' '.join(args)
    await ctx.send(arguments)

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        content = message.content
        content = content.replace(f'<@{bot.user.id}>', 'Lucius')
        response = luciusreplies(content, author=message.author.display_name)
        await message.channel.send(response)




bot.run(TOKEN)