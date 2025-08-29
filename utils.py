import os
from moviepy.video.io.VideoFileClip import VideoFileClip

def extrair_audio(video_path, audio_saida="temp_audio.wav"):
   """Extrai o áudio de um arquivo de vídeo e salva em WAV."""
   if not os.path.exists(video_path):
       raise FileNotFoundError(f"Arquivo de vídeo não encontrado: {video_path}")

   clip = VideoFileClip(video_path)
   clip.audio.write_audiofile(audio_saida, codec="pcm_s16le")  # WAV padrão para Whisper
   clip.close()
   return audio_saida
