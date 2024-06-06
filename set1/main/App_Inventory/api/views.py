from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
    HTTP_405_METHOD_NOT_ALLOWED, HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_404_NOT_FOUND
)
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework import (
    generics, mixins
)

# Models and Serializers
from App_Inventory.models import CarInventory

from App_Inventory.api.serializer import CarInventorySerializer


@api_view(['GET'])
def get_inventory(request):
    
    try:
        username = request.headers.get('Authorization')
        if username:
            if User.objects.filter(username=username).exists():
                inventory = CarInventory.objects.all()
                serializer = CarInventorySerializer(inventory,many=True)
                return Response({
                    'data':serializer.data,
                    'status':'Sucess'
                    
                },status=HTTP_200_OK)
            else:
                return Response({
                    'status':'Auth Failed',
                    'msg':'User Not Found'

                },status=HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status':'Auth Failed',
                'msg':'Provide Valid Authorization'
            },status=HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({
            'status':'Failed',
            'errors':str(e)
        })

class CreateItem(
    generics.GenericAPIView,
    mixins.CreateModelMixin
):
    queryset = CarInventory.objects.all()
    serializer_class = CarInventorySerializer


    def post(self, request, *args, **kwargs):

        try:
            username = request.headers.get('Authorization')
            if username:
                if User.objects.filter(username=username).exists():
                    user = User.objects.get(username=username)
                    if user.is_superuser:
                        if len(request.data) == 0:
                            return Response({
                                'status':'Failed',
                                'errors':'Recieved Empty Object'
                            },status=HTTP_400_BAD_REQUEST)
                        serializer = self.get_serializer(data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                            return Response({
                                'status':'Sucessful',
                                'msg':'Item Created'
                            },status=HTTP_200_OK)
                        else:
                            return Response({
                                'status':'Failed',
                                'errors':serializer.errors
                            },status=HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            'status':'Failed',
                            'errors':'User Not Authorized'
                        },status=HTTP_401_UNAUTHORIZED)
                else:
                    return Response({
                        'status':'Auth Failed',
                        'errors':'User Not Found'
                    },status=HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    'status':'Auth Failed',
                    'msg':'Provide valid Authorization'
                },status=HTTP_401_UNAUTHORIZED)
        except ValidationError as ve:
            return Response({
                'status':'Failed',
                'errors':ve.detail
            })
        except Exception as e:
            return Response({
                'status':'Failed',
                'errors':str(e)
            })

@api_view(['GET','DELETE','PUT','PATCH'])
def get_item(request,pk):
    

    try:
        if request.method == 'GET':
            username = request.headers.get('Authorization')
            if username:
                if User.objects.filter(username=username).exists():
                    instance = CarInventory.objects.get(pk=pk)
                    if instance:
                        serializer = CarInventorySerializer(instance)
                        return Response({
                            'status':'Sucess',
                            'data':serializer.data
                        })
                    else:
                        return Response({
                            'status':'Failed',
                            'msg':'Reccord Not Found'
                        },status=HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        'status':'Auth Failed',
                        'errors':'User Not Found'
                    })
            else:
                return Response({
                    'status':'Failed',
                    'errors':'Provide Valid Authorization Header'
                })
        elif request.method == 'DELETE':
            try:
                username = request.headers.get('Authorization')
                if username:
                    if User.objects.filter(username=username).exists():
                        user = User.objects.get(username=username)
                        if user.is_superuser:
                            instance = CarInventory.objects.get(pk=pk)
                            instance.delete()
                            return Response({
                                'status':'Deletion Sucessful',
                            },status=HTTP_200_OK)
                        else:
                            return Response({
                                'status':'Deletion Failed',
                                'errors':'User Not Authorize'
                            },status=HTTP_401_UNAUTHORIZED)
                    else:
                        return Response({
                            'status':'Failed',
                            'errors':'User Does Not Exsists'
                        },status=HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        'status':'Auth Failed',
                        'errors':'Provide Valid Authorization Header'
                    },status=HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response({
                    'status':'Failed',
                    'errors':str(e)
                },status=HTTP_500_INTERNAL_SERVER_ERROR)
        
        elif request.method == 'PUT':
            try:
                username = request.headers.get('Authorization')
                if username:
                    if User.objects.filter(username=username).exists():
                       
                        user = User.objects.get(username=username)
                        if user.is_superuser:
                            if len(request.data) == 0:
                                return Response({
                                    'status':'Failed',
                                    'errors':'Recieved Empty Object'
                                },status=HTTP_400_BAD_REQUEST)
                            instance = CarInventory.objects.get(pk=pk)
                            serializer = CarInventorySerializer(instance,data=request.data)
                            if serializer.is_valid():
                                serializer.save()
                                return Response({
                                    'status':'Sucessful',
                                    'data':serializer.data
                                },status=HTTP_200_OK)
                            else:
                                return Response({
                                    'status':'Failed',
                                    'errors':serializer.errors
                                },status=HTTP_400_BAD_REQUEST)
                        else:
                            return Response({
                                'status':'Auth Failed',
                                'errors':'User Not Authorized'
                            },status=HTTP_401_UNAUTHORIZED)
                    else:
                        return Response({
                            'status':'Failed',
                            'errors':'User Does Not Exsists'
                        },status=HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        'status':'Auth Failed',
                        'msg':'Provide Valid Authorization Header'
                    },status=HTTP_401_UNAUTHORIZED)
            except ValidationError as ve:
                return Response({
                    'status':'Failed',
                    'errors':ve.detail
                },status=HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    'status':'Failed',
                    'errors':str(e)
                },status=HTTP_500_INTERNAL_SERVER_ERROR)
        elif request.method == 'PATCH':
            try:
                username = request.headers.get('Authorization')
                if username:
                    if User.objects.filter(username=username).exists():
                        user = User.objects.get(username=username)
                        if user.is_superuser:
                            if len(request.data) == 0:
                                return Response({
                                    'status':'Failed',
                                    'errros':'Recieved Empty Object'
                                },status=HTTP_400_BAD_REQUEST)
                            instance = CarInventory.objects.get(pk=pk)
                            serializer = CarInventorySerializer(instance,data=request.data,partial=True)
                            if serializer.is_valid():
                                serializer.save()
                                return Response({
                                    'status':'Sucessful',
                                    'data':serializer.data
                                },status=HTTP_200_OK)
                            else:
                                return Response({
                                    'status':'Failed',
                                    'errors':serializer.errors
                                },status=HTTP_400_BAD_REQUEST)
                        else:
                            return Response({
                                'status':'Auth Failed',
                                'errors':'User Not Authorize'
                            },status=HTTP_401_UNAUTHORIZED)
                    else:
                        return Response({
                            'status':'Failed',
                            'errors':'User Does Not Exsists'
                        },status=HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        'status':'Auth Failed',
                        'errors':'Provide Valid Authorization Header'
                    },status=HTTP_401_UNAUTHORIZED)
            except ValidationError as ve:
                return Response({
                    'status':'Failed',
                    'errors':ve.detail
                },status=HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    'status':'Failed',
                    'errors':str(e)
                },status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                'status':'Failed',
                'errors':'Method Not Allowed'
            },status=HTTP_405_METHOD_NOT_ALLOWED)
    except ValidationError as ve:
        return Response({
            'status':'Failed',
            'errors':ve.detail
        })
    except Exception as e:
        return Response({
            'status':'Failed',
            'errors':str(e)
        },status=HTTP_500_INTERNAL_SERVER_ERROR)
