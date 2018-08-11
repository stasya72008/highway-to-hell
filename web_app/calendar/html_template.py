from calendar_routes import *
import datetime
from os import path

_today = datetime.datetime.now()

# ================ HTML ========================
# year, month, day, hour

with open(path.join('static', 'pages', 'task_form.html'), 'r') as f:
    task_preset_form = f.read()

with open(path.join('static', 'pages', 'calendar_page.html'), 'r') as f:
    main_page = f.read()

with open(path.join('static', 'pages', 'daily_page.html'), 'r') as f:
    daily_page = f.read()

daily_page = daily_page.replace('[daily_route]', daily_route) \
                       .replace('[months_link]', months_link)\
                       .replace('[days_link]', days_link)\
                       .replace('[hours_link]', hours_link)\
                       .replace('[tasks_add_route]', tasks_add_route)

daily_body = daily_page.format(year=_today.year,
                               month=_today.month,
                               day=_today.day,
                               hour=_today.hour)

main_page = main_page.replace('[daily_route]', daily_route) \
                     .replace('[months_link]', months_link) \
                     .replace('[days_link]', days_link) \
                     .replace('[hours_link]', hours_link) \
                     .replace('[tasks_add_route]', tasks_add_route)

body_html = main_page.format(year=_today.year,
                             month=_today.month,
                             day=_today.day,
                             hour=_today.hour)

# ================ HOUR ========================

hour_table = body_html.replace('[current_link]', days_link)\
                      .replace('[prev_link]', prev_hours_link)\
                      .replace('[next_link]', next_hours_link)

# year, month, day, hour
cell_add_task_link = '''
<a href="{tasks_add_route}?y={{year}}&m={{month}}&d={{day}}&h={{hour}}"> 
<img src="/static/plus.png" alt="Create Task" title="Add" class="icon"></a>
'''.format(tasks_add_route=tasks_add_route)

# bgcolor: #c9f1de - busy
# hour
# task_name
# cell_add_task_link
hour_cell_free = '''
<tr>
    <th width=60>{hour}</th>
    <th colspan="3"> </th>
    <th width=60>{cell_add_task_link}</th>
</tr>'''
hour_cell = '''
<tr bgcolor="#c9f1de">
        <th width=60>{hour}</th>
        <th colspan="3">{task_name}</th>
        <th width=60>{cell_add_task_link}</th>
</tr>'''


# ToDo(den) add links for done, edit, delete ...
# ToDo(den) add styles ...
t_table_inner = '''
    <table class="inner">
        {tasks}
    </table>
'''
t_cell_inner = '''
<tr><td><a href="[tasks_close_reopen_link]" 
         title="Close/Reopen">{task_name}</a></td>

    <td class="icon-cell"><a href="[tasks_close_reopen_link]">
<img src="/static/done.png" alt="done" title="Close/Reopen" class="icon">
</a></td>
 
    <td class="icon-cell"><a href="[tasks_edit_link]">
<img src="/static/edit.png" alt="edit" title="Edit" class="icon">
</a></td> 

    <td class="icon-cell"><a href="[tasks_archive_link]">
<img src="/static/archive.png" alt="archive" title="To Archive" class="icon">
</a></td>

    <td class="icon-cell"><a href="[tasks_delete_link]">
<img src="/static/delete.png" alt="delete" title="Delete" class="icon">
</a></td></tr>
'''.replace('[tasks_delete_link]', tasks_delete_link)\
   .replace('[tasks_archive_link]', tasks_archive_link)\
   .replace('[tasks_close_reopen_link]', tasks_close_reopen_link)\
   .replace('[tasks_edit_link]', tasks_edit_link)

# ==================== DAY ===============

day_table = body_html.replace('[current_link]', months_link)\
                     .replace('[prev_link]', prev_days_link)\
                     .replace('[next_link]', next_days_link)


# bgcolor: #c9f1de - busy, #aaa - Day zero (from another month)
# task_count
# year, month, day (hours_link)
day_cell = '''
<th width=50 bgcolor="#c9f1de"> <a href="{hours_link}">{{day}} ({{task_count}})</a>
</th>'''.format(hours_link=hours_link)
day_cell_free = '''
<th width=50 > <a href="{hours_link}">{{day}}</a></th>
'''.format(hours_link=hours_link)

day_cell_another_month = '<th width=50 bgcolor="#aaa">{day}</th>'

# ================ WEEK ========================

week_table = ' <tr> [d_1] [d_2] [d_3] [d_4] [d_5] [d_6] [d_7] </tr>'

# ================ MONTH ========================

months_line = '''
<tr> [m_1]  [m_2]  [m_3] </tr>  <tr> [m_4]  [m_5]  [m_6] </tr> 
<tr> [m_7]  [m_8]  [m_9] </tr>  <tr> [m_10] [m_11] [m_12] </tr>'''

month_table = body_html.replace('[current_link]', '""')\
                       .replace('[prev_link]', prev_months_link)\
                       .replace('[next_link]', next_months_link)\
                       .replace('{table}', months_line)\

# bgcolor: #c9f1de - busy
month_cell_free = '''
<th><a href="{months_link}/{{month}}/days">{{month_name}}</a></th>
'''.format(months_link=months_link)
month_cell = '''
<th bgcolor="#c9f1de"><a href="{months_link}/{{month}}/days">{{month_name}} ({{task_count}})</a></th>
'''.format(months_link=months_link)

# ================= YEAR ========================
# deprecated
year_table = '''
<table style="width:50%">
   <tr>
       <th><a href="{year_2018_link}"> 2018 </a></th>
       <th><a href="{year_2019_link}"> 2019 </a></th>
       <th><a href="{year_2020_link}"> 2020 </a></th>
   </tr>
</table>'''.format(year_2018_link=year_2018_link,
                   year_2019_link=year_2019_link,
                   year_2020_link=year_2020_link)
