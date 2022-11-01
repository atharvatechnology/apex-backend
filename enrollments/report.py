from common.report import BaseDynamicTableData
from enrollments.api.utils import get_student_rank

class ExamThroughEnrollmentTableData(BaseDynamicTableData):
    field_to_header_names = {
        "enrollment": 'Student\'s Name',
        "exam": "Exam",
        "selected_session": "Selected Session",
        # "rank": "Rank",
        "score": "Score",
        "negative_score": "Negative Score",
        "status": "Status"
    }

    def get_students_name(self, linea):
        return str(linea.enrollment.student.first_name)+str(linea.enrollment.student.last_name)
    
    def get_exam_name(self, linea):
        return linea.exam.name

    def get_session(self, linea):
        return str(linea.selected_session.start_date.date())

    def get_score(self, linea):
        return str(linea.score)
    
    def get_negative_score(self, linea):
        print("111111111111111")
        return str(linea.negative_score)

    def get_status(self, linea):
        print(linea.status)
        return linea.status
    
    def get_rank(self, linea):
        print("passed1")
        return get_student_rank(linea)

    def get_values_from_fields(self, field_name, linea):
        fields_and_values = {
            "enrollment": self.get_students_name,
            "exam": self.get_exam_name,
            "selected_session": self.get_session,
            "rank": self.get_rank,
            "score": self.get_score,
            "negative_score": self.get_negative_score,
            "status": self.get_status
        }
        return fields_and_values[field_name](linea)
    