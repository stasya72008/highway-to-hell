years_route = '/calendar/years'

months_route = years_route + '/<int:year_id>/months'
days_route = months_route + '/<int:month_id>/days'
hours_route = days_route + '/<int:day_id>/hours'

months_link = years_route + '/{year}/months'
days_link = months_link + '/{month}/days'
hours_link = days_link + '/{day}/hours'

next_months_link = years_route + '/{next_year}/months'
next_days_link = next_months_link + '/{next_month}/days'
next_hours_link = next_days_link + '/{next_day}/hours'

prev_months_link = years_route + '/{prev_year}/months'
prev_days_link = prev_months_link + '/{prev_month}/days'
prev_hours_link = prev_days_link + '/{prev_day}/hours'

# deprecated
year_2018_link = years_route + '/2018/months'
year_2019_link = years_route + '/2019/months'
year_2020_link = years_route + '/2020/months'

task_preset_link = '/task_preset'
task_creator_link = '/task_creator'