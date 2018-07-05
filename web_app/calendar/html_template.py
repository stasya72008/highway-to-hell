from calendar_routes import *
import json

with open('date_template.json', 'r') as f:
    date_template = json.loads(f.read())

# ================ HTML ========================

body_html = '''<html><head>
                <style>
                   table, th, td {{border: 1px solid black; collapse;}}
                   a {{text-decoration: none; color: black; background-color: while; }}
                </style>
               </head><body>{}</body></html>'''

# ================ HOUR ========================
# ToDO(den) change (add) to button "Create task"
# bgcolor: #eee - busy, #ffffff - free
# hour_id
# task_name
# (add) action for task creation
hour_cell_free = '''
<tr>
    <th width=60 bgcolor="#ffffff">{hour_id}</th>
    <th bgcolor="#ffffff" colspan="3"> </th>
    <th width=60 bgcolor="#ffffff">(add)</th>
</tr>'''
hour_cell = '''
<tr>
        <th width=60 bgcolor="#eee">{hour_id}</th>
        <th bgcolor="#ffffff" colspan="3">{task_name}</th>
        <th width=60 bgcolor="#ffffff">(add)</th>
</tr>'''

# year_id (days_link)
# month_id (days_link)
# day_id
# hours
# prev_day_id, next_day_id
# ToDo add switch to previous and next month
# ToDo(den) move title with previous and next (month, year, day) to out
hour_table = '''
    <table style="width:50%">
        <tr>
            <th colspan="2"><a href="{days_link}/{{prev_day_id}}/hours">({{prev_day_id}})</a></th>
            <th><a href="{days_link}">^ {{day_id}} ^</a></th>
            <th colspan="2"><a href="{days_link}/{{next_day_id}}/hours">({{next_day_id}})</a></th>
        </tr>
        <tr>{{hours}}</tr>
    </table>
'''.format(days_link=days_link)

# ==================== DAY ===============
# bgcolor: #eee - busy, #ffffff - free, #aaa - Day zero (from another month)

# year_id (months_link)
# prev_m_id, prev_m_name - previous month
# next_m_id, next_m_name - next month
# weeks
# ToDo(den) move title with previous and next (month, year, day) to out
day_table = '''
    <table style="width:50%">
        <tr>
            <th colspan="2"><a href="{months_link}/{{prev_m_id}}/days">({{prev_m_name}})</a></th>
            <th colspan="3"><a href="{months_link}">^ {{month_name}} ^</a></th>
            <th colspan="2"><a href="{months_link}/{{next_m_id}}/days">({{next_m_name}})</a></th>
        </tr>
        {{weeks}}
    </table>
'''.format(months_link=months_link)

# day_id
day_cell_another_month = '<th width=50 bgcolor="#aaa">{day_id}</th>'

# task_count: int
# year_id (hours_link)
# month_id (hours_link)
# day_id (hours_link)
# task_count
day_cell = '''
<th width=50 bgcolor="#eee"> <a href="{hours_link}">{{day_id}} ({{task_count}})</a>
</th>'''.format(hours_link=hours_link)
day_cell_free = '''
<th width=50 bgcolor="#ffffff"> <a href="{hours_link}">{{day_id}}</a></th>
'''.format(hours_link=hours_link)

# ================ WEEK ========================

week_table = ' <tr> {d_1} {d_2} {d_3} {d_4} {d_5} {d_6} {d_7} </tr>'

# ================ MONTH ========================
# ToDo(den) move title with previous and next (month, year, day) to out
# year_id (months_link)
month_table = '''
    <table style="width:50%">
        <tr>
            <th><a href="{year_2018_link}"> 2018 </a></th>
            <th><a href="{year_2019_link}"> 2019 </a></th>
            <th><a href="{year_2020_link}"> 2020 </a></th>
        </tr>
        <tr>
            <th bgcolor="{{January}}"><a href="{months_link}/1/days">January{{January_task_count}}</a></th>
            <th bgcolor="{{February}}"><a href="{months_link}/2/days">February{{February_task_count}}</a></th>
            <th bgcolor="{{March}}"><a href="{months_link}/3/days">March{{March_task_count}}</a></th>
        </tr>
        <tr>
            <th bgcolor="{{April}}"><a href="{months_link}/4/days">April{{April_task_count}}</a></th>
            <th bgcolor="{{May}}"><a href="{months_link}/5/days">May{{May_task_count}}</a></th>
            <th bgcolor="{{June}}"><a href="{months_link}/6/days">June{{June_task_count}}</a></th>
        </tr>
        <tr>
            <th bgcolor="{{July}}"><a href="{months_link}/7/days">July{{July_task_count}}</a></th>
            <th bgcolor="{{August}}"><a href="{months_link}/8/days">August{{August_task_count}}</a></th>
            <th bgcolor="{{September}}"><a href="{months_link}/9/days">September{{September_task_count}}</a></th>
        </tr>
        <tr>
            <th bgcolor="{{October}}"><a href="{months_link}/10/days">October{{October_task_count}}</a></th>
            <th bgcolor="{{November}}"><a href="{months_link}/11/days">November{{November_task_count}}</a></th>
            <th bgcolor="{{December}}"><a href="{months_link}/12/days">December{{December_task_count}}</a></th>
        </tr>
    </table>'''.format(months_link=months_link,
                       year_2018_link=year_2018_link,
                       year_2019_link=year_2019_link,
                       year_2020_link=year_2020_link)

# ToDO(den) drop it
month_busy = {
    'January': "#ffffff",
    'February': "#ffffff",
    'March': "#ffffff",
    'April': "#ffffff",
    'May': "#ffffff",
    'June': "#ffffff",
    'July': "#ffffff",
    'August': "#ffffff",
    'September': "#ffffff",
    'October': "#ffffff",
    'November': "#ffffff",
    'December': "#ffffff",
    'January_task_count': "",
    'February_task_count': "",
    'March_task_count': "",
    'April_task_count': "",
    'May_task_count': "",
    'June_task_count': "",
    'July_task_count': "",
    'August_task_count': "",
    'September_task_count': "",
    'October_task_count': "",
    'November_task_count': "",
    'December_task_count': "",
}

# ================= YEAR ========================

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

