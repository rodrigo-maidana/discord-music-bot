import discord
from discord.ext import commands

# import all of the cogs
from music_cog import MusicCommands
from help_cog import HelpCommands
# import all of the cogs
from music_cog import music_cog
from help_cog import help_cog

my_secret = "TOKEN"

# Definir los intentos que necesita tu bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# Crea instancias de tus clases Cog
music_cog = MusicCommands(bot)
help_cog = HelpCommands(bot)

# Agrega las instancias de las clases Cog a tu bot
bot.add_cog(music_cog)
bot.add_cog(help_cog)


@bot.event
async def on_ready():
    print(f'Conectado como: {bot.user}')

bot.run(my_secret)
