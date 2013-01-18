from django.contrib import admin
from assignments.models import Assignment, Submission


class SubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'assignment', 'time_submitted', 'late')


class AssignmentAdmin(admin.ModelAdmin):
    readonly_fields = ('total_submissions',)


admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Submission, SubmissionAdmin)
