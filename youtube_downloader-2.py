
class YoutubeDownloader:
    """
        For using this install "pip install pytube && pip install scrapetube"
    """
    def __init__(self, url, path="Videos"):
        self.url = url 
        self.path = path 
        self.fetchAllUrlOfAnyVideos()

    def convert_size(self, size_bytes):
        """
            Convert Bytes into Kb/Mb
        """
        import math
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def on_progress(self, stream, chunk, bytes_remaining):
        print("Downloading...", self.convert_size(bytes_remaining))

    def on_complete(self, stream, file_path):
        print("Download Complete", file_path)

    def youtubeDownload(self, url, count=0, file_extension="mp4"):
        """Downloader Video according to best resolution auto but you can change using count number"""
        from pytube import YouTube
        import os
        res = ["1080p", "720p", "480p", "360p", "240p", "144p"]
        try:
            yt = YouTube(
                    url,
                    on_progress_callback=self.on_progress,
                    on_complete_callback=self.on_complete,
                    use_oauth=False,
                    allow_oauth_cache=True
                )

            containt = yt.streams.filter(file_extension=file_extension, res=res[count]).first()
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            containt.download(self.path)
        except Exception as e:
            count +=1
            return self.youtubeDownload(url, count=count, file_extension="mp4")

    def fetchAllUrlOfAnyVideos(self):
        """
        It will find all url of any playlist for download all videos
        open youtube and any video and open developer tool and use this code to find current video channel id on console.
        console.log(ytInitialPlayerResponse.microformat.playerMicroformatRenderer.externalChannelId)
        videos = scrapetube.get_channel("UCrkQMtWNtuq-1j0q8c2RVeQ") : get_channel for download current channel all vieos.
        
        """
        import scrapetube
        try:
            count = str(self.url).find("list=")
            videos = scrapetube.get_playlist(self.url[count+5::])
            for video in videos:
                self.youtubeDownload(f"https://www.youtube.com/watch?v="+str(video['videoId']))
            
        except Exception as e:
            print(e)

# just copy youtube url and name/path of folder
video_Url = input("Youtube Video Url : ") # https://www.youtube.com/watch?v=Rc8tGuyHXR0&list=PLfP3JxW-T70HIvqQpoDpP-WK-uzD-wnsH
location = input("Path Name : ")
if not location:
    location = "Videos"
YoutubeDownloader(video_Url, location)