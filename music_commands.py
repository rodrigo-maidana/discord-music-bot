import discord
from discord.ext import commands
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
import sys

spotify_client = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queues = {}  # Inicializa las colas de canciones aquí.
        # Aquí puedes inicializar cualquier estado necesario, como la cola de canciones.

    @commands.command(name='join', help='El bot se une al canal de voz del usuario.')
    async def join(self, ctx):
        # Verifica si el autor del comando está en un canal de voz
        if not ctx.author.voice:
            await ctx.send("No estás conectado a un canal de voz.")
            return

        # Obtiene el canal de voz del autor del mensaje
        channel = ctx.message.author.voice.channel

        # Verifica si el bot ya está en un canal de voz
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()

        await ctx.send(f"Conectado al canal de voz: {channel.name}")

    @commands.command(name='leave', help='El bot se retira del canal de voz.')
    async def leave(self, ctx):
        # Verifica si el bot está conectado a un canal de voz
        if ctx.voice_client is None:
            await ctx.send("No estoy en un canal de voz.")
            return

        # Guarda el nombre del canal para usarlo en el mensaje de salida
        channel_name = ctx.voice_client.channel.name

        # Desconectar
        await ctx.voice_client.disconnect()
        
        await ctx.send(f"Me he desconectado del canal de voz: {channel_name}")

    #Funciones varias del comando $PLAY
    def get_song_queue(self, ctx):
        guild_id = ctx.guild.id
        if guild_id not in self.song_queues:
            self.song_queues[guild_id] = []
        return self.song_queues[guild_id]

    async def join_voice_channel(self, ctx):
        if ctx.voice_client is not None:
            return ctx.voice_client
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            return await voice_channel.connect()
        else:
            await ctx.send("No estás conectado a un canal de voz.")
            raise commands.CommandError("Autor del comando no está en un canal de voz.")

    async def play_song(self, ctx, song):
        source = discord.FFmpegPCMAudio(song['url'], executable='ffmpeg', options='-vn')
        ctx.voice_client.play(source, after=lambda e: self.play_next_in_queue(ctx))

    def play_next_in_queue(self, ctx):
        queue = self.get_song_queue(ctx)
        if queue:
            song = queue.pop(0)
            coro = self.play_song(ctx, song)
            self.bot.loop.create_task(coro)

    @commands.command(name='play', help='Reproduce una canción o la añade a la cola de reproducción.')
    async def play(self, ctx, *, search: str):
        voice_client = await self.join_voice_channel(ctx)

        # Aquí se utiliza la API de Spotify
        try:
            results = spotify_client.search(q=search, limit=1, type='track')
            track = results['tracks']['items'][0]
            track_info = f"{track['name']} - {track['artists'][0]['name']}"
        except spotipy.SpotifyException as e:
            await ctx.send("Hubo un problema al buscar en Spotify.")
            print(f"Spotify search failed: {e}", file=sys.stderr)
            return

        # Y aquí se utiliza yt-dlp para buscar en YouTube
        with yt_dlp.YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True', 'quiet': True}) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{track_info}", download=False)['entries'][0]
            except Exception as e:
                await ctx.send("Hubo un problema al buscar la canción en YouTube.")
                print(f"YoutubeDL search failed: {e}", file=sys.stderr)
                return

        song = {'title': track_info, 'url': info['url']}

        # Lógica para reproducir o encolar la canción
        if voice_client.is_playing() or voice_client.is_paused():
            song_queue = self.get_song_queue(ctx)
            song_queue.append(song)
            await ctx.send(f"\"{song['title']}\" ha sido añadida a la cola.")
        else:
            await self.play_song(ctx, song)
#
#    @commands.command(name='pause', help='Pausa la canción actual.')
#    async def pause(self, ctx):
#        pass

#    @commands.command(name='resume', help='Reanuda la reproducción de la canción actual.')
#    async def resume(self, ctx):
#        pass

#    @commands.command(name='stop', help='Detiene la reproducción y vacía la cola.')
#    async def stop(self, ctx):
#        pass

#    @commands.command(name='skip', help='Salta a la siguiente canción en la cola.')
#    async def skip(self, ctx):
#        pass

#    @commands.command(name='queue', help='Muestra las canciones en la cola.')
#    async def queue(self, ctx):
#        pass

#    @commands.command(name='nowplaying', help='Muestra la canción que se está reproduciendo actualmente.')
#    async def now_playing(self, ctx):
#        pass

#    @commands.command(name='volume', help='Ajusta el volumen del bot.')
#    async def volume(self, ctx, volume: int):
#        pass

#    @commands.command(name='loop', help='Activa o desactiva el modo bucle para la canción actual o la cola entera.')
#    async def loop(self, ctx):
#        pass

#    @commands.command(name='shuffle', help='Mezcla las canciones en la cola.')
#    async def shuffle(self, ctx):
#        pass

#    @commands.command(name='remove', help='Elimina una canción específica de la cola.')
#    async def remove(self, ctx, index: int):
#        pass

#    @commands.command(name='search', help='Busca una canción y muestra los resultados para elegir.')
#    async def search(self, ctx, *, search: str):
#        pass

#    @commands.command(name='save', help='Guarda la cola actual en una playlist de Spotify (si es posible).')
#    async def save(self, ctx):
#        pass

#    @commands.command(name='lyrics', help='Muestra la letra de la canción actual.')
#    async def lyrics(self, ctx):
#        pass
        
def setup(bot):
    bot.add_cog(Music(bot))
