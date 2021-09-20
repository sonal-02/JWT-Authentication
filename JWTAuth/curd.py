from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import UserSerializer, CURDSerializer
from .models import User
from rest_framework.response import Response


class ListCreateUserView(ListCreateAPIView):
    """
    This API is for create and get list of employee. To use this API manager authentication is needed with JWT Token.
    """
    queryset = User.objects.filter(is_manager=False)
    serializer_class = CURDSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class UpdateRetrieveDeleteUser(RetrieveUpdateDestroyAPIView):
    """
    This API is used to update, partial update, retrieve specific data and delete specific data.
    To use this API manager authentication is needed with JWT Token.
    """
    queryset = User.objects.filter(is_manager=False)
    serializer_class = CURDSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def destroy(self, request, *args, **kwargs):
        """
        After delete request called this method is used to send response back
        :param request: 5
        :return:  Employee deleted successfully
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Employee deleted successfully"
        },
            status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """
        This function actually delete the employee.
        """
        instance.delete()

    @swagger_auto_schema(request_body=CURDSerializer(required=True, partial=True))
    def patch(self, request, *args, **kwargs):
        """
        This method is for partial update. To do partial update correctly on swagger used @swagger_auto_schema
        decorator.
        """
        kwargs['partial'] = True
        return self.partial_update(request, *args, **kwargs)
