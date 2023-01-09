from accounts.models import Profile
from attendance.models import StudentAttendance, TeacherAttendance
from common.report import BaseDynamicTableData
from enrollments.models import (
    CourseSession,
    CourseThroughEnrollment,
    ExamEnrollmentStatus,
    ExamSession,
    ExamThroughEnrollment,
)


class ExamThroughEnrollmentTableData(BaseDynamicTableData):
    model = ExamThroughEnrollment
    field_to_header_names = {
        "enrollment": "Student's Name",
        "phone_number": "Phone Number",
        "exam": "Exam",
        "created_date": "Created Date",
        "payment": "Payment",
        # "selected_session": "Selected Session",
        # "rank": "Rank",
        # "score": "Score",
        # "negative_score": "Negative Score",
        "status": "Status",
    }

    def get_students_name(self, obj):
        return obj.enrollment.student.__str__()

    def get_phone_number(self, obj):
        return str(obj.enrollment.student.username)

    def get_exam(self, obj):
        return obj.exam.name

    def get_created_date(self, obj):
        return str(obj.enrollment.created_at.date())

    def get_payment(self, obj):
        return str(obj.exam.price)

    def get_status(self, obj):
        return obj.status

    # def get_rank(self, obj):
    #     return get_student_rank(obj)

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "enrollment": self.get_students_name,
            "phone_number": self.get_phone_number,
            "exam": self.get_exam,
            "created_date": self.get_created_date,
            # "rank": self.get_rank,
            # "score": self.get_score,
            "payment": self.get_payment,
            "status": self.get_status,
        }
        return fields_and_values[field_name](obj)


class CourseThroughEnrollmentTableData(BaseDynamicTableData):
    model = CourseThroughEnrollment
    field_to_header_names = {
        "enrollment": "Student's Name",
        "phone_number": "Phone Number",
        "course_name": "Course Name",
        "payment": "Payment",
        "course_enroll_status": "Status",
    }

    def get_students_name(self, obj):
        return obj.enrollment.student.__str__()

    def get_phone_number(self, obj):
        return str(obj.enrollment.student.username)

    def get_course_name(self, obj):
        return obj.course.name

    def get_payment(self, obj):
        return str(obj.course.price)

    # def get_session(self, obj):
    #     return str(obj.selected_session.start_date.date())

    def get_status(self, obj):
        return obj.course_enroll_status

    # def get_completed_date(self, obj):
    #     return str(obj.completed_date)

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "enrollment": self.get_students_name,
            "phone_number": self.get_phone_number,
            "course_name": self.get_course_name,
            "payment": self.get_payment,
            "course_enroll_status": self.get_status,
        }
        return fields_and_values[field_name](obj)


class StudentTableData(BaseDynamicTableData):
    """status field not found."""

    model = Profile
    field_to_header_names = {
        "fullname": "Student Name",
        "date_joined": "Created date",
        "phone_number": "Phone Number",
        "email": "Email",
    }

    def get_fullname(self, obj):
        return obj.user.__str__()

    def get_created_date(self, obj):
        return str(obj.user.date_joined.date())

    def get_phone(self, obj):
        return str(obj.user.username)

    def get_email(self, obj):
        return obj.user.email

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "fullname": self.get_fullname,
            "date_joined": self.get_created_date,
            "phone_number": self.get_phone,
            "email": self.get_email,
        }
        return fields_and_values[field_name](obj)


class ExamTableData(BaseDynamicTableData):
    model = ExamSession
    field_to_header_names = {
        "exam": "Exam",
        "exam_type": "Type",
        "exam_date": "Exam Date",
        "examinee": "Examinee",
        "passes": "Passes",
        "failed": "Failed",
    }

    def get_exam_name(self, obj):
        return obj.exam.name

    def get_exam_type(self, obj):
        return obj.exam.exam_type

    def get_exam_date(self, obj):
        return str(obj.exam.start_date.date())

    def get_examinee_count(self, obj):
        return str(obj.session_enrolls.all().count())

    def get_passed_count(self, obj):
        return str(
            obj.session_enrolls.filter(status=ExamEnrollmentStatus.PASSED).count()
        )

    def get_failed_count(self, obj):
        return str(
            obj.session_enrolls.filter(status=ExamEnrollmentStatus.FAILED).count()
        )

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "exam": self.get_exam_name,
            "exam_type": self.get_exam_type,
            "exam_date": self.get_exam_date,
            "examinee": self.get_examinee_count,
            "passes": self.get_passed_count,
            "failed": self.get_failed_count,
        }
        return fields_and_values[field_name](obj)


class CourseTableData(BaseDynamicTableData):

    model = CourseSession
    field_to_header_names = {
        "course_name": "Course Name",
        "price": "Price",
        "students_enrolled": "Student Enrolled",
        "start_date": "Start Date",
        "status": "Status",
    }

    def get_course_name(self, obj):
        return obj.course.name

    def get_price(self, obj):
        return obj.course.price

    def get_students_enrolled_count(self, obj):
        return str(obj.course_enrolls.all().count())

    def get_start_date(self, obj):
        return str(obj.course.start_date.date())

    def get_status(self, obj):
        return obj.course.status

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "course_name": self.get_course_name,
            "price": self.get_price,
            "students_enrolled": self.get_students_enrolled_count,
            "start_date": self.get_start_date,
            "status": self.get_status,
        }
        return fields_and_values[field_name](obj)


class StudentAttendanceTableData(BaseDynamicTableData):
    model = StudentAttendance
    field_to_header_names = {
        "student_name": "Student Name",
        "phone_number": "Phone number",
        "date": "Date",
        # "attendance_time": "Attendance time",
    }

    def get_student_name(self, obj):
        return obj.user.__str__()

    def get_phone_number(self, obj):
        return obj.user.username

    def get_date(self, obj):
        return str(obj.date.date())

    # def get_time(self, obj):
    #     return str(obj.date.time())

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "student_name": self.get_student_name,
            "phone_number": self.get_phone_number,
            "date": self.get_date,
            # "attendance_time": self.get_time,
        }
        return fields_and_values[field_name](obj)


class TeacherAttendanceTableData(BaseDynamicTableData):
    model = TeacherAttendance
    field_to_header_names = {
        "teachers_name": "Teacher Name",
        "phone_number": "Phone number",
        "date": "Date",
    }

    def get_teachers_name(self, obj):
        return obj.user.__str__()

    def get_phone_number(self, obj):
        return obj.user.username

    def get_date(self, obj):
        return str(obj.date.date())

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "teachers_name": self.get_teachers_name,
            "phone_number": self.get_phone_number,
            "date": self.get_date,
        }
        return fields_and_values[field_name](obj)
