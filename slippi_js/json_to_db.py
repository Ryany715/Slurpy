import json
from os import listdir
from os.path import isfile, join
#from slippi.parse import parse
#from slippi.parse import ParseEvent
#from slippi import Game
#import pandas as pd
#import matplotlib.pyplot as plt
#from IPython.display import display
from datetime import date, datetime
import sqlite3
from slippi_classes import SlippiActionCounts, SlippiOverall
#from slippi.parse import ParseError

#conn = sqlite3.connect(':memory:')
conn = sqlite3.connect('slippi.db')
c = conn.cursor()

# Need to change connectCode to connect_code
sql = """CREATE TABLE slippi_action_counts (
           filename TEXT,
           connect_code TEXT,
           wavedash INTEGER,
           waveland INTEGER,
           airdodge INTEGER,
           dashdance INTEGER,
           spotdodge INTEGER,
           ledgegrab INTEGER,
           roll INTEGER,
           lcancel_success_ratio REAL,
           grab_success INTEGER,
           grab_fail INTEGER,
           tech_away INTEGER,
           tech INTEGER,
           tech_in INTEGER,
           tech_fail INTEGER,
           wall_tech_success_ratio REAL,
           datetime DATETIME
   )"""
sql2 = """CREATE TABLE slippi_overall (
            filename TEXT,
            connect_code TEXT,
            input_counts INTEGER,
            total_damage REAL,
            kill_count INTEGER,
            successful_conversions INTEGER,
            successful_conversion_ratio REAL,
            inputs_per_minute REAL,
            digital_inputs_per_minute REAL,
            openings_per_kill REAL,
            damage_per_opening REAL,
            neutral_win_ratio REAL,
            counter_hit_ratio REAL,
            beneficial_trade_ratio REAL,
            datetime DATETIME
            )"""
#c.execute(sql2)

def insert_slippi_action_count(slippi_action_counts):
    with conn:
        c.execute("INSERT INTO slippi_action_counts VALUES (:filename, :connect_code, :wavedash, :waveland, :airdodge, :dashdance, :spotdodge, :ledgegrab, :roll, :lcancel_success_ratio, :grab_success, :grab_fail, :tech_away, :tech_in, :tech, :tech_fail, :wall_tech_success_ratio, :datetime)", 
            {'filename':slippi_action_counts.filename, 'connect_code':slippi_action_counts.connect_code, 'wavedash':slippi_action_counts.wavedash, 'waveland':slippi_action_counts.waveland, 
            'airdodge':slippi_action_counts.airdodge, 'dashdance':slippi_action_counts.dashdance, 'spotdodge':slippi_action_counts.spotdodge, 'ledgegrab':slippi_action_counts.ledgegrab, 
            'roll':slippi_action_counts.roll, 'lcancel_success_ratio':slippi_action_counts.lcancel_success_ratio, 'grab_success':slippi_action_counts.grab_success, 
            'grab_fail':slippi_action_counts.grab_fail, 'tech_away':slippi_action_counts.tech_away, 'tech_in':slippi_action_counts.tech_in, 'tech':slippi_action_counts.tech, 
            'tech_fail':slippi_action_counts.tech_fail, 'wall_tech_success_ratio':slippi_action_counts.wall_tech_success_ratio, 'datetime':slippi_action_counts.datetime})

def get_slippi_action_count(filename):
    c.execute("SELECT * FROM slippi_action_counts WHERE filename=:filename", {'filename':filename})
    return c.fetchall()

def get_slippi_action_counts():
    c.execute("SELECT * FROM slippi_action_counts")
    return c.fetchall()

'''
def update_file(slippi_file, lcancel):
    with conn:
        c.execute("""UPDATE slippi SET lcancel = :lcancel
                    WHERE filename = :filename""",
                  {'filename': slippi_file.filename, 'lcancel': lcancel})
'''

def remove_action_count(slippi_file):
    with conn:
        c.execute("DELETE from slippi_action_counts WHERE filename = :filename",
                  {'filename': slippi_file.filename})

def calc_ratio(count):
    total = count['success'] + count['fail']
    if total > 0:
        ratio = count['success'] / total
    else:
        ratio = ""
    return ratio


def get_slippi_files(folder):
    files = []
    for filename in listdir(folder):
        if (not get_slippi_action_count(filename) or not get_slippi_overall(filename)) and isfile(join(folder, filename)):
            files.append(join(folder, filename))
    return files

