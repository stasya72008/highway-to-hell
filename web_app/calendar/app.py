from flask import Flask, request, redirect
import config

from helpers import gen_day_cell, gen_month_cell, gen_year_cell, \
    border_items, set_parameters, pop_parameter, gen_daily_cells, user_id
from html_template import *
from web_app.rest_client.client import create_task, delete_task, edit_task, \
    get_task_by_id

app = Flask(__name__)

config = config.CalendarConfig()


# Create task
@app.route(tasks_add_route + '/', methods=['get'])
@app.route(tasks_add_route, methods=['get'])
def tasks_add():
    _today = datetime.datetime.now()

    form = task_preset_form.format(
        year=request.args.get('y', _today.year),
        month=request.args.get('m', _today.month),
        day=request.args.get('d', _today.day),
        hour=request.args.get('h', _today.hour))
    return form


@app.route(task_creator_link, methods=['post'])
def tasks_creator():
    if request.form.get('calendar') == 'on':
        calendar_date = '|'.join([request.form.get('year'),
                                  request.form.get('month'),
                                  request.form.get('day'),
                                  request.form.get('hour')])
    else:
        calendar_date = ''

    # ToDo(den) get user_id from header (global dict...(= )
    create_task(user_id=user_id,
                task_name=request.form.get('task_title'),
                calendar_date=calendar_date)
    # ToDo(den) check return status
    url_for_redirect = pop_parameter()

    return redirect(url_for_redirect)


# Delete task
@app.route(tasks_delete_route, methods=['get'])
def task_remover(task_id):
    delete_task(task_id)

    # ToDo(den) check return status
    url_for_redirect = pop_parameter()

    return redirect(url_for_redirect)


# Close/ reopen task
@app.route(tasks_close_reopen_route, methods=['get'])
def tasks_close_reopen(task_id):

    if get_task_by_id(task_id)['status'] == 'active':
        edit_task(task_id, status='done')
    elif get_task_by_id(task_id)['status'] == 'done':
        edit_task(task_id, status='active')
    else:
        # ToDo(den) return error for invalid status
        pass
    # ToDo(den) check return status

    url_for_redirect = pop_parameter()
    return redirect(url_for_redirect)


# Archive task
@app.route(tasks_archive_route, methods=['get'])
def tasks_archive(task_id):

    edit_task(task_id, status='archive')
    # ToDo(den) return error for invalid status

    # ToDo(den) check return status
    url_for_redirect = pop_parameter()
    return redirect(url_for_redirect)


# deprecated
@app.route(years_route + '/', methods=['get'])
@app.route(years_route, methods=['get'])
def page_of_years():
    return body_html.replace('[table]', year_table)


@app.route(months_route + '/', methods=['get'])
@app.route(months_route, methods=['get'])
def page_of_months(year_id):
    set_parameters(base_url=request.base_url)

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
    set_parameters(base_url=request.base_url)

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
    set_parameters(base_url=request.base_url)

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


@app.route(daily_route + '/', methods=['get'])
@app.route(daily_route, methods=['get'])
def daily_page():
    set_parameters(base_url=request.base_url)
    return daily_body.replace('{table}', gen_daily_cells(user_id))


if __name__ == '__main__':
    app.run(host=config.host, port=int(config.port), debug=config.debug)
