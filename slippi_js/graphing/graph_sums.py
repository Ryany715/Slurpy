import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from IPython.display import display
from datetime import date, datetime
import sqlite3
from slippi_classes import SlippiActionCounts

conn = sqlite3.connect('slippi.db')
c = conn.cursor()

c.execute("SELECT * FROM slippi_action_counts WHERE connectCode='CATS#636' ORDER BY datetime")
result = c.fetchall()

database_dict = {
    "Wavedash":2,
    "Waveland":3,
    "Airdodge":4,
    "Dashdance":5,
    "Spotdodge":6,
    "Ledgegrab":7,
    "Roll":8,
    "Grabs Gotten":10,
    "Missed Grabs":11,
}

def save_graph(pic_folder, database_key):
    time = datetime.now()
    
    plt.savefig(pic_folder + database_key + time.strftime("%Y%m%dT%H%M%S") + ".png")

def graph_data(database_key, chart_type, data_points, pic_folder):
    slippi_datetimes = []
    date_dict = {}
    for row in result:
        datapoint = row[database_dict[database_key]]
        if datapoint:
            slp_datetime = datetime.strptime(row[17], '%Y%m%dT%H%M%S')
            if data_points == "all":
                slp_datetime = slp_datetime.strftime("%Y-%m-%d %H:%M:%S")
                date_dict[slp_datetime] = datapoint
            elif data_points == "daily":
                day = slp_datetime.strftime("%Y%m%d")
                if day in date_dict.keys():
                    date_dict[day] += datapoint
                else:
                    date_dict[day] = datapoint
            elif data_points == "monthly":
                month = slp_datetime.strftime("%Y%m")
                if month in date_dict.keys():
                    date_dict[month] += datapoint
                else:
                    date_dict[month] = datapoint
    
    #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    if data_points == "all":
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=100))
    elif data_points == "daily":
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    elif data_points == "monthly":
        print("")
    if chart_type == "plot":
        plt.plot(date_dict.keys(), date_dict.values())
    elif chart_type == "scatter":
        plt.scatter(date_dict.keys(), date_dict.values(), 1)
    plt.xlabel("Datetime")
    plt.ylabel(database_key)
    plt.title(database_key + " Over Time")
    plt.gcf().autofmt_xdate()
    save_graph(pic_folder, database_key)
    plt.show()

if __name__ == "__main__":
    database_key = "Wavedash"
    #connect_code = 'CATS#636' #This isn't actually used
    chart_type = "plot"
    data_points = "monthly"
    pic_folder = "graphs\\"
    graph_data(database_key, chart_type, data_points, pic_folder)

