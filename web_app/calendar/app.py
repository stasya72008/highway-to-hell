import os
import logging
import config

from flask import Flask, flash, request, redirect, render_template
from flask_login import LoginManager, login_user, login_required, \
    logout_user, UserMixin, current_user

from html_template import *
from helpers import gen_day_cell, gen_month_cell, gen_year_cell, \
    gen_daily_cells, border_items, \
    set_parameters, pop_parameter, get_parameter
from web_app.rest_client.client import create_task, delete_task, edit_task, \
    get_task_by_id, get_user_by_name

app = Flask(__name__)
login_manager = LoginManager()

config.LogConfig()
logger = logging.getLogger("UI")
config = config.CalendarConfig()


# ------------ Login ------------------
class UserLogin(UserMixin):
    def __init__(self, user_id, name=None, password=None, admin=False):
        self.id = user_id
        self.name = name
        self.password = password
        self.is_admin = admin


@login_manager.user_loader
def load_user(user_id):
    # ToDo probably better get user from DB
    return UserLogin(user_id)


@app.after_request
def redirect_to_signing(response):
        if response.status_code == 401:
            logger.warning('Response code 401. Redirecting user to login page')
            flash("Please, Login!")
            return redirect('/login')
        else:
            return response


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        # ToDo(den) Add password
        user = get_user_by_name(request.form['username'])
        if user:
            login_user(UserLogin(user_id=user['id'], name=user['name']))
            logger.info('User %s successfully logged in' % user['name'])
            return daily_page()
        else:
            flash('Wrong user name or password!')
            logger.warning('User %s login failed' % request.form['username'])
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    logger.info('User logged out')
    flash('Logout successfully!')
    return redirect('/login')


# ------------ TASK ------------------
@app.route(tasks_add_route + '/', methods=['get'])
@app.route(tasks_add_route, methods=['get'])
@login_required
def tasks_add():
    _today = datetime.now()
    url_for_redirect = get_parameter()

    form = task_preset_form.format(
        year=request.args.get('y', _today.year),
        month=request.args.get('m', _today.month),
        day=request.args.get('d', _today.day),
        hour=request.args.get('h', _today.hour),
        redirect=url_for_redirect)
    # make calendar date hidden
    if request.args.get('calendar', '1') == '0':
        form = form.replace('checked="checked"', '')

    # send request to tasks_creator
    form = form.replace('[task_creator_link]', task_creator_link)
    return form


@app.route(task_creator_link, methods=['post'])
@login_required
def tasks_creator():
    if request.form.get('calendar') == 'on':
        calendar_date = datetime(int(request.form.get('year')),
                                 int(request.form.get('month')),
                                 int(request.form.get('day')),
                                 int(request.form.get('hour'))) \
            .strftime("%Y-%m-%d %H:%M:%S")
    else:
        calendar_date = None

    create_task(user_id=current_user.id,
                task_name=request.form.get('task_title'),
                calendar_date=calendar_date)
    # ToDo(den) check return status
    url_for_redirect = pop_parameter()

    return redirect(url_for_redirect)


@app.route(tasks_edit_route + '/', methods=['get'])
@app.route(tasks_edit_route, methods=['get'])
@login_required
def tasks_edit(task_id):
    task = get_task_by_id(task_id)
    url_for_redirect = get_parameter()

    if task.get('calendar_date') is not None:
        obj_date = datetime.strptime(task.get('calendar_date'),
                                     "%Y-%m-%d %H:%M:%S")
    else:
        obj_date = datetime.now()

    form = task_preset_form.format(
        year=obj_date.year,
        month=obj_date.month,
        day=obj_date.day,
        hour=obj_date.hour,
        redirect=url_for_redirect)

    # make calendar date hidden
    if task.get('calendar_date') is None:
        form = form.replace('checked="checked"', '')

    # set name of task
    form = form.replace('</textarea>', task.get('name') + '</textarea>')
    # set id of task
    form = form.replace('[task_id]', str(task_id))
    # send request to tasks_editor
    form = form.replace('[task_creator_link]', task_editor_link)

    return form


