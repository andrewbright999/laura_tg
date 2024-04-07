import requests, asyncio, logging
import time
from datetime import datetime, date, timedelta
from LauraGpt.search import get_aiata, get_data


logging.basicConfig(level=logging.INFO)


APIKEY = "fd080359-0a35-447d-b578-81bc767611fe"


mounts = {"01": "янв.","02": "февр.","03":"марта","04": "апр.","05": "мая","06": "июня","07": "июля","08": "авг.","09": "сент.","10": "окт.","11": "нояб.","12": "дек."}
visa = {"Шенгенская ":["Мадрид","Варшава","Лиссабон", "Амстердам","Париж","Брюссель","Цюрих","Рим","Лондон","Милан","Цюрих","Барселона","Лиссабон","хельсинки","Франкфурт-на-Майне"],
        "Туристическая":["Каир", "Аддис-Абеба"],
        "Американская":["Нью‑Йорк","Чикаго","Шарлотт","Майами", "Бостон", "Даллас"],
        "Канадская":["Торонто"]}

visa_list = []
for i in visa.values():
    visa_list.extend(i)


# ["Аддис-Абеба","Мадрид","Варшава","Лиссабон", "Амстердам","Париж","Брюссель","Цюрих","Рим","Лондон","Милан","Цюрих","Барселона","Лиссабон","хельсинки","Каир","Нью‑Йорк","Чикаго","Шарлотт","Майами", "Бостон", "Даллас","Торонто","Франкфурт-на-Майне"]

from_city = "Moscow"
to_city = "Аргентина"
flight_date = date(2024, 4, 9)

from_station_iata = "AER"
to_station_iata = "SCL"
to_station_iata = "TNR"


def get_durotation_flight(departure,arival):
    flight_time = datetime.strptime(arival, "%Y-%m-%dT%H:%M:%S%z") - datetime.strptime(departure, "%Y-%m-%dT%H:%M:%S%z")
    flight_sec = str(flight_time.total_seconds())
    return flight_sec


def magic_time(departure,arival):
    flight_time = datetime.strptime(arival, "%Y-%m-%dT%H:%M:%S%z") - datetime.strptime(departure, "%Y-%m-%dT%H:%M:%S%z")
    departure = beuty_date(datetime.strptime(departure, "%Y-%m-%dT%H:%M:%S%z").strftime( "%H:%M %d.%m"))
    arival = beuty_date(datetime.strptime(arival, "%Y-%m-%dT%H:%M:%S%z").strftime( "%H:%M %d.%m"))
    flight_time = str(flight_time)
    if "day" in flight_time:
        flight_time = flight_time.split(",")
        days = flight_time[0].replace(" days", "дн").replace("day", "дн")
        flight_time = flight_time[1].removesuffix(":00").replace(":","ч ", 1)
        if flight_time.endswith("00"):
            flight_time = flight_time.replace(" 00","")
        else: 
            flight_time = flight_time + "мин"
        flight_time = days + flight_time
    else:
        flight_time = flight_time.removesuffix(":00").replace(":","ч ", 1)
        if flight_time.endswith("00"):
            flight_time.replace("00","")
        else: 
            flight_time = flight_time + "мин"
    return departure, arival, flight_time


def beuty_date(date):
    date = date.split(" ")
    time = date[0]
    date = date[1]
    date = date.split(".")
    day = date[0]
    mounth = date[1]
    day = str(int(day))
    mounth = mounts[mounth]
    return day + " " + mounth + " " + time 


def seconds_to_hours(sec):
    time_format = time.strftime("%H:%M", time.gmtime(sec))
    time_format = time_format.split(":")
    hours = int(time_format[0])
    minuts = int(time_format[1])
    string_time = ""
    if minuts != 0:
        string_time = str(hours) + "ч " + str(minuts) + "мин"
    else:
        string_time = str(hours) + "ч "
    return string_time


def get_stations():
    url = (f"https://api.rasp.yandex.net/v3.0/nearest_stations/?apikey={APIKEY}&format=json&lat=43.585472&lng=39.723098&distance=50&lang=ru_RU&transport_types=plane")
    res = requests.get(url)
    data = res.json()
    print(data)


