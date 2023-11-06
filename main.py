import discord
from discord.ext import commands

# import all of the cogs
from music_cog import music_cog
from help_cog import help_cog

my_secret = "MTEwOTE3MTY4MzE0MDU3NTI0Mg.GS7UdB.dckfs4qeDSiHwBpjmzpFUxEdeqnHPFTVuV6SLc"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# remove the default help command so that we can write out own
bot.remove_command('help')

# register the class with the bot
bot.add_cog(help_cog(bot))
bot.add_cog(music_cog(bot))


@bot.event
async def on_ready():
    print(f'Conexion realizada como: {bot.user}')

# start the bot with our token
bot.run(my_secret)
