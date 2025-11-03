import datetime
import pandas as pd
import json
import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

#connect records to google sheets
SPREADSHEET_ID = "1ub3j5jaROYqDSTuRzQbaPUYfhQP9a3XwEF_OGM4TBZI"

RANGE_NAME = "Sheet1!A:C"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

#method to open to google sheets
#def get_sheet_service():
#    creds = Credentials.from_service_account_file(
       # "my-project-2025-477105-40e880fb878b.json",
#        scopes=SCOPES  )
#    service = build("sheets", "v4", credentials=creds)
#    return service.spreadsheets()

#call streamlit secret
def get_sheet_service():
    creds = Credentials.from_service_account_info(
        st.secrets["GOOGLE_SA_JSON"],
        scopes=SCOPES
    )
    service = build("sheets", "v4", credentials=creds)
    return service.spreadsheets()

#log mood method
def log_mood(mood: str, note: str = ""):
    sheet = get_sheet_service()

    #the format that will be shown on the google sheet
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    values = [[timestamp, mood, note]]
    body = {"values": values}

    #append records
    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()

    #print success message
    return "Mood logged to Google Sheet, success"

#get today mood record from google sheet, default selection 
def get_today_moods():
    sheet = get_sheet_service()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()
    #get time, emoji, note values
    rows = result.get("values", [])

    # no data/only header
    if len(rows) <= 1:
        return pd.DataFrame(columns=["timestamp", "mood", "note"])

    # skip header 
    data = rows[1:]
    df = pd.DataFrame(data, columns=["timestamp", "mood", "note"])

    # double check timestamp forat is align
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    #filter for today
    today = datetime.date.today()
    df = df[df["timestamp"].dt.date == today]

    return df
#get mood record from google sheet for any date range, similar to previous method
def get_moods_by_date(start_date, end_date):
    sheet = get_sheet_service()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()
    #get time, emoji, note values
    rows = result.get("values", [])
    # no data/only header
    if len(rows) <= 1:
        return pd.DataFrame(columns=["timestamp", "mood", "note"])
    # skip header 
    data = rows[1:]
    df = pd.DataFrame(data, columns=["timestamp", "mood", "note"])
    # double check timestamp forat is align
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    #return data from selected date range
    df = df[(df["timestamp"].dt.date >= start_date) &
            (df["timestamp"].dt.date <= end_date)]
    
    return df

