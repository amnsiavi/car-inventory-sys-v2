from rest_framework.status import (
    HTTP_200_OK,HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import (
    generics, mixins
)
from django.contrib.auth.models import User
from Auth.api.serializer import AuthSerializer

class CreateUser(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.ListModelMixin
):
    queryset = User.objects.all()
    serializer_class = AuthSerializer



    def get(self, request, *args, **kwargs):

        try:
            return Response({
                'data':self.list(request,*args,**kwargs).data,
                'status':'Fetch Sucessful'
            },status=HTTP_200_OK)
        except Exception as e:
            return Response({
                'status':'Failed',
                'errors':str(e)
            })


    def post(self,request,*args,**kwargs):

        try:
            if len(request.data) == 0:
                return Response({
                    'status':'Failed',
                    'errors':'Recieved Empty Object'
                },status=HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                username = request.data.get('username')
                email = request.data.get('email')
                password = request.data.get('password')
                is_admin = request.data.get('is_superuser')
                if User.objects.filter(username=username).exists():
                    return Response({
                        'status':'Failed',
                       'msg':'Username Already Exists'
                    },status=HTTP_400_BAD_REQUEST)
                if User.objects.filter(email=email).exists():
                    return Response({
                        'status':'Failed',
                       'msg':'Email Already Exists'
                    },status=HTTP_400_BAD_REQUEST)
                if is_admin:
                    User.objects.create_superuser(
                        username=username, email=email,
                        password=password
                    )
                    return Response({
                        'status':'Sucess',
                        'msg':'User Created'
                    },status=HTTP_201_CREATED)
                else:
                    User.objects.create_user(
                        username=username, email=email,
                        password=password
                    )
                    return Response({
                        'status':'Sucess',
                        'msg':'User Created'
                    },status=HTTP_201_CREATED)
            else:
                return Response({
                    'status':'Failed',
                    'errors':serializer.errors
                },status=HTTP_400_BAD_REQUEST)
            
        
                
        except ValidationError as ve:
            return Response({
                'status':'Failed',
                'errors':ve.detail
            },status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status':'Failed',
                'errors':str(e)
            })
