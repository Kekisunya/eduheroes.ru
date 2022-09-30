from django.contrib.auth.decorators import login_required
from django.urls import path

from user_login.decorators import has_no_employee
from .views import *

urlpatterns = [
    path('search/', EmployeesList.as_view(), name='employees_search'),
    path('<int:pk>/', EmployeeCard.as_view(), name='employee_detailed'),
    path('add/', login_required(has_no_employee(EmployeeCreate.as_view(), edit_url='employee_edit'), login_url='login'), name='employee_add'),
    path('edit/', login_required(EmployeeEdit.as_view(), login_url='login'), name='employee_edit'),
    path('delete/', login_required(EmployeeDelete.as_view()), name='employee_delete'),
]