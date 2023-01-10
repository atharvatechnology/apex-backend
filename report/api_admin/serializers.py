from rest_framework import serializers

from report.models import GeneratedReport


class GeneratedReportRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedReport
        fields = ["report_file"]
