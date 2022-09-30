from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Job


class AuthorPermissionMixin(PermissionRequiredMixin):
    raise_exception = True

    def has_permission(self):
        if self.request.user == Job.objects.get(pk=self.kwargs['pk']).user:
            return True
        return False
