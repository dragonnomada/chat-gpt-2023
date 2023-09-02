# python3 -m pip install pytube
from pytube import YouTube

url = "https://www.youtube.com/watch?v=SqB4FSettTI"

yt = YouTube(url)

stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()

# /Applications/Python 3.11/Install Certificates.command

output_audio = stream.download()

print(output_audio)