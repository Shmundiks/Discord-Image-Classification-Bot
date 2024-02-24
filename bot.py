import discord
from discord.ext import commands
from cl_model import get_class
import os
from OPTIONS import TOKEN

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def photo(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachment:
            image_name = attachment.filename
            if image_name.endswith('.jpg') or image_name.endswith('jpeg') or image_name.endswith('.png'):
                await attachment.save(f'images/{image_name}')
                msg = await ctx.send("Фото успешно сохранено. Пытаюсь понять что на изображении")
                class_name, percentage_probability = get_class(model_path = "model/keras_model.h5", labels_path = "model/labels.txt", image_path = f'images/{image_name}')
                await msg.delete()
                await ctx.send(f'Я считаю, что с вероятностью {percentage_probability}% на фото {class_name.lower()}')
                os.remove(f'images/{image_name}')
        else:
            await ctx.send("Прикреплённый файл не является изображением")
            return
    else:
        await ctx.send("Нет прикреплённых файлов. Попробуй заново")

bot.run(TOKEN)