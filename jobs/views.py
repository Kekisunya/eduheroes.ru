from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .utilities import AuthorPermissionMixin
from .models import *
from .forms import JobCreateForm


class JobsList(ListView):
    model = Job
    context_object_name = 'jobs'
    paginate_by = 30


    def get_queryset(self):
        request = self.request.GET
        created_after = request.get('created_after')
        created_by = request.getlist('created_by')
        job_types = request.getlist('job_types')
        roles = request.getlist('roles')
        remote = request.getlist('remote')
        students = request.getlist('students')
        location_id = request.get('location_id')
        longitude = request.get('longitude')
        latitude = request.get('latitude')
        radius = request.get('radius')
        query = Job.objects.all()
        if created_after:
            query = query.filter(updated_at__gte=created_after)
        if created_by:
            query = query.filter(user__pk__in=created_by)
        if len(job_types):
            query = query.filter(job_types__pk__in=job_types)
        if len(roles):
            query = query.filter(role_id__in=roles)
        if len(remote):
            query = query.filter(remote_id__in=remote)
        if len(students):
            query = query.filter(students_id__in=students)
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


class JobCard(DetailView):
    model = Job
    context_object_name = 'job'

    def get(self, request, *args, **kwargs):
        ip = get_user_ip(request)
        job = self.get_object()
        if JobViews.objects.filter(ip=ip).exists():
            job.views.add(JobViews.objects.get(ip=ip))
        else:
            JobViews.objects.create(ip=ip)
            job.views.add(JobViews.objects.get(ip=ip))
        return super().get(request, *args, **kwargs)


class JobCreate(CreateView):
    form_class = JobCreateForm
    template_name = 'jobs/job_add.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data() | {
            'view': 'add',
            'title': 'Добавление вакансии'
        }
        return context


class JobEdit(AuthorPermissionMixin, UpdateView):
    model = Job
    form_class = JobCreateForm
    template_name = 'jobs/job_add.html'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data() | {
            'view': 'edit',
            'title': 'Редакция вакансии'
        }
        return context


class JobByUser(JobsList):
    template_name = 'jobs/jobs_my.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data() | {
            'title': 'Мои вакансии',
            'sidebar': False
        }
        return context


class JobDelete(AuthorPermissionMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('jobs_by_user')


def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
