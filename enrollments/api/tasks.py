from celery import shared_task


@shared_task
def excelcelery(model_fields, model_name, filtered_data, user_id):
    from report.tabledata import (
        CourseTableData,
        CourseThroughEnrollmentTableData,
        ExamTableData,
        ExamThroughEnrollmentTableData,
        StudentAttendanceTableData,
        StudentTableData,
        TeacherAttendanceTableData,
    )

    call_table = {
        "ExamThroughEnrollment": ExamThroughEnrollmentTableData,
        "CourseThroughEnrollment": CourseThroughEnrollmentTableData,
        "StudentProfile": StudentTableData,
        "Exam": ExamTableData,
        "Course": CourseTableData,
        "StudentAttendance": StudentAttendanceTableData,
        "TeacherAttendance": TeacherAttendanceTableData,
    }
    call_table[model_name](filtered_data, user_id, model_fields).generate_report()