# Нужно получить самый быстрый маршрут в целом и самый быстрый без визы.
def search(from_station_iata,to_station_iata, flight_date):
    for from_station in from_station_iata:
        for to_station in to_station_iata:
            url = (f"https://api.rasp.yandex.net/v3.0/search/?apikey={APIKEY}&format=json&from={from_station}&system=iata&to={to_station}&transfers=True&lang=ru_RU&result_timezone=Europe/Moscow&page=1&date={flight_date}")
            res = requests.get(url)
            print(res)
            data = res.json()
            durations = []
            visas = []
            for item in data["segments"]:
                flight_sec = float(get_durotation_flight(item['departure'],item['arrival']))
                durations.append(flight_sec)
                if item["has_transfers"] == True: # Если есть пересадки
                    points = []
                    for i in range(len(item["details"])): # Перебор всех пересадок 
                        details = item["details"][i]
                        if (i % 2 == 0):
                            points.append(details["from"]["title"])
                            points.append(details["to"]["title"])
                    if len( list(set(points) & set(visa_list))) > 0:
                        visas.append("Visa")
                    else:
                        visas.append("None") 
    indices = [i for i, x in enumerate(visas) if x == "None"]
    free_flights = []
    for i in indices:
        free_flights.append(durations[i])
    if len(free_flights) > 0: 
        free_fastest = durations.index(min(free_flights))
    else:
        free_fastest = "None"
    fastest = durations.index(min(durations))
    if free_fastest != "None":
        if free_fastest == fastest:
            return [data["segments"][free_fastest]]
        else:
            return [data["segments"][free_fastest],data["segments"][fastest]]
    elif visas.count("Visa") == 0:
        return [data["segments"][fastest]]
    else:
        return [data["segments"][fastest]]


def create_messages(best_flights):
    messages = []
    for item in best_flights:
        departure_time, arrival_time, flight_time = magic_time(item['departure'],item['arrival'])
        if item["has_transfers"] == True: # Если есть пересадки
            points = []
            durotion = []
            company = []
            numbers = []
            for i in range(len(item["details"])): # Перебор всех пересадок 
                details = item["details"][i]
                if (i % 2 == 0):
                    points.append(details["from"]["title"]) 
                    points.append(details["to"]["title"])
                    numbers.append(details["thread"]["number"])
                    company.append(details["thread"]["carrier"]["title"])
                else:
                    durotion.append(seconds_to_hours(details["duration"]))
            print(company,numbers)
            message = f"""
<b>Вылет:</b> <code>{points.pop(0)}</code> - {departure_time} 
     <i>{company.pop(0)}</i> <b>{numbers.pop(0)}</b> 
<b>Прилет:</b> <code>{points.pop(-1)}</code> - {arrival_time}
<b>Время полета:</b> <u>{flight_time}</u>
<b>Пересадки:</b>\n"""
            points = points[::2]
            for i in range(len(points)):
                if points[i] not in visa_list:
                    message = message + f"""    <code>{points[i]}</code> {durotion[i]}\n"""
                else: 
                    for type in visa:
                        if points[i] in visa[type]:
                            print(visa[type])
                            message = message + f"""    <code>{points[i]}</code> {durotion[i]} ({type} виза)\n"""
                message = message + f"""    <b>Вылет:</b> <i>{company[i]}</i> <b>{numbers[i]}<b>\n"""
            messages.append(message)
        else:
            title = item['thread']['title']
            number = item['thread']['number']
            company = item["thread"]["carrier"]["title"]
            title = title.split(" — ", 1)
            message = f"""
<b>Вылет:</b> <code>{title[0]}</code> - {departure_time} 
      <i>{company}</i> <b>{number}</b> 
<b>Прилет:</b> <code>{title[-1]}</code> - {arrival_time}
Время полета: <u>{flight_time}</u>\n"""
            messages.append(message)
    return messages     
    

async def search_flights(message_text):
    search_data = await get_data(message_text)
    print(search_data)
    from_iata = await get_aiata(search_data[0])
    to_iata = await get_aiata(search_data[1])
    print(from_iata)
    print(to_iata)
    search_date = search_data[-1].lower().replace(" ", '')
    if ("today" in search_date) or ("сегодня" in search_date):
        flight_date = datetime.now().isoformat()
    elif ("tomorrow" in search_date) or ("завтра" in search_date):  
        today = date.today()
        flight_date = (today + timedelta(days=1)).isoformat()
    else:
        search_date = search_date.split("-")
        year = datetime.now().year
        search_date = date(year, int(search_date[1]), int(search_date[2]))
        flight_date = search_date.isoformat()
    print(flight_date)
    best_flights = search(from_iata, to_iata, flight_date)
    answer = create_messages(best_flights)
    return answer

res = asyncio.run(search_flights("из сочи в чили на завтра"))

print(*res)