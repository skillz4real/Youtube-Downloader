from pytube import Playlist, YouTube
from pytube.cli import on_progress
import os
import time 

class bot:
    def __init__(self):
        """instantiate bot with a link and define what the link is pointing to"""
        self.object = input("Downloading a (V)ideo or a (P)laylist? ").lower()
        if self.object not in ('p','v'):
            self.object = None
        self.url = input("Paste the url of the object (the playlist,channel or video) ")

    def chose_function(self):
        """Chose what function to call"""
        if self.object == 'p':
            self.download_playlist()
        if self.object == 'v':
            self.download_video()

    def auth(self):
        """Authetication function"""
        print("For a more secure app YTDL checks the environment variable $YT_OAUTH before prompting you for your keys. To avoid pasting your keys at each use you can set the keys in your terminal before launching running the bot or add 'export YT_OAUTH=<your keys>' to your shell rc file")
        time.sleep(5)
        oauth_keys = os.getenv("YT_OAUTH")
        if not oauth_keys:
            oauth_keys = input("Please enter your OAUTH keys: ")
        return oauth_keys



    def download_playlist(self):
        """Downloading the playlist in a folder with same title"""
        playlist = Playlist(self.url)
        only_audio = None
        
        #asking user if he needs video or only_audio
        while not only_audio:
            user_input = input("Would you like to only download the audio?(N/y)").lower()
            if user_input in ('y','n',''):
                audio = user_input == 'y'
                break
            else:
                print("please make a valid choice")

        #user needs to make sure the playlist is set to Public on YouTube
        try:
            assert(playlist.title)
        except:
            print(f"Please make sure the playlist is publicly available or add your OAuth keys")
            return 0
        #creating folder to download videos will fail if user doesn't have appropriate permissions
        directory = playlist.title
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
            if only_audio:
                stream = vid.streams.filter(only_audio=only_audio).filter().last()
                stream.download()
                title = stream.title
                ext = stream.mime_type.split('/')[1]
                os.rename(f"{title}.{ext}", f"{title}_audio.{ext}")
            else:
                stream = vid.streams.order_by("resolution").filter(progressive=True).last()
                stream.download()


    def download_video(self):
        """downloads single video"""
        vid = YouTube(self.url,
                      on_progress_callback=on_progress,
                      use_oauth=True)
        vid.register_on_progress_callback(on_progress)
        only_audio = None
        
        while not only_audio:
            user_input = input("Would you like to only download the audio?(N/y)").lower()
            if user_input in ('y','n',''):
                only_audio = user_input == 'y'
                break
            else:
                print("please make a valid choice")

        if not vid:
            print(f"check video availability. Video should be publicly available or add your OAuth keys")

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
    
