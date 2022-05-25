from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated


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
