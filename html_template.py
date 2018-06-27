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

day_cell_zero = '<th bgcolor="#aaa"> </th>'
day_cell_empty = '<th bgcolor="#ffffff">{day_id}</th>'
day_cell = '<th bgcolor="#eee">{day_id} ({task_count})</th>'

hour_cell_empty = '<th bgcolor="#ffffff">{hour_id}</th>' \
                  '<th bgcolor="#ffffff"> </th>'
hour_cell = '<th bgcolor="#ffffff">{hour_id}</th>' \
            '<th bgcolor="#ffffff">{task_name}</th>'


body_html = '''<html><head>
                <style>
                   table, th, td {{border: 1px solid black;border-collapse: collapse;}}
                   a {{text-decoration: none; color: black; background-color: while; }}
                </style>
               </head><body>{}</body></html>'''

year_table = '''
    <table style="width:50%">
        <tr>
            <th><a href="/years/2018/months"> 2018 </a></th>
        </tr>
</table>
'''

month_table = '''
    <table style="width:50%">
        <tr>
            <th><a href="/years"> <--- </a></th>
            <th><a href="/years"> {year_id} </a></th>
            <th><a href="/years"> ---> </a></th>
        </tr>
        <tr>
            <th bgcolor="{January}"><a href="/years/{year_id}/months/1/days">January{January_task_count}</a></th>
            <th bgcolor="{February}"><a href="/years/{year_id}/months/2/days">February{February_task_count}</a></th>
            <th bgcolor="{March}"><a href="/years/{year_id}/months/3/days">March{March_task_count}</a></th>
        </tr>
        <tr>
            <th bgcolor="{April}"><a href="/years/{year_id}/months/4/days">April{April_task_count}</a></th>
            <th bgcolor="{May}"><a href="/years/{year_id}/months/5/days">May{May_task_count}</a></th>
            <th bgcolor="{June}"><a href="/years/{year_id}/months/6/days">June{June_task_count}</a></th>
        </tr>
        <tr>
            <th bgcolor="{July}"><a href="/years/{year_id}/months/7/days">July{July_task_count}</a></th>
            <th bgcolor="{August}"><a href="/years/{year_id}/months/8/days">August{August_task_count}</a></th>
            <th bgcolor="{September}"><a href="/years/{year_id}/months/9/days">September{September_task_count}</a></th>
        </tr>
        <tr>
            <th bgcolor="{October}"><a href="/years/{year_id}/months/10/days">October{October_task_count}</a></th>
            <th bgcolor="{November}"><a href="/years/{year_id}/months/11/days">November{November_task_count}</a></th>
            <th bgcolor="{December}"><a href="/years/{year_id}/months/12/days">December{December_task_count}</a></th>
        </tr>
    </table>'''

day_table = '''
    <table style="width:50%">
        <tr>
            <th colspan="2"><a href="/years/{year_id}/months/{pr_month_id}/days">{pr_month_name} <- </a></th>
            <th colspan="3"><a href="/years/{year_id}/months">{month}</a></th>
            <th colspan="2"><a href="/years/{year_id}/months/{nx_month_id}/days"> -> {nx_month_name}</a></th>
        </tr>
        <tr><th colspan="7">...</th></tr>
        <tr><th colspan="7">...</th></tr>
        <tr><th colspan="7">...</th></tr>
        <tr><th colspan="7">...</th></tr>
    </table>
'''

hour_table = '''
    <table style="width:50%">
        <tr>
            <th><a href="/years/{year_id}/months/{month_id}/days">{d_id}</a></th>
        </tr>
        <tr>{hours}</tr>
    </table>
'''