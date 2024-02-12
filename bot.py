from pytube import Playlist, YouTube, Channel
from pytube.cli import on_progress
import os
import time
import json

class bot:
    def __init__(self):
        """instantiate bot with a link and define what the link is pointing to"""
        while True:
            self.object = input("Downloading a (V)ideo, a (P)laylist or the content of a (C)hannel? ").strip().lower()
            if self.object not in ('p','v','c'):
                print("Please enter a valid choice")
            else:
                break
        self.url = input("Paste the url of the object (the playlist,channel or video) \n If you are trying to download a channel paste a link to a video from that channel.\n >>> ").strip()
        while True:
            user_input = input("Would you want to authenticate your YouTube Account to bypass age restrictions?(y/n) ").lower().strip()
            if user_input in ('y','n',''):
                self.auth = user_input == 'y'
                break
            else:
                print("Please enter a valid choice")

    def chose_function(self):
        """Chose what function to call"""
        if self.auth == True:
            self.oauth()
        if self.object == 'p':
            self.download_playlist()
        if self.object == 'v':
            self.download_video()
        if self.object == 'c':
            self.download_channel()

    def oauth(self):
        """Auth function"""
        print("As part of the authentication process YtDl will download a sample video")
        print("Please follow the instructions")
        YouTube("https://www.youtube.com/watch?v=K4TOrB7at0Y",use_oauth=True,allow_oauth_cache=True,on_progress_callback=on_progress).streams.order_by("resolution").first().download()
    
    def audio_prompt(self):
        """Prompt for audio"""
        while True:
            user_input = input("Do you want to download the video's audio only? (N/y)").lower().strip()
            if user_input in ('y','n',''):
                return user_input == 'y'
            else:
                print("Please make a valid choice")


    def download_playlist(self, url=None, only_audio=None):
        """Downloading the playlist in a folder with same title"""
        playlist = Playlist(self.url)
        only_audio = self.audio_prompt()

        #user needs to make sure the playlist is set to Public on YouTube
        try:
            directory = playlist.title
        except:
            print(f"This playlist is not publicly available. Please make sure the playlist is publicly available or use the Authetication option. If you did, you can ignore this message")
            directory = "Playlist"
        
        #creating folder to download videos will fail if user doesn't have appropriate permissions
        try:
            os.mkdir(f'{directory}')
            os.chdir(f"{directory}")
        except:
            try:
                os.chdir(f"{directory}")
            except:
                print("check the permissions for current folder")


        #downloading videos in playlist
        for vid in playlist.videos:
            vid.register_on_progress_callback(on_progress)
            self.download_video(vid, only_audio)


    def download_video(self, vid=None, only_audio=None):
        """downloads single video, Uses Progressive download"""
        if not vid:
            vid = YouTube(self.url,on_progress_callback=on_progress)
        
        if only_audio is None:
            only_audio = self.audio_prompt()
       
        if only_audio:
            stream = vid.streams.filter(only_audio=only_audio).filter(file_extension="mp4").last()
            title = stream.title
            print(f"\nDownloading {title}\n")
            stream.download()
            ext = stream.mime_type.split('/')[1]
            os.rename(f"{title}.{ext}", f"{title}_audio.{ext}")
        else:
            stream = vid.streams.order_by("resolution").filter(progressive=True).last()
            title = stream.title
            print(f"\nDownloading {title}\n")
            stream.download()
       
    def download_channel(self):
        """Downloads the entire content of a Youtube Channel"""
        c = Channel(YouTube(self.url).channel_url)
        only_audio = self.audio_prompt()

        #user needs to make sure the playlist is set to Public on YouTube
        try:
            directory = c.channel_name
        except:
            print(f"There was an issue getting the channel name. If you know why, you can ignore this message")
            directory = "Channel"
        
        #creating folder to download videos will fail if user doesn't have appropriate permissions
        try:
            os.mkdir(f'{directory}')
            os.chdir(f"{directory}")
        except:
            try:
                os.chdir(f"{directory}")
            except:
                print("check the permissions for current folder")
        for video in c.videos:
            video.register_on_progress_callback(on_progress)
            self.download_video(video,only_audio)
            


if __name__ == "__main__":
    bot = bot()
    bot.chose_function()
    
