**Web application**

*Start* 
python -m flask run --host=0.0.0.0 -p=50xx


**Calendar**
url - /calendar/users[/user_id/years[/year_id/months[/month_id/days[/day_id/hours]]]]


Planner

Note



**Database object**

User
```
{
"id" : int,
"username": string
}
```


Task
```
{
"id": int,
"user_id": int,
"name": string,
"date": ?
"status": string
}
```
Task Status:
- active
- done
- archive
- deleted

**REST**

```
/users
  [GET] – get all users in JSON format
  [POST] – add new user

/users/<user_id>
  [DELETE] – delete user with given id
  [GET] – get user with given id

/users/<user_id>/tasks
  [GET] – get all tasks for the user

/tasks
  [POST] – create new task

/tasks/<task_id>
  [GET] – get task with given id
```
