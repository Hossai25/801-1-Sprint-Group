from django.contrib import admin
from .models import User, PublicInfo, PrivateInfo, Course, Lab, CourseTa


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'account_type')


class PublicInfoAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'office_hours', 'user_id')


class PrivateInfoAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone_number', 'user_id')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'instructor_id')


class LabAdmin(admin.ModelAdmin):
    list_display = ('lab_name', 'course_id', 'ta_id')


class CourseTaAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'ta_id', 'is_grader', 'number_of_labs')


admin.site.register(User, UserAdmin)
admin.site.register(PublicInfo, PublicInfoAdmin)
admin.site.register(PrivateInfo, PrivateInfoAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lab, LabAdmin)
admin.site.register(CourseTa, CourseTaAdmin)
