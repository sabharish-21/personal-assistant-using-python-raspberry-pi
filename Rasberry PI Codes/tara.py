'''
pip install youtube_dl
pip install youtube-dl==2020.12.2
pip install python-vlc
pip install pafy
pip install pipwin
pip install pyaudio
pip install wikipedia
'''
import speech_recognition as sr
from playMusic import *
from smallFunctions import *
import pyttsx3
import random
import socket
import json

class connectSocket:
    def __init__(self, host=socket.gethostname(), port=8120, serverID='localhost', serverPort=8121):
        self.host = host
        self.port = port
        self.serverID = serverID
        self.serverPort = serverPort
        self.__connect()
        
    def __connect(self):
        self.server = (self.serverID, self.serverPort)
        self.socketHandle = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socketHandle.bind((self.host, self.port))
        
    def send(self, data):      
        threading.Thread(target=self._sendData, args=(data,)).start()
       
    def _sendData(self, data):
        try:
            self.socketHandle.sendto(str.encode(json.dumps(data)), self.server)           
        except Exception as e:
            pass
    
    def close(self):
        self.socketHandle.close()
        

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    
    
def listen(toSpeak=None, wake=False):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        if toSpeak:
            speak(toSpeak)
        while True:
            try:
                if not wake:
                    audio = recognizer.listen(source, timeout=5)
                if wake:
                    audio = recognizer.listen(source)
                if toSpeak:
                    speak("Okay")
                break
            except Exception as e:
                continue
    try:
        outText = recognizer.recognize_google(audio, language = 'en-IN')
        return outText.lower().strip()
    
    except sr.UnknownValueError: 
        return ''
    
    except Exception as e:
        print(e)
        return ''

def checkForCommand(text):
    global musicClass, misc
    commands = {
        musicClass.play : [
            'play a song',
            'play',
            'play song',
            'play music'
        ],
        musicClass.pause : [
            'pause',
            'pause song',
            'pause music',
            'pause the music',
            'pause the song',
        ],
        musicClass.resume : [
            'resume',
            'resume song',
            'resume the song',
            'resume the music'
        ],
        musicClass.stop : [
            'stop',
            'stop playing',
            'stop song',
            'stop the song',
            'stop the music'
        ],
        misc.getTime : [
            'time',
            'get time',
            'what is the time',
            'whats time'
        ],
        misc.getDay : [
            'what day is it',
        ],
        misc.getWiki : [
            'wiki',
            'wikipedia',
            'search'
        ],
        misc.getDate : [
            'date',
            "whats's today",
            'what day is it'
        ],
        misc.getWeather : [
            'weather',
            'today weather',
            'weather outside'
        ],
         
    }
    
    for function, keywords in commands.items():
        temp = text.strip()
        for key in  keywords:
            if temp.find(key) > -1:
                return function
    else:
        return None

## ---------------------- > MAIN DECLARATION < ---------------------- ##

botName = "alexa".lower()
USER_NAME = 'BDG'
USER_ID   = 'IN069' 
CITY_NAME = 'Coimbatore'
SERVER_IP = '192.168.243.124'
CLIENT_IP = '192.168.243.117'

wakeReplies = [
    "Yes, I'm Listening", 
    "I hear you",
    "I got you",
    "Yes, Tell me"
    ]

socketConn = connectSocket(serverID=SERVER_IP, host=CLIENT_IP)
musicClass = musicYoutube(listen, socketConn, USER_ID, USER_NAME)
misc = smallFunction(listen, speak, socketConn, USER_ID, USER_NAME, CITY_NAME)

if __name__ == "__main__":
    print("[Code Started]\n")
    
    while True:
        text = listen(wake=True)
        print(text)
        if text.count(botName) > 0:
            socketConn.send({
                    'id' : USER_ID,
                    'user' : USER_NAME,
                    'data' : 'WOKE_WORD'
                })
            speak(random.choice(wakeReplies))
            text = listen()
            print(text)
            outFunction = checkForCommand(text)
            
            if outFunction is not None:
                socketConn.send({
                    'id' : USER_ID,
                    'user' : USER_NAME,
                    'data' : text
                })
                outFunction()
