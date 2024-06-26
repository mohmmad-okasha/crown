from json import dumps
import os
from os import path

from django.http import HttpResponse, JsonResponse
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

# to upload files

class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file_name = self.request.query_params.get('file_name')
        image_file = request.FILES.get('image')
        file_path = path.abspath('frontend/public/media/'+path.curdir)+file_name
        # to remove last img for this customer
        if (os.path.exists(file_path)):
            os.remove(os.path.join(file_path))

        default_storage.save(file_path, image_file)
        return Response({'success': True})


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

# to get max id from any table

@api_view(['GET'])
def get_max_id(request):
    table_name = request.query_params['table_name']
    max_id = eval(table_name).objects.aggregate(Max('id'))
    return Response({'data': max_id})

#####################################################################################

# to save db backup
import shutil
import os
from datetime import datetime, timedelta
import glob

@api_view(['GET'])
def get_backup_files(backup_folder):
    file_pattern = os.path.join('db_backup/*.sqlite3')
    backup_files = glob.glob(file_pattern)
    backup_file_info = []
    
    for file in backup_files:
        file_name = os.path.basename(file)
        creation_time = datetime.fromtimestamp(os.path.getctime(file))
        three_hours_in_seconds = 3 * 60 * 60
        creation_time = creation_time + timedelta(seconds=three_hours_in_seconds)
        size= os.path.getsize(file)
        backup_file_info.append({"name":os.path.splitext(file_name)[0], "time":creation_time.strftime('%d/%m/%Y %H:%M'), "size": str(size/1000000)[:4] +" MB"})
    return Response({'data': sorted(backup_file_info, key=lambda x: x['time'], reverse=True)})

#####################################################################################

@api_view(['GET'])
def save_backup(request):
    # Path to the original database file
    original_db_path = 'db.sqlite3'
    
    # Destination folder for the backup
    backup_folder = 'db_backup'
    
    # Create the backup file name based on the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_file_name = f'backup_{timestamp}.sqlite3'
    
    # Construct the full paths for the original database and the backup file
    original_db_full_path = os.path.abspath(original_db_path)
    backup_file_full_path = os.path.join(backup_folder, backup_file_name)
    
    # Copy the database file to the backup folder
    shutil.copy2(original_db_full_path, backup_file_full_path) 

    # Remove old backup files older than one week
    one_week_ago = datetime.now() - timedelta(days=7)
    file_pattern = os.path.join(backup_folder, 'backup_*.sqlite3')
    
    # Get a list of all backup files matching the pattern
    backup_files = glob.glob(file_pattern)
    
    for file_path in backup_files:
        file_modified_time = datetime.fromtimestamp(os.path.getctime(file_path))
        if file_modified_time < one_week_ago:
            os.remove(file_path)
            print(f'Removed old backup file: {file_path}')

    return Response({'data': 'Successfully created a backup of the SQLite database'})

#####################################################################################
@api_view(['GET'])
def restore_backup(request):
    backup_name = request.query_params['backup_name']

    # Path to the backup file
    backup_file_path = 'db_backup/'+backup_name+'.sqlite3'
    
    # Path to the destination database file
    destination_db_path = 'db.sqlite3'
    
    # Copy the backup file to the destination database location
    shutil.copy2(backup_file_path, destination_db_path)

    return Response({'data': f'Successfully restored the SQLite database from the backup file: {backup_file_path}'})

#####################################################################################
@api_view(['GET'])
def remove_backup_file(request):
    file_name = request.query_params['backup_name']

    file_path = os.path.join('db_backup/'+ file_name+'.sqlite3')
        
    if os.path.exists(file_path):
        os.remove(file_path)
        return Response({'data':f"Successfully removed backup file: {file_name}"})
    else:
        return Response({'data':f"Backup file not found: {file_name}"})
    
#####################################################################################

# to delete rooms by hotel id

@api_view(['GET'])
def delete_hotel_rooms(request):
    hotel_id = request.query_params['hotel_id']
    Rooms.objects.filter(hotel_id=hotel_id).delete()

    return Response({'data': 1})

#####################################################################################

@api_view(['GET'])
def get_user_name_id(request):
    username = request.query_params['username']
    user_name_id= User.objects.filter(username=username).first().id

    return Response({'data': user_name_id})

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

# to get users