def get_date_from_filename(filename):
    return filename[5:13]

def get_slippi_files_multi_folder(folder_list):
    files = []
    for folder in folder_list:
        files.extend(get_slippi_files(folder))
    return files

def insert_slippi_overall(slippi_overall):
    with conn:
        c.execute("INSERT INTO slippi_overall VALUES (:filename, :connect_code, :input_counts, :total_damage, :kill_count, :successful_conversions, :successful_conversion_ratio, :inputs_per_minute, :digital_inputs_per_minute, :openings_per_kill, :damage_per_opening, :neutral_win_ratio, :counter_hit_ratio, :beneficial_trade_ratio, :datetime)",
        {'filename': slippi_overall.filename, 'connect_code': slippi_overall.connect_code, 'input_counts': slippi_overall.input_counts, 'total_damage': slippi_overall.total_damage, 'kill_count': slippi_overall.kill_count, 'successful_conversions': slippi_overall.successful_conversions, 'successful_conversion_ratio': slippi_overall.successful_conversion_ratio, 'inputs_per_minute': slippi_overall.inputs_per_minute, 'digital_inputs_per_minute': slippi_overall.digital_inputs_per_minute, 'openings_per_kill': slippi_overall.openings_per_kill, 'damage_per_opening': slippi_overall.damage_per_opening, 'neutral_win_ratio': slippi_overall.neutral_win_ratio, 'counter_hit_ratio': slippi_overall.counter_hit_ratio, 'beneficial_trade_ratio': slippi_overall.beneficial_trade_ratio, 'datetime': slippi_overall.datetime})

def get_slippi_overall(filename):
    c.execute("SELECT * FROM slippi_overall WHERE filename=:filename", {'filename':filename})
    return c.fetchall()

def get_slippi_overalls():
    c.execute("SELECT * FROM slippi_overall")
    return c.fetchall()

folders = ['json/']
files = get_slippi_files_multi_folder(folders)

overall_stats = []
action_counts = []
for folder_filename in files:
    filename_len = len(folder_filename)
    filename = folder_filename[filename_len-25:filename_len]
    #print(filename)
    if not get_slippi_action_count(filename) or not get_slippi_overall(filename):
        with open(folder_filename) as f:
            try:
                data = json.load(f)
            except:
                print("Couldn't load file: " + filename)
                continue
            slippi_datetime = filename[5:20]
            settings = data['settings']
            stats = data['stats']
            metadata = data['metadata']
            players = metadata['players']
            actionCounts = stats['actionCounts']
            if not get_slippi_action_count(filename):
                for player in actionCounts:
                    player_index = str(player['playerIndex'])
                    player_info = players[player_index]
                    connect_code = player_info['names']['code']
                    
                    lcancel_ratio = calc_ratio(player['lCancelCount'])
                    wall_tech_ratio = calc_ratio(player['wallTechCount'])
                    
                    new_action_count = SlippiActionCounts(filename, connect_code, player['wavedashCount'], player['wavelandCount'], 
                        player['airDodgeCount'], player['dashDanceCount'], player['spotDodgeCount'], player['ledgegrabCount'], 
                        player['rollCount'], lcancel_ratio, player['grabCount']['success'], player['grabCount']['fail'],
                        player['groundTechCount']['away'], player['groundTechCount']['in'], player['groundTechCount']['neutral'], player['groundTechCount']['fail'], wall_tech_ratio,
                        slippi_datetime
                    )
                    #print(new_action_count)
                    insert_slippi_action_count(new_action_count)
                    action_counts.append(new_action_count)
            overall = stats['overall']
            if not get_slippi_overall(filename):
                for player in overall:
                    player_index = str(player['playerIndex'])
                    player_info = players[player_index]
                    connect_code = player_info['names']['code']

                    new_overall_stat = SlippiOverall(filename, connect_code, player['inputCounts']['total'],player['totalDamage'],player['killCount'],
                        player['successfulConversions']['total'],player['successfulConversions']['ratio'],player['inputsPerMinute']['ratio'],player['digitalInputsPerMinute']['ratio'],
                        player['openingsPerKill']['ratio'],player['damagePerOpening']['ratio'],player['neutralWinRatio']['ratio'],player['counterHitRatio']['ratio'],player['beneficialTradeRatio']['ratio'],
                        slippi_datetime
                    )
                    insert_slippi_overall(new_overall_stat)
                    overall_stats.append(new_overall_stat)

print(overall_stats)


