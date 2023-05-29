# bot.py
import os







import gpt4all
modelpath = 'C:/Users/Derek/AppData/Local/nomic.ai/GPT4All/'
modelname = 'ggml-mpt-7b-chat'

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

def luciusreplies(msg, author = 'human'):
    prompt = f'''
{author}:
{msg}

Lucius (Roman Dictator): 
'''
    print(prompt)

    response = generate_line(gpt, prompt, n_predict = 500, temp = .5)
    return response













import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


from discord.ext import commands
bot = commands.Bot(command_prefix='%',intents=discord.Intents.all())




@bot.command(name='99', help='Salve Consul, here is my help menu')
async def nine_nine(ctx):
    await ctx.send('99 bottles of beer on the wall!')


@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello master.')

@bot.hybrid_command()
async def test(ctx):
    await ctx.send("this is a hybrid command!")
    

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