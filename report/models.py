from django.db import models

from common.models import CreatorBaseModel


class GeneratedReport(CreatorBaseModel):
    def report_upload(self, filename):
        """To upload report."""
        return f"reports/{self.created_by.username}/{filename}"

    report_file = models.FileField(upload_to=report_upload)
