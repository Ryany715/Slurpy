import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from IPython.display import display
from datetime import date, datetime
import sqlite3
from slippi_classes import SlippiActionCounts

conn = sqlite3.connect('../slippi.db')
c = conn.cursor()

c.execute("SELECT * FROM slippi_overall WHERE connect_code='CATS#636' ORDER BY datetime")
result = c.fetchall()

database_dict = {
    "Input Count":2,
    "Total Damage":3,
    "Kill Count":4,
    "Successful Conversions":5,
    "Successful Conversion Ratio":6,
    "Inputs per Minute":7,
    "Digital Inputs per Minute":8,
    "Openings per Kill":9,
    "Damage per Opening":10,
    "Neutral Win Ratio":11,
    "Counter Hit Ratio":12,
    "Beneficial Trade Ratio":13,
}

def save_graph(pic_folder, database_key):
    time = datetime.now()
    plt.savefig(pic_folder + database_key + "_" + time.strftime("%Y%m%dT%H%M%S") + ".png")

def graph_data(database_key, chart_type, data_points, pic_folder):
    date_dict = {}
    for row in result:
        datapoint = row[database_dict[database_key]]
        if datapoint:
            slp_datetime = datetime.strptime(row[14], '%Y%m%dT%H%M%S')
            if data_points == "all":
                slp_datetime = slp_datetime.strftime("%Y-%m-%d %H:%M:%S")
                if slp_datetime in date_dict.keys():
                    date_dict[slp_datetime][0] += datapoint
                    date_dict[slp_datetime][1] += 1
                else:
                    date_dict[slp_datetime] = [datapoint,1]
            elif data_points == "daily":
                day = slp_datetime.strftime("%Y-%m-%d")
                if day in date_dict.keys():
                    date_dict[day][0] += datapoint
                    date_dict[day][1] += 1
                else:
                    date_dict[day] = [datapoint,1]
            elif data_points == "monthly":
                month = slp_datetime.strftime("%Y-%m")
                if month in date_dict.keys():
                    date_dict[month][0] += datapoint
                    date_dict[month][1] += 1
                else:
                    date_dict[month] = [datapoint,1]
    per_game_values = []
    for key in date_dict.keys():
        per_game = date_dict[key][0] / date_dict[key][1]
        per_game_values.append(per_game)
    #print(date_dict)
    #print(per_game_values)
    #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    if data_points == "all":
        plt.xlabel("Datetime")
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=100))
    elif data_points == "daily":
        plt.xlabel("Day")
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    elif data_points == "monthly":
        plt.xlabel("Month")
    if chart_type == "plot":
        plt.plot(date_dict.keys(), per_game_values)
    elif chart_type == "scatter":
        plt.scatter(date_dict.keys(), per_game_values, 1)
    
    plt.ylim(bottom=0)
    plt.ylabel(database_key)
    plt.title(database_key + " Per Game Over Time")
    plt.gcf().autofmt_xdate()
    save_graph(pic_folder, database_key)
    plt.show()

if __name__ == "__main__":
    chart_types = ["Input Count", "Total Damage", "Kill Count", "Successful Conversions", "Successful Conversion Ratio", "Inputs per Minute", "Digital Inputs per Minute", "Openings per Kill", "Damage per Opening", "Neutral Win Ratio", "Counter Hit Ratio", "Beneficial Trade Ratio"]
    #connect_code = 'CATS#636' #This isn't actually used]
    chart_type = "plot"
    data_points = "monthly"
    pic_folder = "graphs\\"
    for chart in chart_types:
        graph_data(chart, chart_type, data_points, pic_folder)

