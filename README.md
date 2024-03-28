# GyanGrove Assignment - Event Management System
This application provides endpoints for managing events and retrieving events based on user location and date.

# Technologies Used
  - FastAPI
  - SQLAlchemy
  - MySQL

# Design Decision

  Adapter Design Pattern
- Used this design pattern to convert the model from pydantic model to SQLAlchemy model.
    
# Setup Instructions

## Install and run directly
  1. Clone the repository.
  2. Install dependencies using `pip install -r requirements.txt`
  3. Set up a MySQL database and update the `connection_string` variable in main.py with your database credentials.
  4. Set up an environment variable `weatherAPIKey` with the API key for the weather service.
  5. Run the FastAPI server using `uvicorn main:app --reload`. Remove `--reload` for non-developmental uses.

## Run using docker-compose
1. Run `docker-compose -f docker-compose.yml up -d --build`

# Breakdown

The project is broken down into 3 major components:
1. Database model of events
2. API endpoints 
3. Dockerizing and hosting

# Endpoints

1. Upload Event Data
     ```
     a. Method: POST
     b. Endpoint: /upload
     c. Description: Uploads a CSV file containing event data
     d. Request Body: Form data with a single file upload parameter named file.
     e. Response: JSON status, message indicating success or failure.

     {
          status: 200,
          message: Successfully uploaded filename.csv
     }
     ```

2. Add Event
     ```
     a. Method: POST
     b. Endpoint: /add_event
     c. Description: Adds a single event to the database.
     d. Request Body:
          - eventName: String (name of the event).
          - cityName: String (name of the city).
          - date: Date (date of the event).
          - time: Time (time of the event).
          - latitude: Float (latitude coordinate of the event location).
          - longitude: Float (longitude coordinate of the event location).

     {
          eventName: test,
          cityName: Mumbai,
          date: 25-04-2022,
          time: 12:24:21,
          latitude: 20.3423,
          longitude: 23.43243
     }

     e. Response: JSON status and message indicating success or failure.

     {
          status: 200,
          message: Event added successfully
     }
     ```

4. Show Events
     ```
     a. Method: POST
     b. Endpoint: /show_events
     c. Description: Retrieves events occurring within the next 14 days from the specified date, sorted by date, with pagination.
     d. Request Parameters:
          - latitude: Float (latitude coordinate of the user's location).
          - longitude: Float (longitude coordinate of the user's location).
          - startDate: Date (start date to search events).
          - page: Integer (page number for pagination).

     {
          latitude: 70.25646,
          longitude: 52.656,
          startDate: 2024-03-28,
          page: 5
     }

     e. Response:
          - events: List of dictionaries containing event details.
          - page: Integer (current page number).
          - pageSize: Integer (number of events in the current page).
          - totalEvents: Integer (total number of events matching the criteria).
          - totalPages: Integer (total number of pages).
     
     {
     "status": 200,
     "events": [
          {
               "event_name": "Off father",
               "city_name": "Lake Kirsten",
               "date": "2024-04-08",
               "distance_km": 11983.709707613507,
               "weather": "Cloudy 0C"
          },
          {
               "event_name": "Weight perform loss",
               "city_name": "Bridgetmouth",
               "date": "2024-04-10",
               "distance_km": 2886.3419847462787,
               "weather": "Rainy 8C"
          },
          {
               "event_name": "Peace seem west",
               "city_name": "Curtisville",
               "date": "2024-04-10",
               "distance_km": 15150.348506273958,
               "weather": "Windy 3C"
          },
          {
               "event_name": "Nor particularly practice",
               "city_name": "Lake Perryville",
               "date": "2024-04-10",
               "distance_km": 14862.82267475563,
               "weather": "Windy 15C"
          },
          {
               "event_name": "Candidate",
               "city_name": "East Carolyn",
               "date": "2024-04-10",
               "distance_km": 17830.357634318,
               "weather": "Cloudy 3C"
          },
          {
               "event_name": "Husband pretty ago",
               "city_name": "Meghanside",
               "date": "2024-04-10",
               "distance_km": 5323.647821554792,
               "weather": "Snowy 16C"
          },
          {
               "event_name": "Organization party notice",
               "city_name": "New Greg",
               "date": "2024-04-10",
               "distance_km": 17326.972047849726,
               "weather": "Rainy 25C"
          },
          {
               "event_name": "Than sort work",
               "city_name": "Howardton",
               "date": "2024-04-10",
               "distance_km": 14622.307366888686,
               "weather": "Sunny 15C"
          },
          {
               "event_name": "Perhaps lead determine",
               "city_name": "Lake Andrew",
               "date": "2024-04-11",
               "distance_km": 13613.467809653577,
               "weather": "Cloudy 17C"
          }
     ],
     "page": 5,
     "pageSize": 9,
     "totalEvents": 49,
     "totalPages": 5
     }
     ```

5. Show Events (Direct Database Query)
     ```
     a. Method: POST
     b. URL: /show_events_page_by_db
     c. Description: Retrieves events occurring within the next 14 days from the specified date, sorted by date, with pagination using direct database query.
     d. Request Body: Same as show_events.
     e. Response: Same as show_events.
     ```

# Dockerizing and Hosting on AWS
  1. Dockerize the application
  2. Build and run the docker image
  3. Host this image on EC2, pull code from github using deploy keys, install docker/git on ec2, edit inbound rules to access port 80.
