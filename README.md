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
  1. Clone the repository.
  2. Install dependencies using 'pip install -r requirements.txt'.
  3. Set up a MySQL database and update the connection_string variable in main.py with your database credentials.
  4. Set up an environment variable weatherAPIKey with the API key for the weather service.
  5. Run the FastAPI server using 'uvicorn main:app --reload'.

The project was broken down into 3 major components:
1. Database model of events
2. API endpoints 
3. Dockerizing and hosting

# Endpoints

1. Upload Event Data\
     a. Method: POST\
     b. URL: '/upload'\
     c. Description: Uploads a CSV file containing event data.\
     d. Request Body: Form data with a single file upload parameter named file.\
     e. Response: JSON message indicating success or failure.\

2. Add Event
     a. Method: POST
     b. URL: /add
     c. Description: Adds a single event to the database.
     d. Request Body:
          - eventName: String (name of the event).
          - cityName: String (name of the city).
          - date: Date (date of the event).
          - time: Time (time of the event).
          - latitude: Float (latitude coordinate of the event location).
          - longitude: Float (longitude coordinate of the event location).
     e. Response: JSON message indicating success or failure.

3. Show Events
     a. Method: POST
     b. URL: /show_events
     c. Description: Retrieves events occurring within the next 14 days from the specified date, sorted by date, with pagination.
     d. Request Body:
          - latitude: Float (latitude coordinate of the user's location).
          - longitude: Float (longitude coordinate of the user's location).
          - startDate: Date (start date to search events).
          - page: Integer (page number for pagination).
     e. Response:
          - events: List of dictionaries containing event details.
          - page: Integer (current page number).
          - pageSize: Integer (number of events in the current page).
          - totalEvents: Integer (total number of events matching the criteria).
          - totalPages: Integer (total number of pages).

4. Show Events (Direct Database Query)
     a. Method: POST
     b. URL: /show_events_page_by_db
     c. Description: Retrieves events occurring within the next 14 days from the specified date, sorted by date, with pagination using direct database query.
     d. Request Body: Same as show_events.
     e. Response: Same as show_events.

# Dockerizing and Hosting on AWS
  a. Dockerize the application
  b. Build and run the docker image
  c. Host this image on EC2, pull code from github using deploy keys, install docker/git on ec2, edit inbound rules to access port 80.
