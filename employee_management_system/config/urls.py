from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from employees.views import (
    DepartmentViewSet, JobRoleViewSet, SkillViewSet, EmployeeViewSet,
    EmployeeProfileViewSet, AttendanceViewSet, LeaveRequestViewSet,
)

router = DefaultRouter()
router.register("departments", DepartmentViewSet)
router.register("job-roles", JobRoleViewSet)
router.register("skills", SkillViewSet)
router.register("employees", EmployeeViewSet)
router.register("employee-profiles", EmployeeProfileViewSet)
router.register("attendance", AttendanceViewSet)
router.register("leave-requests", LeaveRequestViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
