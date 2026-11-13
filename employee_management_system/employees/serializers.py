from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from .models import Department, JobRole, Skill, Employee, EmployeeProfile, Attendance, LeaveRequest


class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.IntegerField(source="employees.count", read_only=True)

    class Meta:
        model = Department
        fields = "__all__"


class JobRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRole
        fields = "__all__"

    def validate_minimum_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Minimum salary cannot be negative.")
        return value


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class EmployeeProfileSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.full_name", read_only=True)

    class Meta:
        model = EmployeeProfile
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)
    job_role_title = serializers.CharField(source="job_role.title", read_only=True)
    skills_detail = SkillSerializer(source="skills", many=True, read_only=True)
    profile = EmployeeProfileSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id", "employee_id", "first_name", "last_name", "full_name",
            "email", "phone", "hire_date", "salary", "department",
            "department_name", "job_role", "job_role_title", "skills",
            "skills_detail", "status", "profile", "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    full_name = serializers.CharField(read_only=True)

    def validate_salary(self, value):
        if value <= 0:
            raise serializers.ValidationError("Salary must be greater than zero.")
        return value

    def validate(self, attrs):
        role = attrs.get("job_role", getattr(self.instance, "job_role", None))
        salary = attrs.get("salary", getattr(self.instance, "salary", None))
        if role and salary is not None and salary < role.minimum_salary:
            raise serializers.ValidationError({
                "salary": f"Salary must be at least {role.minimum_salary} for the selected job role."
            })
        return attrs

    def create(self, validated_data):
        skills = validated_data.pop("skills", [])
        employee = Employee(**validated_data)
        try:
            employee.full_clean()
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict)
        employee.save()
        employee.skills.set(skills)
        return employee

    def update(self, instance, validated_data):
        skills = validated_data.pop("skills", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        try:
            instance.full_clean()
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict)
        instance.save()
        if skills is not None:
            instance.skills.set(skills)
        return instance


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.full_name", read_only=True)

    class Meta:
        model = Attendance
        fields = "__all__"

    def validate(self, attrs):
        check_in = attrs.get("check_in", getattr(self.instance, "check_in", None))
        check_out = attrs.get("check_out", getattr(self.instance, "check_out", None))
        if check_in and check_out and check_out <= check_in:
            raise serializers.ValidationError({"check_out": "Check-out must be later than check-in."})
        return attrs


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.full_name", read_only=True)
    duration_days = serializers.SerializerMethodField()
    status = serializers.ChoiceField(choices=LeaveRequest.LeaveStatus.choices, required=False)

    class Meta:
        model = LeaveRequest
        fields = "__all__"
        read_only_fields = ["applied_at"]

    def get_duration_days(self, obj):
        return (obj.end_date - obj.start_date).days + 1

    def validate(self, attrs):
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end = attrs.get("end_date", getattr(self.instance, "end_date", None))
        if start and end and end < start:
            raise serializers.ValidationError({"end_date": "End date cannot be earlier than start date."})
        return attrs
