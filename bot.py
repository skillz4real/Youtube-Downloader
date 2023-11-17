from pytube import Playlist, YouTube
from pytube.cli import on_progress
import os 

class bot:
    def __init__(self):
        """instantiate bot with a link and define what the link is pointing to"""
        self.object = input("Are we dealing with a (C)hannel, a (P)laylist or a plain YouTube (V)ideo? ").lower()
        if self.object not in ('c','p','v'):
            self.object = None
        self.url = input("Paste the url of the object (the playlist,channel or video) ")


    def chose_function(self):
        """Chose what function to call"""
        if self.object == 'p':
            self.download_playlist()
        if self.object == 'v':
            self.download_video()
        if self.object == 'c':
            print("This part still hasn't been completed")

    def download_playlist(self):
        """Downloading the playlist in a folder with same title"""
        playlist = Playlist(self.url)
        audio = None
        
        #asking user if he needs video or only_audio
        while not audio:
            user_input = input("Would you like to only download the audio?(N/y) ").lower()
            if user_input in ('y','n'):
                audio = user_input == 'y'
                break
            else:
                print("please make a valid choice")

        #user needs to make sure the playlist is set to Public on YouTube
        if not playlist:
            print(f"please make sure the playlist is publicly available")

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
            if audio:
                #print(os.listdir())
                vid.streams.filter(only_audio=audio).first().download()
                #os.rename(f"{vid.title}.mp4", f"{vid.title}_audio.mp4")
            else:
                vid.steams.order_by("resolution").first().download()


    def download_video(self):
        """downloads single video"""
        vid = YouTube(self.url)
        audio = None
        
        while not audio:
            user_input = input("Would you like to only download the audio?(N/y)").lower()
            if user_input in ('y','n'):
                audio = user_input == 'y'
                break
            else:
                print("please make a valid choice")

        if not vid:
            print(f"check video availability")

        if audio:
            vid.streams.filter(only_audio=audio).first().download()
            os.rename(f"{vid.title}.mp4", f"{vid.title}_audio.mp4")
        else:
            vid.steams.order_by("resolution").first().download()


if __name__ == "__main__":
    bot = bot()
    bot.chose_function()
    
