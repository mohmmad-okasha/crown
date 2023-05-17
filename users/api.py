import os
from os import path
from django.conf import settings
 
from .models import Users
from .models import Test_model
from .models import Customers
# from .serializers import users_ser
from .serializers import flights_serializer
# from .serializers import test_ser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework import mixins


# class UsersViewSet(ModelViewSet):
#     queryset= Test_model.objects.all()
#     serializer_class= test_ser
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from django.core.files.storage import default_storage
from django.db.models import Max


class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file_name = self.request.query_params.get('file_name')
        image_file = request.FILES.get('image')

        #to remove last img for this customer
        if(os.path.exists(path.abspath('frontend/public/media/'+path.curdir)+file_name)):
          os.remove(os.path.join(path.abspath('frontend/public/media/'+path.curdir)+file_name))
       
        default_storage.save(path.abspath('frontend/public/media/'+path.curdir)+file_name, image_file)
        return Response({'success': True})


class customers_api(ModelViewSet, mixins.DestroyModelMixin):

    queryset = Customers.objects.all()
    serializer_class = flights_serializer

    # to search for id
    def get_queryset(self):
        #print(path.abspath('../frontend/public/media/'+path.curdir))

        queryset = Customers.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = queryset.filter(id=id)
        if self.request.query_params.get('max_id'):
            queryset = Customers.objects.aggregate(Max('id'))
        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

# get max id
@api_view(['GET'])
def get_max_id(request):
    table_name = request.query_params['table_name']
    max_id= eval(table_name).objects.aggregate(Max('id'))
    return Response({'data':max_id})

# remove file
@api_view(['GET'])
def remove_file(request):
    file_name = request.query_params['file_name']
    file_path=path.abspath('frontend/public/media/'+path.curdir)+file_name
    if(os.path.exists(file_path)):
        os.remove(os.path.join(file_path))
        return Response({'removed':1})
    else:
        return Response({'removed':0})


# @api_view(['GET'])
# def get_users_api(request):
#     all_users= Users.objects.all()
#     data = users_ser(all_users,many=True).data
#     return Response({'data':data})

# @api_view(['GET'])
# def get_user_api(request,id):
#     user= Users.objects.get(id=id)
#     data = users_ser(user).data
#     return Response({'data':data})

# @api_view(['POST'])
# def save_user_api(request):
#         data = JSONParser().parse(request)
#         # instanciate with the serializer
#         serializer = users_ser(data=data)
#         # check if the sent information is okay
#         if(serializer.is_valid()):
#             # if okay, save it on the database
#             serializer.save()


# class get_users_class(generics.ListAPIView):
#     queryset= Users.objects.all()
#     serializer_class= users_ser

# class users_class2(generics.CreateAPIView):
#     queryset= Users.objects.all()
#     serializer_class= users_ser
#     # lookup_field='id'
