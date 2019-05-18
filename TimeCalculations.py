import datetime
import  pymysql

#TODO How to intergrate with Website

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


x = 0
lightPurple = []
Sage = []
Purple = []
Salmon = []
Yellow = []
Orange = []
Blue = []
Grey = []
DarkBlue =[]
Green = []
Red = []

while x < len(eventsNameArr):
    colorTemp = ColorArr[x]
    if colorTemp == 1:
        #print("Light Purple")
        lightPurple.append(TotalTimeArr[x])
    if colorTemp == 2:
        #print("Sage")
        Sage.append(TotalTimeArr[x])
    if colorTemp == 3:
        #print("Purple")
        Purple.append(TotalTimeArr[x])
    if colorTemp == 4:
        #print("Salmon")
        Salmon.append(TotalTimeArr[x])
    if colorTemp == 5:
        #print("Yellow")
        Yellow.append(TotalTimeArr[x])
    if colorTemp == 6:
        #print("Orange")
        Orange.append(TotalTimeArr[x])
    if colorTemp == 7:
        #print("Blue")
        Blue.append(TotalTimeArr[x])
    if colorTemp == 8:
        #print("Grey")
        Grey.append(TotalTimeArr[x])
    if colorTemp == 9:
        #print("DarkBlue")
        DarkBlue.append(TotalTimeArr[x])
    if colorTemp == 10:
        #print("Green")
        Green.append(TotalTimeArr[x])
    if colorTemp == 11:
        #print("Red")
        Red.append(TotalTimeArr[x])
    x = x + 1

outputTime = sum(TotalTimeArr)
print("Light Purple: ",sum(lightPurple))
print("Sage: ",sum(Sage))
print("Purple: ",sum(Purple))
print("Salmon: ",sum(Salmon))
print("Yellow: ",sum(Yellow))
print("Orange: ",sum(Orange))
print("Blue: ",sum(Blue))
print("Grey: ",sum(Grey))
print("DarkBlue: ",sum(DarkBlue))
print("Green: ",sum(Green))
print("Red: ",sum(Red))

#print(eventsNameArr)
#print(ColorArr)
print("Total Time: ", sum(TotalTimeArr)/60,": Hours")
#print(outputTime)

#Calculate most common time for events
#Which Event Color is most common at what hours

db.close()
