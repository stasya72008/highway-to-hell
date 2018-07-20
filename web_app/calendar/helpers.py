from copy import copy
import json

from html_template import *
from web_app.rest_client.client import get_all_user_tasks

with open('date_template.json', 'r') as f:
    date_template = json.loads(f.read())


def gen_year_cell(year):
    full_year = copy(month_table)
    for m_index in range(1, 13):
        month_name = date_template[str(year)][str(m_index)]['name']
        task_count = len(get_tasks_for_period(year, m_index))
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
        task_count = len(get_tasks_for_period(year, month, d_index))
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
    for h_index in range(0, 24):
        tasks = get_tasks_for_period(year, month, day, h_index)

        cell = cell_add_task_link.format(year=year,
                                         month=month,
                                         day=day,
                                         hour=h_index)

        if tasks:
            task_line = ''
            for task in tasks:
                if task.get('status') == 'done':
                    task_name = '<s>{}</s>'.format(task.get('name'))
                else:
                    task_name = task.get('name')
                task_line += t_cell_inner.format(task_name=task_name)
            full_day += hour_cell.format(
                hour=h_index,
                task_name=t_table_inner.format(tasks=task_line),
                cell_add_task_link=cell)
        else:
            full_day += hour_cell_free.format(hour=h_index,
                                              cell_add_task_link=cell)
    return full_day


# ToDo(den) move this logic to rest
def get_tasks_for_period(*args):
    """ The method for selecting tasks for user by date

    :param args: year, [month], [day], [hour]
    :return: list of tasks for the period
    """

    # ToDo(den) get user_id from header or cookies request
    tasks = get_all_user_tasks(user_id=1)

    period = '|'.join([str(arg) for arg in args])

    tasks = [task for task in tasks if
             task.get('calendar_date').startswith(period) and
             task.get('status') in ('active', 'done')]

    return tasks
