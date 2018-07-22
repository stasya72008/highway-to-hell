from flask import Flask, request, redirect
import config

from helpers import date_template, gen_day_cell, gen_month_cell, gen_year_cell
from html_template import *
from web_app.rest_client.client import create_task

app = Flask(__name__)

config = config.CalendarConfig()

global_url_for_redirect = task_preset_link


@app.route(task_preset_link + '/', methods=['get'])
@app.route(task_preset_link, methods=['get'])
def get_form():
    _today = datetime.datetime.now()

    form = task_preset_form.format(
        year=request.args.get('y', _today.year),
        month=request.args.get('m', _today.month),
        day=request.args.get('d', _today.day),
        hour=request.args.get('h', _today.hour))
    return form


@app.route(task_creator_link, methods=['post'])
def set_form():
    if request.form.get('calendar') == 'on':
        calendar_date = '|'.join([request.form.get('year'),
                                  request.form.get('month'),
                                  request.form.get('day'),
                                  request.form.get('hour')])
    else:
        calendar_date = ''

    create_task(user_id=1,
                task_name=request.form.get('task_title'),
                calendar_date=calendar_date)
    # ToDo(den) check return status
    # ToDo(den) remove global ++)
    global global_url_for_redirect
    url_for_redirect = global_url_for_redirect
    global_url_for_redirect = task_preset_link

    return redirect(url_for_redirect)


@app.route(years_route + '/', methods=['get'])
@app.route(years_route, methods=['get'])
def page_of_years():
    # ToDo(den) Drop it url
    return body_html.replace('[table]', year_table)


@app.route(months_route + '/', methods=['get'])
@app.route(months_route, methods=['get'])
def page_of_months(year_id):
    global global_url_for_redirect
    global_url_for_redirect = request.base_url

    if year_id == 2018:
        prev_year_id = 2018
        next_year_id = year_id + 1
    elif year_id == 2020:
        prev_year_id = year_id - 1
        next_year_id = 2020
    else:
        prev_year_id = year_id - 1
        next_year_id = year_id + 1

    full_year = gen_year_cell(year_id).format(year=year_id,
                                              prev_year=prev_year_id,
                                              next_year=next_year_id)

    return body_html.replace('[table]', full_year)


@app.route(days_route + '/', methods=['get'])
@app.route(days_route, methods=['get'])
def page_of_days(year_id, month_id):
    global global_url_for_redirect
    global_url_for_redirect = request.base_url

    # ToDo add switch to previous and next year
    prev_month_id = 1 if month_id == 1 else month_id - 1
    next_month_id = 12 if month_id == 12 else month_id + 1

    prev_month_name = date_template[str(year_id)][str(prev_month_id)]['name']
    next_month_name = date_template[str(year_id)][str(next_month_id)]['name']
    month_name = date_template[str(year_id)][str(month_id)]['name']

    full_month = day_table.format(year=year_id,
                                  month_name=month_name,
                                  prev_m=prev_month_id,
                                  next_m=next_month_id,
                                  prev_m_name=prev_month_name,
                                  next_m_name=next_month_name,
                                  weeks=gen_month_cell(year_id, month_id))
    return body_html.replace('[table]', full_month)


@app.route(hours_route + '/', methods=['get'])
@app.route(hours_route, methods=['get'])
def page_of_hours(year_id, month_id, day_id):
    global global_url_for_redirect
    global_url_for_redirect = request.base_url

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

    full_day = hour_table.format(year=year_id,
                                 month=month_id,
                                 day=day_id,
                                 prev_day=prev_day_id,
                                 next_day=next_day_id,
                                 hours=gen_day_cell(year_id, month_id, day_id))
    return body_html.replace('[table]', full_day)


if __name__ == '__main__':
    app.run(host=config.host, port=int(config.port), debug=config.debug)
