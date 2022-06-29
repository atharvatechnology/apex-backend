from rest_framework import serializers


def validate_gt_than_template_marks(template_marks, marks):
    if marks > template_marks:
        raise serializers.ValidationError(
            f"The marks cannot be greater than {template_marks}"
        )
