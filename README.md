# GyanGrove Assignment - Event Management System
This application provides endpoints for managing events and retrieving events based on user location and date.

# Technologies Used
  - FastAPI
  - SQLAlchemy
  - MySQL
    
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

1. Upload Event Data
     a. Method: POST
     b. URL: '/upload'
     c. Description: Uploads a CSV file containing event data.
     d. Request Body: Form data with a single file upload parameter named file.
     e. Response: JSON message indicating success or failure.

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

5. 

Breaking down the tasks further:
1. Database model
  a. Model definition for events
2. API endpoints
  a. 
Integration Ace code editor for leveraging syntax highlighting and other cool editor features
  b. Extract code from this editor and using subprocess run this code to test against our correct solution
  c. Give support to users to see testcases and their output along with expected output. Do the same for custom testcase input.
4. Dockerizing and hosting
  a. Dockerize the application
  b. Build and run the docker image
  c. Host this image on EC2, pull code from github using deploy keys, install docker/git on ec2, edit inbound rules to access port 8000.
