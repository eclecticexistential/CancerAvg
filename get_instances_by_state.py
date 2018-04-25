import csv
from database import insert_into_db, get_1999_stats


def get_states():
    states = []
    with open('us census bureau regions and divisions.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            states.append(row[0])
    return states


def compile_data(states):
    reduced_data = []
    with open('BYAREA.TXT', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            info = row[0].split('|')
            if info[0] in states:
                if info[5] == 'Incidence' and info[7] == 'All Races':
                    if info[8] == 'Male and Female' and info[9] == 'All Cancer Sites Combined':
                        if len(info[10]) < 6:
                            reduced_data.append([info[10], info[0], info[6], info[4]])
    return reduced_data


def organize_data():
    states = get_states()
    totals = compile_data(states)
    count = 1999
    while count < 2015:
        state_num = 0
        for item in totals:
            if item[0] == str(count):
                if item[1] != 'Wyoming':
                    insert_into_db(item[0], item[1], item[2], item[3])
                    state_num += 1
                if item[1] == 'Wyoming' and state_num != 0:
                    insert_into_db(item[0], item[1], item[2], item[3])
                    state_num += 1
                if state_num == 51:
                    count += 1
                    state_num = 0


def get_data_by_year(year):
    us_pop = 0
    us_cancer = 0
    organize_data()
    yoke = list(get_1999_stats())
    for x in yoke:
        if x[0] == year:
            us_pop += x[2]
            if type(x[3]) == int:
                us_cancer += x[3]
    percent_pop = us_cancer / us_pop
    return percent_pop


def get_state_data_by_year(state):
    organize_data()
    soak = list(get_1999_stats())
    array = []
    for x in soak:
        if x[1] == state:
            array.append(x)
    return array


def cancer2015(file, ign):
    array = []
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        skip = ign
        while skip != 0:
            next(reader)
            skip -= 1
        for row in reader:
            array.append(row)
    return array


def filter_data(file, ign, state='', states_only=False):
    data = cancer2015(file, ign)
    placehold = []
    state_data = []
    us_stats = 0
    multi = 12
    for key, value in enumerate(data):
        if key == 0 or key == multi:
            placehold.append(value)
        if key == 1 or key == (multi + 1):
            num = value[0] + value[1]
            enter = ""
            for number in num:
                if number != ' ':
                    enter += number
            placehold.append(enter)
            state_data.append(placehold)
            placehold = []
            us_stats += int(enter)
            if key == (multi + 1):
                multi += 12
    if states_only is False:
        return us_stats
    if states_only:
        for area in state_data:
            if area[0][0] == state:
                return area


def get_pops():
    all_ages = []
    states = get_states()
    with open('sc-est2016-agesex-civ.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[4] in states and row[5] == '0' and row[6] == '999':
                all_ages.append([row[4], row[13], row[14]])
    return all_ages


def us_pop(year):
    data = get_pops()
    us_tots = 0
    for x in data:
        if year == 2015:
            num = int(x[1])
            us_tots += num
        if year == 2016:
            num = int(x[2])
            us_tots += num
    return us_tots


def get_dual_years(year):
    if year == 2015:
        first = filter_data('cancerorg2015.txt', 22)
        pop15 = us_pop(2015)
        re15 = first / pop15
        return re15
    else:
        second = filter_data('cancerorg2016.txt', 0)
        pop16 = us_pop(2016)
        re16 = second / pop16
        return re16


def get_states99_16(state):
    array = get_state_data_by_year(state)
    state_pop = []
    pops = get_pops()
    for y in pops:
        if y[0] == state:
            state_pop = y
    y15 = filter_data('cancerorg2015.txt', 22, state, states_only=True)
    can15 = state_pop[1]
    array.append(['2015', y15[0], can15, y15[1]])
    y16 = filter_data('cancerorg2016.txt', 0, state, states_only=True)
    can16 = state_pop[2]
    array.append(['2016', y16[0], can16, y16[1]])
    return array


def get_state_percent(state):
    decda = get_states99_16(state)
    stats = []
    for x in decda:
        if '~' not in x:
            num = int(x[3]) / int(x[2])
            stats.append([x[0], num])
        else:
            num = 0
            stats.append([x[0], num])
    return stats

# print(get_state_percent('Alaska'))

def get_info_decades():
    counter = 1999
    buffer = []
    totals = []
    while counter < 2017:
        buffer.append(counter)
        if counter < 2015:
            buffer.append(get_data_by_year(counter))
        if counter > 2014:
            buffer.append(get_dual_years(counter))
        totals.append(buffer)
        buffer = []
        counter += 1
    return totals

# print(get_info_decades())

# https://www.cdc.gov/cancer/npcr/uscs/download_data.htm
# cancer.org
