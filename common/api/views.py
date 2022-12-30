from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.api.serializers import ModelFieldsAndFilterParamsSerializer
from common.permissions import IsAccountant, IsAdminorSuperAdminorDirector
from enrollments.api.tasks import excelcelery
from report.models import GeneratedReport


class BaseCreatorCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user,
        )


class BaseCreatorUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(
            updated_by=self.request.user,
        )


class BaseReportGeneratorAPIView(GenericAPIView):
    filter_backends = None
    search_fields = None
    queryset = None
    filterset_class = None
    model_name = None
    serializer_class = ModelFieldsAndFilterParamsSerializer
    permission_classes = [
        IsAuthenticated & (IsAdminorSuperAdminorDirector | IsAccountant)
    ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.model_name:
            ctx["model_name"] = self.model_name
        return ctx

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.data["filter_params"]:
            filtered_data = self.filter_queryset(
                self.get_queryset().filter(**serializer.data["filter_params"])
            )
        else:
            filtered_data = self.filter_queryset(self.get_queryset())

        report_object = GeneratedReport.objects.last()
        id_of_last_report = report_object.id if report_object else 0

        new_generated_id = int(id_of_last_report) + 1
        excelcelery.delay(
            list(serializer.data["model_fields"]),
            self.model_name,
            list(filtered_data.values_list("pk", flat=True)),
            request.user.id,
        )
        return Response(
            {
                "msg": "Your will be notified after your file is ready.",
                "new_generated_id": new_generated_id,
            }
        )
