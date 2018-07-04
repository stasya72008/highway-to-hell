import json
from copy import copy

from flask import Flask
from html_template import *

app = Flask(__name__)


with open('date_template.json', 'r') as file:
    date_template = json.loads(file.read())


@app.route(years_route)
def get_years_page():
    # ToDo Get years from date_template and form page
    return body_html.format(year_table)


@app.route(months_route)
def get_months_page_for_year(year_id):
    # ToDo(den) add logic
    # https://github.com/stasya72008/highway-to-hell/issues/13
    # remove -----------
    month_busy.update({'May': "#eee", 'May_task_count': " (3)"})
    month_busy.update({'April': "#eee", 'April_task_count': " (1)"})
    # ------------------

    month = month_table.format(year_id=year_id,
                               **month_busy)
    return body_html.format(month)


@app.route(days_route)
def get_days_page_for_month(year_id, month_id):
    # ToDo(den) add logic
    # https://github.com/stasya72008/highway-to-hell/issues/13
    # tasks = get_task_for_rest()

    # ToDo add switch to previous and next year
    pr_month_id = 1 if month_id == 1 else month_id - 1
    nx_month_id = 12 if month_id == 12 else month_id + 1

    pr_month_name = date_template[str(year_id)][str(pr_month_id)]['name']
    nx_month_name = date_template[str(year_id)][str(nx_month_id)]['name']
    month_name = date_template[str(year_id)][str(month_id)]['name']

    day = day_table.format(year_id=year_id,
                           month_name=month_name,
                           pr_m_id=pr_month_id,
                           nx_m_id=nx_month_id,
                           pr_m_name=pr_month_name,
                           nx_m_name=nx_month_name,
                           weeks=gen_weeks(year_id, month_id, {}))
    return body_html.format(day)


@app.route(hours_route)
def get_hours_page_for_day(year_id, month_id, day_id):
    # ToDo(den) add logic
    # https://github.com/stasya72008/highway-to-hell/issues/13
    # tasks = get_task_for_rest()
    tasks = {}

    # ToDo add switch to previous and next month / year
    if day_id == 1:
        pr_day_id = date_template[str(year_id)][str(month_id - 1)]['days']
        nx_day_id = 2
        # pr_month_id = month_id - 1
        # nx_month_id = month_id
    elif day_id == date_template[str(year_id)][str(month_id)]['days']:
        pr_day_id = day_id - 1
        nx_day_id = 1
        # pr_month_id = month_id
        # nx_month_id = month_id + 1
    else:
        pr_day_id = day_id - 1
        nx_day_id = day_id + 1
        # pr_month_id = month_id
        # nx_month_id = month_id

    hour = hour_table.format(year_id=year_id,
                             month_id=month_id,
                             day_id=day_id,
                             pr_day_id=pr_day_id,
                             nx_day_id=nx_day_id,
                             # pr_month_id=pr_month_id,
                             # nx_month_id=nx_month_id,
                             hours=gen_hours(tasks))
    return body_html.format(hour)


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
    if month_id == 1:
        prev_month = date_template[str(year_id - 1)][str(12)]['days']\
                     - first_d + 2
    else:
        prev_month = date_template[str(year_id)][str(month_id - 1)]['days']\
                     - first_d + 2

    # form previous month
    while first_d > day_of_week:
        week = week.replace('{{d_{}}}'.format(day_of_week),
                            day_cell_pr_month.format(day_id=prev_month))
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

        week = week.replace('{{d_{}}}'.format(day_of_week), day)
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
        week = week.replace('{{d_{}}}'.format(day_of_week),
                            day_cell_pr_month.format(day_id=d_index))
        d_index += 1
        day_of_week += 1

    month = '{}{}'.format(month, week)
    return month
