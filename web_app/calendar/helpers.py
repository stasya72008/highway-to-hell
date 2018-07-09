from copy import copy
import json

from html_template import *


with open('date_template.json', 'r') as f:
    date_template = json.loads(f.read())


def gen_hours(tasks):
    day = ''
    for hour_id in range(0, 24):
        # ToDo(den) add logic
        # https://github.com/stasya72008/highway-to-hell/issues/13
        # remove ----------
        if hour_id in (3,15,20):
            day += hour_cell.format(hour_id=hour_id,
                                    task_name='test_{}'.format(hour_id))
        else:
            day += hour_cell_free.format(hour_id=hour_id)
        # -----------------
    return day


def gen_weeks(year_id, month_id, tasks):
    week = copy(week_table)
    month = ''

    day_of_week = 1
    d_index = 1

    number_of_d = date_template[str(year_id)][str(month_id)]['days']
    first_d = date_template[str(year_id)][str(month_id)]['first_day']
    # ToDo add switch to previous and next month / year
    if month_id == 1:
        prev_month = date_template[str(year_id - 1)]['12']['days'] - \
                     first_d + 2
    else:
        prev_month = date_template[str(year_id)][str(month_id - 1)]['days'] - \
                     first_d + 2

    # form previous month
    while first_d > day_of_week:
        week = week.replace('[d_{}]'.format(day_of_week),
                            day_cell_another_month.format(day_id=prev_month))
        prev_month += 1
        day_of_week += 1

    # form previous month
    while d_index < number_of_d + 1:
        # ToDo(den) add logic
        # https://github.com/stasya72008/highway-to-hell/issues/13
        # remove --------------
        if d_index not in (3, 15, 20):
            day = day_cell_free.format(year_id=year_id,
                                       month_id=month_id,
                                       day_id=d_index)
        else:
            day = day_cell.format(year_id=year_id,
                                  month_id=month_id,
                                  day_id=d_index,
                                  task_count='3')

        week = week.replace('[d_{}]'.format(day_of_week), day)
        # -------------------

        d_index += 1
        if day_of_week % 7 == 0:
            month = '{}{}'.format(month, week)
            week = copy(week_table)
            day_of_week = 0
        day_of_week += 1

    # form next month
    d_index = 1
    while day_of_week < 8:
        week = week.replace('[d_{}]'.format(day_of_week),
                            day_cell_another_month.format(day_id=d_index))
        d_index += 1
        day_of_week += 1

    month = '{}{}'.format(month, week)
    return month
