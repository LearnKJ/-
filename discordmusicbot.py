import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os
from dotenv import load_dotenv

# 전역 상태 변수
music_queue = []
is_playing = False
current_song = None 

load_dotenv() 
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="ㅁ", intents=intents, help_command=None)

# FFmpeg 옵션 (연결 끊김 방지 옵션 유지)
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

# YTDL 옵션 (스트리밍 시 사용)
YTDL_STREAM_OPTIONS = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0'
}


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('webpage_url') # 웹페이지 URL 저장

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        
        # 함수 호출 시마다 최신 yt-dlp 객체를 사용
        with yt_dlp.YoutubeDL(YTDL_STREAM_OPTIONS) as ydl_stream:
            try:
                # 다운로드 없이 정보만 추출
                data = await loop.run_in_executor(None, lambda: ydl_stream.extract_info(url, download=not stream))
            except Exception as e:
                return None, f"❌ 오류 발생: {str(e)}"

        if 'entries' in data:
            data = data['entries'][0]
        
        # 추출된 데이터에서 실제 스트림 URL을 가져와 FFmpeg에 전달
        stream_url = data.get('url') 
        if not stream_url:
             return None, "❌ 실제 오디오 스트림 URL을 찾을 수 없습니다."

        return cls(discord.FFmpegPCMAudio(stream_url, **ffmpeg_options), data=data), None


@bot.event
async def on_ready():
    print(f'✅ 로그인 성공: {bot.user.name}')
    print(f'✅ 봇 ID: {bot.user.id}')


# 노래 재생이 끝난 후 호출되는 콜백 함수
async def after_song_finished(ctx, error):
    if error:
        print(f"음악 재생 중 오류가 발생했습니다: {error}")
        # 오류 발생 시 사용자에게 알림은 play_next 내부에서 처리
    
    await play_next(ctx)

# play_next 함수 수정
async def play_next(ctx):
    global is_playing, current_song
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client and voice_client.is_connected():
        if music_queue:
            is_playing = True
            current_song = music_queue.pop(0) 

            song_url = current_song['url'] # webpage_url (검색어)
            song_title = current_song['title']

            # 재생 직전에 스트림 정보 다시 추출
            song_source, error = await YTDLSource.from_url(song_url, loop=bot.loop, stream=True)
            
            if error:
                await ctx.send(f"❌ '{song_title}' 재생 오류: {error}. 다음 곡을 재생합니다.")
                return await play_next(ctx) 

            # 노래 재생, after 콜백 사용
            voice_client.play(song_source, after=lambda e: asyncio.run_coroutine_threadsafe(after_song_finished(ctx, e), bot.loop))
            await ctx.send(f"▶ **{song_title}**가 재생 중입니다.")
        else:
            is_playing = False
            current_song = None
            await ctx.send("🎶 대기열에 더 이상 곡이 없습니다. 자동으로 퇴장하려면 `ㅁ정지`를 입력하세요.")
    else:
        is_playing = False
        current_song = None
        # 봇이 음성 채널에 없으면 더 이상 play_next를 호출하지 않음


