import discord
from discord.ext import commands
import sys
from config import DISCORD_BOT_TOKEN, COMMAND_PREFIX

# Lista de cogs para cargar
initial_extensions = [
    'music_commands',  # El nombre del módulo debe coincidir con el nombre de tu archivo.
]

class MusicBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix, intents=intents)

        # Carga de cogs
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Error al cargar la extensión {extension}: {e}', file=sys.stderr)

    async def on_ready(self):
        print(f'Logged in as {self.user.name} - {self.user.id}\nVersion: {discord.__version__}')

# Configura los intents según lo que necesites. Los intents son necesarios para recibir ciertos tipos de eventos.
intents = discord.Intents.default()

# Creación de una instancia de tu bot
bot = MusicBot(command_prefix=COMMAND_PREFIX, intents=intents)

# Ejecución del bot con el token de Discord
bot.run(DISCORD_BOT_TOKEN)
