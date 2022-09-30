from django import template

from jobs.forms import JobsSearchForm

register = template.Library()


@register.inclusion_tag('jobs/search_sidebar.html', takes_context=True)
def jobs_search_sidebar(context):
    form = JobsSearchForm()
    context['form'] = form
    return {'form': form}
