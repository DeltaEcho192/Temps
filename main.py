from __future__ import print_function
import datetime
import  pymysql
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

    ip_adressS = 'localhost'
    usernameS = 'root'
    passwordS = 'xxmaster'
    db_nameS = 'temps'

    #
    #
    #

    # Connection to Database.
    db = pymysql.connect(ip_adressS, usernameS, passwordS, db_nameS)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Pull all the record in the data base.


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

    ###
    ###
    ###

    sql = "SELECT * FROM temps_testing;"
    #print(sql)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        eventsNameArr = []
        StartTimeArr = []
        EndTimeArr = []
        for row in results:
            eventName = row[0]
            color = row[1]
            StartTime = row[2]
            EndTime = row[3]
            TotalTime = row[4]
            # Now print fetched result
            StartTime = str(StartTime.strftime("%Y-%m-%d %H:%M:%S"))
            EndTime = str(EndTime.strftime("%Y-%m-%d %H:%M:%S"))

            eventsNameArr.append(eventName)
            StartTimeArr.append(StartTime)
            EndTimeArr.append(EndTime)

    except:
        print("Error: unable to fecth data")
        exit()

    db.close()

    ###
    ###
    ###

    db = pymysql.connect(ip_adressS, usernameS, passwordS, db_nameS)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    #TODO Add the timeZone Change
    if not events:
        print('No upcoming events found.')
    for event in events:
        UserInfo = event['creator']
        email = UserInfo.get('email')
        #print(email)
        start = event['start'].get('dateTime', event['start'].get('date'))
        startSplit1 = start.split('T')

        dateStart = startSplit1[0]
        timeStart = startSplit1[1]

        dateStartFinal = dateStart.split('-')
        #print(dateStartFinal)

        if '+' in timeStart:
            timeSplitStart = timeStart.split('+')
        elif '-' in timeStart:
            timeSplitStart = timeStart.split('-')

        SQLTimeStart = dateStart + ' ' + timeSplitStart[0]
        timeFinalStart = timeSplitStart[0].split(':')
        timeZoneStart = timeSplitStart[1]
        #print(timeZoneStart)

        #print(timeFinalStart)
        #print(timeZoneStart)
        #print(timeZoneStart)

        hourStart = timeFinalStart[0]
        minuteStart = timeFinalStart[1]
        secStart = timeFinalStart[2]


        end = event['end'].get('dateTime', event['end'].get('date'))

        endSplit1 = end.split('T')

        dateEndFinal = endSplit1[0].split('-')
        timeEnd = endSplit1[1]

        timeSplitEnd = timeEnd.split('+')
        SQLTimeEnd = timeSplitEnd[0]
        #Reverse Order TODO
        SQLTimeEnd = endSplit1[0] + ' ' + SQLTimeEnd
        timeFinalEnd = timeSplitEnd[0].split(':')
        timeZoneEnd = timeSplitEnd[1]

        EventName = event['summary']
        try:
            colorId = event['colorId']
        except:
            colorId = 1
        eventsNameArrCP = eventsNameArr
        print(SQLTimeStart)
        print(StartTimeArr)
        #print(SQLTimeEnd)
        if EventName in eventsNameArr and SQLTimeStart in StartTimeArr and SQLTimeEnd in EndTimeArr:
            #print("Event has already been entered")
            #print(SQLTimeStart)
            #print(SQLTimeEnd)
            eventsNameArrCP.remove(EventName)
        else:

            #Check what Month it is
            #Check if Leap Year
            deltaYear = int(dateEndFinal[0]) - int(dateStartFinal[0])
            deltaMonth = int(dateEndFinal[1]) - int(dateStartFinal[1])
            deltaDay = int(dateEndFinal[2]) - int(dateStartFinal[2])

            deltaCheck = deltaYear + deltaMonth + deltaDay


            if deltaCheck > 0:
                totalDays = deltaYear * 365 + deltaMonth * 30.436875 + deltaDay

                timeHourStart = 24 - int(timeFinalStart[0])
                minConv = int(timeFinalStart[1]) / 60
                StartTime1 = timeHourStart - minConv

                dayHour = (totalDays - 1) * 24

                minConv = int(timeFinalEnd[1]) / 60
                EndTime1 = int(timeFinalEnd[0]) + minConv

                FinalTime = (StartTime1 + dayHour + EndTime1) * 60

                #print(FinalTime)



            elif deltaCheck == 0:
                deltaHour = int(timeFinalEnd[0]) - int(timeFinalStart[0])
                deltaMin = int(timeFinalEnd[1]) - int(timeFinalStart[1])
                deltaSec = int(timeFinalEnd[2]) - int(timeFinalStart[2])

                hourMin = deltaHour * 60

                FinalTime = hourMin - deltaMin
                #print(FinalTime)



            sql1 = 'insert into temps_testing (EventName,color,StartTime,EndTime,TotalTime,email) VALUES ("{0}","{1}","{2}","{3}",{4},"{5}")'.format(EventName,colorId,SQLTimeStart,SQLTimeEnd,FinalTime,email)
            print(sql1)
            try:
            	cursor.execute(sql1)
            	db.commit()
            	print('Data has been Entered into the DataBase')
            except:
            	db.rollback()
            	print("There has been an error with entering the data.")


        print("Start Time: ",start," End time ",end," EventColor: ", colorId," Event Name: ",event['summary'])

    print(eventsNameArrCP)
    if len(eventsNameArrCP) > 0:
        print("Files have been deleted in the calendar")
        r = 0
        while r < len(eventsNameArrCP):
            condition2 = eventsNameArrCP[r]
		#The SQL Code Needed.
            sql2 = "DELETE FROM temps_testing WHERE EventName = '{0}'".format(condition2)
            print("Delete Statment", sql2)
            try:
                cursor.execute(sql2)
                db.commit()
                print("Command has been executed")
            except:
                print("The Command did not go through.")
            r = r + 1
    db.close()

if __name__ == '__main__':
    main()
