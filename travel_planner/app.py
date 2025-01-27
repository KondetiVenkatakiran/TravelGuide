# app.py  
import os  
from flask import Flask, request, jsonify, render_template  
import requests  
from datetime import datetime  
from dotenv import load_dotenv  

# Load environment variables  
load_dotenv()  

# Flask application setup  
app = Flask(__name__)  

# Airtable configuration  
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')  
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')  
AIRTABLE_TABLE_NAME = 'TravelPreferences'  

# Google Calendar API configuration  
GOOGLE_CALENDAR_API_KEY = os.getenv('GOOGLE_CALENDAR_API_KEY')  
# OAuth setup for Google Calendar will be covered later.  

# Function to save preferences to Airtable  
def save_preferences_to_airtable(preferences):  
    url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'  
    headers = {  
        'Authorization': f'Bearer {AIRTABLE_API_KEY}',  
        'Content-Type': 'application/json',  
    }  
    data = {  
        "fields": preferences  
    }  
    response = requests.post(url, headers=headers, json=data)  
    return response.json()  

# Function to create a calendar event  
def create_google_calendar_event(event_details):  
    # This will require OAuth2.0 and additional setup  
    # Placeholder for Google Calendar integration  
    pass  

@app.route('/create_trip', methods=['POST'])  
def create_trip():  
    trip_data = request.json  

    # Save preferences to Airtable  
    preferences = {  
        "Destination": trip_data['destination'],  
        "Start Date": trip_data['start'],  
        "End Date": trip_data['end'],  
        "Budget": trip_data['budget'],  
        "Preferences": trip_data['preferences'],  
    }  
    
    preferences_response = save_preferences_to_airtable(preferences)  

    # Event creation (optional) - Uncomment and implement when OAuth set up  
    # create_google_calendar_event({  
    #     "summary": trip_data['destination'],  
    #     "start": {"dateTime": trip_data['start']},  
    #     "end": {"dateTime": trip_data['end']},  
    # })  

    return jsonify({"message": "Trip created successfully!", "preferences": preferences_response}), 201  

@app.route('/')  
def index():  
    return render_template('index.html')  

if __name__ == '__main__':  
    app.run(debug=True)