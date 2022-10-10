def get_model_and_its_fields(model_type, model_fields):
    from enrollments.models import ExamThroughEnrollment

    data = [
        {
            "model_type": "ExamThroughEnrollment",
            "model_name": ExamThroughEnrollment
        }
    ]

    model = None
    for d in data:
        if model_type == d["model_type"]:
            model = d["model_name"]
    get_fields(model_type, model_fields)        


def get_fields(model_type, model_fields):
    field_names = []
    if model_type == "ExamThroughEnrollment":
        for field_name in model_fields:
            if field_name == "exam":
                
