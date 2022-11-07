from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.api.serializers import ModelFieldsSerializer
from enrollments.api.tasks import excelcelery


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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.model_name:
            ctx["model_name"] = self.model_name
        return ctx

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        filtered_data = self.filter_queryset(self.get_queryset())
        excelcelery.delay(
            list(serializer.data["model_fields"]),
            self.model_name,
            list(filtered_data.values_list("pk", flat=True)),
            request.user.id,
        )
        return Response({"msg": "Your will be notified after your file is ready."})
