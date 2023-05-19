from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import AccountSerializer, RegisterSerializer, LoginSerializer, AccountUpdateSerializer, MyAccountSerializer
from .models import Account
from .permissions import IsOwnerReadOnly


class AccountListAPIView(generics.ListAPIView):
    #  http://127.0.0.1:8000/account/list/
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class RegisterAPIView(generics.GenericAPIView):
    #  http://127.0.0.1:8000/account/register/
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, 'data': "Account successfully created"}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    #  http://127.0.0.1:8000/account/login/
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"tokens": serializer.data['tokens']}, status=status.HTTP_200_OK)


class AccountRUDApiView(generics.RetrieveUpdateAPIView):
    serializer_class = AccountUpdateSerializer
    queryset = Account.objects.all()
    permission_classes = [IsOwnerReadOnly]

    def get(self, request, *args, **kwargs):
        query = self.get_object()
        if query:
            serializer = self.serializer_class(query)
            return Response({"success": True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'query did not exit'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, 'message': "credentials is invalid"}, status=status.HTTP_404_NOT_FOUND)



class MyAccountAPIView(generics.ListAPIView):
    serializer_class = MyAccountSerializer
    queryset = Account.objects.all()
    permission_classes = [IsOwnerReadOnly]