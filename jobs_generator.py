from jobs.models import *
from employees.models import *

User = get_user_model()

for i in range(100):
    j = Job()
    j.title = 'Вакансия ' + str(i)
    j.description = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis commodo mauris ipsum, ut ultricies lacus tincidunt sed. Sed commodo lacus nec ligula pharetra ullamcorper. Ut nec lorem et mauris commodo varius et ac tellus. Donec ac lacus massa. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas at erat sed nisi aliquam blandit non sed turpis. Vivamus sit amet justo justo. Fusce dignissim, tellus eget lacinia blandit, enim arcu auctor ante, a interdum ipsum enim a elit.'''
    j.contacts = '''Телефон +79519516543
    email test@bk.ru'''
    j.role_id = 3
    j.save()
    j.user_id=2
    j.job_types.add(4)
    j.job_types.add(5)
    j.save()

