import os
from pathlib import Path

import xlsxwriter
from django.conf import settings
from django.contrib.auth import get_user_model

from common.utils import get_random_string
from report.models import GeneratedReport

User = get_user_model()


class BaseDynamicTableData:
    field_to_header_names = None
    model = None

    def __init__(self, queryset, user_id, model_fields):
        self.model_fields = model_fields
        self.user_id = user_id
        self.queryset = queryset

    def get_header_names_from_field_names(self):
        header_list = []
        for key, value in self.field_to_header_names.items():
            for fields in self.model_fields:
                if fields == key:
                    header_list.append(value)
        return header_list

    def generate_report(self):
        # retrieve model data
        queryset = self.model.objects.filter(id__in=self.queryset)

        user = User.objects.get(id=self.request.user.id)
        media_path = f"reports/{user.username}"
        base_path = os.path.join(settings.BASE_DIR, f"media/{media_path}")
        os.makedirs(base_path, exist_ok=True)

        filename = get_random_string()
        p = Path(f"{base_path}/{filename}.xlsx")
        workbook = xlsxwriter.Workbook(p)
        worksheet = workbook.add_worksheet("report")

        worksheet.write(0, 0, "S.No")
        i = 1
        # For header names
        for head_name in self.get_header_names_from_field_names():
            worksheet.write(0, i, head_name)
            i = i + 1

        # For data
        col = 0
        row = 1
        for linea in queryset:
            worksheet.write(row, col, row)  # For serial number.
            for field_name in self.model_fields:
                col = col + 1
                worksheet.write(
                    row, col, self.get_values_from_fields(field_name, linea)
                )
            row = row + 1
            col = 0

        workbook.close()

        GeneratedReport.objects.create(
            created_by=user,
            updated_by=user,
            report_file=f"{media_path}/{filename}.xlsx",
        )
