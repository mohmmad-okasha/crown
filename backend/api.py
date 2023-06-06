from json import dumps
import os
from os import path

from django.http import JsonResponse
from .models import Flights
from .models import Flight_dates
from .models import Accounts
from .models import Dashboard_buttons
from .models import Settings
from .models import *
from . import serializers

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins

from django.db.models import Max
from django.db.models import Q

from django.core.files.storage import default_storage

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

#####################################################################################

# Login

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
     return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    return Response({'access': access_token}, status=status.HTTP_200_OK)

#####################################################################################

# to upload files

class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file_name = self.request.query_params.get('file_name')
        image_file = request.FILES.get('image')
        file_path = path.abspath(
            'frontend/public/media/'+path.curdir)+file_name
        # to remove last img for this customer
        if (os.path.exists(file_path)):
            os.remove(os.path.join(file_path))

        default_storage.save(file_path, image_file)
        return Response({'success': True})

#####################################################################################

# to get max id from any table

@api_view(['GET'])
def get_max_id(request):
    table_name = request.query_params['table_name']
    max_id = eval(table_name).objects.aggregate(Max('id'))
    return Response({'data': max_id})


#####################################################################################
from django.db.models import Subquery, OuterRef

@api_view(['GET'])
def booking_report(request):
    hotel = str(request.query_params['hotel'])
    hotel_id= Hotels.objects.filter(name=hotel).first().id

    from_date = str(request.query_params['from_date'])
    to_date = str(request.query_params['to_date'])

    data = Bookings.objects.filter(hotel=hotel,dates__gte=from_date,dates__lte=to_date)
    
    #.raw("select backend_bookings.*,backend_rooms.meals from backend_rooms,backend_bookings where hotel_id='"+str(hotel_id)+"' and backend_bookings.room_id = backend_rooms.room_id")
   
    all_data = []
    for d in data:
        all_data.append({
            'id': d.id,
            'hotel': d.hotel,
            'persons_names': d.persons_names,
            'persons_number': d.persons_number,
            'kids_names': d.kids_names,
            'kids_number': d.kids_number,
            'dates': d.dates,
            'room_id': d.room_id,
            'room_type': d.room_type,
            'meals': Rooms.objects.filter(hotel_id=hotel_id,room_id=d.room_id).first().meals,
            'room_categ': Rooms.objects.filter(hotel_id=hotel_id,room_id=d.room_id).first().room_categ,
            'notes': d.notes,
        })


    serializer = serializers.bookings_serializer(all_data, many=True)

    return Response(all_data)

#####################################################################################

# to get rooms by hotel

@api_view(['GET'])
def get_rooms(request):
    hotel = request.query_params['hotel']
    hotel_id= Hotels.objects.filter(name=hotel).first().id
    rooms = Rooms.objects.filter(hotel=hotel_id).values('room_id')
    unique_rooms = set(room['room_id'] for room in rooms)
    return Response(list(unique_rooms))

#####################################################################################

# to get hotels

@api_view(['GET'])
def get_hotels(request):
    hotels = set(Hotels.objects.values_list('name', flat=True))
    return Response(list(hotels))

#####################################################################################

# to get room type

@api_view(['GET'])
def get_room_info(request):
    room_id = request.query_params['room_id']
    hotel = request.query_params['hotel']
    hotel_id= Hotels.objects.filter(name=hotel).first().id

    room_info = Rooms.objects.filter(room_id=room_id, hotel=hotel_id).first()
    #room_dates = Rooms.objects.values_list('range',flat=True).filter(room_id=room_id, hotel=hotel)

    return Response({"id": room_info.id,"type": room_info.room_type,"range": room_info.range,"notes": room_info.notes})

#####################################################################################
# to get room id

@api_view(['GET'])
def get_room_id(request):
    room_id = request.query_params['room_id']
    hotel = request.query_params['hotel']
    dates = request.query_params['dates']

    room = Rooms.objects.filter(room_id=room_id, hotel=hotel, dates=dates).first()
    if room:
        return JsonResponse({'room_id': room.id})
    else:
        return JsonResponse({'room_id': None})

#####################################################################################

@api_view(['GET'])
def get_room_dates(request):
    room_id = str(request.query_params['room_id'])
    hotel = request.query_params['hotel']

    room_dates = Room_dates.objects.values_list('date',flat=True).filter(room_id_id=room_id).filter(hotel=hotel)
    
    return Response ({room_dates[0]})

#####################################################################################

@api_view(['GET'])
def get_booked_dates(request):
    room_id = str(request.query_params['room_id'])
    hotel = str(request.query_params['hotel'])

    booked_dates = Bookings.objects.values_list('dates',flat=True).filter(room_id=room_id).filter(hotel=hotel)
    dates_string = ', '.join(map(str, booked_dates))  # Join the dates using a delimiter

    return Response({dates_string})

    # booked_dates = Bookings.objects.raw("select id,dates from backend_Bookings where room_id='"+room_id+"' and hotel='"+hotel+"'")
    # dates_list = [booking.dates for booking in booked_dates]  # Convert RawQuerySet to list of dates
    # return Response({"booked_dates": dates_list})

