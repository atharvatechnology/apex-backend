from common.report import BaseDynamicTableData

class ExamThroughEnrollmentTableData(BaseDynamicTableData):
    field_to_header_names = {
        "enrollment": 'Student\'s Name',
        "exam": "Exam",
        "selected_session": "Selected Session",
        "exam_questions": "Exam Questions",
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
        return str(linea.negative_score)

    def get_status(self, linea):
        return linea.status

    def get_exam_questions(self, linea):
        questions_list = ""
        for questions in linea.exam.questions.all():
            questions_list+= questions.detail + "\n"
        return questions_list

    def get_values_from_fields(self, field_name, linea):
        fields_and_values = {
            "enrollment": self.get_students_name(linea),
            "exam": self.get_exam_name(linea),
            "selected_session": self.get_session(linea),
            "exam_questions": self.get_exam_questions(linea),
            "score": self.get_score(linea),
            "negative_score": self.get_negative_score(linea),
            "status": self.get_status(linea)
        }
        return fields_and_values[field_name]
    