from celery import shared_task

from enrollments.models import ExamThroughEnrollment


@shared_task
def calculate_score(exam_through_enrollment_id):
    exam_through_enrollment = ExamThroughEnrollment.objects.get(
        id=exam_through_enrollment_id
    )
    exam_through_enrollment.score = exam_through_enrollment.calculate_score()
    # exam_through_enrollment.save()
    pass_marks = exam_through_enrollment.exam.template.pass_marks
    if exam_through_enrollment.score >= pass_marks:
        # pass trigger
        exam_through_enrollment.pass_exam()
    else:
        # fail trigger
        exam_through_enrollment.fail_exam()
