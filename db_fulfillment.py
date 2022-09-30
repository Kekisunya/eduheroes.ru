from news.models import NewsCategory
from jobs.models import *
from employees.models import *

newscats = ['Новости', 'Бизнес', 'Продажи', 'Методика', 'Взрослые', 'Дети']
jobtypes = ['Полная занятость', 'Частичная занятость', 'Проект']
jobremotes = ['В офисе', 'На удаленке', 'Гибрид']
students = ['Дети', 'Взрослые', 'ДПО', 'Корпоративное обучение']
roles = ['Методист', 'Продюсер', 'Куратор', 'Проджект', 'Продакт']

for cat in newscats:
    c = NewsCategory()
    c.title = cat
    c.save()

for typ in jobtypes:
    t = JobType()
    t.title = typ
    t.save()

for remote in jobremotes:
    r = JobRemote()
    r.title = remote
    r.save()

for student in students:
    s = JobStudents()
    s.title = student
    s.save()

for role in roles:
    r = EmployeeRole()
    r.title = role
    r.save()