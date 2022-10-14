
class BaseDynamicTableData:
    field_to_header_names = None

    def __init__(self, model_fields, queryset, worksheet):
        self.model_fields = model_fields
        self.worksheet = worksheet
        self.queryset = queryset
    
    def get_header_names_from_field_names(self):
        header_list = []
        for key, value in self.field_to_header_names.items():
            for fields in self.model_fields:
                if fields == key:
                    header_list.append(value)
        return header_list

    def generate_report(self):
        # retrieve ExamThroughEnrollment model data
        queryset = self.queryset

        worksheet = self.worksheet
        worksheet.write(0, 0,'S.No')
        i = 1
        # For header names
        for head_name in self.get_header_names_from_field_names():
            worksheet.write(0, i, head_name)
            i= i+1

        # For data
        col = 0
        row = 1
        for linea in queryset:
            worksheet.write(row, col, row)  #For serial number.
            for field_name in self.model_fields:
                col=col+1
                worksheet.write(row, col, self.get_values_from_fields(field_name, linea))
            row=row+1
            col = 0
        return worksheet