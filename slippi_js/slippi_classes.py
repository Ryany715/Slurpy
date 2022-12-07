class SlippiActionCounts:
    """A slippi action counts"""

    def __init__(self, filename, connect_code, wavedash, waveland, airdodge, dashdance, spotdodge, ledgegrab, roll, lcancel_success_ratio, grab_success, grab_fail, tech_away, tech_in, tech, tech_fail, wall_tech_success_ratio, datetime):
        self.filename = filename
        self.connect_code = connect_code
        self.wavedash = wavedash
        self.waveland = waveland
        self.airdodge = airdodge
        self.dashdance = dashdance
        self.spotdodge = spotdodge
        self.ledgegrab = ledgegrab
        self.roll = roll
        self.lcancel_success_ratio = lcancel_success_ratio
        self.grab_success = grab_success
        self.grab_fail = grab_fail
        self.tech_away = tech_away
        self.tech_in = tech_in
        self.tech = tech
        self.tech_fail = tech_fail
        self.wall_tech_success_ratio = wall_tech_success_ratio
        self.datetime = datetime

    def __repr__(self):
        return "SlippiActionCount({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(self.filename, self.connect_code, self.wavedash, self.waveland, self.airdodge, self.dashdance, self.spotdodge, self.ledgegrab, self.roll, self.lcancel_success_ratio, self.grab_success, self.grab_fail, self.tech_away, self.tech_in, self.tech, self.tech_fail, self.wall_tech_success_ratio, self.datetime)

class SlippiOverall:
    """A slippi overall stats"""

    def __init__(self, filename, connect_code, input_counts, total_damage, kill_count, successful_conversions, successful_conversion_ratio, inputs_per_minute, digital_inputs_per_minute, openings_per_kill, damage_per_opening, neutral_win_ratio, counter_hit_ratio, beneficial_trade_ratio, datetime):
        self.filename = filename
        self.connect_code = connect_code
        self.input_counts = input_counts
        self.total_damage = total_damage 
        self.kill_count = kill_count
        self.successful_conversions = successful_conversions
        self.successful_conversion_ratio = successful_conversion_ratio
        self.inputs_per_minute = inputs_per_minute
        self.digital_inputs_per_minute = digital_inputs_per_minute
        self.openings_per_kill = openings_per_kill
        self.damage_per_opening = damage_per_opening
        self.neutral_win_ratio = neutral_win_ratio
        self.counter_hit_ratio = counter_hit_ratio
        self.beneficial_trade_ratio = beneficial_trade_ratio
        self.datetime = datetime

    def __repr__(self):
        return "SlippiOverall('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(self.filename, self.connect_code, self.input_counts, self.total_damage, self.kill_count, self.successful_conversions, self.successful_conversion_ratio, self.inputs_per_minute, self.digital_inputs_per_minute, self.openings_per_kill, self.damage_per_opening, self.neutral_win_ratio, self.counter_hit_ratio, self.beneficial_trade_ratio, self.datetime)


