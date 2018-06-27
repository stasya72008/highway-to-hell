import json
from flask import Flask
from html_template import *

app = Flask(__name__)


date_template = {}
with open('date_template.json', 'r') as file:
    date_template = json.loads(file.read())


@app.route('/years')
def get_years_page():
    return body_html.format(year_table)


@app.route('/years/<y_id>/months')
def get_months_page_for_year(y_id):

    # ToDo(den) add logic
    # https://github.com/stasya72008/highway-to-hell/issues/13

    # tasks = get_task_for_rest()

    # remove
    month_busy.update({'May': "#eee",
                       'May_task_count': " (3)"})
    month_busy.update({'April': "#eee",
                       'April_task_count': " (1)"})
    # ------

    month = month_table.format(year_id=y_id,
                               **month_busy)
    return body_html.format(month)


@app.route('/years/<int:y_id>/months/<int:m_id>/days')
def get_days_page_for_month(y_id, m_id):

    # tasks = get_task_for_rest()
    tasks = {}

    # ToDo(den) add logic
    # https://github.com/stasya72008/highway-to-hell/issues/13


    pr_month_id = (m_id - 1) if (m_id - 1) != 0 else 12
    nx_month_id = (m_id + 1) if (m_id + 1) != 13 else 1

    pr_month_name = date_template[str(y_id)][str(pr_month_id)]['name']
    nx_month_name = date_template[str(y_id)][str(nx_month_id)]['name']
    month_name = date_template[str(y_id)][str(m_id)]['name']

    day = day_table.format(year_id=y_id,
                           month=month_name,
                           pr_month_id=pr_month_id,
                           nx_month_id=nx_month_id,
                           pr_month_name=pr_month_name,
                           nx_month_name=nx_month_name)
    return body_html.format(day)

@app.route('/years/<y_id>/months/<int:m_id>/days/<int:d_id>')
def get_hours_page_for_day(y_id, m_id, d_id):

    # tasks = get_task_for_rest()
    tasks = {}

    return body_html.format(hour_table.format(
        year_id=y_id, month_id=m_id, day_id=d_id, hours=gen_hours(tasks)))


def gen_hours(tasks):
    day = ''
    for h_id in range(1, 24):

        # ToDo(den) add logic
        # https://github.com/stasya72008/highway-to-hell/issues/13


        # remove
        if h_id in (3,15,20):
            day += hour_cell.format(hour_id=h_id,
                                    task_name='test_{}'.format(h_id))
        else:
            day += hour_cell_empty.format(hour_id=h_id)
        # --------

    return day


def gen_week(y_id, m_id, tasks):
    week = ''
    number_of_day = date_template[y_id][str(m_id)]['days']
    first_day_in_month = date_template[y_id][str(m_id)]['first_day']

    for d_id in range(1, number_of_day):
        first_week = True

        if first_week:
            first_week = False
            for d_index in range(1, first_day_in_month):
                week += day_cell_zero
            for d_index in range(first_day_in_month, 8):
                week += day_cell_empty
        else:
            for d_index in range(1, 8):
                pass

        # ToDo(den) add logic
        # https://github.com/stasya72008/highway-to-hell/issues/13


                # # remove
        # if h_id in (3,15,20):
        #     day += hour_cell.format(hour_id=h_id,
        #                             task_name='test_{}'.format(h_id))
        # else:
        #     day += hour_cell_empty.format(hour_id=h_id)
        # # --------

    return week
