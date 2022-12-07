import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from IPython.display import display
from datetime import date, datetime
import sqlite3
from slippifile import SlippiFile

conn = sqlite3.connect('slippi.db')
c = conn.cursor()

c.execute("SELECT * FROM slippi ORDER BY datetime")
result = c.fetchall()
#print(result)
 
slippi_datetimes = []
lcancels = []

for i in result:
    slp_datetime = datetime.strptime(i[2], '%Y%m%dT%H%M%S')
    slippi_datetimes.append(slp_datetime.strftime("%Y-%m-%d %H:%M:%S"))
    lcancels.append(i[1])

print(lcancels)

#print(slippi_datetimes)
#print("Name of Students = ", filenames)
#print("Marks of Students = ", lcancels)

# Visulizing Data using Matplotlib
#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=50))
#plt.scatter(slippi_datetimes, lcancels,1)
plt.plot(slippi_datetimes, lcancels)
plt.ylim(0, 1)
plt.xlabel("Datetime")
plt.ylabel("L-Cancel Percentage")
plt.title("L-Cancel Percentage Over Time")
plt.gcf().autofmt_xdate()

time = datetime.now()
pic_folder = "graphs\\"
plt.savefig(pic_folder + time.strftime("%Y%m%dT%H%M%S") + ".png")

plt.show()
