import discord
from discord.ext import commands
import sys
from config import DISCORD_BOT_TOKEN, COMMAND_PREFIX

# Carga dinámica de cogs
initial_extensions = [
    'music_commands',  # Asegúrate de que el nombre del módulo coincida con tu archivo de comandos de música.
]

class MusicBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix, intents=intents)
        
        # Carga de todos los cogs al iniciar el bot
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Error al cargar la extensión {extension}', file=sys.stderr)
                print(e, file=sys.stderr)

    async def on_ready(self):
        # Este evento se ejecuta cuando el bot ha terminado su inicio y está listo para trabajar
        print(f'Logged in as {self.user.name} - {self.user.id}\nVersion: {discord.__version__}')

# Configura los intents según lo que necesites. Los intents son necesarios para recibir ciertos tipos de eventos.
intents = discord.Intents.default()

# Creación de una instancia de tu bot
bot = MusicBot(command_prefix=COMMAND_PREFIX, intents=intents)

# Ejecución del bot con el token de Discord
bot.run(DISCORD_BOT_TOKEN)
