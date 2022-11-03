from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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


class BaseReportGeneratorAPIView(ListAPIView):
    filter_backends = None
    search_fields = None
    queryset = None
    filterset_class = None
    model_name = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.model_name:
            ctx["model_name"] = self.model_name
        return ctx

    def get(self, request):
        filtered_data = self.filter_queryset(self.get_queryset())
        excelcelery.delay(
            list(filtered_data.values_list("pk", flat=True)),
            self.model_name,
            request.user.id,
        )
        return Response({"msg": "Your will be notified after your file is ready."})
