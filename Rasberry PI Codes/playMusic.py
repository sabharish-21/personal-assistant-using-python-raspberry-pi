import threading
import urllib
import pafy
import vlc
import re

class musicYoutube:
    def __init__(self, listen, socketConn, USER_ID, USER_NAME):
        self.Instance = vlc.Instance()
        self.socket = socketConn
        self.USER_ID = USER_ID
        self.USER_NAME = USER_NAME
        self.player   = self.Instance.media_player_new()   
        self.listen   = listen
        self.status   = 0
        
    def play(self):
        if self.status == 0:
            threading.Thread(target=self._playAudio).start()
        else:
            self.stop()
            threading.Thread(target=self._playAudio).start()
        
    def _playAudio(self):
        songName = str(self.listen("Name the song.")).strip().title()
        
        self.socket.send({
                    'id' : self.USER_ID,
                    'user' : self.USER_NAME,
                    'data' : songName
                })
        if songName.strip() == '':
            return
        query = urllib.parse.urlencode({"search_query": songName})
        formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query)
        search = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
        url = "https://www.youtube.com/watch?v={}".format(search[0])
        
        video = pafy.new(url)
        best = video.getbestaudio()
        playurl = best.url
    
        Media = self.Instance.media_new(playurl)
        Media.get_mrl()
        self.player.set_media(Media)
        self.player.play()
        self.status = 1
        
        while str(self.player.get_state()) != 'State.Ended' and self.status != 0:
            pass
        else:
            self.status = 0
            print("Song ended.")
    
    def stop(self):
        self.status = 0
        self.player.stop()
        
    def pause(self):
        self.player.pause()
        
    def resume(self):
        if self.status == 1:
            self.player.play()
            
            
if __name__ == "__main__":
 
    # Testing Purpose
    from tara import listen
    
    music = musicYoutube(listen)
    music.play()
    
    while True:
        inp = int(input('->'))
        if inp == 1:
            music.pause()
        if inp == 2:
            music.resume()
        if inp == 3:
            music.play()
        if inp == 4:
            music.stop()