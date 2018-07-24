from flask import Flask, request, redirect
import config

from helpers import gen_day_cell, gen_month_cell, gen_year_cell, \
    border_items
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


# deprecated
@app.route(years_route + '/', methods=['get'])
@app.route(years_route, methods=['get'])
def page_of_years():
    return body_html.replace('[table]', year_table)


@app.route(months_route + '/', methods=['get'])
@app.route(months_route, methods=['get'])
def page_of_months(year_id):
    global global_url_for_redirect
    global_url_for_redirect = request.base_url

    calendar = border_items(year_id)
    return gen_year_cell(year_id).format(year=year_id,
                                         current_item=year_id,
                                         prev_item=calendar['prev_y'],
                                         next_item=calendar['next_y'],
                                         prev_year=calendar['prev_y'],
                                         next_year=calendar['next_y'])


@app.route(days_route + '/', methods=['get'])
@app.route(days_route, methods=['get'])
def page_of_days(year_id, month_id):
    global global_url_for_redirect
    global_url_for_redirect = request.base_url

    calendar = border_items(year_id, month_id)
    return day_table.format(year=year_id,
                            month=month_id,
                            current_item=calendar['m_name'],
                            prev_item=calendar['prev_m_name'],
                            next_item=calendar['next_m_name'],
                            prev_year=calendar['prev_y'],
                            next_year=calendar['next_y'],
                            prev_month=calendar['prev_m'],
                            next_month=calendar['next_m'],
                            table=gen_month_cell(year_id, month_id))


@app.route(hours_route + '/', methods=['get'])
@app.route(hours_route, methods=['get'])
def page_of_hours(year_id, month_id, day_id):
    global global_url_for_redirect
    global_url_for_redirect = request.base_url

    calendar = border_items(year_id, month_id, day_id)
    return hour_table.format(year=year_id,
                             month=month_id,
                             day=day_id,
                             current_item=day_id,
                             prev_item=calendar['prev_d'],
                             next_item=calendar['next_d'],
                             prev_year=calendar['prev_y'],
                             next_year=calendar['next_y'],
                             prev_month=calendar['prev_m'],
                             next_month=calendar['next_m'],
                             prev_day=calendar['prev_d'],
                             next_day=calendar['next_d'],
                             table=gen_day_cell(year_id, month_id, day_id))


if __name__ == '__main__':
    app.run(host=config.host, port=int(config.port), debug=config.debug)
