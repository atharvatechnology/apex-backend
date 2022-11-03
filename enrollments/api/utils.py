from django.contrib.auth import get_user_model
from rest_framework import serializers

from enrollments.models import (
    CourseThroughEnrollment,
    EnrollmentStatus,
    ExamSession,
    ExamThroughEnrollment,
    SessionStatus,
)
from exams.models import ExamStatus


def is_enrolled(enrolled_obj, user):
    """Return True if user has enrollment for that obj.

    Parameters
    ----------
    enrolled_obj : exam/course
        obj to which user is enrolled into
    user : user
        whose enrollment is to be checked

    Returns
    -------
    bool
        state of enrollment of user to that obj

    """
    enrollments = []
    if user.is_authenticated:
        enrollments = enrolled_obj.enrolls.all().filter(student=user)
    if len(enrollments) > 0:
        return True
    return False


def is_enrolled_active(enrolled_obj, user):
    """Return True if user has active enrollment for that obj.

    Parameters
    ----------
    enrolled_obj : exam/course
        obj to which user is enrolled into
    user : user
        whose enrollment is to be checked

    Returns
    -------
    bool
        state of active enrollment of user to that obj

    """
    enrollments = []
    if user.is_authenticated:
        enrollments = enrolled_obj.enrolls.all().filter(
            student=user, status=EnrollmentStatus.ACTIVE
        )
    if len(enrollments) > 0:
        return True
    return False


def get_student_rank(obj):
    """Get the rank of the user in the exam.

    This is based on the score of current exam takers.

    Parameters
    ----------
    obj : ExamThroughEnrollment
        exam enrollment.

    Returns
    -------
    int
        rank of the user in the exam.

    """
    if obj.selected_session.status == "resultsout":
        all_examinee_states = ExamThroughEnrollment.objects.filter(
            exam=obj.exam, selected_session=obj.selected_session
        )
        num_examinee = all_examinee_states.count()
        num_examinee_lower_score = all_examinee_states.filter(
            score__lt=obj.score
        ).count()
        return num_examinee - num_examinee_lower_score
    else:
        return None


def batch_is_enrolled_and_price(enrolled_objs, user):
    sum_price = 0.0
    for enrolled_obj in enrolled_objs:
        sum_price += float(enrolled_obj.price)
        if is_enrolled(enrolled_obj, user):
            raise serializers.ValidationError(
                f"{user} is already enrolled into {enrolled_obj}"
            )
    return sum_price


def exam_data_save(exams_data, enrollment):
    if exams_data:
        for data in exams_data:
            exam = data.get("exam")
            selected_session = data.get("selected_session")
            ExamThroughEnrollment(
                enrollment=enrollment, exam=exam, selected_session=selected_session
            ).save()


# TODO Need to be discussed. Status send in List.
# TODO Change self to user. since user is only used.
def retrieve_exam_status(self, obj):
    user = self.context["request"].user
    if not user.is_authenticated:
        return None
    enrollment = ExamThroughEnrollment.objects.filter(
        enrollment__student=user,
        exam=obj,
    ).first()
    if enrollment:
        session_id = enrollment.selected_session.id
        exam_session = ExamSession.objects.filter(id=session_id).first()
        if exam_session:
            if exam_session.status == SessionStatus.INACTIVE:
                return ExamStatus.SCHEDULED
            elif exam_session.status == SessionStatus.ACTIVE:
                return ExamStatus.IN_PROGRESS
        return ExamStatus.CREATED
    return ExamStatus.CREATED


def dynamic_excel_generator(queryset_id, data, user_id):
    import os
    from pathlib import Path

    import xlsxwriter
    from django.conf import settings

    from accounts.models import Profile
    from report.models import GeneratedReport
    from report.views import (
        CourseThroughEnrollmentTableData,
        ExamThroughEnrollmentTableData,
        StudentTableData,
    )

    User = get_user_model()
    # Create a workbook and add a worksheet.
    user = User.objects.get(id=1)
    media_path = f"reports/{user.username}"
    base_path = os.path.join(settings.BASE_DIR, f"media/{media_path}")
    os.makedirs(base_path, exist_ok=True)

    filename = get_random_string()
    p = Path(f"{base_path}/{filename}.xlsx")
    workbook = xlsxwriter.Workbook(p)
    worksheet = workbook.add_worksheet("report")
    # bold = workbook.add_format({"bold": True})
    # Some data we want to write to the worksheet.
    # passing field names received from front-end

    if data == "ExamThroughEnrollment":
        # get model names and it correcponding headers needed in report.
        model_fields = [
            "enrollment",
            "exam",
            "selected_session",
            "rank",
            "score",
            "negative_score",
            "status",
        ]
        queryset = ExamThroughEnrollment.objects.filter(id__in=queryset_id)
        report = ExamThroughEnrollmentTableData(model_fields, queryset, worksheet)
    elif data == "CourseThroughEnrollment":
        model_fields = [
            "enrollment",
            "course_name",
            "selected_session",
            "course_enroll_status",
            "completed_date",
        ]
        queryset = CourseThroughEnrollment.objects.filter(id__in=queryset_id)
        report = CourseThroughEnrollmentTableData(model_fields, queryset, worksheet)
    elif data == "StudentProfile":
        model_fields = [
            "username",
            "fullname",
            "email",
            "college_name",
            "faculty",
        ]
        queryset = Profile.objects.filter(id__in=queryset_id)
        report = StudentTableData(model_fields, queryset, worksheet)
    worksheet = report.generate_report()
    workbook.close()

    GeneratedReport.objects.create(
        created_by=user, updated_by=user, report_file=f"{media_path}/{filename}.xlsx"
    )

    """
    if need to send file to front-end
    """
    # output.seek(0)
    # """
    # For testing without front-end
    # """
    # response = HttpResponse(
    #     output.read(),
    #     content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    # )
    # # response['Content-Disposition'] = "attachment; filename=report.xlsx"
    # """
    # To send actual xlsx file.
    # """
    # blob = base64.b64encode(output.read())
    # response = HttpResponse(blob, content_type="application/ms-excel")
    # response["Content-Disposition"] = "attachment; filename=report.xlsx"

    # return response


def get_random_string():
    import random
    import string

    # With combination of lower and upper case
    result_str = "".join(random.choice(string.ascii_letters) for i in range(7))
    return result_str
