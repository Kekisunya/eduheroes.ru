from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Employee, EmployeeViews
from .forms import EmployeeCreateForm


class EmployeesList(ListView):
    model = Employee
    context_object_name = 'employees'
    paginate_by = 30

    def get_queryset(self):
        request = self.request.GET
        min_rating = request.get('min_rating')
        max_rating = request.get('max_rating')
        job_types = request.getlist('job_types')
        roles = request.getlist('roles')
        students = request.getlist('students')
        remote = request.getlist('remote')
        location_id = request.get('location_id')
        longitude = request.get('longitude')
        latitude = request.get('latitude')
        radius = request.get('radius')
        query = Employee.objects.all()
        if min_rating:
            query = query.filter(rating__gte=min_rating)
        if max_rating:
            query = query.filter(rating__lte=max_rating)
        if len(job_types):
            query = query.filter(job_types__pk__in=job_types)
        if len(roles):
            query = query.filter(roles__pk__in=roles)
        if len(students):
            query = query.filter(students__pk__in=students)
        if len(remote):
            query = query.filter(remote__pk__in=remote)
        if location_id:
            longitude = float(longitude)
            latitude = float(latitude)
            radius = int(radius) if radius else 0
            jobs_ids = []
            for job in query:
                distance = job.get_distance(latitude=latitude, longitude=longitude)
                if distance is not None and distance <= radius:
                    jobs_ids.append(job.id)
            query = query.filter(pk__in=jobs_ids)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) | {
            'title': 'Поиск соискателей'
        }
        return context


class EmployeeCard(DetailView):
    model = Employee
    context_object_name = 'employee'

    def get(self, request, *args, **kwargs):
        ip = get_user_ip(request)
        employee = self.get_object()
        if EmployeeViews.objects.filter(ip=ip).exists():
            employee.views.add(EmployeeViews.objects.get(ip=ip))
        else:
            EmployeeViews.objects.create(ip=ip)
            employee.views.add(EmployeeViews.objects.get(ip=ip))
        return super().get(request, *args, **kwargs)


class EmployeeCreate(CreateView):
    form_class = EmployeeCreateForm
    template_name = 'employees/employee_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) | {
            'view': 'add'
        }
        return context


class EmployeeEdit(UpdateView):
    form_class = EmployeeCreateForm
    template_name = 'employees/employee_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) | {
            'view': 'edit',
            'title': 'Редакция анкеты'
        }
        return context

    def get_object(self, queryset=None):
        return Employee.objects.get(user=self.request.user)


class EmployeeDelete(DeleteView):
    model = Employee
    success_url = reverse_lazy('main')

    def get_object(self, queryset=None):
        return Employee.objects.get(user=self.request.user)


def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip