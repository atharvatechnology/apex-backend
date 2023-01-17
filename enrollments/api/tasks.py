from celery import shared_task


@shared_task
def excelcelery(model_fields, model_name, filtered_data, user_id):
    from report.tabledata import (
        AllStudentAttendanceTableData,
        AllTeacherAttendanceTableData,
        CourseTableData,
        CourseThroughEnrollmentTableData,
        ExamTableData,
        ExamThroughEnrollmentTableData,
        StudentAttendanceTableData,
        StudentTableData,
        TeacherAttendanceTableData,
        TeacherTableData,
    )

    call_table = {
        "ExamThroughEnrollment": ExamThroughEnrollmentTableData,
        "CourseThroughEnrollment": CourseThroughEnrollmentTableData,
        "StudentProfile": StudentTableData,
        "Exam": ExamTableData,
        "Course": CourseTableData,
        "StudentAttendance": StudentAttendanceTableData,
        "TeacherAttendance": TeacherAttendanceTableData,
        "TeacherProfile": TeacherTableData,
        "AllTeacherAttendance": AllTeacherAttendanceTableData,
        "AllStudentAttendance": AllStudentAttendanceTableData,
    }
    call_table[model_name](filtered_data, user_id, model_fields).generate_report()
