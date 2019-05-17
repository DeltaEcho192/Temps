import datetime
import  pymysql

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

sql = "SELECT * FROM temps_testing;"
#print(sql)
try:
    # Execute the SQL command
    cursor.execute(sql)
    # Fetch all the rows in a list of lists.
    results = cursor.fetchall()
    eventsNameArr = []
    ColorArr = []
    StartTimeArr = []
    EndTimeArr = []
    TotalTimeArr = []
    EmailArr = []
    for row in results:
        eventName = row[0]
        color = row[1]
        StartTime = row[2]
        EndTime = row[3]
        TotalTime = row[4]
        Email = row[5]
        # Now print fetched result
        StartTime = str(StartTime.strftime("%Y-%m-%d %H:%M:%S"))
        EndTime = str(EndTime.strftime("%Y-%m-%d %H:%M:%S"))

        eventsNameArr.append(eventName)
        ColorArr.append(color)
        StartTimeArr.append(StartTime)
        EndTimeArr.append(EndTime)
        TotalTimeArr.append(TotalTime)
        EmailArr.append(Email)
except:
    print("Error: unable to fecth data")
    exit()

outputTime = sum(TotalTimeArr)
print(eventsNameArr)
print(ColorArr)
print(TotalTimeArr)
print(outputTime)
db.close()
