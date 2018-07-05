years_route = '/calendar/years'

months_route = years_route + '/<int:year_id>/months'
days_route = months_route + '/<int:month_id>/days'
hours_route = days_route + '/<int:day_id>/hours'

months_link = years_route + '/{year_id}/months'
days_link = months_link + '/{month_id}/days'
hours_link = days_link + '/{day_id}/hours'

year_2018_link = years_route + '/2018/months'
year_2019_link = years_route + '/2019/months'
year_2020_link = years_route + '/2020/months'