#####################################################################################
@api_view(['GET'])
def get_booked_rooms(request):
    booked = Bookings.objects.raw("select id,(hotel || ' / ' || room_id) as room, GROUP_CONCAT(dates, ' / ') AS all_dates from backend_bookings where status='Booked' group by room")
    pending = Bookings.objects.raw("select id,(hotel || ' / ' || room_id) as room, GROUP_CONCAT(dates, ' / ') AS all_dates from backend_bookings where status='Pending' group by room")
    
    # Convert RawQuerySet to list of dictionaries
    booked_rooms = []
    for booking in booked:
        booked_rooms.append({
            'id': booking.id,
            'room': booking.room,
            'dates': booking.all_dates
        })
    pending_rooms = []
    for booking in pending:
        pending_rooms.append({
            'id': booking.id,
            'room': booking.room,
            'dates': booking.all_dates
        })
    
    return Response({"booked_rooms": booked_rooms,"pending_rooms": pending_rooms})

##################################################################################################################
@api_view(['GET'])
def get_open_rooms(request):
    hotel = str(request.query_params['hotel'])
    if (hotel):
        hotel_id= Hotels.objects.filter(name=hotel).first().id

    room_type = str(request.query_params['room_type'])

    if(hotel and room_type):
        rooms = Rooms.objects.filter(hotel=hotel_id).filter(room_type=room_type).all()
    elif(hotel):
        rooms = Rooms.objects.filter(hotel=hotel_id).all()
    else:
        rooms = Rooms.objects.all()
    
    response_data = []

    for room in rooms:
        hotel_name=Hotels.objects.filter(id=room.hotel_id).first().name
        room_data = {
            'name': room.room_id +' - '+ hotel_name,
            'dates': list(room.room_dates_set.values_list('date', flat=True))
        }
        response_data.append(room_data)

    return JsonResponse(response_data, safe=False)

##################################################################################################################

@api_view(['GET'])
def get_close_rooms(request):
    hotel = str(request.query_params['hotel'])
    room_type = str(request.query_params['room_type'])
    room_type = str(request.query_params['room_type'])

    if(hotel and room_type):
        rooms = Bookings.objects.filter(hotel=hotel).filter(room_type=room_type).raw("select id,(room_id || ' - ' || hotel) as room, GROUP_CONCAT(dates, ' / ') AS all_dates, GROUP_CONCAT(out_date, ',') AS out_dates from backend_bookings where status='Booked' group by room")
    elif(hotel):
        rooms = Bookings.objects.filter(hotel=hotel).raw("select id,(room_id || ' - ' || hotel) as room, GROUP_CONCAT(dates, ' / ') AS all_dates, GROUP_CONCAT(out_date, ',') AS out_dates from backend_bookings where status='Booked' group by room")
    else:
        rooms = Bookings.objects.raw("select id,(room_id || ' - ' || hotel) as room, GROUP_CONCAT(dates, ' / ') AS all_dates, GROUP_CONCAT(out_date, ',') AS out_dates from backend_bookings where status='Booked' group by room")
    response_data = []

    for room in rooms:
        room_data = {
            'name': room.room,
            'dates': room.all_dates,
            'out_dates': room.out_dates
        }
        response_data.append(room_data)

    return JsonResponse(response_data, safe=False)

#####################################################################################
# to remove files

@api_view(['GET'])
def remove_file(request):
    file_name = request.query_params['file_name']
    file_path = path.abspath('frontend/public/media/'+path.curdir)+file_name
    if (os.path.exists(file_path)):
        os.remove(os.path.join(file_path))
        return Response({'removed': 1})
    else:
        return Response({'removed': 0})

#####################################################################################

@api_view(['POST'])
def new_account(request):
    parent = request.query_params['parent']
    name = request.query_params['name']
    return Response(parent+" "+name)

#####################################################################################
from django.contrib.auth.models import User
from datetime import datetime
from django.shortcuts import get_object_or_404

class UserDataView(APIView):
    
    def get(self, request):
        users = User.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            users = users.filter(id=id)
        
        # Serialize the user data to a JSON response
        user_data = [{'id':user.id,'username': user.username, 'email': user.email,'first_name':user.first_name ,'last_name':user.last_name,'is_superuser':user.is_superuser,'last_login':user.last_login,'date_joined':user.date_joined} for user in users]
        
        return Response(user_data)
    
    def post(self, request):
        # Get the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')
        roles_list = request.data.get('roles_list')
        
        # Create a new user instance
        user = User(username=username,last_login=datetime.now())
        
        # Set the password for the user
        user.set_password(password)
        
        # Save the user instance
        user.save()

        last_id = User.objects.last().id         

        role = Roles(user_name_id=last_id)
        for column_name in roles_list:
            setattr(role, column_name, 1)

        role.save()
        
        return Response({'message': 'User created successfully'})
    
    def delete(self, request):
        id = request.query_params.get('id')
        
        # Retrieve the user object
        user = get_object_or_404(User, id=id)
        
        # Delete the user
        user.delete()
        
        return Response({'message': 'User deleted successfully'})

    
