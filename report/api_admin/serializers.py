from rest_framework import serializers

from report.models import GeneratedReport


class GeneratedReportSerializers(serializers.ModelSerializer):
    class Meta:
        model = GeneratedReport
        fields = ["report_file"]
