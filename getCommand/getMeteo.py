from weather import Weather, Unit

import os

def getWeathercli(loc):
    loc = loc.replace(" ", "-")
    cmd = "curl http://wttr.in/"+loc+".png\?3\&lang\=fr --output weather/"+loc+".png"
    os.system(cmd)
    return "weather/"+loc+".png"

def getWeather(loc, day):
    wth = Weather(unit=Unit.CELSIUS)
    location = wth.lookup_by_location(loc)

    text_weather = " ------- "+loc + " -------\n"
    if (location != ""):
        if (day == 0):
            condition = location.condition
            text_weather += "Date : "+ condition.date[5:-13] + "\n"
            text_weather += "Condition : "+condition.text+"\n"
            text_weather += "Temp : "+ condition.temp + "°C\n"

        else:
            ft = location.forecast
            if (int(day) <= len(ft)):
                for i in range(0, int(day)):
                    text_weather += "Date : "+ft[i].date + "\n"
                    text_weather += "Condition : "+ft[i].text +"\n"
                    text_weather += "Min Temp : "+ft[i].low +"°C\n"
                    text_weather += "Max Temp : "+ft[i].high +"°C\n"
                    text_weather += "~~~~~~~~~~\n"
            else:
                for f in ft:
                    text_weather += "Date : "+f.date + "\n"
                    text_weather +="Condition : "+f.text+"\n"
                    text_weather += "Min Temp : "+f.low+"°C\n"
                    text_weather += "Max Temp : "+f.high+"°C\n"
                    text_weather += "~~~~~~~~~~\n"
    return text_weather