@api_view(['GET'])
def get_users(request):
    users = set(User.objects.values_list('username', flat=True))
    return Response(list(users))
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
        hotel_id= Hotels.objects.get(name=hotel).id

    room_type = str(request.query_params['room_type'])

    if hotel:
        if room_type:
            rooms = Rooms.objects.filter(hotel=hotel_id).filter(room_type=room_type).all()
        else:
            rooms = Rooms.objects.filter(hotel=hotel_id).all()
    else:
        rooms = []

    
    response_data = []

    for room in rooms:
        hotel_name=Hotels.objects.filter(id=room.hotel_id).first().name
        room_data = {
            'categ': room.room_categ,
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

    if(hotel and room_type):
        rooms = Bookings.objects.filter(hotel=hotel).filter(room_type=room_type).raw("select id,(room_id || ' - ' || hotel) as room, GROUP_CONCAT(dates, ' / ') AS all_dates, GROUP_CONCAT(out_date, ',') AS out_dates from backend_bookings where status='Booked' group by room")
    elif(hotel):
        rooms = Bookings.objects.filter(hotel=hotel).raw("select id,(room_id || ' - ' || hotel ) as room , GROUP_CONCAT(dates, ' / ') AS all_dates, GROUP_CONCAT(out_date, ',') AS out_dates from backend_bookings where status='Booked' group by room")
    else:
        rooms = Bookings.objects.raw("SELECT MAX(id) as id, (room_id || ' - ' || hotel) as room, GROUP_CONCAT(dates, ' / ') AS all_dates, GROUP_CONCAT(out_date, ',') AS out_dates FROM backend_bookings WHERE status='Booked' GROUP BY room")

    response_data = []


    for room in rooms:
        room_data = {
            'name': room.room,
            'dates': room.all_dates,
            'out_dates': room.out_dates
        }
        response_data.append(room_data)

    return JsonResponse(response_data, safe=False)

#######################################################################################################################################################################################################


@api_view(['GET'])
def get_no_show_rooms(request):
    hotel = str(request.query_params['hotel'])
    room_type = str(request.query_params['room_type'])

    if(hotel and room_type):
        rooms = Bookings.objects.filter(hotel=hotel).filter(room_type=room_type).raw("select id,(room_id || ' - ' || hotel) as room, GROUP_CONCAT(dates, ' / ') AS all_dates, GROUP_CONCAT(out_date, ',') AS out_dates from backend_bookings where status='No Show' group by room")
    elif(hotel):
        rooms = Bookings.objects.filter(hotel=hotel).raw("select id,(room_id || ' - ' || hotel) as room, GROUP_CONCAT(dates, ' / ') AS all_dates, GROUP_CONCAT(out_date, ',') AS out_dates from backend_bookings where status='No Show' group by room")
    else:
        rooms = Bookings.objects.raw("select id,(room_id || ' - ' || hotel) as room, GROUP_CONCAT(dates, ' / ') AS all_dates, GROUP_CONCAT(out_date, ',') AS out_dates from backend_bookings where status='No Show' group by room")
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
        users = User.objects.all().exclude(username = 'admin')
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
        #roles_list = request.data.get('roles_list')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        
        # Create a new user instance
        user = User(username=username,last_login=datetime.now(),first_name=first_name,last_name=last_name,email=email)
        
        # Set the password for the user
        user.set_password(password)
        
        # Save the user instance
        user.save()

        # last_id = User.objects.last().id         

        # role = Roles(user_name_id=last_id)
        # for column_name in roles_list:
        #     setattr(role, column_name, 1)

        # role.save()
        
        return Response({'message': 'User created successfully'})
    
    def delete(self, request):
        id = request.query_params.get('id')
        
        # Retrieve the user object
        user = get_object_or_404(User, id=id)
        
        # Delete the user
        user.delete()
        
        return Response({'message': 'User deleted successfully'})
    
    def patch(self, request):
        id = request.data.get('id')
        new_data = request.data.get('new_data')


        # Retrieve the user object
        user = User.objects.filter(id=id).first()
        
        # Update the user data
        user.first_name = new_data.get('first_name', user.first_name)
        user.last_name = new_data.get('last_name', user.last_name)
        user.username = new_data.get('username', user.username)
        user.email = new_data.get('email', user.email)
        if(new_data.get('password', user.password)):
            user.set_password(new_data.get('password', user.password))
        
        # Save the updated user instance
        user.save()
 
        #update roles
        roles_list = new_data.get('roles')
        del roles_list["user_name"]
        del roles_list["id"]
        role = get_object_or_404(Roles,user_name_id=id)
        for column_name in roles_list:
            setattr(role, column_name, 1)
        role.save()
        
        return Response({'message': 'User data updated successfully'})
    
#####################################################################################

class roles(ModelViewSet, mixins.DestroyModelMixin):
    queryset = Roles.objects.all()
    serializer_class = serializers.roles_serializer

    def get_queryset(self):
        queryset = self.queryset
        id = self.request.query_params.get('id')
        user_name_id = self.request.query_params.get('user_name_id')
        if id is not None:
            queryset = queryset.filter(id=id)
        if user_name_id is not None:
            queryset = queryset.filter(user_name_id=user_name_id)

        return queryset
    
    def put(self, request, *args, **kwargs):
        user_name_id = request.data.get('user_name')
        roles_instance = self.get_object()  # Get the Roles instance based on the provided ID

        # Get the User instance based on user_name_id
        user_instance = get_object_or_404(User, id=user_name_id)

        # Update the user_name field with the User instance
        roles_instance.user_name = user_instance

        serializer = serializers.roles_serializer(roles_instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

#####################################################################################

@api_view(['GET'])
def get_roles(request):
    
    user_id = request.query_params.get('user_id', False)
    user_name = request.query_params.get('user_name', False)

    if (user_name):
        user_id=User.objects.filter(username=user_name).first().id

    roles = Roles.objects.filter(user_name_id=user_id)
    roles = serializers.roles_serializer(roles, many=True)

    return Response(roles.data[0])

#####################################################################################
# to get room id

@api_view(['GET'])
def get_role_id(request):
    user_name_id = request.query_params['user_name_id']

    role = Roles.objects.filter(user_name_id=user_name_id).first()
    if role:
        return JsonResponse({'role_id': role.id})
    else:
        return JsonResponse({'role_id': None})

#####################################################################################

@api_view(['GET'])
def get_all_roles(request):

    roles = Roles.objects.first()
    roles = serializers.roles_serializer(roles, many=False)

    return Response(roles.data)

#####################################################################################
@api_view(['POST'])
def send_message(request):
    
        sender = request.user
        receiver_id = request.POST.get('receiver_id')
        message = request.POST.get('message')

        if receiver_id and message:
            receiver = User.objects.get(id=receiver_id)
            chat_message = ChatMessage.objects.create(sender=sender, receiver=receiver, message=message)
            return JsonResponse({'status': 'success'})
    
        return JsonResponse({'status': 'error'})

@api_view(['GET'])
def get_messages(request):
    if request.method == 'GET':
        receiver_id = request.GET.get('receiver_id')
        if receiver_id:
            sender = request.user
            receiver = User.objects.get(id=receiver_id)
            messages = ChatMessage.objects.filter(sender=sender, receiver=receiver) | ChatMessage.objects.filter(sender=receiver, receiver=sender)
            message_list = [{'sender': str(message.sender), 'message': message.message, 'timestamp': message.timestamp} for message in messages]
            return JsonResponse({'messages': message_list})
    
    return JsonResponse({'status': 'error'})

#####################################################################################

class bookings(ModelViewSet, mixins.DestroyModelMixin):

    queryset = Bookings.objects.all()
    serializer_class = serializers.bookings_serializer

    def get_queryset(self):
        queryset = Bookings.objects.order_by('-id').all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = queryset.filter(id=id)
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(
                Q(id__contains=search) 
                | Q(status__contains=search) 
                | Q(room_id__contains=search) 
                | Q(hotel__contains=search) 
                | Q(room_type__contains=search) 
                | Q(notes__contains=search)
                | Q(persons_names__contains=search)
                | Q(user__contains=search) )
        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

#####################################################################################

class logs(ModelViewSet, mixins.DestroyModelMixin):

    queryset = Logs.objects.all()
    serializer_class = serializers.logs_serializer

    def get_queryset(self):
        queryset = Logs.objects.exclude(user_name="test").order_by('-id').all() #exclude do not get
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = queryset.filter(id=id)
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(
                Q(id__contains=search) 
                | Q(time__contains=search) 
                | Q(log__contains=search) 
                | Q(user_name__contains=search) )
            
        user = self.request.query_params.get('user')
        range = self.request.query_params.get('range')
            
        if user is not None and range is None:
            queryset = queryset.filter(Q(user_name__contains=user))
        elif range is not None and user is None:
            start_date_str, end_date_str = range.split(',')
            start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
            end_date = datetime.strptime(end_date_str, '%d/%m/%Y')
            queryset = queryset.filter(time__gte=start_date, time__lt=end_date)
        elif range is not None and user is not None:
            start_date_str, end_date_str = range.split(',')
            start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
            end_date = datetime.strptime(end_date_str, '%d/%m/%Y')
            queryset = queryset.filter(Q(user_name__contains=user), time__gte=start_date, time__lt=end_date)

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

class flights(ModelViewSet, mixins.DestroyModelMixin):

    queryset = Flights.objects.all()
    serializer_class = serializers.flights_serializer

    def get_queryset(self):
        queryset = Flights.objects.all()
        #queryset = Flights.objects.raw("select * from backend_flights,backend_settings")
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

class airlines(ModelViewSet, mixins.DestroyModelMixin):

    queryset = Airlines.objects.all()
    serializer_class = serializers.airlines_serializer

    def get_queryset(self):
        queryset = Airlines.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = queryset.filter(id=id)
        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

#####################################################################################

class airports(ModelViewSet, mixins.DestroyModelMixin):

    queryset = Airports.objects.all()
    serializer_class = serializers.airports_serializer

    def get_queryset(self):
        queryset = Airports.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = queryset.filter(id=id)
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

