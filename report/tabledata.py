from accounts.models import User
from attendance.models import StudentAttendance, TeacherAttendance
from common.report import BaseDynamicTableData
from common.utils import get_human_readable_date_time
from courses.models import Course
from enrollments.api.utils import get_student_rank
from enrollments.models import (
    CourseThroughEnrollment,
    ExamEnrollmentStatus,
    ExamThroughEnrollment,
)
from exams.models import Exam
from payments.models import Payment


class ExamThroughEnrollmentTableData(BaseDynamicTableData):
    model = ExamThroughEnrollment
    field_to_header_names = {
        "enrollment": "Student's Name",
        "college_name": "College Name",
        "phone_number": "Phone Number",
        "exam": "Exam",
        "created_date": "Created Date",
        "payment": "Payment",
        "status": "Status",
    }

    def get_students_name(self, obj):
        return obj.enrollment.student.__str__()

    def get_college_name(self, obj):
        return obj.enrollment.student.profile.college_name

    def get_phone_number(self, obj):
        return str(obj.enrollment.student.username)

    def get_exam(self, obj):
        return obj.exam.name

    def get_created_date(self, obj):
        return str(obj.enrollment.created_at.strftime("%a %b %d %Y"))

    def get_payment(self, obj):
        price = obj.enrollment.payments_payment_related.first()
        return str(price.amount if price else "-")

    def get_status(self, obj):
        return obj.enrollment.status

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "enrollment": self.get_students_name,
            "college_name": self.get_college_name,
            "phone_number": self.get_phone_number,
            "exam": self.get_exam,
            "created_date": self.get_created_date,
            "payment": self.get_payment,
            "status": self.get_status,
        }
        return fields_and_values[field_name](obj)


class CourseThroughEnrollmentTableData(BaseDynamicTableData):
    model = CourseThroughEnrollment
    field_to_header_names = {
        "enrollment": "Student's Name",
        "college_name": "College Name",
        "phone_number": "Phone Number",
        "course_name": "Course Name",
        "created_date": "Created Date",
        "payment": "Payment",
        "course_enroll_status": "Status",
    }

    def get_students_name(self, obj):
        return obj.enrollment.student.__str__()

    def get_phone_number(self, obj):
        return str(obj.enrollment.student.username)

    def get_created_date(self, obj):
        return str(obj.enrollment.created_at.strftime("%a %b %d %Y"))

    def get_course_name(self, obj):
        return obj.course.name

    def get_payment(self, obj):
        price = obj.enrollment.payments_payment_related.first()
        return str(price.amount if price else "-")

    def get_college_name(self, obj):
        return obj.enrollment.student.profile.college_name

    # def get_session(self, obj):
    #     return str(obj.selected_session.start_date.date())

    def get_status(self, obj):
        return obj.course_enroll_status

    # def get_completed_date(self, obj):
    #     return str(obj.completed_date)

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "enrollment": self.get_students_name,
            "college_name": self.get_college_name,
            "phone_number": self.get_phone_number,
            "course_name": self.get_course_name,
            "created_date": self.get_created_date,
            "payment": self.get_payment,
            "course_enroll_status": self.get_status,
        }
        return fields_and_values[field_name](obj)


class StudentTableData(BaseDynamicTableData):
    model = User
    field_to_header_names = {
        "fullname": "Student Name",
        "date_joined": "Joined date",
        "phone_number": "Phone Number",
        "email": "Email",
        "status": "Status",
        "college_name": "College Name",
        "address": "Address",
    }

    def get_fullname(self, obj):
        return obj.__str__()

    def get_created_date(self, obj):
        return get_human_readable_date_time(obj.date_joined)

    def get_phone(self, obj):
        return str(obj.username)

    def get_email(self, obj):
        return obj.email

    def get_status(self, obj):
        if obj.is_active:
            return "Active"
        return "Inactive"

    def get_college_name(self, obj):
        return obj.profile.college_name

    def get_address(self, obj):
        return obj.profile.address

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "fullname": self.get_fullname,
            "date_joined": self.get_created_date,
            "phone_number": self.get_phone,
            "email": self.get_email,
            "status": self.get_status,
            "college_name": self.get_college_name,
            "address": self.get_address,
        }
        return fields_and_values[field_name](obj)


