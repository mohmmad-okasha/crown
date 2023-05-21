from django.urls import path
from rest_framework import routers
from . import api
# from . import views


router = routers.DefaultRouter()
router.register('flights', api.flights)
router.register('bookings', api.bookings)
router.register('rooms', api.rooms)
router.register('room_dates', api.room_dates)
router.register('accounts', api.accounts)
router.register('dashboard_buttons', api.dashboard_buttons)
router.register('settings', api.settings)

urlpatterns = router.urls
urlpatterns += [
    # to login
    path("login/", api.login, name="login"),
    # to upload files
    path("upload_file/", api.FileUploadView.as_view(), name='upload_file'),
    # to get max id
    path("get_max_id/", api.get_max_id, name="get_max_id"),
    # to remove file
    path("remove_file/", api.remove_file, name="remove_file"),

    # flights
    path("flight_delete/<int:id>", api.flights.destroy, name="flight_delete"),
    
    #accounts
    path("new_account/", api.new_account, name="new_account"),

    #Booking
    path("get_rooms/", api.get_rooms, name="get_rooms"),

    path("get_hotels/", api.get_hotels, name="get_hotels"),

    path("get_room_type/", api.get_room_type, name="get_room_type"),

    path("get_room_dates/", api.get_room_dates, name="get_room_dates"),

    path("get_booked_dates/", api.get_booked_dates, name="get_booked_dates"),
    
    path("get_booked_rooms/", api.get_booked_rooms, name="get_booked_rooms"),


]
