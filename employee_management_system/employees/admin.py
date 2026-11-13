from django.contrib import admin
from .models import Department, JobRole, Skill, Employee, EmployeeProfile, Attendance, LeaveRequest


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("created_at",)


@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "minimum_salary")
    search_fields = ("title",)
    ordering = ("title",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


class EmployeeProfileInline(admin.StackedInline):
    model = EmployeeProfile
    extra = 0
    max_num = 1


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "first_name", "last_name", "email", "department", "job_role", "salary", "status")
    search_fields = ("employee_id", "first_name", "last_name", "email")
    list_filter = ("department", "job_role", "status")
    ordering = ("employee_id",)
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("skills",)
    inlines = [EmployeeProfileInline]


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ("employee", "date_of_birth", "emergency_contact")
    search_fields = ("employee__employee_id", "employee__first_name", "employee__last_name")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("employee", "date", "status", "check_in", "check_out")
    search_fields = ("employee__employee_id", "employee__first_name", "employee__last_name")
    list_filter = ("status", "date")
    ordering = ("-date",)


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ("employee", "leave_type", "start_date", "end_date", "status", "applied_at")
    search_fields = ("employee__employee_id", "employee__first_name", "reason")
    list_filter = ("leave_type", "status")
    ordering = ("-applied_at",)
    readonly_fields = ("applied_at",)