@app.route(task_editor_link, methods=['post'])
@login_required
def tasks_editor():
    task_id = request.form.get('task')
    task = get_task_by_id(task_id)

    calendar_date = None
    status = None
    if request.form.get('calendar') == 'on':
        set_date = datetime(int(request.form.get('year')),
                            int(request.form.get('month')),
                            int(request.form.get('day')),
                            int(request.form.get('hour')))

        # Calendar is on, task does not have date or has not the same date
        # - set date, activate task
        status = 'active'
        calendar_date = set_date.strftime("%Y-%m-%d %H:%M:%S")

        # Calendar is on, task has the same date - ignore changing
        if task.get('calendar_date') and \
            set_date == datetime.strptime(
                task.get('calendar_date'), "%Y-%m-%d %H:%M:%S"):

            calendar_date = None

    # Calendar is off, task has date - clear date
    elif task.get('calendar_date'):
        calendar_date = '0000-00-00 00:00:00'

    task_name = None
    if task.get('name') != request.form.get('task_title'):
        task_name = request.form.get('task_title')

    if task_name or calendar_date:
        edit_task(task_id=task_id,
                  task_name=task_name,
                  calendar_date=calendar_date,
                  status=status)

    # ToDo(den) check return status
    url_for_redirect = pop_parameter()
    return redirect(url_for_redirect)


@app.route(tasks_delete_route, methods=['get'])
@login_required
def task_remover(task_id):
    delete_task(task_id)

    # ToDo(den) check return status
    url_for_redirect = pop_parameter()

    return redirect(url_for_redirect)


@app.route(tasks_close_reopen_route, methods=['get'])
@login_required
def tasks_close_reopen(task_id):
    status = get_task_by_id(task_id)['status']

    if status == 'active':
        edit_task(task_id, status='done')
    elif status == 'done':
        edit_task(task_id, status='active')
    else:
        # ToDo(den) return error for invalid status
        pass
    # ToDo(den) check return status

    url_for_redirect = pop_parameter()
    return redirect(url_for_redirect)


@app.route(tasks_archive_route, methods=['get'])
@login_required
def tasks_archive(task_id):
    status = get_task_by_id(task_id)['status']

    edit_task(task_id, status='active') if status == 'archive' \
        else edit_task(task_id, status='archive')

    # ToDo(den) check return status
    url_for_redirect = pop_parameter()
    return redirect(url_for_redirect)


# ------------ PAGES ------------------
# deprecated
@app.route(years_route + '/', methods=['get'])
@app.route(years_route, methods=['get'])
def page_of_years():
    return body_html.replace('[table]', year_table)


@app.route(months_route + '/', methods=['get'])
@app.route(months_route, methods=['get'])
@login_required
def page_of_months(year_id):
    set_parameters(base_url=request.url)

    calendar = border_items(year_id)
    return gen_year_cell(current_user.id, year_id).format(
        year=year_id,
        current_item=year_id,
        prev_item=calendar['prev_y'],
        next_item=calendar['next_y'],
        prev_year=calendar['prev_y'],
        next_year=calendar['next_y'])


@app.route(days_route + '/', methods=['get'])
@app.route(days_route, methods=['get'])
@login_required
def page_of_days(year_id, month_id):
    set_parameters(base_url=request.url)

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
                            table=gen_month_cell(current_user.id,
                                                 year_id, month_id))


@app.route(hours_route + '/', methods=['get'])
@app.route(hours_route, methods=['get'])
@login_required
def page_of_hours(year_id, month_id, day_id):
    set_parameters(base_url=request.url)

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
                             table=gen_day_cell(current_user.id,
                                                year_id, month_id, day_id))


@app.route(daily_route + '/', methods=['get'])
@app.route(daily_route, methods=['get'])
@login_required
def daily_page():
    set_parameters(base_url=request.url)

    archive = True if request.args.get('archive') == 'True' else False
    body = daily_body.format(table=gen_daily_cells(current_user.id, archive),
                             archive=not archive)

    return body.replace('Daily', 'Archive') if archive else body


if __name__ == '__main__':
    login_manager.init_app(app)
    app.secret_key = os.urandom(12)
    app.run(host=config.host, port=int(config.port), debug=config.debug)
