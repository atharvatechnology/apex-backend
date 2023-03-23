from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.api.serializers import ModelFieldsSerializer
from common.permissions import IsAccountant, IsAdminOrSuperAdminOrDirector
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
    serializer_class = ModelFieldsSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsAccountant]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.model_name:
            ctx["model_name"] = self.model_name
        return ctx

    def post(self, request, *args, **kwargs):
        original_data_headers = self.get(request).data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        queryset = self.get_queryset()
        # Comparing headers needed for operation vs headers sent from front-end.
        frontend_headers = serializer.data["model_fields"]
        actual_headers = original_data_headers["model_fields"]
        if not set(frontend_headers).issubset(set(actual_headers)):
            return Response(
                {
                    "msg": "Different header parameters. \
                        Please send only those headers sent in get request."
                }
            )

        # sorting of list as per actual list
        new_ordered_header = [
            header for header in actual_headers if header in frontend_headers
        ]

        if self.request.GET.get("user_id"):
            user_id = self.request.GET.get("user_id")
            queryset = self.get_queryset().filter(user=user_id)
        filtered_data = self.filter_queryset(queryset)
        report_object = GeneratedReport.objects.last()
        id_of_last_report = report_object.id if report_object else 0

        new_generated_id = int(id_of_last_report) + 1
        excelcelery.delay(
            new_ordered_header,
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
