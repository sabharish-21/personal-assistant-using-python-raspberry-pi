from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import userLog
import datetime as dt
import random


# Create your views here.
def homepage(request):
    data = userLog.objects.all()
    outData = []
    for i in range(1, len(data) + 1):
        outData.append([i, data[i - 1]])
    return render(request, 'home.html', {'data': outData})


def ajax_reload_log(request):
    try:
        query = str(request.GET.get('search', '')).strip()
        data = ''
        if query == '':
            data = userLog.objects.all()

        else:
            listA = []
            for _ in userLog.objects.filter(userName__contains=query):
                listA.append(_)
            for _ in userLog.objects.filter(action__contains=query):
                listA.append(_)
            for _ in userLog.objects.filter(dateTime__contains=query):
                listA.append(_)
            for _ in userLog.objects.filter(userID__contains=query):
                listA.append(_)

            data = []
            for i in listA:
                if i.logID not in data:
                    data.append(i)

        outData = []
        for i in range(1, len(data) + 1):
            outData.append([i, {
                'userID': data[i - 1].userID,
                'userName': data[i - 1].userName,
                'dateTime': data[i - 1].dateTime,
                'action': data[i - 1].action,
            }])

        return JsonResponse({'obj': outData})

    except Exception as e:
        print(e)
        return JsonResponse({'obj': False})


def getWeather(city_name):
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


@csrf_exempt
def fetchWeather(request):
    if request.method == "POST":
        data = dict(request.POST)
        out = getWeather(data['weather_cityName'][0])
        return JsonResponse({'data': out})


@csrf_exempt
def putRequest(request):
    if request.method == 'POST':
        data = dict(request.POST)
        date = str(dt.datetime.today()).split('.')[0]
        userLog(userName=data['user'][0], userID=data['id'][0], action=data['data'][0], dateTime=date,
                logID=generateLogID()).save()
        return JsonResponse({})


def generateLogID():
    takenIDs = [j.logID for j in userLog.objects.all()]
    id_ = random.randint(100000, 999999)
    if id_ not in takenIDs:
        return id_
    else:
        return generateLogID()
