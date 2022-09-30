from django import template

from employees.forms import EmployeeSearchForm

register = template.Library()


@register.inclusion_tag('employees/search_sidebar.html', takes_context=True)
def employees_search_sidebar(context):
    form = EmployeeSearchForm()
    context['form'] = form
    return {'form': form}
