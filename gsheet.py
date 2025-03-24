import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import pytz
import random 
import pandas as pd
import pickle

# Set up the credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]


Token=''
# Open the file in read-binary mode
with open("Token.pkl", "rb") as file:
    Token = pickle.load(file)
#creds = ServiceAccountCredentials.from_json_keyfile_name(file, scope)
#creds=ServiceAccountCredentials.from_json_keyfile_dict(Token)
#client = gspread.authorize(creds)

def add_entry(sheet, data):
    sheet.append_row(data)

def time_now_old():
    # Define the Mountain Time zone (UTC-7 during standard time, UTC-6 during daylight saving time)
    mountain_time_zone = pytz.timezone('US/Mountain')
    # Get the current time in UTC
    current_time_utc = datetime.now(pytz.utc)
    # Convert the current time to Mountain Time
    current_time_mt = current_time_utc.astimezone(mountain_time_zone)
    time_stamp=current_time_mt.strftime("%Y-%m-%d %H:%M:%S")
    return time_stamp

def time_now():
    # Define the Mountain Time Zone
    mountain_time_zone = pytz.timezone('US/Mountain')
    
    # Get the current Mountain Time
    current_time_mt = datetime.now(mountain_time_zone)
    
    # Subtract a random number of minutes (0-120)
    random_minutes = random.randint(0, 120)
    adjusted_time_mt = current_time_mt - timedelta(minutes=random_minutes)
    
    # Format the timestamp
    time_stamp = adjusted_time_mt.strftime("%Y-%m-%d %H:%M:%S")
    
    return time_stamp

def generate_data():
        
        drivers = ["Shabir", "Paras", "Raghav", "Anmol"]
        vehicle_ids = {"Shabir":"JK02-0041", "Paras":"Van B456","Anmol":"PB02-0041", "Raghav":"Van D987"}
        violations = ["Harsh Braking", "Harsh Acceleration", "Sharp Turns"]

        data = []
        for _ in range(20):
            driver_chosen=random.choice(drivers)
            data.append([time_now(),driver_chosen,vehicle_ids[driver_chosen],random.choice(violations)])
            
        
        return data

def read_gsheet():
     creds=ServiceAccountCredentials.from_json_keyfile_dict(Token)
     client = gspread.authorize(creds)
     sheet = client.open("MicropythonTest").worksheet("EmbeddedProject")
     data = sheet.get_all_values()
     df = pd.DataFrame(data[1:], columns=data[0])  # Use first row as column headers
     return df
