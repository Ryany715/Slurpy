import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from IPython.display import display
from datetime import date, datetime
import sqlite3
from slippi_classes import SlippiActionCounts

conn = sqlite3.connect('slippi.db')
c = conn.cursor()

c.execute("SELECT * FROM slippi_action_counts WHERE connectCode='CATS#636' ORDER BY datetime", {'connect_code': connect_code})
result = c.fetchall()

slippi_datetimes = []
datapoints = []


database_dict = {
    "Wavedash":2,
    "Waveland":3,
    "Airdodge":4,
    "Dashdance":5,
    "Spotdodge":6,
    "Ledgegrab":7,
    "Roll":8,
    "L-Cancel":9,
    "Grabs Gotten":10,
    "Missed Grabs":11,
}

for row in result:
    datapoint = row[database_dict[database_key]]
    #print(row)
    if datapoint:
        slp_datetime = datetime.strptime(row[17], '%Y%m%dT%H%M%S')
        #print(slp_datetime)
        slippi_datetimes.append(slp_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        datapoints.append(datapoint)
#print(slippi_datetimes)
#print(datapoints)

#print(slippi_datetimes)

#print(slippi_datetimes)
#print("Name of Students = ", filenames)
#print("Marks of Students = ", lcancels)

# Visulizing Data using Matplotlib
#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=100))
plt.scatter(slippi_datetimes, datapoints, 1)
#lt.plot(slippi_datetimes, datapoints)
#plt.ylim(0, 1)
plt.xlabel("Datetime")
plt.ylabel(database_key)
plt.title(database_key + " Over Time")
plt.gcf().autofmt_xdate()

time = datetime.now()
pic_folder = "graphs\\"
plt.savefig(pic_folder + time.strftime("%Y%m%dT%H%M%S") + ".png")

plt.show()

if __name__ == "__main__":
    database_key = "Wavedash"
    connect_code = 'CATS#636'
