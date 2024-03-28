from fastapi import FastAPI, File, UploadFile
import requests
import csv
import mysql.connector
from sqlalchemy import create_engine
from models import EventModel, EventAdapter
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import traceback
from uuid import uuid4
from math import radians, sin, cos, sqrt, asin
import math
from datetime import date, time



app = FastAPI()

connection_string = "mysql+mysqlconnector://root:password@mysql-local:3306/gyangrove"
engine = create_engine(connection_string, echo=True)

weatherAPIUrl = "https://gg-backend-assignment.azurewebsites.net/api/Weather"
weatherAPIKey = "KfQnTWHJbg1giyB_Q9Ih3Xu3L9QOBDTuU5zwqVikZepCAzFut3rqsg=="

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
        pushToDb(file.filename)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        await file.close()

    return{"message": f"Successfully uploaded {file.filename}"}

def pushToDb(filename: str):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                pydanticEvent = EventModel(
                    eventId=uuid4(),
                    eventName = row['event_name'],
                    cityName = row['city_name'],
                    date = row['date'],
                    time = row['time'],
                    latitude = float(row['latitude']),
                    longitude = float(row['longitude']),
                )
                eventAdapter = EventAdapter(pydanticEvent)
                event = eventAdapter.to_event()
                with Session(engine) as session:
                    session.add(event)
                    session.commit()
            except Exception as exception:
                traceback.print_exc()
                raise exception


def getWeather(cityName, date):
    params = {
        "code": weatherAPIKey,
        "city": cityName,
        "date": date
    }
    response = requests.get(weatherAPIUrl, params=params)
    if response.status_code == 200:
        return response.json()["weather"]     
    else:
        return f"Error: {response.status_code}"


def getDistance(lat1, lon1, lat2, lon2):
    # Earth's radius in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    
    # Calculate the distance
    distance = R * c
    
    return distance

@app.post('/add')
def addEvent(eventName:str, cityName: str, date: date, time: time, latitude: float, longitude: float):
    try:
        pydanticEvent = EventModel(
            eventId=uuid4(),
            eventName = eventName,
            cityName = cityName,
            date = date,
            time = time,
            latitude = latitude,
            longitude = longitude
        )
        eventAdapter = EventAdapter(pydanticEvent)
        event = eventAdapter.to_event()
        with Session(engine) as session:
            session.add(event)
            session.commit()
    except Exception as exception:
        traceback.print_exc()
        raise exception

    

@app.post("/show_events")
def show_events(latitude: float, longitude: float, startDate: date, page: int):
    try:
        with engine.connect() as connection:
            offset = (page-1) * 10
            args = {
                'startdate': startDate
            }
            eventList = []
            statement = text(f"""SELECT * FROM event WHERE date BETWEEN :startdate AND DATE_ADD(:startdate, INTERVAL 14 DAY) ORDER BY date""")
            eventData = connection.execute(statement, parameters=args)
            for event in eventData:
                eventLatitude =  event.latitude
                eventLongitude = event.longitude
                eventCityName = event.cityName
                eventDate = event.date
                event_data = {
                    "event_name": event.eventName,
                    "city_name": event.cityName,
                    "date": event.date,
                    "distance_km": getDistance(latitude, longitude, eventLatitude, eventLongitude)
                }
                eventList.append(event_data)
            
            totalEvents = len(eventList)
            totalPages = math.ceil(totalEvents/10)
            eventList = eventList[offset:offset+10]
            for event in eventList:
                event["weather"] = getWeather(event["city_name"], event["date"])
                    
            return {
                "events": eventList,
                "page": page,
                "pageSize": len(eventList),
                "totalEvents": totalEvents,
                "totalPages": totalPages
            }
           

    except Exception as e:
        return {"message": f"Error: {e}"}

@app.post("/show_events_page_by_db")
def show_events_page_by_db(latitude: float, longitude: float, startDate: date, page: int):
    try:
        with engine.connect() as connection:
            offset = (page-1) * 10
            args = {
                'startdate': startDate
            }
            eventList = []
            countText = text("""SELECT COUNT(*) FROM event WHERE date BETWEEN :startdate AND DATE_ADD(:startdate, INTERVAL 14 DAY)""")
            count = connection.execute(countText, parameters=args)
            totalEvents = None
            for item in count:
                totalEvents = item[0]
                break

            totalPages = math.ceil(totalEvents/10)
            args['offset'] = offset
            statement = text("""SELECT * FROM event WHERE date BETWEEN :startdate AND DATE_ADD(:startdate, INTERVAL 14 DAY) ORDER BY date LIMIT 10 OFFSET :offset""")
            eventData = connection.execute(statement, parameters=args)
            for event in eventData:
                eventLatitude =  event.latitude
                eventLongitude = event.longitude
                eventCityName = event.cityName
                eventDate = event.date
                event_data = {
                    "event_name": event.eventName,
                    "city_name": event.cityName,
                    "date": event.date,
                    "weather": getWeather(eventCityName, eventDate),
                    "distance_km": getDistance(latitude, longitude, eventLatitude, eventLongitude)
                }
                eventList.append(event_data)
            
            
            return {
                "events": eventList,
                "page": page,
                "pageSize": len(eventList),
                "totalEvents": totalEvents,
                "totalPages": totalPages
            }

    except Exception as e:
        return {"message": f"Error: {e}"}

