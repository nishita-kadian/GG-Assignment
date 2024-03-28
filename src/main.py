from fastapi import FastAPI, File, UploadFile
import requests
import csv
import mysql.connector
from sqlalchemy import create_engine
from models.event import EventModel, EventAdapter
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import traceback
from uuid import uuid4
from math import radians, sin, cos, sqrt, asin
import math
from datetime import date, time
import os
from fastapi import HTTPException



app = FastAPI()

connection_string = "mysql+mysqlconnector://root:password@mysql-local:3306/gyangrove"
engine = create_engine(connection_string, echo=True)

weatherAPIUrl = "https://gg-backend-assignment.azurewebsites.net/api/Weather"
weatherAPIKey = os.environ['weatherAPIKey']

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    """
        API to upload CSV datafile

            Parameters:
                    file (File): File uploaded for processing

            Returns:
                    status (int): HTTP status code
                    message (str): Message related to processing
    """
    try:
        contents = await file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
        pushToDb(file.filename)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        await file.close()

    return{"status": 200, "message": f"Successfully uploaded {file.filename}"}

def pushToDb(filename: str):
    """
        Persist data from the CSV file to persistant storage 

            Parameters:
                    filename (str): Local filename to be processed

            Returns:
                    None
    """
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
                raise HTTPException(status_code=500, detail=exception)


def getWeather(cityName, date):
    """
        Calls weather API provided by GyanGrove

            Parameters:
                    cityName (str): Name of the city to get weather
                    date (date): Date of weather

            Returns:
                    weather (str): String with details like "Cloudy 17C"
    """
    params = {
        "code": weatherAPIKey,
        "city": cityName,
        "date": date
    }
    response = requests.get(weatherAPIUrl, params=params)
    if response.status_code == 200:
        return response.json()["weather"]     
    else:
        raise HTTPException(status_code=500, detail=f"Error, got response code from weather API: {response.status_code}")


def getDistance(lat1, lon1, lat2, lon2):
    """
        Calculate distance using Haversine formula between two points on Earth.

            Parameters:
                    lat1 (float): Latitude of first point
                    lon1 (float): Longitude of first point
                    lat2 (float): Latitude of second point
                    lon2 (float): Longitude of second point

            Returns:
                    distance (float): Distance in kilometers
    """

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

@app.post('/add_event')
def addEvent(eventName:str, cityName: str, date: date, time: time, latitude: float, longitude: float):
    """
        Add a single event to persistant storage. 

            Parameters:
                    eventName (str): Name of the event
                    cityName (str): Name of the city
                    date (date): Date of the event
                    time (time): Time of the event
                    latitude (float): Latitude of the city
                    longitude (float): Longitude of the city

            Returns:
                    status (int): HTTP status code
                    message (str): Message related to the endpoint
    """
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
        return {"status": 200, "message": "Event added succesfully"}
    except Exception as exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=exception)

    

@app.get("/show_events")
def show_events(latitude: float, longitude: float, startDate: date, page: int):
    """
        Show events 14 days from the start date with distance from latitude and longitude point provided
        in this paginated API. The data is paginated after getting all the data from the DB.

            Parameters:
                    latitude (float): Latitude of the city
                    longitude (float): Longitude of the city
                    startDate (date): 14 days from which date
                    page (int): Requested page number of the paginated response 
      
            Returns:
                    status (int): 200
                    events (List): List of events, each containing
                        event_name (str): Name of the event
                        city_name (str): Name of the city
                        date (str): Date of the event
                        distance_km (float): Distance of the event city from given latitude and longitude
                        weather (str): Weather of the listed event city
                    page (int): Page number
                    pageSize (int): Entries in this page
                    totalEvents (int): Total number of events
                    totalPages (int): Total number of pages for the events, give a full page contains 10 entries
    """
    try:
        with engine.connect() as connection:
            offset = (page-1) * 10
            args = {
                'startdate': startDate
            }
            eventList = []
            statement = text(f"""SELECT * FROM event WHERE date BETWEEN :startdate AND DATE_ADD(:startdate, INTERVAL 14 DAY) ORDER BY date, time""")
            eventData = connection.execute(statement, parameters=args)
            for event in eventData:
                eventLatitude =  event.latitude
                eventLongitude = event.longitude
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
                "status": 200,
                "events": eventList,
                "page": page,
                "pageSize": len(eventList),
                "totalEvents": totalEvents,
                "totalPages": totalPages
            }
           

    except Exception as exception:
        raise HTTPException(status_code=500, detail=exception)

@app.get("/show_events_page_by_db")
def show_events_page_by_db(latitude: float, longitude: float, startDate: date, page: int):
    """
        Show events 14 days from the start date with distance from latitude and longitude point provided
        in this paginated API. The API is paginated at the DB level.

            Parameters:
                    latitude (float): Latitude of the city
                    longitude (float): Longitude of the city
                    startDate (date): 14 days from which date
                    page (int): Requested page number of the paginated response 
      
            Returns:
                    status (int): 200
                    events (List): List of events, each containing
                        event_name (str): Name of the event
                        city_name (str): Name of the city
                        date (str): Date of the event
                        distance_km (float): Distance of the event city from given latitude and longitude
                        weather (str): Weather of the listed event city
                    page (int): Page number
                    pageSize (int): Entries in this page
                    totalEvents (int): Total number of events
                    totalPages (int): Total number of pages for the events, give a full page contains 10 entries
    """
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
            statement = text("""SELECT * FROM event WHERE date BETWEEN :startdate AND DATE_ADD(:startdate, INTERVAL 14 DAY) ORDER BY date, time LIMIT 10 OFFSET :offset""")
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

    except Exception as exception:
        raise HTTPException(status_code=500, detail=exception)
