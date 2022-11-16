from datetime import datetime
import pandas as pd
import openpyxl
import string
from copy import deepcopy

# ----------------------- CLASS ----------------------- #

class User:
    """
    User class for scheduling
    """
    def __init__(self, name):
        self.name = name
        self.available_day = {}
    
    def __repr__(self) -> str:
        return self.name

    def attend(self, day, time_consts = None):
        if self.available_day.get(day, False):
            self.available_day[day].append(time_consts)
        else:
            self.available_day[day] = [time_consts]

    def available(self, date, time = None):
        # 가져온 값이 
        if self.available_day.get(date, False):
            if time is None:
                return True
            else:
                consts = self.available_day[date]
                for const in consts:
                    # 되는 시간대. 
                    if const == const:
                        s, e = const.split("~")
                        s, e = int(s), int(e)
                        if s <= time < e:
                            return True

                    else: # nan const 
                        return True
                return False
                
        else:
            return False


class Song:
    def __init__(self, configs) -> None:
        members = []
        for k, v in configs.items():
            if v != "x":
                setattr(self, k, v)
                if k not in ['artist', 'name']:
                    members.append(v)
        
        self.members = set(members)
        wo_V = deepcopy(self.members)
        wo_V.remove(self.V)
        self.wo_V = wo_V
    def __repr__(self) -> str:
        return f"{self.artist} : {self.name}"

    def possible(self, users, date, time = None, exclude_V = False):
        available_users = set()
        for name, user in users.items():
            if user.available(date, time):
                available_users.add(user.name)
    
        return self.members.issubset(available_users)


# Util functions

def load_data():
    setlist = pd.read_csv('set_list.csv')
    setlist = setlist.drop(['연번'], axis = 1)
    setlist.columns = ['artist', 'name', 'V', 'G1', 'G2', 'B', 'D', 'K']
    schedule = pd.read_csv("schedule.csv")


    return setlist, schedule

def preprocess(setlist, schedule):
    users = {}

    for i in range(schedule.shape[0]):
        # get schedule
        name, date, const = schedule.iloc[i, :].values.tolist()

        # new member
        if not users.get(name, False):
            users[name] = User(name)
        
        # get user
        user = users[name]

        # add schedule
        user.attend(date, const)

    songs = {}

    for i in range(setlist.shape[0]):
        info = dict(setlist.iloc[i, :])
        song = Song(info)
        songs[song.name] = song

    return users, songs

def get_possible_list(users, songs, date, weekday):

    assert weekday in [4, 5, 6], "Invalid Weekday"

    if weekday == 4:
        tRange = (19, 24)
    else:
        tRange = (12, 24)

    possible_songs = {}
    for t in range(*tRange):
        possible_songs[t] = []
        for s_name, song in songs.items():
            if song.possible(users, date, t):
                possible_songs[t].append(song)

    return possible_songs


def get_meeting_candidates(users, songs, dates):
    meeting_candidates = {}
    for date in dates:
        weekday = datetime.weekday(datetime.strptime(f"22-{date}", "%y-%m-%d"))
        p_songs = get_possible_list(users, songs, date = date, weekday= weekday)
        meeting_candidates[date] = {}
        prev_songs = set()
        start = 0

        for t, _p_song in p_songs.items():
            songs_inverval = set(song.name for song in _p_song) 
            
            # 이전하고 같으면 그냥 패스. 담에 추가
            if songs_inverval == prev_songs:
                continue

            else:
                if prev_songs:
                    # 기존곡들 추가
                    meeting_candidates[date][f"{start}~{t}"] = prev_songs

                # 새로 시작
                start = t
                prev_songs = songs_inverval

        meeting_candidates[date][f"{start}~{t + 1}"] = prev_songs

    return meeting_candidates

G_COL = 0

def add(sheet, date, values):
    global G_COL
    col = string.ascii_uppercase[G_COL]
    sheet[f'{col}1'] = date
    for i, value in enumerate(values):
        sheet[f'{col}{i+2}'] = value
    G_COL += 1



def to_sheet(meeting_candidates):
    ver = datetime.now().strftime("%y-%m-%d")
    file_name = f"Meeting Candidates{ver}.xlsx"
    wb = openpyxl.Workbook()
    wb.save(file_name)

    sheet = wb.active
    sheet.title = "candidates"

    meeting_candidates.keys()

    for date, p_songs in meeting_candidates.items():
        for t_range, songs in p_songs.items():
            songs = list(songs)
            add(sheet, f"{date} {t_range} ",  songs)

    wb.save(file_name)



# setlist, schedule = load_data()
# users, songs = preprocess(setlist, schedule)
# dates =  schedule['day'].unique().tolist()
# duration = 3


# schedule['']


# meeting_candidates = get_meeting_candidates(users, songs, dates)
# to_sheet(meeting_candidates)



if __name__ == "__main__":
    setlist, schedule = load_data()
    users, songs = preprocess(setlist, schedule)
    dates =  schedule['day'].unique().tolist()
    duration = 3

    meeting_candidates = get_meeting_candidates(users, songs, dates)
    to_sheet(meeting_candidates)