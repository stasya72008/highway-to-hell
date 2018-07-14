from copy import copy
import json

from html_template import *


with open('date_template.json', 'r') as f:
    date_template = json.loads(f.read())


def gen_hours(year, month, day, redirect, tasks):
    day_line = ''
    for h_index in range(0, 24):
        cell = cell_add_task_link.format(year=year,
                                         month=month,
                                         day=day,
                                         hour=h_index,
                                         redirect=redirect)
        # ToDo(den) add logic
        # https://github.com/stasya72008/highway-to-hell/issues/13
        # remove ----------
        if h_index in (3,15,20):
            day_line += hour_cell.format(hour=h_index,
                                         task_name='test_{}'.format(h_index),
                                         cell_add_task_link=cell)
        else:
            day_line += hour_cell_free.format(hour=h_index,
                                              cell_add_task_link=cell)
        # -----------------
    return day_line


def gen_weeks(year, month, tasks):
    week = copy(week_table)
    month_line = ''

    day_of_week = 1
    d_index = 1

    number_of_d = date_template[str(year)][str(month)]['days']
    first_d = date_template[str(year)][str(month)]['first_day']
    # ToDo add switch to previous and next month / year
    if month == 1:
        prev_month_days = date_template[str(year - 1)]['12']['days'] - \
                     first_d + 2
    else:
        prev_month_days = date_template[str(year)][str(
            month - 1)]['days'] - first_d + 2

    # form previous month
    while first_d > day_of_week:
        week = week.replace('[d_{}]'.format(day_of_week),
                            day_cell_another_month.format(day=prev_month_days))
        prev_month_days += 1
        day_of_week += 1

    # form previous month
    while d_index < number_of_d + 1:
        # ToDo(den) add logic
        # https://github.com/stasya72008/highway-to-hell/issues/13
        # remove --------------
        if d_index not in (3, 15, 20):
            day = day_cell_free.format(year=year,
                                       month=month,
                                       day=d_index)
        else:
            day = day_cell.format(year=year,
                                  month=month,
                                  day=d_index,
                                  task_count='3')

        week = week.replace('[d_{}]'.format(day_of_week), day)
        # -------------------

        d_index += 1
        if day_of_week % 7 == 0:
            month_line = '{}{}'.format(month_line, week)
            week = copy(week_table)
            day_of_week = 0
        day_of_week += 1

    # form next month
    d_index = 1
    while day_of_week < 8:
        week = week.replace('[d_{}]'.format(day_of_week),
                            day_cell_another_month.format(day=d_index))
        d_index += 1
        day_of_week += 1

    month_line = '{}{}'.format(month_line, week)
    return month_line