class TeacherTableData(BaseDynamicTableData):
    model = User
    field_to_header_names = {
        "fullname": "Teacher Name",
        "phone_number": "Phone Number",
        "email": "Email",
    }

    def get_fullname(self, obj):
        return obj.__str__()

    def get_phone(self, obj):
        return str(obj.username)

    def get_email(self, obj):
        return obj.email

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "fullname": self.get_fullname,
            "phone_number": self.get_phone,
            "email": self.get_email,
        }
        return fields_and_values[field_name](obj)


class ExamTableData(BaseDynamicTableData):
    model = Exam
    field_to_header_names = {
        "exam": "Exam",
        "exam_type": "Type",
        "exam_date": "Exam Date",
        "examinee": "Examinee",
        "passes": "Passes",
        "failed": "Failed",
    }

    def get_exam_name(self, obj):
        return obj.name

    def get_exam_type(self, obj):
        return obj.exam_type

    def get_exam_date(self, obj):
        exam_sessions = obj.sessions.all()
        return ", ".join(
            [
                exam_session.start_date.strftime("%d %b %Y")
                for exam_session in exam_sessions
            ]
        )

    def examinee_filter(self, obj, filter_args):
        exam_enrolls = obj.exam_enrolls.all().order_by("selected_session")
        exam_sessions = obj.sessions.all()
        examinees = []
        for exam_session in exam_sessions:
            exam_enrolls_count = exam_enrolls.filter(selected_session=exam_session)
            exam_enrolls_count = (
                exam_enrolls_count.filter(**filter_args).count()
                if filter_args
                else exam_enrolls_count.count()
            )
            examinees.append(exam_enrolls_count)
        return ", ".join([str(examinee) for examinee in examinees])

    def get_examinee_count(self, obj):
        return self.examinee_filter(obj, None)

    def get_passed_count(self, obj):
        return self.examinee_filter(obj, {"status": ExamEnrollmentStatus.PASSED})

    def get_failed_count(self, obj):
        return self.examinee_filter(obj, {"status": ExamEnrollmentStatus.FAILED})

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

    model = Course
    field_to_header_names = {
        "course_name": "Course Name",
        "price": "Price",
        "duration": "Duration",
        "students_enrolled": "Students Enrolled",
        "start_date": "Start Date",
        "status": "Status",
    }

    def get_course_name(self, obj):
        return obj.name

    def get_price(self, obj):
        return obj.price

    def get_duration(self, obj):
        return obj.duration

    def get_students_enrolled_count(self, obj):
        return str(obj.enrolls.all().count())

    def get_start_date(self, obj):
        return " ,".join(x.start_date.strftime("%d %b %Y") for x in obj.sessions.all())

    def get_status(self, obj):
        return obj.status.upper()

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "course_name": self.get_course_name,
            "price": self.get_price,
            "duration": self.get_duration,
            "students_enrolled": self.get_students_enrolled_count,
            "start_date": self.get_start_date,
            "status": self.get_status,
        }
        return fields_and_values[field_name](obj)


class StudentAttendanceTableData(BaseDynamicTableData):
    model = StudentAttendance
    field_to_header_names = {
        "date": "Date",
        "time": "Time",
    }

    def get_date(self, obj):
        return obj.date.strftime("%Y-%m-%d")

    def get_time(self, obj):
        return obj.date.strftime("%H:%M %p")

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "date": self.get_date,
            "time": self.get_time,
        }
        return fields_and_values[field_name](obj)


