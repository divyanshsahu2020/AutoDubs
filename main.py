import streamlit as st
import whisper
from pytube import YouTube
import Conversion
from pydub import AudioSegment
import pandas as pd
import io
import os
from elevenlabs import generate, play
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import subprocess
from elevenlabs import generate, set_api_key
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context


def shorten_audio(filename):
    song="cut_audio.mp3"
    audio = AudioSegment.from_file(filename)
    one_min=70*1000
    cut_audio=audio[:]
    cut_audio.export(song,format="mp3")
    return song

def combine_video(video_filename, audio_filename):
    ffmpeg_extract_subclip(video_filename,0,115, targetname="cut_video.mp4")
    output_filename = "output.mp4"
    command = ["ffmpeg", "-y", "-i", "cut_video.mp4", "-i", audio_filename, "-c:v", "copy", "-c:a", "aac", output_filename]
    subprocess.run(command)
    return output_filename

def generate_translation(original_text,destination_language):
    print('HERE')
    print(original_text)
    converted_text=Conversion.convert(original_text,destination_language)
    return converted_text


def generate_dubs(translated):
    translated="".join(list(translated))
    filename = "output.mp3"
    print("in generated_dubs")
    set_api_key("c26621c673f247395636dd56cfed5cfa")
    audio = generate(
        text=translated,
        voice="Bella",
        model='eleven_multilingual_v1'
    )
    #play(audio)
    audio_io = io.BytesIO(audio)
    insert_audio = AudioSegment.from_file(audio_io, format='mp3')
    insert_audio.export(filename, format="mp3")
    return filename


st.title("AutoDubs 📺🎵")
link = st.text_input("Link To Youtube Video")
language = st.selectbox("Translate to", ("French", "German", "Hindi", "Italian", "Polish", "Portuguese", "Spanish"))

if st.button("Transcribe!"):
    print(f"downloading from link: {link}")
    model = whisper.load_model("base")
    yt = YouTube(link)
    if yt:
        st.subheader(yt.title)
        st.image(yt.thumbnail_url)
        audio_name=st.caption("Downloading audio stream")
        audio_stream=yt.streams.filter(only_audio=True)
        filename = audio_stream.first().download()
        if filename:
            audio_name.caption(filename)
            cut_audio = shorten_audio(filename)
            transcription = model.transcribe(cut_audio,fp16=False)
            if transcription:
                df = pd.DataFrame(transcription['segments'], columns=['start', 'end', 'text'])
                x=st.dataframe(df)
                df['converted_text']=generate_translation(df['text'],language)
                x.dataframe(df)
                dubbing_caption = st.caption("Begin dubbing...")
                dubs_audio = generate_dubs(df['converted_text'])
                dubbing_caption.caption("Dubs generated! combining with the video...")
                video_streams = yt.streams.filter(only_video=True)
                video_filename = video_streams.first().download()
                if video_filename:
                    dubbing_caption.caption("Video downloaded! combining the video and the dubs...")
                    output_filename = combine_video(video_filename, dubs_audio)
                    if os.path.exists(output_filename):
                        dubbing_caption.caption("Video successfully dubbed! Enjoy! 😀")
                        st.video(output_filename)









