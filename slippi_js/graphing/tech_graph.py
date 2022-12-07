import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from IPython.display import display
from datetime import date, datetime
import sqlite3
from slippi_classes import SlippiActionCounts
import numpy as np

conn = sqlite3.connect('slippi.db')
c = conn.cursor()

time = datetime.now()
pic_folder = "graphs\\"
connect_code = 'CATS#636'
c.execute("SELECT * FROM slippi_action_counts WHERE connectCode='CATS#636' ORDER BY datetime", {'connect_code': connect_code})
result = c.fetchmany(1000)

slippi_datetimes = []
wavedash = []
waveland = []
airdodge = []
dashdance = []
spotdodge = []
ledgegrab = []
roll = []
lcancel = []
grab_success = []
grab_fail = []
tech_away = []
tech = []
tech_in = []
tech_fail = []
tech_total = []

title = "Wavedash"

for row in result:
    slp_datetime = datetime.strptime(row[17], '%Y%m%dT%H%M%S')
    slippi_datetimes.append(slp_datetime.strftime("%Y-%m-%d %H:%M:%S"))
    wavedash.append(row[2])
    waveland.append(row[3])
    airdodge.append(row[4])
    dashdance.append(row[5])
    spotdodge.append(row[6])
    ledgegrab.append(row[7])
    roll.append(row[8])
    lcancel.append(row[9])
    grab_success.append(row[10])
    grab_fail.append(row[11])

    tech_total_num = row[12] + row[13] + row[14] + row[15] 
    
    if tech_total_num > 0:
        slippi_datetimes.append(slp_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        tech_total.append(tech_total_num)
        tech_away.append(row[12])
        tech.append(row[13])
        tech_in.append(row[14])
        tech_fail.append(row[15])
    
proportion_tech_fail = np.true_divide(tech_fail, tech_total) * 100
proportion_tech = np.true_divide(tech, tech_total) * 100
proportion_tech_away = np.true_divide(tech_away, tech_total) * 100
proportion_tech_in = np.true_divide(tech_in, tech_total) * 100

df = pd.DataFrame(list(zip(slippi_datetimes, proportion_tech_fail, proportion_tech, proportion_tech_away, proportion_tech_in)),
               columns =['Datetime', 'Missed Tech', 'Tech', 'Tech Away', 'Tech In'])

df.plot(
    color=['C3','C2','C1','C0'],
    kind = 'bar',
    stacked = True)
#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=100))
plt.gcf().autofmt_xdate()
plt.xlabel("Datetime")
plt.ylabel("Tech Distribution")
plt.title("Techs Distribution Over Time")
plt.savefig(pic_folder + time.strftime("%Y%m%dT%H%M%S") + ".png")
plt.show()
