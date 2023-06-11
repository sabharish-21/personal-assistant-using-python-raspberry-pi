from datetime import datetime
import wikipedia
import requests
import json
import time

class smallFunction:
    def __init__(self, listen, speak, socketConn, USER_ID, USER_NAME, CITY_NAME):
        self.USER_ID = USER_ID
        self.USER_NAME = USER_NAME
        self.listen   = listen
        self.speak  = speak
        self.socket = socketConn
        self.cityName = CITY_NAME
        
    def getTime(self):
        self.socket.send({
                    'id' : self.USER_ID,
                    'user' : self.USER_NAME,
                    'data' : 'time'
                })
        
        currentTime = datetime.now().strftime("%H:%M:%S")
        self.speak(str(currentTime))
    
    def getDay(self):
        self.socket.send({
                    'id' : self.USER_ID,
                    'user' : self.USER_NAME,
                    'data' : 'day'
                })
        today = datetime.today().strftime("%A")
        self.speak(f"Today is {str(today)}")
    
    def getDate(self):
        toDate = datetime.date(datetime.now()).strftime("%B %d, %Y")
        self.socket.send({
                    'id' : self.USER_ID,
                    'user' : self.USER_NAME,
                    'data' : 'date'
                })
        self.speak(f"Todays Date is {str(toDate)}")
        
    def getWiki(self):
        query = self.listen('What do you want to know about ?')
        self.socket.send({
                    'id' : self.USER_ID,
                    'user' : self.USER_NAME,
                    'data' : f'wiki -> {query}'
                })
        try:
            result = wikipedia.summary(query, sentences = 2)
            self.speak(result)
        except Exception as e:
            self.speak(f"Couldn't find anything on wikipedia for {query}")

    def __getWeather(self, city_name):
        api_key = "91206d855c7f6fe064568cccc27964ff"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + 'd850f7f52bf19300a9eb4b0aa6b80f0d' + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()

        if x["cod"] != "404":
            y = x["main"]
            current_temperature = round(float(y["temp"]) - 273, 2)
            z = x["weather"]
            weather_description = z[0]["description"]
            return f"The current temperature in celcius is {current_temperature} and the weather is {weather_description}."

        else:
            return 'There was an error finding the weather. Try again later.'

    def getWeather(self):
        data = {
            'type' : 'request',
            'weather_cityName' : self.cityName
        }
        
        data = __getWeather(self.cityName)
        # response = requests.post('http://127.0.0.1:8000/getweather', data=data)
        # data = dict(response.json())['data']
        self.speak(data)
        
if __name__ == "__main__":
    
    # Testing Purpose
    from tara import listen, speak, socketConn, USER_ID, USER_NAME, CITY_NAME
    handle = smallFunction(listen, speak, socketConn, USER_ID, USER_NAME, CITY_NAME)
    # handle.getWeather()