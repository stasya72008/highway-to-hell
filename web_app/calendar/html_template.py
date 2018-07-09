from calendar_routes import *


# ================ HTML ========================

body_html = '''<html><head>
                <style>
                   table, th, td {{border: 1px solid black; collapse;}}
                   a {{text-decoration: none; color: black; background-color: while; }}
                </style>
               </head><body>{}</body></html>'''

# ================ HOUR ========================
# ToDO(den) change (add) to button "Create task"
# bgcolor: #eee - busy
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
# bgcolor: #eee - busy, #aaa - Day zero (from another month)
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
<th width=50 > <a href="{hours_link}">{{day_id}}</a></th>
'''.format(hours_link=hours_link)

# ================ WEEK ========================

week_table = ' <tr> [d_1] [d_2] [d_3] [d_4] [d_5] [d_6] [d_7] </tr>'

# ================ MONTH ========================
# ToDo(den) move title with previous and next (month, year, day) to out
# bgcolor: #eee - busy
# year_id (months_link)
# month_id month_name
# task_count
month_cell_free = '''
<th><a href="{months_link}/{{month_id}}/days">{{month_name}}</a></th>
'''.format(months_link=months_link)
month_cell = '''
<th bgcolor="#eee"><a href="{months_link}/{{month_id}}/days">{{month_name}} ({{task_count}})</a></th>
'''.format(months_link=months_link)

# year_id (months_link)
# prev_year_id next_year_id
month_table = '''
    <table style="width:50%">
        <tr>
            <th><a href="{years_route}/{{prev_year_id}}/months"> ({{prev_year_id}}) </a></th>
            <th><a href="{years_route}">^ {{year_id}} ^</a></th>
            <th><a href="{years_route}/{{next_year_id}}/months"> ({{next_year_id}}) </a></th>
        </tr>
        <tr> [m_1]  [m_2]  [m_3] </tr>
        <tr> [m_4]  [m_5]  [m_6] </tr>
        <tr> [m_7]  [m_8]  [m_9] </tr>
        <tr> [m_10] [m_11] [m_12] </tr>
    </table>'''.format(years_route=years_route,
                       months_link=months_link,
                       year_2018_link=year_2018_link,
                       year_2019_link=year_2019_link,
                       year_2020_link=year_2020_link)

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

