# TODO: 
# ADD MULTI DOWNLOAD

# Download Youtube Videos
from pytube import YouTube
video_url = input("Enter link:")
path = input("Enter download path:")
try:
    yt_obj = YouTube(video_url)
    filters = yt_obj.streams.filter(progressive=True, file_extension='mp4')
    # download the highest quality video
    filters.get_highest_resolution().download(output_path = path)
    print('Video Downloaded Successfully')
except Exception as e:
    print(e)
