from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated


class BaseCreatorAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user,
        )
