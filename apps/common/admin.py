from django.contrib import admin
from apps.common.models import Sponsor, University, Student, StudentSponsor


admin.site.register(Sponsor)
admin.site.register(University)
admin.site.register(Student)
admin.site.register(StudentSponsor)
