from calendar_routes import *

# ================ HTML ========================
# year, month, day, hour
task_preset_form = '''
<html>
 <head>
    <meta charset="utf-8"><title>Create task</title>
    <script>
        function changeButtonState(checkbox) {{{{
            document.getElementById('hidden').style.display = checkbox.checked ? 'block': 'none';}}}}
    </script>
    <style type="text/css">#hidden {{{{display: block;}}}}</style>
 </head>
 <body>
  <form action="{task_creator_link}" method="post">
   <p><textarea name="task_name" rows="3" style="width:345px;"></textarea></p>
   <p><label for="calendar">Calendar Date</label><input type="checkbox" id="calendar" name="calendar" onChange="changeButtonState(this)" checked></p>
   <div id="hidden"> 
       Year: <input name="year" style="width:40px;" value="{{year}}"> 
       Month: <input name="month" style="width:40px;" value="{{month}}"> 
       Day: <input name="day" style="width:40px;" value="{{day}}"> 
       Hour: <input  name="hour" style="width:40px;" value="{{hour}}"></div>
   <p><input type="submit" value="Add"></p>
 </form></body></html>
'''.format(task_creator_link=task_creator_link)

body_html = '''
<!DOCTYPE HTML>
<html><head><style>
                   table, th, td {{border: 1px solid black; collapse;}}
                   a {{text-decoration: none; color: black; }}
                </style>
               </head><body>{}</body></html>'''

# ================ HOUR ========================
# year, month, day, hour
cell_add_task_link = '''
<a href="{task_preset_link}?y={{year}}&m={{month}}&d={{day}}&h={{hour}}"> 
<img src="/static/plus.png" alt="Create Task" style="width:20px;height:20px;"></a>
'''.format(task_preset_link=task_preset_link)

# bgcolor: ##00dd7a - busy
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
<tr bgcolor="##00dd7a">
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
            <th colspan="2"><a href="{days_link}/{{prev_day}}/hours">({{prev_day}})</a></th>
            <th><a href="{days_link}">^ {{day}} ^</a></th>
            <th colspan="2"><a href="{days_link}/{{next_day}}/hours">({{next_day}})</a></th>
        </tr>
        <tr>{{hours}}</tr>
    </table>
'''.format(days_link=days_link)

# ToDo(den) add links for done, edit, delete ...
# ToDo(den) add styles ...
t_table_inner = '''
    <table bgcolor="##00ee7a" 
     style="height: 100%; width: 100%; border: 1px solid white; 
     border-collapse: collapse; border-spacing: 0; padding: 0px;">
        {tasks}
    </table>
'''
t_cell_inner = '''
<tr><th><a href="{base_url}" title="Close/Reopen">{{task_name}}
</a></th>

    <th width=30><a href="{base_url}">
<img src="/static/done.png" alt="done" title="Close/Reopen" style="width:20px;height:20px;">
</a></th>
 
    <th width=30><a href="{base_url}">
<img src="/static/edit.png" alt="edit" title="Edit" style="width:20px;height:20px;">
</a></th> 

    <th width=30><a href="{base_url}">
<img src="/static/archive.png" alt="archive" title="To Archive" style="width:20px;height:20px;">
</a></th>

    <th width=30><a href="{base_url}">
<img src="/static/delete.png" alt="delete" title="Delete" style="width:20px;height:20px;">
</a></th></tr>
'''.format(base_url=years_route)

# ==================== DAY ===============
# bgcolor: ##00ee7a - busy, #aaa - Day zero (from another month)
# year (months_link)
# prev_m, prev_m_name - previous month
# next_m, next_m_name - next month
# weeks
# ToDo(den) move title with previous and next (month, year, day) to out
day_table = '''
    <table style="width:50%">
        <tr>
            <th colspan="2"><a href="{months_link}/{{prev_m}}/days">({{prev_m_name}})</a></th>
            <th colspan="3"><a href="{months_link}">^ {{month_name}} ^</a></th>
            <th colspan="2"><a href="{months_link}/{{next_m}}/days">({{next_m_name}})</a></th>
        </tr>
        {{weeks}}
    </table>
'''.format(months_link=months_link)

# day
day_cell_another_month = '<th width=50 bgcolor="#aaa">{day}</th>'

# task_count
# year, month, day (hours_link)
day_cell = '''
<th width=50 bgcolor="#00ee7a"> <a href="{hours_link}">{{day}} ({{task_count}})</a>
</th>'''.format(hours_link=hours_link)
day_cell_free = '''
<th width=50 > <a href="{hours_link}">{{day}}</a></th>
'''.format(hours_link=hours_link)

# ================ WEEK ========================

week_table = ' <tr> [d_1] [d_2] [d_3] [d_4] [d_5] [d_6] [d_7] </tr>'

# ================ MONTH ========================
# ToDo(den) move title with previous and next (month, year, day) to out
# bgcolor: ##00ee7a - busy
# year (months_link)
# month month_name
# task_count
month_cell_free = '''
<th><a href="{months_link}/{{month}}/days">{{month_name}}</a></th>
'''.format(months_link=months_link)
month_cell = '''
<th bgcolor="##00ee7a"><a href="{months_link}/{{month}}/days">{{month_name}} ({{task_count}})</a></th>
'''.format(months_link=months_link)

# year
# prev_year, next_year
month_table = '''
    <table style="width:50%">
        <tr>
            <th><a href="{years_route}/{{prev_year}}/months"> ({{prev_year}}) </a></th>
            <th><a href="{years_route}">^ {{year}} ^</a></th>
            <th><a href="{years_route}/{{next_year}}/months"> ({{next_year}}) </a></th>
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

