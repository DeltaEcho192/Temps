from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    old = datetime.datetime(2019,5,8,12,00,00).isoformat() + 'Z'
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(now)
    print('Getting the past events')
    events_result = service.events().list(calendarId='primary', timeMin=old, timeMax=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        startSplit1 = start.split('T')

        dateStart = startSplit1[0]
        timeStart = startSplit1[1]

        dateFinal = dateStart.split('-')
        print(dateFinal)

        #Check Weather positive or negative time Zone
        #Use '+' or '-' in Main string.
        timeSplitStart = timeStart.split('+')
        timeFinalStart = timeSplitStart[0].split(':')
        timeZoneStart = timeSplitStart[1]

        print(timeFinalStart)
        print(timeZoneStart)

        hourStart = timeFinalStart[0]
        minuteStart = timeFinalStart[1]
        secStart = timeFinalStart[2]



        end = event['end'].get('dateTime', event['end'].get('date'))
        print(start,end, event['summary'], event['colorId'])



if __name__ == '__main__':
    main()
