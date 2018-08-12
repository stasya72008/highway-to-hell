from copy import copy
import json

from html_template import *
from web_app.rest_client.client import get_all_user_tasks, \
    get_task_count_for_period, get_tasks_for_period

with open('date_template.json', 'r') as f:
    _date_template = json.loads(f.read())


# Get / Set Headers
# ToDo(den) create dict with parameters
# ToDo(den) Will do something this it !!!
# https://github.com/stasya72008/highway-to-hell/projects/2#card-11882791
_global_url_for_redirect = tasks_add_route
user_id = 3


def set_parameters(base_url):
    global _global_url_for_redirect
    _global_url_for_redirect = base_url


def pop_parameter():
    global _global_url_for_redirect
    url_for_redirect = _global_url_for_redirect
    _global_url_for_redirect = tasks_add_route
    return url_for_redirect


def get_parameter():
    return _global_url_for_redirect
# Get / Set Headers


def gen_year_cell(user_id, year):
    full_year = copy(month_table)

    task_count_for_period = get_task_count_for_period(user_id, year)
    for m_index in range(1, 13):
        month_name = _date_template[str(m_index)]

        task_count = task_count_for_period.get(str(m_index))
        if task_count:
            m_cell = month_cell.format(year=year,
                                       month=m_index,
                                       month_name=month_name,
                                       task_count=task_count)
        else:
            m_cell = month_cell_free.format(year=year,
                                            month=m_index,
                                            month_name=month_name)

        full_year = full_year.replace('[m_{}]'.format(m_index), m_cell)

    return full_year


def gen_month_cell(year, month):
    week = copy(week_table)
    full_month = ''

    day_of_week = 1
    d_index = 1

    number_of_d = _date_template[str(year)][str(month)]['days']
    first_d = _date_template[str(year)][str(month)]['first_day']
    if month == 1:
        prev_month_days = \
            _date_template[str(year - 1)]['12']['days'] - first_d + 2
    else:
        prev_month_days = \
            _date_template[str(year)][str(month - 1)]['days'] - first_d + 2

    # form previous month
    while first_d > day_of_week:
        week = week.replace('[d_{}]'.format(day_of_week),
                            day_cell_another_month.format(day=prev_month_days))
        prev_month_days += 1
        day_of_week += 1

    # form current month
    task_count_for_period = get_task_count_for_period(user_id, year, month)
    while d_index < number_of_d + 1:
        task_count = task_count_for_period.get(str(d_index))
        if task_count:
            day = day_cell.format(year=year,
                                  month=month,
                                  day=d_index,
                                  task_count=task_count)
        else:
            day = day_cell_free.format(year=year,
                                       month=month,
                                       day=d_index)

        week = week.replace('[d_{}]'.format(day_of_week), day)

        d_index += 1
        if day_of_week % 7 == 0:
            full_month = '{}{}'.format(full_month, week)
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

    full_month = '{}{}'.format(full_month, week)
    return full_month


def gen_day_cell(year, month, day):
    full_day = ''

    tasks = get_tasks_for_period(user_id, year, month, day)
    for h_index in range(0, 24):
        hour_tasks = [t for t in tasks if datetime.strptime(
            t.get('calendar_date'), "%Y-%m-%d %H:%M:%S").hour == h_index and
            t.get('status') in ('active', 'done')]

        if hour_tasks:
            task_line = ''
            for task in hour_tasks:
                if task.get('status') == 'done':
                    task_name = '<s>{}</s>'.format(task.get('name'))
                else:
                    task_name = task.get('name')
                task_line += t_cell_inner.format(task=task.get('id'),
                                                 task_name=task_name)
            full_day += hour_cell.format(
                task_name=t_table_inner.format(tasks=task_line),
                year=year,
                month=month,
                day=day,
                hour=h_index)
        else:
            full_day += hour_cell_free.format(year=year,
                                              month=month,
                                              day=day,
                                              hour=h_index)

    return full_day


def gen_daily_cells(user_id, archive=False):
    if archive:
        status = ('archive', )
    else:
        status = ('active', 'done')

    tasks = [t for t in get_all_user_tasks(user_id)
             if t.get('status') in status]

    task_line = ''
    for task in tasks:
        if task.get('status') == 'done':
            task_name = '<s>{}</s>'.format(task.get('name'))
        else:
            task_name = task.get('name')
        task_line += t_cell_inner.format(task=task.get('id'),
                                         task_name=task_name)
    return task_line


def border_items(year, month=None, day=None):
    result = {}

    if day is not None:
        result['next_y'] = year
        result['prev_y'] = year
        result['next_m'] = month
        result['prev_m'] = month
        result['prev_d'] = day - 1
        result['next_d'] = day + 1

        if day == 1:
            calendar = border_items(year, month)
            result['prev_y'] = str(calendar['prev_y'])
            result['prev_m'] = str(calendar['prev_m'])
            result['prev_d'] = _date_template.get(
                result['prev_y'])[result['prev_m']]['days']

        elif day == _date_template[str(year)][str(month)]['days']:
            calendar = border_items(year, month)
            result['next_y'] = str(calendar['next_y'])
            result['next_m'] = str(calendar['next_m'])
            result['next_d'] = 1

    elif month is not None:
        result['next_y'] = year
        result['prev_y'] = year
        result['prev_m'] = month - 1
        result['next_m'] = month + 1

        if month == 1:
            result['prev_m'] = 12
            result['prev_y'] = str(border_items(year)['prev_y'])
        elif month == 12:
            result['next_m'] = 1
            result['next_y'] = str(border_items(year)['next_y'])

        result['prev_m_name'] = _date_template[str(result['prev_m'])]
        result['next_m_name'] = _date_template[str(result['next_m'])]
        result['m_name'] = _date_template[str(month)]

    elif year:
        result['prev_y'] = year - 1
        result['next_y'] = year + 1

        if year == 2018:
            result['prev_y'] = 2018
        elif year == 2020:
            result['next_y'] = 2020

    return result
