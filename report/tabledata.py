from accounts.models import Profile
from attendance.models import StudentAttendance, TeacherAttendance
from common.report import BaseDynamicTableData
from enrollments.api.utils import get_student_rank
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
        "exam": "Exam",
        "selected_session": "Selected Session",
        "rank": "Rank",
        "score": "Score",
        "negative_score": "Negative Score",
        "status": "Status",
    }

    def get_students_name(self, linea):
        return (
            str(linea.enrollment.student.first_name)
            + " "
            + str(linea.enrollment.student.last_name)
        )

    def get_exam_name(self, linea):
        return linea.exam.name

    def get_session(self, linea):
        return str(linea.selected_session.start_date.date())

    def get_score(self, linea):
        return str(linea.score)

    def get_negative_score(self, linea):
        return str(linea.negative_score)

    def get_status(self, linea):
        return linea.status

    def get_rank(self, linea):
        return get_student_rank(linea)

    def get_values_from_fields(self, field_name, linea):
        fields_and_values = {
            "enrollment": self.get_students_name,
            "exam": self.get_exam_name,
            "selected_session": self.get_session,
            "rank": self.get_rank,
            "score": self.get_score,
            "negative_score": self.get_negative_score,
            "status": self.get_status,
        }
        return fields_and_values[field_name](linea)


class CourseThroughEnrollmentTableData(BaseDynamicTableData):
    model = CourseThroughEnrollment
    field_to_header_names = {
        "enrollment": "Student's Name",
        "phone_number": "Phone Number",
        "course_name": "Course Name",
        "payment": "Payment",
        "course_enroll_status": "Status",
    }

    def get_students_name(self, linea):
        return (
            str(linea.enrollment.student.first_name)
            + " "
            + str(linea.enrollment.student.last_name)
        )

    def get_phone_number(self, linea):
        return str(linea.enrollment.student.username)

    def get_course_name(self, linea):
        return linea.course.name

    def get_payment(self, linea):
        return str(linea.course.price)

    # def get_session(self, linea):
    #     return str(linea.selected_session.start_date.date())

    def get_status(self, linea):
        return linea.course_enroll_status

    # def get_completed_date(self, linea):
    #     return str(linea.completed_date)

    def get_values_from_fields(self, field_name, linea):
        fields_and_values = {
            "enrollment": self.get_students_name,
            "phone_number": self.get_phone_number,
            "course_name": self.get_course_name,
            "payment": self.get_payment,
            "course_enroll_status": self.get_status,
        }
        return fields_and_values[field_name](linea)


class StudentTableData(BaseDynamicTableData):
    """status field not found."""

    model = Profile
    field_to_header_names = {
        "fullname": "Student Name",
        "date_joined": "Created date",
        "phone_number": "Phone Number",
        "email": "Email",
        # "college_name": "College Name",
    }

    def get_fullname(self, linea):
        return str(linea.user.first_name) + " " + str(linea.user.last_name)

    def get_created_date(self, linea):
        return linea.date_joined

    def get_phone(self, linea):
        return str(linea.user.username)

    def get_email(self, linea):
        return linea.user.email

    def get_values_from_fields(self, field_name, linea):
        fields_and_values = {
            "fullname": self.get_fullname,
            "date_joined": self.get_created_date,
            "phone_number": self.get_phone,
            "email": self.get_email,
            # "college_name": self.get_college_name,
        }
        return fields_and_values[field_name](linea)


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

    def get_exam_name(self, linea):
        return linea.exam.name

    def get_exam_type(self, linea):
        return linea.exam.exam_type

    def get_exam_date(self, linea):
        return str(linea.exam.start_date.date())

    def get_examinee_count(self, linea):
        return str(linea.session_enrolls.all().count())

    def get_passed_count(self, linea):
        return str(
            linea.session_enrolls.filter(status=ExamEnrollmentStatus.PASSED).count()
        )

    def get_failed_count(self, linea):
        return str(
            linea.session_enrolls.filter(status=ExamEnrollmentStatus.FAILED).count()
        )

    def get_values_from_fields(self, field_name, linea):
        fields_and_values = {
            "exam": self.get_exam_name,
            "exam_type": self.get_exam_type,
            "exam_date": self.get_exam_date,
            "examinee": self.get_examinee_count,
            "passes": self.get_passed_count,
            "failed": self.get_failed_count,
        }
        return fields_and_values[field_name](linea)


class CourseTableData(BaseDynamicTableData):

    model = CourseSession
    field_to_header_names = {
        "course_name": "Course Name",
        "price": "Price",
        "students_enrolled": "Student Enrolled",
        "start_date": "Start Date",
        "status": "Status",
    }

    def get_course_name(self, linea):
        return linea.course.name

    def get_price(self, linea):
        return linea.course.price

    def get_students_enrolled_count(self, linea):
        return str(linea.course_enrolls.all().count())

    def get_start_date(self, linea):
        return str(linea.course.start_date.date())

    def get_status(self, linea):
        return linea.course.status

    def get_values_from_fields(self, field_name, linea):
        fields_and_values = {
            "course_name": self.get_course_name,
            "price": self.get_price,
            "students_enrolled": self.get_students_enrolled_count,
            "start_date": self.get_start_date,
            "status": self.get_status,
        }
        return fields_and_values[field_name](linea)


class StudentAttendanceTableData(BaseDynamicTableData):
    model = StudentAttendance
    field_to_header_names = {
        "student_name": "Student Name",
        "phone_number": "Phone number",
        "date": "Date",
        "attendance_time": "Attendance time",
    }

    def get_student_name(self, linea):
        return str(linea.user.first_name) + " " + str(linea.user.last_name)

    def get_phone_number(self, linea):
        return linea.user.username

    def get_date(self, linea):
        return str(linea.date.date())

    def get_time(self, linea):
        return str(linea.date.time())

    def get_values_from_fields(self, field_name, linea):
        fields_and_values = {
            "student_name": self.get_student_name,
            "phone_number": self.get_phone_number,
            "date": self.get_date,
            "attendance_time": self.get_time,
        }
        return fields_and_values[field_name](linea)


class TeacherAttendanceTableData(BaseDynamicTableData):
    model = TeacherAttendance
    field_to_header_names = {
        "teachers_name": "Teacher Name",
        "phone_number": "Phone number",
        "date": "Date",
        "attendance_time": "Attendance time",
    }

    def get_student_name(self, linea):
        return str(linea.user.first_name) + " " + str(linea.user.last_name)

    def get_phone_number(self, linea):
        return linea.user.username

    def get_date(self, linea):
        return str(linea.date.date())

    def get_time(self, linea):
        return str(linea.date.time())

    def get_values_from_fields(self, field_name, linea):
        fields_and_values = {
            "student_name": self.get_student_name,
            "phone_number": self.get_phone_number,
            "date": self.get_date,
            "attendance_time": self.get_time,
        }
        return fields_and_values[field_name](linea)
