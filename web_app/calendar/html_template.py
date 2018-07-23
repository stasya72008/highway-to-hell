from calendar_routes import *
import datetime
from os import path

_today = datetime.datetime.now()

# ================ HTML ========================
# year, month, day, hour

with open(path.join('static', 'pages', 'task_creation_form.html'), 'r') as f:
    task_preset_form = f.read().replace('[task_creator_link]', task_creator_link)

with open(path.join('static', 'pages', 'calendar_page.html'), 'r') as f:
    main_page = f.read()

main_page = main_page.replace('[years_route]', years_route) \
                     .replace('[months_link]', months_link) \
                     .replace('[days_link]', days_link) \
                     .replace('[hours_link]', hours_link) \
                     .replace('[task_preset_link]', task_preset_link)

body_html = main_page.format(year=_today.year,
                             month=_today.month,
                             day=_today.day,
                             hour=_today.hour)

# ================ HOUR ========================
# year, month, day, hour
cell_add_task_link = '''
<a href="{task_preset_link}?y={{year}}&m={{month}}&d={{day}}&h={{hour}}"> 
<img src="/static/plus.png" alt="Create Task" title="Add" class="icon"></a>
'''.format(task_preset_link=task_preset_link)

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


# year, month (days_link)
# day, hours
# prev_day, next_day
# ToDo add switch to previous and next month
# ToDo(den) move title with previous and next (month, year, day) to out
hour_table = '''
    <table style="width:50%">
        <tr>
            <th colspan="2"><a href="[prev_hours_link]"> ({prev_day}) </a></th>
            <th><a href="[days_link]">{day}</a></th>
            <th colspan="2"><a href="[next_hours_link]"> ({next_day}) </a></th>
        </tr>
        <tr>{hours}</tr>
    </table>
'''.replace('[days_link]', days_link)\
   .replace('[prev_hours_link]', prev_hours_link)\
   .replace('[next_hours_link]', next_hours_link)


# ToDo(den) add links for done, edit, delete ...
# ToDo(den) add styles ...
t_table_inner = '''
    <table class="inner">
        {tasks}
    </table>
'''
t_cell_inner = '''
<tr><td><a href="" title="Close/Reopen">{task_name}</a></td>

    <td class="icon-cell"><a href="">
<img src="/static/done.png" alt="done" title="Close/Reopen" class="icon">
</a></td>
 
    <td class="icon-cell"><a href="">
<img src="/static/edit.png" alt="edit" title="Edit" class="icon">
</a></td> 

    <td class="icon-cell"><a href="">
<img src="/static/archive.png" alt="archive" title="To Archive" class="icon">
</a></td>

    <td class="icon-cell"><a href="">
<img src="/static/delete.png" alt="delete" title="Delete" class="icon">
</a></td></tr>
'''

# ==================== DAY ===============
# bgcolor: #c9f1de - busy, #aaa - Day zero (from another month)
# year (months_link)
# prev_m, prev_m_name - previous month
# next_m, next_m_name - next month
# weeks
# ToDo(den) move title with previous and next (month, year, day) to out
day_table = '''
    <table style="width:50%">
        <tr>
            <th colspan="2"><a href="[prev_days_link]">({prev_m_name})</a></th>
            <th colspan="3"><a href="[months_link]">{month_name} ({year})</a></th>
            <th colspan="2"><a href="[next_days_link]">({next_m_name})</a></th>
        </tr>
        {weeks}
    </table>
'''.replace('[months_link]', months_link)\
   .replace('[prev_days_link]', prev_days_link)\
   .replace('[next_days_link]', next_days_link)


# day
day_cell_another_month = '<th width=50 bgcolor="#aaa">{day}</th>'

# task_count
# year, month, day (hours_link)
day_cell = '''
<th width=50 bgcolor="#c9f1de"> <a href="{hours_link}">{{day}} ({{task_count}})</a>
</th>'''.format(hours_link=hours_link)
day_cell_free = '''
<th width=50 > <a href="{hours_link}">{{day}}</a></th>
'''.format(hours_link=hours_link)

# ================ WEEK ========================

week_table = ' <tr> [d_1] [d_2] [d_3] [d_4] [d_5] [d_6] [d_7] </tr>'

# ================ MONTH ========================
# ToDo(den) move title with previous and next (month, year, day) to out
# bgcolor: #c9f1de - busy
# year (months_link)
# month month_name
# task_count
month_cell_free = '''
<th><a href="{months_link}/{{month}}/days">{{month_name}}</a></th>
'''.format(months_link=months_link)
month_cell = '''
<th bgcolor="#c9f1de"><a href="{months_link}/{{month}}/days">{{month_name}} ({{task_count}})</a></th>
'''.format(months_link=months_link)

# year
# prev_year, next_year
month_table = '''
    <table style="width:50%">
        <tr>
            <th><a href="[prev_months_link]"> ({prev_year}) </a></th>
            <th>{year}</th>
            <th><a href="[next_months_link]"> ({next_year}) </a></th>
        </tr>
        <tr> [m_1]  [m_2]  [m_3] </tr>  <tr> [m_4]  [m_5]  [m_6] </tr> 
        <tr> [m_7]  [m_8]  [m_9] </tr>  <tr> [m_10] [m_11] [m_12] </tr>
    </table>'''.replace('[prev_months_link]', prev_months_link)\
               .replace('[next_months_link]', next_months_link)


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