class TeacherAttendanceTableData(BaseDynamicTableData):
    model = TeacherAttendance
    field_to_header_names = {
        "date": "Date",
        "time": "Time",
    }

    def get_date(self, obj):
        return obj.date.strftime("%Y-%m-%d")

    def get_time(self, obj):
        return obj.date.strftime("%H:%M %p")

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "date": self.get_date,
            "time": self.get_time,
        }
        return fields_and_values[field_name](obj)


class AllStudentAttendanceTableData(BaseDynamicTableData):
    model = StudentAttendance
    field_to_header_names = {
        "student_name": "Student Name",
        "phone_number": "Phone Number",
        "attendance_time": "Attendance time",
    }

    def get_student_name(self, obj):
        return obj.user.__str__()

    def get_phone_number(self, obj):
        return str(obj.user.username)

    def get_time(self, obj):
        return obj.date.strftime("%H:%M %p")

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "student_name": self.get_student_name,
            "phone_number": self.get_phone_number,
            "attendance_time": self.get_time,
        }
        return fields_and_values[field_name](obj)


class AllTeacherAttendanceTableData(BaseDynamicTableData):
    model = TeacherAttendance
    field_to_header_names = {
        "teachers_name": "Teacher Name",
        "phone_number": "Phone Number",
        "attendance_time": "Attendance time",
    }

    def get_teachers_name(self, obj):
        return obj.user.__str__()

    def get_phone_number(self, obj):
        return str(obj.user.username)

    def get_time(self, obj):
        return obj.date.strftime("%H:%M %p")

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "teachers_name": self.get_teachers_name,
            "phone_number": self.get_phone_number,
            "attendance_time": self.get_time,
        }
        return fields_and_values[field_name](obj)


class ExamResultTableData(BaseDynamicTableData):
    model = ExamThroughEnrollment
    field_to_header_names = {
        "student_name": "Student's Name",
        "college_name": "College Name",
        "rank": "Rank",
        "score": "Score",
        "negative_score": "Negative Score",
        "status": "Status",
    }

    def get_students_name(self, obj):
        return obj.enrollment.student.__str__()

    def get_college_name(self, obj):
        return obj.enrollment.student.profile.college_name

    def get_rank(self, obj):
        return str(get_student_rank(obj))

    def get_score(self, obj):
        return str(obj.score)

    def get_negative_score(self, obj):
        return str(obj.negative_score)

    def get_status(self, obj):
        return obj.status

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "student_name": self.get_students_name,
            "college_name": self.get_college_name,
            "rank": self.get_rank,
            "score": self.get_score,
            "negative_score": self.get_negative_score,
            "status": self.get_status,
        }
        return fields_and_values[field_name](obj)


class PaymentTableData(BaseDynamicTableData):
    model = Payment
    field_to_header_names = {
        "name": "Name",
        "type": "Type",
        "enrollment": "Enrollment",
        "revenue": "Revenue",
    }

    def get_name(self, obj):
        return obj.enrollment.student.__str__()

    def get_payment_category(self, obj):
        type_string = []
        if obj.enrollment.exams.all().count() > 0:
            type_string.append("Exam")
        if obj.enrollment.courses.all().count() > 0:
            type_string.append("Course")
        return ",".join(type_string)

    def get_enrollment(self, obj):
        enrollment_string = []
        if obj.enrollment.exams.all().count() > 0:
            for exam_name in obj.enrollment.exams.all():
                enrollment_string.append(exam_name.name)
        if obj.enrollment.courses.all().count() > 0:
            for course_name in obj.enrollment.courses.all():
                enrollment_string.append(course_name.name)
        return ",".join(enrollment_string)

    def get_revenue(self, obj):
        return str(obj.amount)

    def get_values_from_fields(self, field_name, obj):
        fields_and_values = {
            "name": self.get_name,
            "type": self.get_payment_category,
            "enrollment": self.get_enrollment,
            "revenue": self.get_revenue,
        }
        return fields_and_values[field_name](obj)
