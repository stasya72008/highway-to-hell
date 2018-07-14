import copy
from flask import Flask, request, redirect

from helpers import gen_hours, gen_weeks, date_template
from html_template import *

app = Flask(__name__)


@app.route(task_preset_link)
@app.route(task_preset_link + '/')
def get_form():
    args = dict(request.args)
    form = task_preset_form.format(redirect=args.get('redirect')[0],
                                   year=args.get('y')[0],
                                   month=args.get('m')[0],
                                   day=args.get('d')[0],
                                   hour=args.get('h')[0])
    return form


@app.route(task_creator_link, methods=['post'])
def set_form():
    print dict(request.form)
    args = dict(request.args)

    redirect_to_url = args.get('redirect', [task_preset_link])[0]
    # print request.form
    # resp = create_task(user_id='1', task_name=request.form.get('title')[0], date=None)

    return redirect(redirect_to_url)


@app.route(years_route)
@app.route(years_route + '/')
def get_years_page():
    # ToDo Get years from date_template and form page
    return body_html.format(year_table)


@app.route(months_route)
@app.route(months_route + '/')
def get_months_page_for_year(year_id):
    month = copy.copy(month_table)
    for m_index in range(1, 13):
        month_name = date_template[str(year_id)][str(m_index)]['name']

        # ToDo(den) add logic
        # https://github.com/stasya72008/highway-to-hell/issues/13
        # remove -----------
        if m_index not in (1, 3, 9):
            m_cell = month_cell_free.format(year=year_id,
                                            month=m_index,
                                            month_name=month_name)
        else:
            m_cell = month_cell.format(year=year_id,
                                       month=m_index,
                                       month_name=month_name,
                                       task_count='3')
        # ------------------
        month = month.replace('[m_{}]'.format(m_index), m_cell)

    if year_id == 2018:
        prev_year_id = 2018
        next_year_id = year_id + 1
    elif year_id == 2020:
        prev_year_id = year_id - 1
        next_year_id = 2020
    else:
        prev_year_id = year_id - 1
        next_year_id = year_id + 1

    month = month.format(year=year_id,
                         prev_year=prev_year_id,
                         next_year=next_year_id)

    return body_html.format(month)


@app.route(days_route)
@app.route(days_route + '/')
def get_days_page_for_month(year_id, month_id):
    # ToDo(den) add logic
    # https://github.com/stasya72008/highway-to-hell/issues/13
    # tasks = get_task_for_rest()

    # ToDo add switch to previous and next year
    prev_month_id = 1 if month_id == 1 else month_id - 1
    next_month_id = 12 if month_id == 12 else month_id + 1

    prev_month_name = date_template[str(year_id)][str(prev_month_id)]['name']
    next_month_name = date_template[str(year_id)][str(next_month_id)]['name']
    month_name = date_template[str(year_id)][str(month_id)]['name']

    day = day_table.format(year=year_id,
                           month_name=month_name,
                           prev_m=prev_month_id,
                           next_m=next_month_id,
                           prev_m_name=prev_month_name,
                           next_m_name=next_month_name,
                           weeks=gen_weeks(year_id, month_id, {}))
    return body_html.format(day)


@app.route(hours_route)
@app.route(hours_route + '/')
def get_hours_page_for_day(year_id, month_id, day_id):
    base_url = request.base_url

    # ToDo(den) add logic
    # https://github.com/stasya72008/highway-to-hell/issues/13
    # tasks = get_task_for_rest()
    tasks = {}

    if day_id == 1:
        # ToDo add switch to previous and next month / year
        prev_day_id = 1
        next_day_id = 2
    elif day_id == date_template[str(year_id)][str(month_id)]['days']:
        prev_day_id = day_id - 1
        next_day_id = day_id
    else:
        prev_day_id = day_id - 1
        next_day_id = day_id + 1

    hour = hour_table.format(year=year_id,
                             month=month_id,
                             day=day_id,
                             prev_day=prev_day_id,
                             next_day=next_day_id,
                             hours=gen_hours(year_id,
                                             month_id,
                                             day_id,
                                             base_url,
                                             tasks))
    return body_html.format(hour)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