# 재생 명령
@bot.command(name="재생")
async def play(ctx, *, query):
    global is_playing

    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("⚠ 먼저 음성 채널에 입장해야 합니다.")
            return

    # 대기열에 곡 정보를 가져올 때 사용할 옵션 (플레이리스트도 처리)
    ydl_queue_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extract_flat': 'in_playlist',
        'playlistend': 100 # 최대 100곡 제한
    }

    try:
        with yt_dlp.YoutubeDL(ydl_queue_opts) as ydl_queue:
            info = await asyncio.get_event_loop().run_in_executor(None, lambda: ydl_queue.extract_info(query, download=False))

            if 'entries' in info:
                # 플레이리스트 처리
                count = 0
                for entry in info['entries']:
                    if entry and 'url' in entry and 'title' in entry:
                         # webpage_url을 저장 (재생 직전 스트림 URL 재추출용)
                        song = {'url': entry['url'], 'title': entry['title']} 
                        music_queue.append(song)
                        count += 1
                await ctx.send(f"📥 플레이리스트에서 **{count}곡**이 대기열에 추가되었습니다!")
            else:
                # 단일 곡 처리
                if not info or 'webpage_url' not in info or 'title' not in info:
                     await ctx.send("음악 정보를 찾을 수 없습니다.")
                     return
                
                song = {'url': info['webpage_url'], 'title': info['title']}
                music_queue.append(song)
                await ctx.send(f"📥 **{info['title']}**이(가) 대기열에 추가되었습니다!")

            if not is_playing:
                await play_next(ctx)

    except Exception as e:
        await ctx.send(f"음악을 재생하는 중 문제가 발생했습니다: {type(e).__name__} - {str(e)}")
        print(f"[ERROR] {type(e).__name__}: {e}")


# 정지 명령
@bot.command(name="정지")
async def stop(ctx):
    global is_playing, current_song
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if voice_client and voice_client.is_connected():
        if voice_client.is_playing() or voice_client.is_paused():
            voice_client.stop() # 재생 중지
            
        music_queue.clear() 
        current_song = None
        is_playing = False
        await voice_client.disconnect()
        await ctx.send("⏹ 음악을 멈추고 봇이 퇴장했습니다.")
    else:
        await ctx.send("⚠ 봇이 음성 채널에 있지 않습니다.")


# 검색 명령
@bot.command(name="검색")
async def search(ctx, *, query: str):
    async with ctx.typing():
        # 검색용 yt-dlp 옵션
        ydl_search_options = {
            'format': 'bestaudio/best',
            'quiet': True,
            'default_search': 'ytsearch',
            'noplaylist': True,
            'extract_flat': 'auto'
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_search_options) as ydl_search:
                data = await asyncio.get_event_loop().run_in_executor(None, lambda: ydl_search.extract_info(f'ytsearch:{query}', download=False))
            
            if 'entries' not in data or len(data['entries']) == 0:
                await ctx.send("❌ 검색 결과를 찾을 수 없습니다.")
                return
            
            first_result = data['entries'][0]
            video_title = first_result.get('title', '제목 없음')
            video_url = first_result.get('webpage_url', 'URL 없음')
            await ctx.send(f'🔍 검색 결과: **[{video_title}]**({video_url})')
        except Exception as e:
            await ctx.send(f'❌ 오류 발생: {str(e)}')


# 대기열 명령
@bot.command(name="대기열")
async def queue_list(ctx):
    global current_song
    
    if not music_queue and not current_song:
        await ctx.send("📭 현재 재생 중인 곡도, 대기열도 비어 있습니다.")
    else:
        # 현재 재생 중인 곡 정보 추가
        msg = "📜 **현재 재생 중:**\n"
        if current_song:
            msg += f"▶ {current_song['title']}\n"
        else:
            msg += "없음\n"
            
        if music_queue:
            msg += "\n📜 **대기열 목록:**\n"
            queue_msg = '\n'.join([f'{i+1}. {song["title"]}' for i, song in enumerate(music_queue)])
            msg += queue_msg
        
        await ctx.send(msg)


# 건너뛰기 명령
@bot.command(name="건너뛰기")
async def skip(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and (voice_client.is_playing() or voice_client.is_paused()):
        voice_client.stop() 
        # play_next는 stop() 후 after 콜백에 의해 자동으로 호출됨
        await ctx.send("⏭ 현재 곡을 건너뛰었습니다.")
    else:
        await ctx.send("⚠ 현재 재생 중인 음악이 없습니다.")

try:
    bot.run(TOKEN)
except discord.HTTPException as e:
    print(f"❌ Discord 연결 오류 발생: {e}")
except Exception as e:
    print(f"❌ 봇 실행 중 예상치 못한 오류 발생: {e}")
