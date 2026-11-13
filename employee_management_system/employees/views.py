from rest_framework import viewsets
from .models import Department, JobRole, Skill, Employee, EmployeeProfile, Attendance, LeaveRequest
from .serializers import (
    DepartmentSerializer, JobRoleSerializer, SkillSerializer, EmployeeSerializer,
    EmployeeProfileSerializer, AttendanceSerializer, LeaveRequestSerializer,
)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    filterset_fields = ["name"]


class JobRoleViewSet(viewsets.ModelViewSet):
    queryset = JobRole.objects.all()
    serializer_class = JobRoleSerializer
    search_fields = ["title", "description"]
    ordering_fields = ["title", "minimum_salary"]
    filterset_fields = ["title"]


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    search_fields = ["name", "description"]
    ordering_fields = ["name"]
    filterset_fields = ["name"]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related("department", "job_role", "profile").prefetch_related("skills")
    serializer_class = EmployeeSerializer
    search_fields = ["employee_id", "first_name", "last_name", "email", "department__name", "job_role__title"]
    ordering_fields = ["employee_id", "first_name", "hire_date", "salary", "created_at"]
    filterset_fields = ["department", "job_role", "status", "hire_date"]


class EmployeeProfileViewSet(viewsets.ModelViewSet):
    queryset = EmployeeProfile.objects.select_related("employee")
    serializer_class = EmployeeProfileSerializer
    search_fields = ["employee__employee_id", "employee__first_name", "employee__last_name", "address"]
    ordering_fields = ["employee__first_name", "date_of_birth"]
    filterset_fields = ["employee"]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related("employee")
    serializer_class = AttendanceSerializer
    search_fields = ["employee__employee_id", "employee__first_name", "employee__last_name", "notes"]
    ordering_fields = ["date", "check_in", "check_out"]
    filterset_fields = ["employee", "date", "status"]


class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.select_related("employee")
    serializer_class = LeaveRequestSerializer
    search_fields = ["employee__employee_id", "employee__first_name", "employee__last_name", "reason"]
    ordering_fields = ["start_date", "end_date", "applied_at"]
    filterset_fields = ["employee", "leave_type", "status", "start_date", "end_date"]
