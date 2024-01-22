from pytube import Playlist, YouTube
from pytube.cli import on_progress
import os
import time
import json

class bot:
    def __init__(self):
        """instantiate bot with a link and define what the link is pointing to"""
        self.object = input("Downloading a (V)ideo or a (P)laylist? ").strip().lower()
        if self.object not in ('p','v'):
            self.object = None
        self.url = input("Paste the url of the object (the playlist,channel or video) ").strip()
        while True:
            user_input = input("Would you want to authenticate your YouTube Account?(y/n)").lower().strip()
            if user_input in ('y','n',''):
                self.auth = user_input == 'y'
                break
            else:
                print("Please enter a valid choice")

    def chose_function(self):
        """Chose what function to call"""
        oauth = None
        if self.auth == True:
            oauth = self.oauth()
        if self.object == 'p':
            self.download_playlist(oauth)
        if self.object == 'v':
            self.download_video(oauth)

    def oauth(self):
        """Authetication function"""
        print("As part of the authentication process YtDl will now download a sample video")
        print("Please follow the instructions")
        YouTube("https://www.youtube.com/watch?v=K4TOrB7at0Y",use_oauth=True,allow_oauth_cache=True,on_progress_callback=on_progress).streams.order_by("resolution").first().download()

    def download_playlist(self):
        """Downloading the playlist in a folder with same title"""
        playlist = Playlist(self.url)
        only_audio = None
        
        #asking user if he needs video or only_audio
        while not only_audio:
            user_input = input("Would you like to download the audio without the video?(N/y)").lower().strip()
            if user_input in ('y','n',''):
                audio = user_input == 'y'
                break
            else:
                print("please make a valid choice")

        #user needs to make sure the playlist is set to Public on YouTube
        try:
            directory = playlist.title
        except:
            print(f"This playlist is not publicly available. Please make sure the playlist is publicly available or use the Authetication option. If you did authetify you can ignore this message")
            directory = "Playlist"
            #return 0
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
            print(f"downloading {vid.title}\n")
            vid.register_on_progress_callback(on_progress)
            if p_oauth:
                vid.use_oauth = True
                vid.allow_oauth_cache = True
            if only_audio:
                stream = vid.streams.filter(only_audio=only_audio).last()
                stream.download()
                title = stream.title
                ext = stream.mime_type.split('/')[1]
                os.rename(f"{title}.{ext}", f"{title}_audio.{ext}")
            else:
                stream = vid.streams.order_by("resolution").filter(progressive=True).last()
                stream.download()


    def download_video(self):
        """downloads single video, Uses Progressive download"""
        vid = YouTube(self.url,on_progress_callback=on_progress)
        only_audio = None
        
        while not only_audio:
            user_input = input("Would you like to only download the audio?(N/y)").lower().strip()
            if user_input in ('y','n',''):
                only_audio = user_input == 'y'
                break
            else:
                print("please make a valid choice")
        
        if only_audio:
            stream = vid.streams.filter(only_audio=only_audio).filter().last()
            stream.download()
            title = stream.title
            ext = stream.mime_type.split('/')[1]
            os.rename(f"{title}.{ext}", f"{title}_audio.{ext}")
        else:
            stream = vid.streams.order_by("resolution").filter(progressive=True).last()
            stream.download()
        
if __name__ == "__main__":
    bot = bot()
    bot.chose_function()
    