#####################################################################################

@api_view(['GET'])
def get_roles(request):
    user_id = str(request.query_params['user_id'])

    roles = Roles.objects.filter(user_name_id=user_id)
    roles = serializers.roles_serializer(roles, many=True)

    return Response(roles.data[0])

    
#####################################################################################

@api_view(['GET'])
def get_all_roles(request):

    roles = Roles.objects.first()
    roles = serializers.roles_serializer(roles, many=False)

    return Response(roles.data)


#####################################################################################

class bookings(ModelViewSet, mixins.DestroyModelMixin):

    queryset = Bookings.objects.all()
    serializer_class = serializers.bookings_serializer

    def get_queryset(self):
        queryset = Bookings.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = queryset.filter(id=id)
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(Q(id__contains=search) | Q(status__contains=search) | Q(room_id__contains=search) | Q(hotel__contains=search) | Q(room_type__contains=search) | Q(notes__contains=search)| Q(user__contains=search) )
        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

#####################################################################################

class flights(ModelViewSet, mixins.DestroyModelMixin):

    queryset = Flights.objects.all()
    serializer_class = serializers.flights_serializer

    def get_queryset(self):
        # queryset = Flights.objects.all()
        queryset = Flights.objects.raw("select * from backend_flights,backend_settings")
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = queryset.filter(id=id)
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(Q(code__contains=search) | Q(airline__contains=search) | Q(from_airport__contains=search) | Q(
                to_airport__contains=search) | Q(seats__contains=search) | Q(status__contains=search))
        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

#####################################################################################

class flight_dates(ModelViewSet, mixins.DestroyModelMixin):

    queryset = Flight_dates.objects.all()
    serializer_class = serializers.flight_dates_serializer

    def get_queryset(self):
        queryset = Flight_dates.objects.all()
        id = self.request.query_params.get('flight_id')
        if id is not None:
            queryset = queryset.filter(id=id)
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(Q(flight_id__contains=search) | Q(departure_date__contains=search) | Q(arrival_date__contains=search))
        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

#####################################################################################

class rooms(ModelViewSet, mixins.DestroyModelMixin):

    queryset = Rooms.objects.all()
    serializer_class = serializers.rooms_serializer

    def get_queryset(self):
        queryset = Rooms.objects.all()
        id = self.request.query_params.get('id')
        hotel_id = self.request.query_params.get('hotel_id')
        if id is not None:
            queryset = queryset.filter(id=id)
        if hotel_id is not None:
            queryset = queryset.filter(hotel=hotel_id)
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(Q(hotel__contains=search) | Q(room_id__contains=search) | Q(room_type__contains=search) | Q(
                dates__contains=search) )
        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

#####################################################################################

class hotels(ModelViewSet, mixins.DestroyModelMixin):

    queryset = Hotels.objects.all()
    serializer_class = serializers.hotels_serializer

    def get_queryset(self):
        queryset = Hotels.objects.all()
        id = self.request.query_params.get('id')
        
        if id is not None:
            queryset = queryset.filter(id=id)
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(Q(name__contains=search) | Q(rate__contains=search)|Q(notes__contains=search)| Q(area__contains=search) | Q(country__contains=search) | Q(
                city__contains=search) )
        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

#####################################################################################

class room_dates(ModelViewSet, mixins.DestroyModelMixin):

    queryset = Room_dates.objects.all()
    serializer_class = serializers.room_dates_serializer

    def get_queryset(self):
        queryset = Room_dates.objects.all()
        id = self.request.query_params.get('hotel_id')
        if id is not None:
            queryset = queryset.filter(id=id)
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(Q(flight_id__contains=search) | Q(departure_date__contains=search) | Q(arrival_date__contains=search))
        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

#####################################################################################

class accounts(ModelViewSet, mixins.DestroyModelMixin):

    queryset = Accounts.objects.all()
    serializer_class = serializers.accounts_serializer

    def get_queryset(self):
        queryset = Accounts.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = queryset.filter(id=id)
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(Q(name__contains=search) | Q(parent__contains=search) | Q(debit__contains=search) | Q(
                credit__contains=search) | Q(user__contains=search))
        return queryset

    def create(self):
        id = self.request.query_params.get('id')
        name = self.request.query_params.get('name')
        parent = self.request.query_params.get('parent')
        Accounts.objects.create(id=id, name=name, parent=parent)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

#####################################################################################

class dashboard_buttons(ModelViewSet, mixins.DestroyModelMixin):

    queryset = Dashboard_buttons.objects.all()
    serializer_class = serializers.dashboard_buttons_serializer

    def get_queryset(self):
        queryset = Dashboard_buttons.objects.all()
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(title__contains=search)

        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

#####################################################################################

class settings(ModelViewSet):

    queryset = Settings.objects.all()
    serializer_class = serializers.settings_serializer

    def get_queryset(self):
        queryset = Settings.objects.all()
        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

#####################################################################################
